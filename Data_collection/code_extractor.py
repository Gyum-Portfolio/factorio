import base64
import time
import requests
from github_config import GitHubConfig

class CodeExtractor:
    def __init__(self, owner, repo):
        """
        Initialize the CodeExtractor with the repository owner, repository name, and configuration.
        """
        self.owner = owner
        self.repo = repo
        self.config = GitHubConfig.get_instance()

    def handle_rate_limit(self, response):
        """
        Handles GitHub API rate limits by pausing execution until the rate limit resets.
        Returns True if a rate limit was handled, allowing the caller to retry the request.
        """
        if response.status_code == 403:  # Rate limit exceeded
            reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))
            current_time = time.time()
            sleep_time = reset_time - current_time + 5  # Add buffer to avoid immediate retry
            print(f"\nRate limit reached while extracting code. Sleeping for {int(sleep_time)} seconds...")
            time.sleep(max(sleep_time, 0))
            return True
        return False

    def get_file_content_at_commit(self, commit_sha, file_path):
        """
        Fetch the content of a file at a specific commit SHA. Handles decoding of base64-encoded content.
        Returns None if the file does not exist or is a directory.
        """
        url = f"{self.config.base_url}repos/{self.owner}/{self.repo}/contents/{file_path}"
        params = {"ref": commit_sha}
        
        while True:  # Retry mechanism for rate limits
            try:
                response = requests.get(url, headers=self.config.headers, params=params)
                
                if self.handle_rate_limit(response):
                    continue

                if response.status_code == 404:  # File not found
                    return None
                    
                response.raise_for_status()
                break  # Exit retry loop on success
            except requests.exceptions.RequestException as e:
                if response.status_code != 403:  # Handle other errors besides rate limits
                    print(f"Error getting file content: {str(e)}")
                    return None
                continue  # Retry on rate limit

        try:
            data = response.json()
            if isinstance(data, list):  # If the path points to a directory
                return None
                
            if data.get("encoding") == "base64":  # Decode base64-encoded content
                return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            return data.get("content")
        except Exception as e:
            print(f"Error decoding file content: {str(e)}")
            return None

    def __call__(self, commit_sha, parent_sha, file_path):
        """
        Fetch the 'before' and 'after' code for a given file in a commit. 
        Only processes Java files. Returns a tuple of (before_code, after_code).
        """
        if not file_path.endswith('.java'):  # Skip non-Java files
            return None, None
            
        before_code = None
        if parent_sha:  # Fetch 'before' code if parent SHA exists
            before_code = self.get_file_content_at_commit(parent_sha, file_path)
        after_code = self.get_file_content_at_commit(commit_sha, file_path)
        return before_code, after_code
