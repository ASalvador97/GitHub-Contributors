import unittest
from unittest.mock import MagicMock, patch
from repo_contributors import *

class GitHubClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = GitHubClient()
        
    def test_get_repos_success(self):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"repo1": {"name": "repo1"}}'
        
        # Patch the 'requests.get' method
        with patch('requests.get', return_value=mock_response):
            repos = self.client.get_repos("USERNAME")
            self.assertEqual(repos, {"repo1": {"name": "repo1"}})
    
    def test_get_repos_failure(self):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '{"message": "Not Found"}'
        
        # Patch the 'requests.get' method
        with patch('requests.get', return_value=mock_response):
            self.assertRaises(Exception, self.client.get_repos)
            
    def test_get_contributors_success(self):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '[{"login": "user1", "contributions": 10}]'
        
        # Patch the 'requests.get' method
        with patch('requests.get', return_value=mock_response):
            contributors = self.client.get_contributors("contributors_url")
            self.assertEqual(contributors, [{"login": "user1", "contributions": 10}])
    
    def test_get_contributors_failure(self):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '{"message": "Not Found"}'
        
        # Patch the 'requests.get' method
        with patch('requests.get', return_value=mock_response):
            self.assertRaises(Exception, self.client.get_contributors)

class GitHubServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = GitHubService()
        self.repository = GitHubRepository()

    def test_get_contributors_by_username(self):
        # Create a mock repository object
        mock_repository = MagicMock()
        mock_repository.get_repos.return_value = [{"name": "test_repo", "contributors_url": "test_contributors_url"}]
        mock_repository.get_contributors_by_username.return_value = [{"login": "test_user", "contributions": 10}, {"login": "test_user2", "contributions": 11}]
        
        # Patch the repository object
        self.service.repository = mock_repository
        
        contributors = self.service.get_contributors_by_username("test_username")
        
        # Assert that the correct number of contributors are returned
        self.assertEqual(len(contributors), 2)
        
        # Assert that the correct repository name is added to the contributor object
        self.assertEqual(contributors[0]["repo_name"], "test_repo")

        # Assert that the contributors are ordered by contributions in descending order
        self.assertListEqual([contributor["contributions"] for contributor in contributors], [11, 10])


    def test_get_contributors_by_username_failure(self):
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '{"message": "Not Found"}'

        # Patch the 'requests.get' method
        with patch('requests.get', return_value=mock_response):
            self.assertRaises(Exception, self.service.get_contributors_by_username, "test_username")
