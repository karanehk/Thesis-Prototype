from github_data_extractor import GitHubDataExtractor
from commit_preprocessor import CommitPreprocessor
from commit_analyzer import CommitAnalyzer
from openai_interface import OpenAIAPI
import pandas as pd
from user_interface import UserInterface


class Application:
    def __init__(self):
        self.ui = UserInterface()


    def save_analyzed_df(self, analyzed_df):
        analyzed_df.to_csv('preprocessed_commits.csv', index=False, columns=['sha', 'message', 'author_name', 'author_date', 'committer_name', 'committer_date', 'additions', 'deletions', 'total_changes', 'sentiment', 'diff_score'])


    def run(self):
        # Get git details
        self.owner, self.repo, self.token = self.ui.get_git_details()

        # Instantiate GitHubDataExtractor
        github_extractor = GitHubDataExtractor(self.owner, self.repo, self.token)
        # Get commits
        print("Fetching commits...")
        commits_data = github_extractor.get_commits()

        print(f"Collected {len(commits_data)} commits. Fetching details and preprocessing...")

        # Instantiate CommitPreprocessor
        preprocessor = CommitPreprocessor(self.owner, self.repo, self.token)
        # Preprocess commits
        processed_commits_df = preprocessor.preprocess_commits(commits_data)        

        # Instantiate CommitAnalyzer
        analyzer = CommitAnalyzer(processed_commits_df, self.owner, self.repo, self.token)
        # Analyze commits
        analyzed_df = analyzer.analyze_commits()
        print("Preprocessing & Analyses completed.")
        self.save_analyzed_df(analyzed_df)

        # Instantiate OopenAIAPI
        openai_api = OpenAIAPI()
        # Get the criteria
        criteria = self.ui.get_criteria()
        gpt_response = openai_api.ask_gpt(criteria)

        self.ui.show_results(gpt_response)


if __name__ == "__main__":
    app = Application()
    app.run()