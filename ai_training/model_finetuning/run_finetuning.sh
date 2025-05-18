#!/bin/bash
#SBATCH --partition=gpu-a100
#SBATCH --gpus-per-task=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --mem-per-cpu=5G
#SBATCH --time=24:00:00
#SBATCH --job-name=starcoder2_ft
#SBATCH --output=starcoder2_ft_%j.out
#SBATCH --error=starcoder2_ft_%j.err
#SBATCH --account=Education-EEMCS-Courses-CS4570

module purge
module load 2024r1
module load slurm
module load openmpi
module load cuda/11.7
module load --ignore-cache python/3.10.13

# Create and activate virtual environment
pkill -u $USER python || true
rm -rf "/scratch/aadriouech/venv_starcoder"
VENV_PATH="/scratch/aadriouech/venv_starcoder"
python -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

# Install packages
pip install --upgrade pip
pip install numpy==1.24.3
pip install torch==2.0.1
pip install transformers==4.46.0
pip install datasets
pip install accelerate==0.27.1
pip install peft==0.14.0
pip install wandb
pip install bitsandbytes==0.45.0

find_free_port() {
    lockfile="/scratch/aadriouech/port_lock_$SLURM_JOB_ID"
    port_file="/scratch/aadriouech/master_port_$SLURM_JOB_ID"
    ready_file="/scratch/aadriouech/port_ready_$SLURM_JOB_ID"

    exec 200>"$lockfile"
    flock 200  # Wait for lock

    if [ "$SLURM_PROCID" -eq 0 ]; then
        port=0
        max_retries=10
        for i in $(seq 1 $max_retries); do
            port=$(comm -23 <(seq 49152 65535 | sort) <(ss -tan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)
            if ! ss -tan | grep -q ":$port " && ! lsof -iTCP:$port -sTCP:LISTEN; then
                echo $port > $port_file
                touch $ready_file
                break
            fi
            echo "Retry $i: Port $port is in use, retrying..."
            sleep 1
        done
        if [ $port -eq 0 ]; then
            echo "Error: Failed to find a free port after $max_retries retries."
            exit 1
        fi
    fi

    flock -u 200  # Release lock
    while [ ! -f $ready_file ]; do sleep 1; done
    cat $port_file
}

# Clean up
pkill -u $USER python || true
rm -f /scratch/aadriouech/master_port_$SLURM_JOB_ID /scratch/aadriouech/port_lock_$SLURM_JOB_ID

# Set environment variables
export MASTER_PORT=$(find_free_port)
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export WORLD_SIZE=$SLURM_NTASKS
export RANK=$SLURM_PROCID

echo "Distributed training setup:"
echo "MASTER_PORT=$MASTER_PORT"
echo "MASTER_ADDR=$MASTER_ADDR"
echo "WORLD_SIZE=$WORLD_SIZE"
echo "RANK=$RANK"

#initialize huggingface token
if [ -f "$PWD/.hf_token" ]; then
    export "$PWD/.hf_token"
else
    echo "Error: Hugging Face token not found in $PWD/.hf_token"
    exit 1
fi

if [ -f "$PWD/.wandb_key" ]; then
    export WANDB_API_KEY=$(cat "$PWD/.wandb_key")
else
    echo "Error: wandb API key not found in $PWD/.wandb_key"
    exit 1
fi

sleep 2

srun --ntasks=$SLURM_NTASKS --exclusive bash -c "while [ ! -f /scratch/aadriouech/port_ready_$SLURM_JOB_ID ]; do sleep 1; done"
srun python finetuning.py

# Deactivate virtual environment
deactivate