from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

class OpenAIAPI:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def data_to_gpt_text(self, filename, row_limit=40):
        df = pd.read_csv(filename)
        df = df.head(row_limit)
        result = df.to_markdown(index=False, tablefmt="grid")
        return result

    def get_gpt_prompt(self, criteria):
        preprocessed_commits = self.data_to_gpt_text('preprocessed_commits.csv')
        commit_trends = self.data_to_gpt_text('commit_trends.csv')
        commit_frequency_by_author = self.data_to_gpt_text('commit_frequency_by_author.csv')
        gpt_prompt = f"Based on this commit data:\n\nPREPROCESSED COMMITS:\n{preprocessed_commits}\n\n" \
                f"COMMIT TRENDS:\n{commit_trends}\n\n" \
                f"COMMIT FREQUENCY BY AUTHOR:\n{commit_frequency_by_author}\n\n" \
                f"{criteria}"
        
        return gpt_prompt
    
    def get_gpt_response(self, prompt, model="gpt-3.5-turbo", assistant="You are a helpful assistant, skilled in analyzing data and information given to you, GitHub, software engineering, and detecting cheating after getting related data in a software engineering project."):
        completion = self.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": assistant
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        )
        return completion.choices[0].message.content
    
    def ask_gpt(self, criteria):
        prompt = self.get_gpt_prompt(criteria)
        response = self.get_gpt_response(prompt=prompt)

        return response

    

