import os
import requests
import subprocess

USER = os.getenv('USER_NAME')
TOKEN = os.getenv('API_TOKEN')

SKIP_SUFFIXES = ('-front', '-back', '-docs', 'Hub-Projects', 'ChavesVini', 'Linguagem-de-Programacao')

def get_my_repos():
    url = f"https://api.github.com/users/{USER}/repos?per_page=100"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos_data = response.json()

        # Filtrando FORKS e nomes proibidos
        return [
            r['name'] for r in repos_data 
            if not any(r['name'].endswith(s) for s in SKIP_SUFFIXES)
            and not r['fork'] 
            and not r.get('private', False)
        ]
        
    except Exception as e:
        print(f"❌ Erro ao buscar repositórios: {e}")
        return []

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Erro: API_TOKEN não encontrado.")
    else:
        repos = get_my_repos()
        print(f"🔍 Encontrados {len(repos)} repositórios autorais.")
        
        for repo in repos:
            print(f"🚀 Preparando: {repo}")
            subprocess.run(["bash", "./update_hub.sh"], env={**os.environ, "REPO_NAME": repo, "SKIP_COMMIT": "true"})
        
        print("💾 Finalizando: Fazendo commit de todas as alterações...")
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", ":sparkles: add projects to hub-projects"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)