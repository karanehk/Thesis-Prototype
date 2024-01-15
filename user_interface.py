
class UserInterface:
    def __init__(self):
        pass
    
    def get_git_details(self):
        # Get inputs from user
        owner = "karanehk"
        repo = "software_eng_lab6"
        token = "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"

        return owner, repo, token
    
    def get_criteria(self):
        criteria = "Please review and identify any potential cheating or unusual behavior. Analyze the data above and explain your reasoning:"

        return criteria
    
    def show_results(self, response):
        print(response)


