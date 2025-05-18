import requests
import time
from datetime import datetime
from urllib.parse import urljoin
from github_config import GitHubConfig

class RepoCollector:
    """
    A class to collect repositories from GitHub based on specified criteria like stars, date ranges, and language.
    Handles GitHub's rate limits and paginated results efficiently.
    """
    def __init__(self, max_repos=1000):
        """
        Initialize the RepoCollector with a maximum number of repositories to retrieve.
        """
        self.config = GitHubConfig.get_instance()
        self.max_repos = max_repos
        self.repo_count = 0

    def handle_rate_limit(self, response):
        """
        Handle GitHub API rate limits by pausing execution until the reset time.
        """
        if response.status_code == 403:
            rate_limit_url = urljoin(self.config.base_url, "rate_limit")
            try:
                rate_info = requests.get(rate_limit_url, headers=self.config.headers).json()
                reset_time = rate_info['resources']['search']['reset']
                remaining = rate_info['resources']['search']['remaining']
            except:
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))
                remaining = int(response.headers.get('X-RateLimit-Remaining', 0))

            current_time = time.time()
            sleep_time = reset_time - current_time + 5

            print(f"\nSearch rate limit reached! Status:")
            print(f"Remaining calls: {remaining}")
            print(f"Reset time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_time))}")
            print(f"Sleeping for {int(sleep_time)} seconds...")
            
            time.sleep(max(sleep_time, 0))
            print("Resuming operations...")
            return True
        return False

    def generate_date_ranges(self, start_year=2015):
        """
        Generate date ranges for each year from the specified start year to the current year.

        Args:
            start_year (int): The year to start generating date ranges from.

        Returns:
            list: A list of tuples containing start and end dates for each year.
        """
        end_year = datetime.now().year
        return [(f"{year}-01-01", f"{year}-12-31") for year in range(start_year, end_year + 1)]

    def search_repositories(self, min_stars=3000, per_page=100, pages=10):
        """
        Search for repositories on GitHub matching specific criteria like stars, language, and date range.
        """
        repos = []
        date_ranges = self.generate_date_ranges()

        for start, end in date_ranges:
            if self.repo_count >= self.max_repos:
                break
            print(f"\nSearching repos created between {start} and {end}...")
            
            star_ranges = [
                (min_stars, 1000),
                (1000, 5000),
                (5000, 10000),
                (10000, 50000),
                (50000, None)
            ]
            
            for min_star, max_star in star_ranges:
                star_query = f"stars:{min_star}" if max_star is None else f"stars:{min_star}..{max_star}"
                query = f"{star_query} language:java created:{start}..{end} pushed:>2023-01-01"
                
                for page in range(1, pages + 1):
                    if self.repo_count >= self.max_repos:
                        break
                        
                    params = {
                        'q': query,
                        'sort': 'updated',
                        'order': 'desc',
                        'per_page': per_page,
                        'page': page
                    }
                    
                    while True:
                        try:
                            response = requests.get(
                                urljoin(self.config.base_url, 'search/repositories'),
                                headers=self.config.headers,
                                params=params
                            )
                            
                            if self.handle_rate_limit(response):
                                continue
                                
                            response.raise_for_status()
                            break
                        except requests.exceptions.RequestException as e:
                            if response.status_code != 403:
                                print(f"Error searching repositories: {str(e)}")
                                break
                            continue
                    
                    items = response.json().get('items', [])
                    
                    for repo in items:
                        if self.repo_count >= self.max_repos:
                            break
                        repos.append(repo)
                        self.repo_count += 1

                    print(f"Page {page}: Retrieved {len(items)} repositories. Total: {self.repo_count}")
                    if len(items) < per_page:
                        break
        
        return repos

    def __call__(self, min_stars=3000, per_page=100, pages=10):
        """
        Allow the class instance to be called like a function to start the repository search process.
        """
        return self.search_repositories(min_stars, per_page, pages)
