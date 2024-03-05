import requests
from retry import retry
from time import sleep
from git import Repo



class RepoDataExtractor:
    def __init__(self, repo_url, temp_repo_dir):
        self.repo_url = repo_url
        self.repo = Repo.clone_from(repo_url, temp_repo_dir)
        

    def get_commit_stats(self, sha):
        commit = self.repo.commit(sha)
        stats = {
            'additions': commit.stats.total['insertions'],
            'deletions': commit.stats.total['deletions'],
            'total': commit.stats.total['lines'],
        }
        return stats

    def get_commits(self):
        commits = []
        for commit in self.repo.iter_commits():
            commits.append({
                'sha': commit.hexsha,
                'message': commit.message,
                'author_name': commit.author.name,
                'author_date': commit.authored_datetime.isoformat(),
                'committer_name': commit.committer.name,
                'committer_date': commit.committed_datetime.isoformat(),
            })
        return commits
    
    def get_commit_diff(self, sha):
        commit = self.repo.commit(sha)
        diff_data = []

        for parent in commit.parents:
            diff_index = parent.diff(commit, create_patch=True)
            for diff_item in diff_index.iter_change_type('M'):
                diff_data.append({
                    'file_name': diff_item.b_path,
                    'diff_text': diff_item.diff.decode('utf-8', 'replace'),
                })

        return diff_data