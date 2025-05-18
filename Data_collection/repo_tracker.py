import json
import os

class RepoTracker:
    """
    A class to track processed repositories, persist the information to disk, 
    and retrieve the status of repositories efficiently.
    """
    def __init__(self, storage_path="dataset/processed_repos.json"):
        """
        Initialize the RepoTracker with the storage path for processed repositories.
        """
        self.storage_path = storage_path
        self.processed_repos = self._load_processed_repos()

    def _load_processed_repos(self):
        """
        Load the set of processed repositories from the storage file and return set of processed repository identifiers.
        """
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {self.storage_path}. Starting with an empty set.")
                return set()
        return set()

    def _save_processed_repos(self):
        """
        Save the current set of processed repositories to the storage file.
        """
        with open(self.storage_path, 'w') as f:
            json.dump(list(self.processed_repos), f)

    def is_processed(self, repo_identifier):
        """
        Check if a repository has already been processed.
        """
        return repo_identifier in self.processed_repos

    def mark_as_processed(self, repo_identifier):
        """
        Mark a repository as processed and save the updated set to disk.
        """
        self.processed_repos.add(repo_identifier)
        self._save_processed_repos()

    def get_processed_count(self):
        """
        Get the count of repositories that have been marked as processed.
        """
        return len(self.processed_repos)
