class GitHubConfig:
    def __init__(self, token=None):
        self.token = token or "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"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {self.token}"
        }
        self.base_url = "https://api.github.com/"

    @classmethod
    def get_instance(cls, token=None):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(token)
        return cls._instance