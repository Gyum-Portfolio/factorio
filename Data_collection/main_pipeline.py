from repo_collector import RepoCollector
from commit_analyzer import CommitAnalyzer
from pattern_validator import PatternValidator
from data_saver import DataSaver
from code_extractor import CodeExtractor
from github_config import GitHubConfig
from repo_tracker import RepoTracker
import requests
import time

def process_repository_commits(repo, commit_analyzer, pattern_validator, data_saver, config, pattern_types):
    """
    Process commits in a given repository to identify and save factory-related code changes.
    Filters commits based on keywords, analyzes code changes, and validates factory patterns.
    This function specifically looks for commits that introduce new factory patterns where
    none existed before.
    
    Args:
        repo (dict): Repository information dictionary containing owner and name
        commit_analyzer (CommitAnalyzer): Analyzer instance for processing commits
        pattern_validator (PatternValidator): Validator for detecting factory patterns
        data_saver (DataSaver): Handler for saving validated pattern implementations
        config (GitHubConfig): Configuration for GitHub API access
        pattern_types (list): List of pattern types to check for (e.g., ["factory", "abstract_factory"])
    
    Returns:
        bool: True if any valid pattern implementations were found and saved
    """
    owner, repo_name = repo['owner']['login'], repo['name']
    repo_full_name = f"{owner}/{repo_name}"
    print(f"\n=== Processing Repository: {repo_full_name} ===")

    # Fetch commits for the repository with exponential backoff for rate limits
    commits = commit_analyzer.get_commits(owner, repo_name)

    for pattern in pattern_types:
        print(f"\n=== Processing for {pattern} Pattern ===")
        # Configure analyzers for the current pattern type
        commit_analyzer.set_pattern(pattern)
        pattern_validator.set_pattern(pattern)

        # Filter commits that might contain factory-related changes based on commit messages
        pattern_commits = [
            {
                "repository": repo_full_name,
                "sha": commit["sha"],
                "message": commit["commit"]["message"]
            }
            for commit in commits
            if any(kw in commit.get("commit", {}).get("message", "").lower() 
                  for kw in commit_analyzer.related_keywords)
        ]
    
        print(f"Found {len(pattern_commits)} {pattern}-related commits in {repo_full_name}")

        successfully_processed = False
        processed_commits = 0
    
        for commit_info in pattern_commits:
            processed_commits += 1
            commit_sha = commit_info["sha"]

            print(f"\nProcessing commit {processed_commits}/{len(pattern_commits)}")
            try:
                # Fetch detailed commit information with retry logic for rate limits
                while True:
                    try:
                        commit_url = f"{config.base_url}repos/{owner}/{repo_name}/commits/{commit_sha}"
                        response = requests.get(commit_url, headers=config.headers)

                        if response.status_code == 403:  # Rate limit hit
                            reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))
                            sleep_time = reset_time - time.time() + 5
                            print(f"\nRate limit reached. Sleeping for {int(sleep_time)} seconds...")
                            time.sleep(max(sleep_time, 0))
                            continue

                        response.raise_for_status()
                        commit_data = response.json()
                        break

                    except requests.exceptions.RequestException as e:
                        if not hasattr(e, 'response') or e.response.status_code != 403:
                            raise e
                        continue

                # Get parent commit SHA for comparing changes
                parent_sha = commit_data["parents"][0]["sha"] if commit_data["parents"] else None
                changed_files = commit_data.get("files", [])

                # Initialize code extractor for this repository
                extractor = CodeExtractor(owner, repo_name)
                found_pattern_in_commit = False

                # Process each changed file in the commit
                for f in changed_files:
                    file_path = f["filename"]
                    print(f"Processing file: {file_path}")

                    # Skip non-Java files early
                    if not file_path.endswith(".java"):
                        print(f"  Skipping file (not a Java file)")
                        continue

                    # Extract both versions of the file with rate limit handling
                    while True:
                        try:
                            before_code, after_code = extractor(commit_sha, parent_sha, file_path)
                            break
                        except requests.exceptions.RequestException as e:
                            if not hasattr(e, 'response') or e.response.status_code != 403:
                                raise e
                            reset_time = int(e.response.headers.get('X-RateLimit-Reset', time.time() + 3600))
                            sleep_time = reset_time - time.time() + 5
                            print(f"\nRate limit reached. Sleeping for {int(sleep_time)} seconds...")
                            time.sleep(max(sleep_time, 0))

                    # Skip if we couldn't get the previous version
                    if before_code is None:
                        print(f"  Skipping file (no previous version)")
                        continue

                    # Validate pattern implementation, ensuring it's new
                    if pattern_validator(after_code, before_code):
                        print(f"  Found {pattern} pattern (new implementation)")
                        if data_saver(before_code, after_code, repo_full_name, commit_sha):
                            found_pattern_in_commit = True
                            successfully_processed = True

                if found_pattern_in_commit:
                    print(f"Successfully processed commit {commit_sha}")

            except Exception as e:
                print(f"Error processing commit {commit_sha}: {str(e)}")
                continue

        if successfully_processed:
            print(f"Successfully found and saved {pattern} pattern implementations")

    return successfully_processed

