import os
from datetime import datetime

import numpy as np
import torch
from accelerate import Accelerator
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, set_peft_model_state_dict, TaskType
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, logging, \
    BitsAndBytesConfig
from transformers import TrainerCallback, TrainingArguments, TrainerState, TrainerControl
from transformers.trainer_utils import PREFIX_CHECKPOINT_DIR
from transformers.integrations import WandbCallback
import json
import wandb

class SavePeftModelCallback(TrainerCallback):
    def on_save(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        checkpoint_folder = os.path.join("./starcoder2_factory_pattern", f"{PREFIX_CHECKPOINT_DIR}-{state.global_step}")

        kwargs["model"].save_pretrained(checkpoint_folder)

        pytorch_model_path = os.path.join(checkpoint_folder, "pytorch_model.bin")
        torch.save({}, pytorch_model_path)
        return control


class LoadBestPeftModelCallback(TrainerCallback):
    def on_train_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        print(f"Loading best peft model from {state.best_model_checkpoint} (score: {state.best_metric}).")
        best_model_path = os.path.join(state.best_model_checkpoint, "adapter_model.bin")
        adapters_weights = torch.load(best_model_path)
        model = kwargs["model"]
        set_peft_model_state_dict(model, adapters_weights)
        return control


def prepare_dataset():
    with open('filtered_java_code.json', 'r') as f:
        data = json.load(f)

    processed_data = []

    print("Preprocessing dataset.")
    for item in data:
        prompt = f"""### Instruction: Refactor this code to implement the Factory Pattern.

                    ### Input Code:
                    {item['before']}
                    
                    ### Response:
                    {item['after']}"""

        processed_data.append({
            "text": prompt
        })

    dataset = Dataset.from_list(processed_data)

    # Split into train and validation
    train_test = dataset.train_test_split(test_size=0.1)

    return train_test['train'], train_test['test']


def tokenize_dataset(dataset, tokenizer):

    def tokenize_function(examples):
        tokenized =  tokenizer(
            examples["text"],
            truncation=True,
            max_length=2048,
            padding="max_length"
        )

        tokenized["labels"] = tokenized["input_ids"].copy()
        for i in range(len(tokenized["labels"])):
            attention_mask = tokenized["attention_mask"][i]
            labels = tokenized["labels"][i]
            # Replace padding token id with -100 so the model ignores them
            labels = [label if mask == 1 else -100 for label, mask in zip(labels, attention_mask)]
            tokenized["labels"][i] = labels
        for key in tokenized.keys():
            tokenized[key] = torch.tensor(tokenized[key], dtype=torch.long)

        return tokenized


    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names
    )

    return tokenized_dataset

def prepare_model_and_tokenizer():
    """Initialize and prepare the StarCoder2 model and tokenizer."""
    model_id = "bigcode/starcoder2-7b"
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    bnb_config = BitsAndBytesConfig(load_in_8bit=True)

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        token=hf_token,
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token

    # Load model in 8-bit to save memory
    print("Loading the model")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=hf_token,
        quantization_config=bnb_config,
        device_map="auto",
        use_cache=False
    )

    # Prepare model for LoRA fine-tuning
    model = prepare_model_for_kbit_training(model)

    # Configure LoRA
    lora_config = LoraConfig(
        r=16,  # attention heads
        lora_alpha=32,  # alpha parameter for LoRA scaling
        target_modules = ["c_proj", "c_attn", "q_attn"],  # recommended by starcoder2 team
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    # Get PEFT model
    model.enable_input_require_grads()
    model = get_peft_model(model, lora_config)


    return model, tokenizer

def train_model(model, train_set, test_set, tokenizer):
    """Configure and run the training."""
    wandb.init(
        project="starcoder2-factory-pattern",  # Name of your project
        name=f"lora-training-{datetime.now().strftime('%Y%m%d-%H%M')}",  # Unique name for this run
        config={
            "learning_rate": 5e-6,
            "batch_size": 1,
            "gradient_accumulation_steps": 16,
            "max_steps": 10000,
            "warmup_steps": 100,
            "model_name": "bigcode/starcoder2-7b",
            "lora_r": 16,
            "lora_alpha": 32,
            "lora_dropout": 0.05,
            "train_size": len(train_set),
            "eval_size": len(test_set),
            "max_length": 2048,
        }
    )

    #training arguments suggested by starcoder2 team
    training_args = TrainingArguments(
        output_dir="./starcoder2_factory_pattern",  # Where to save your model checkpoints
        max_steps=2000,  # Total number of training steps
        per_device_train_batch_size=1,  # Small batch size due to model size
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=16,  # Accumulate gradients to simulate larger batch size
        evaluation_strategy="steps",  # Evaluate at regular intervals
        save_strategy="steps",  # Save checkpoints at regular intervals
        eval_steps=50,
        save_steps=200,
        load_best_model_at_end=True,  # Load the best performing model when done
        learning_rate=5e-6,  # Conservative learning rate recommended by StarCoder team
        lr_scheduler_type="cosine",  # Smooth learning rate decay
        warmup_steps=100,  # Gradual warmup to prevent early training instability
        weight_decay=0.05,  # Regularization to prevent overfitting
        bf16=True,
        fp16=False,
        gradient_checkpointing=True,  # Save memory by recomputing gradients when needed
        dataloader_drop_last=True,  # Drop incomplete batches for training stability
        ddp_find_unused_parameters=False,  # Optimize distributed training
        logging_steps=25,  # Log metrics every 25 steps
        report_to="wandb"
    )

    def compute_metrics(eval_preds):
        logits, labels = eval_preds
        predictions = np.argmax(logits, axis=-1)

        accuracy = np.mean(predictions == labels)

        wandb.log({
            "eval/accuracy": accuracy,
            "eval/batch_size": training_args.per_device_eval_batch_size,
        })

        return {"accuracy": accuracy}

    # Initialize trainer, only save lora weights instead of all model weights
    trainer = Trainer(model=model, args=training_args, train_dataset=train_set, eval_dataset=test_set,
                      callbacks=[SavePeftModelCallback, LoadBestPeftModelCallback, WandbCallback],
                      compute_metrics=compute_metrics)

    print("Training...")
    trainer.train()

    print("Saving last checkpoint of the model")
    model.save_pretrained("./starcoder2_factory_pattern/final_checkpoint")

    wandb.finish()


def main():
    print("logging into wandb")
    wandb.login(key=os.getenv("WANDB_API_KEY"))
    # Prepare dataset
    train_set, test_set = prepare_dataset()

    # Initialize model and tokenizer
    model, tokenizer = prepare_model_and_tokenizer()

    # Tokenize dataset
    tokenized_train_set = tokenize_dataset(train_set, tokenizer)
    tokenized_test_set = tokenize_dataset(test_set, tokenizer)

    # Train model
    train_model(model, tokenized_train_set,tokenized_test_set, tokenizer)


if __name__ == "__main__":
    logging.set_verbosity_error()
    main()
