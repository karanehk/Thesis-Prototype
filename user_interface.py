
class UserInterface:
    def __init__(self):
        pass
    
    def get_git_details(self):
        # Get inputs from user
        repo_url = "https://github.com/karanehk/software_eng_lab4"
        temp_repo_dir = "./temp"

        return repo_url, temp_repo_dir
    
    def get_criteria(self):
        criteria = "Please review and identify any potential cheating or unusual behavior. Analyze the data above and explain your reasoning:"

        return criteria
    
    def show_results(self, response):
        print(response)