def main_pipeline():
    """
    Main pipeline to collect repositories and analyze commits for factory patterns.
    Focuses on detecting Factory and Abstract Factory patterns in Java code,
    specifically looking for commits that introduce new pattern implementations.
    
    The pipeline follows these steps:
    1. Initialize components and configuration
    2. Collect high-quality Java repositories
    3. Track processed repositories to avoid duplication
    4. Analyze commits for pattern-related changes
    5. Validate and save pattern implementations
    """
    # Initialize configuration and components
    config = GitHubConfig.get_instance()
    repo_tracker = RepoTracker()
    pattern_types = ["factory"]  # Factory-related patterns only

    print(f"\n=== Starting Factory Pattern Analysis Pipeline ===")
    print("\n=== Collecting Repositories ===")
    
    # Collect repositories with significant activity/usage
    repo_collector = RepoCollector(max_repos=100)
    repos = repo_collector(min_stars=5000, per_page=2, pages=500)
    
    # Display repository information
    print("\nAll found repositories:")
    for repo in repos:
        repo_full_name = f"{repo['owner']['login']}/{repo['name']}"
        status = 'processed' if repo_tracker.is_processed(repo_full_name) else 'unprocessed'
        stars = repo.get('stargazers_count', 'unknown')
        print(f"  - {repo_full_name} ({status}) - {stars} stars")
    
    # Filter out already processed repositories
    unprocessed_repos = [
        repo for repo in repos 
        if not repo_tracker.is_processed(f"{repo['owner']['login']}/{repo['name']}")
    ]
    
    if not unprocessed_repos:
        print("No new repositories to process. Exiting.")
        return
    
    # Initialize analysis components
    commit_analyzer = CommitAnalyzer()
    pattern_validator = PatternValidator()
    data_saver = DataSaver("./dataset")
    
    # Track successfully processed repositories
    successfully_processed_repos = set()
    
    # Process each repository
    for repo in unprocessed_repos:
        repo_full_name = f"{repo['owner']['login']}/{repo['name']}"
        print(f"\n=== Processing Repository: {repo_full_name} ===")
        
        if process_repository_commits(repo, commit_analyzer, pattern_validator, data_saver, config, pattern_types):
            successfully_processed_repos.add(repo_full_name)
            repo_tracker.mark_as_processed(repo_full_name)
            print(f"Successfully processed and marked {repo_full_name}")
    
    # Print summary statistics
    print(f"\n=== Factory Pattern Analysis Completed ===")
    print(f"Repositories successfully processed: {len(successfully_processed_repos)}")
    print(f"Total processed repositories: {repo_tracker.get_processed_count()}")

if __name__ == "__main__":
    main_pipeline()
