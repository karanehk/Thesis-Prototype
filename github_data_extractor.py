import requests
from retry import retry
from time import sleep


class GitHubDataExtractor:
    def __init__(self, owner, repo, token):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    @retry(tries=5, delay=10, backoff=2)
    def get_commit_stats(self, sha):
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/commits/{sha}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['stats']
        else:
            return {'additions': 0, 'deletions': 0, 'total': 0}

    @retry(tries=5, delay=5, backoff=2)
    def get_commits(self):
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/commits"
        commits = []

        while url:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                break
            response_data = response.json()
            commits.extend(response_data)
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
            sleep(1)  # Sleep to avoid hitting rate limit

        return commits
    
    @retry(tries=5, delay=5, backoff=2)
    def get_commit_diff(self, sha):
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/commits/{sha}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            diffs = response.json()['files']
            return diffs
        else:
            return []