import requests
import time
from urllib.parse import urljoin
from github_config import GitHubConfig

class CommitAnalyzer:
    def __init__(self):
        self.config = GitHubConfig.get_instance()
        self.total_commits_analyzed = 0
        self.max_commits_to_analyze = 3000000000  # Maximum commits to analyze

        # Define related keywords for factory pattern detection
        self.related_keywords = None

        self.keywords = {
            'factory': [
                # Core Factory Pattern Terms
                "factory", "factorymethod", "factory method", "factory-method", "factorypattern", "factory pattern",
                "factorybean", "factory_method", "factories", "factory-pattern",
                "concretefactory", "concrete factory", "simplefactory", "simple factory", "staticfactory", "static factory",

                # Factory Types
                "object factory", "bean factory", "service factory", "resource factory",
                "data factory", "proxy factory", "component factory", "entity factory",
                "model factory", "client factory", "session factory", "connection factory",
                "thread factory", "pool factory", "cache factory", "adapter factory",

                # Implementation Terms
                "create instance", "factory class", "factory interface",
                "create object", "generate instance", "factory implementation",
                "factory method pattern", "factory design pattern",

                # Framework-Specific
                "spring factory", "factory bean", "@Factory",
                "@Component factory", "@Bean factory", "factory configuration"
            ],
            'abstract_factory': [
                # Core Abstract Factory Terms
                "abstract factory", "abstractfactory", "abstract-factory", "abstract_factory_pattern",
                "abstract-factory-pattern", "abstract factory pattern",

                # Implementation Terms
                "AbstractFactory", "FactoryInterface", "FactoryImplementation",
                "FactoryMethod", "AbstractCreator", "AbstractFactoryMethod",
                "abstract product", "concrete factory", "create instance",

                # Pattern Concepts
                "factory family", "related factories", "factory of factories",
                "abstract product family", "product family", "related products",
                "factory hierarchy", "abstract creation", "factory abstraction",

                # Framework and Implementation
                "abstract factory implementation", "abstract factory interface",
                "spring abstract factory", "guice abstract factory",
                "abstract factory pattern", "abstract factory design",
                
                # Common Usage Terms
                "Creator", "Abstract Product", "Product Family",
                "Abstract Factory Class", "Factory Pattern Extension",
                "Factory Abstraction", "Product Interface"
            ]
        }

    def set_pattern(self, pattern_type):
        """Update keywords for the specified pattern."""
        self.related_keywords = self.keywords.get(pattern_type, [])

    def handle_rate_limit(self, response):
        """Handle GitHub API rate limit by sleeping until the reset time"""
        if response.status_code == 403:  # Rate limit exceeded
            rate_limit_url = urljoin(self.config.base_url, "rate_limit")
            try:
                rate_info = requests.get(rate_limit_url, headers=self.config.headers).json()
                reset_time = rate_info['resources']['core']['reset']
                remaining = rate_info['resources']['core']['remaining']
            except:
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))
                remaining = int(response.headers.get('X-RateLimit-Remaining', 0))

            current_time = time.time()
            sleep_time = reset_time - current_time + 5

            print(f"\nRate limit reached! Current rate limit status:")
            print(f"Remaining calls: {remaining}")
            print(f"Reset time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_time))}")
            print(f"Sleeping for {int(sleep_time)} seconds...")
            
            time.sleep(max(sleep_time, 0))
            print("Resuming operations...")
            return True
        return False

    def get_commits(self, owner, repo, per_page=100):
        """Get all commits for a repository, handling pagination and rate limits"""
        commits = []
        page = 1

        while True:
            print(f"Fetching page {page} of commits for {owner}/{repo}...")
            
            params = {'per_page': per_page, 'page': page}
            url_commits = urljoin(self.config.base_url, f'repos/{owner}/{repo}/commits')
            
            while True:  # Keep trying if rate limited
                try:
                    response = requests.get(url_commits, headers=self.config.headers, params=params)
                    
                    if self.handle_rate_limit(response):
                        continue  # Retry the same request after rate limit sleep
                    
                    response.raise_for_status()
                    break  # Break if request was successful
                    
                except requests.exceptions.RequestException as e:
                    if response.status_code == 403:  # Rate limit error
                        self.handle_rate_limit(response)
                        continue
                    else:
                        print(f"Error fetching commits for {owner}/{repo}: {str(e)}")
                        return commits

            data = response.json()
            
            if not data:  # No more commits
                break
                
            commits.extend(data)
            self.total_commits_analyzed += len(data)
            
            print(f"Retrieved {len(data)} commits from page {page}")
            
            # Check if the total commits analyzed have reached the maximum limit
            if self.total_commits_analyzed >= self.max_commits_to_analyze:
                print(f"Reached the maximum limit of {self.max_commits_to_analyze} commits. Stopping further analysis.")
                break
                
            if len(data) < per_page:  # Last page
                break
                
            page += 1

        print(f"\nFinished retrieving commits for {owner}/{repo}")
        print(f"Total commits found: {len(commits)}")
        return commits
