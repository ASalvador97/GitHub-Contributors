import requests
import json
from itertools import groupby


class GitHubController:
    # Calls the service, REST interface, exposes functionality
    def __init__(self):
        self.service = GitHubService()
    
    def get_contributors_by_username(self, username):
        contributors = self.service.get_contributors_by_username(username)
        return contributors

class GitHubService:
    # Calls the repository for data, contains business logic
    def __init__(self):
        self.repository = GitHubRepository()

    def get_contributors_by_username(self, username):
        repos = self.repository.get_repos(username)
        contributors = []
        for repo in repos:
            repo_contributors = self.repository.get_contributors_by_username(repo['contributors_url'])
            try:
                repo_contributors.sort(key=lambda x: x['contributions'], reverse=True)
                for contributor in repo_contributors:
                    contributor["repo_name"] = repo["name"]
                    contributors.append(contributor)
            except:
                print(f"Could not read contributors from {repo['full_name']}")
        return contributors

class GitHubRepository:
    # Calls the client, ingress for data
    def __init__(self):
        self.client = GitHubClient()
    
    def get_repos(self, username):
        repos = self.client.get_repos(username)
        return repos

    def get_contributors_by_username(self, contributors_url):
        contributors = self.client.get_contributors(contributors_url)
        return contributors

class GitHubClient:
    # Makes http calls, called by repository
    def __init__(self):
        self.base_url = "https://api.github.com"
    
    def get_repos(self, username):
        endpoint = f"{self.base_url}/users/{username}/repos"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(f"Error getting repos for user: {username} Error code: {response.status_code}")
    
    def get_contributors(self, contributors_url):
        response = requests.get(contributors_url)
        if response.status_code == 204 or response.status_code == 200:
            try:
                contributors_data = json.loads(response.text)
                return contributors_data
            except:
                print(f"Error reading data for: {contributors_url}")               
        else:
            raise Exception(f"Error getting contributors: {response.status_code}")

# Usage example
controller = GitHubController()
contributors = controller.get_contributors_by_username("USERNAME")

for repo_name, repo_contributors in groupby(contributors, key=lambda x: x['repo_name']):
    print(f"{repo_name}")
    for contributor in repo_contributors:
        print(f"{contributor['login']} : {contributor['contributions']}")

#for contributor in contributors:
#    print(f"{contributor['login']} contributions to {contributor['repo_name']}: {contributor['contributions']}")
