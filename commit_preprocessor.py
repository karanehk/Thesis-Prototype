from time import sleep
import pandas as pd


class CommitPreprocessor:

    def __init__(self, data_extractor):
        self.data_extractor = data_extractor

    def preprocess_commits(self, commits):
        commit_list = []

        for commit_data in commits:
            stats = self.data_extractor.get_commit_stats(commit_data['sha'])
            #commit_data = commit['commit']
            commit_list.append({
                'sha': commit_data['sha'],
                'message': commit_data['message'],
                'author_name': commit_data['author_name'],
                'author_date': commit_data['author_date'],
                'committer_name': commit_data['committer_name'],
                'committer_date': commit_data['committer_date'],
                'additions': stats['additions'],
                'deletions': stats['deletions'],
                'total_changes': stats['total']
            })

        # Convert to DataFrame
        df = pd.DataFrame(commit_list)
        df['author_date'] = pd.to_datetime(df['author_date'])
        df['committer_date'] = pd.to_datetime(df['committer_date'])

        return df