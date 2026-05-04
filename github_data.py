import requests
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["robotics_docs"]
collection = db["documentation"]


repos = [
    {"owner": "ros2", "repo": "ros2_documentation", "branch": "jazzy"},
    {"owner": "ros-navigation", "repo": "docs.nav2.org", "branch": "main"},
    {"owner": "moveit", "repo": "moveit2_tutorials", "branch": "main"},
    {"owner": "gazebosim", "repo": "docs", "branch": "master"}
]


GITHUB_API_BASE_URL = "https://api.github.com"

def fetch_repo_contents(owner, repo, branch):
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/contents?ref={branch}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {owner}/{repo}. Status code: {response.status_code}")
        return []

def fetch_raw_file_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch raw file content. Status code: {response.status_code}")
        return ""

def insert_documentation_to_mongo(owner, repo, branch):
    contents = fetch_repo_contents(owner, repo, branch)
    for item in contents:
        if item["type"] == "file" and item["name"].endswith((".md", ".rst")):  
            raw_content = fetch_raw_file_content(item["download_url"])
            if raw_content:
                document = {
                    "repository": f"{owner}/{repo}",
                    "file_name": item["name"],
                    "file_url": item["html_url"],
                    "content": raw_content
                }
                collection.insert_one(document)
                print(f"Inserted {item['name']} from {owner}/{repo} into MongoDB.")

if __name__ == "__main__":
    for repo in repos:
        insert_documentation_to_mongo(repo["owner"], repo["repo"], repo["branch"])

