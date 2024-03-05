from repo_data_extractor import RepoDataExtractor
from commit_preprocessor import CommitPreprocessor
from commit_analyzer import CommitAnalyzer
from openai_interface import OpenAIAPI
import pandas as pd
from user_interface import UserInterface
import shutil


class Application:
    def __init__(self):
        self.ui = UserInterface()


    def save_analyzed_df(self, analyzed_df):
        analyzed_df.to_csv('preprocessed_commits.csv', index=False, columns=['sha', 'message', 'author_name', 'author_date', 'committer_name', 'committer_date', 'additions', 'deletions', 'total_changes', 'sentiment', 'diff_score'])


    def run(self):
        # Get git details
        self.repo_url, self.temp_repo_dir = self.ui.get_git_details()

        # Instantiate GitHubDataExtractor
        data_extractor = RepoDataExtractor(self.repo_url, self.temp_repo_dir)
        # Get commits
        print("Fetching commits...")
        commits_data = data_extractor.get_commits()

        print(f"Collected {len(commits_data)} commits. Fetching details and preprocessing...")

        # Instantiate CommitPreprocessor
        preprocessor = CommitPreprocessor(data_extractor)
        # Preprocess commits
        processed_commits_df = preprocessor.preprocess_commits(commits_data)        

        # Instantiate CommitAnalyzer
        analyzer = CommitAnalyzer(processed_commits_df, data_extractor)
        # Analyze commits
        analyzed_df = analyzer.analyze_commits()
        print("Preprocessing & Analyses completed.")
        self.save_analyzed_df(analyzed_df)

        # Instantiate openAIAPI
        openai_api = OpenAIAPI()
        # Get the criteria
        criteria = self.ui.get_criteria()
        gpt_response = openai_api.ask_gpt(criteria)

        self.ui.show_results(gpt_response)

        shutil.rmtree(self.temp_repo_dir)



if __name__ == "__main__":
    app = Application()
    app.run()