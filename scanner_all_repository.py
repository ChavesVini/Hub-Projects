import os
import requests
import subprocess

USER = os.getenv('USER_NAME')
TOKEN = os.getenv('API_TOKEN')
SKIP_SUFFIXES = ('-front', '-back', '-docs', 'Hub-Projects')

def get_my_repos():
    url = f"https://api.github.com/users/{USER}/repos"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)
    return [r['name'] for r in response.json() if not r['name'].endswith(SKIP_SUFFIXES)]

def run_update(repo_name):
    print(f"🚀 Processando: {repo_name}")
    subprocess.run(["bash", "./update_hub.sh"], env={**os.environ, "REPO_NAME": repo_name})

if __name__ == "__main__":
    repos = get_my_repos()
    for repo in repos:
        run_update(repo)