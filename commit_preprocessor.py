from github_data_extractor import GitHubDataExtractor
from time import sleep
import pandas as pd


class CommitPreprocessor:

    def __init__(self, owner, repo, token):
        self.github_extractor = GitHubDataExtractor(owner, repo, token)

    def preprocess_commits(self, commits):
        commit_list = []

        for commit in commits:
            stats = self.github_extractor.get_commit_stats(commit['sha'])
            commit_data = commit['commit']
            commit_list.append({
                'sha': commit.get('sha'),
                'message': commit_data['message'],
                'author_name': commit_data['author']['name'],
                'author_date': commit_data['author']['date'],
                'committer_name': commit_data['committer']['name'],
                'committer_date': commit_data['committer']['date'],
                'additions': stats['additions'],
                'deletions': stats['deletions'],
                'total_changes': stats['total']
            })
            sleep(1)  # Sleep to avoid hitting rate limit

        # Convert to DataFrame
        df = pd.DataFrame(commit_list)
        df['author_date'] = pd.to_datetime(df['author_date'])
        df['committer_date'] = pd.to_datetime(df['committer_date'])

        return df