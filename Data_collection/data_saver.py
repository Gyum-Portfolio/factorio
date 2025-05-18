import os
import json
from datetime import datetime

class DataSaver:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.index = 1
        os.makedirs(output_dir, exist_ok=True)
        self.file_path = os.path.join(self.output_dir, "changes.json")
        self.saved_commits = set()
        
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    self.index = len(data) + 1
                    for entry in data:
                        self.saved_commits.add(f"{entry['repo']}/{entry['commit_sha']}")
            except json.JSONDecodeError:
                self.index = 1
                # Backup corrupted file
                backup_path = f"{self.file_path}.corrupted"
                if os.path.exists(self.file_path):
                    os.rename(self.file_path, backup_path)
                    print(f"Corrupted JSON file backed up to {backup_path}")
        
        if not os.path.exists(self.file_path):
            self._atomic_write([])

    def _atomic_write(self, data):
        """Write data atomically using a temporary file"""
        # Create temporary file in same directory to ensure atomic move
        temp_path = os.path.join(self.output_dir, f".test.json.{os.getpid()}.tmp")
        try:
            # Write to temporary file first
            with open(temp_path, "w", encoding="utf-8") as tmp_file:
                json.dump(data, tmp_file, ensure_ascii=False, indent=4)
                # Flush file buffers
                tmp_file.flush()
                # Ensure write is flushed to disk
                os.fsync(tmp_file.fileno())
            
            os.replace(temp_path, self.file_path)
        except Exception as e:
            # Clean up temp file if something went wrong
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except:
                    pass
            raise e

    def __call__(self, before_code, after_code, repo_name, commit_sha):
        commit_id = f"{repo_name}/{commit_sha}"
        
        if commit_id in self.saved_commits:
            print(f"Skipping duplicate commit: {commit_id}")
            return False

        # Create the data entry
        data_entry = {
            "index": self.index,
            "repo": repo_name,
            "commit_sha": commit_sha,
            "before": before_code,
            "after": after_code,
            "timestamp": datetime.now().isoformat()
        }

        try:
            current_data = []
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as json_file:
                    current_data = json.load(json_file)
            
            current_data.append(data_entry)
            
            # Save atomically
            self._atomic_write(current_data)
            
            # Update tracking only after successful save
            self.saved_commits.add(commit_id)
            self.index += 1
            
            print(f"Saved commit {commit_id} to {self.file_path}")
            return True
            
        except Exception as e:
            print(f"Error saving commit {commit_id}: {str(e)}")
            return False
