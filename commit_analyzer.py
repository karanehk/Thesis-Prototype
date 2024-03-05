from time import sleep
from textblob import TextBlob
import pandas as pd
import difflib


class CommitAnalyzer:
    def __init__(self, df_commits, data_extractor):
        self.data_extractor = data_extractor
        self.df_commits = df_commits


    def analyze_commit_messages(self):
        self.df_commits['sentiment'] = self.df_commits['message'].apply(lambda msg: TextBlob(msg).sentiment.polarity)


    def time_series_analysis(self):
        self.df_commits.set_index(pd.to_datetime(self.df_commits['author_date']), inplace=True)
        commit_counts = self.df_commits.resample('D').size()  
        commit_counts.to_csv('commit_trends.csv', index=True)


    def commit_frequency_by_author(self):
        freq_by_author = self.df_commits.groupby('author_name').size().sort_values(ascending=False)
        freq_by_author.to_csv('commit_frequency_by_author.csv', index=True)
    

    def parse_diffs(self, diffs):
        parsed_diffs = {}
        for file_diff in diffs:
            file_name = file_diff['file_name']
            diff_text = file_diff['diff_text']
            '''diff_lines = diff_text.split('\n')
            diff_blocks = []
            for line in diff_lines:
                if line.startswith('@@'):
                    diff_blocks.append([line])
                elif line.startswith('+') or line.startswith('-') or line.startswith(' '):
                    if diff_blocks:
                        diff_blocks[-1].append(line)'''
            parsed_diffs[file_name] = diff_text
        return parsed_diffs


    def diff_analysis(self, all_diffs):
        diff_scores = []
        for index, row in self.df_commits.iterrows():
            sha = row['sha']
            diffs = all_diffs.get(sha, {})
            total_diff_score = 0
            for _, diff_blocks in diffs.items():
                for diff_block in diff_blocks:
                    diff_score = difflib.SequenceMatcher(None, diff_block[0][0][2:], diff_block[0][-1][2:]).ratio()
                    total_diff_score += diff_score
            diff_scores.append(total_diff_score)
        self.df_commits['diff_score'] = diff_scores


    def analyze_commit_diffs(self):
        all_diffs = {}
        for sha in self.df_commits['sha']:
            diffs = self.data_extractor.get_commit_diff(sha)
            parsed_diffs = self.parse_diffs(diffs)
            all_diffs[sha] = parsed_diffs
            sleep(1)  # Sleep between requests

        self.diff_analysis(all_diffs)


    def analyze_commits(self):
        self.time_series_analysis()
        self.commit_frequency_by_author()
        self.analyze_commit_messages()
        self.analyze_commit_diffs()

        return self.df_commits
        
    
    # Other analysis methods...