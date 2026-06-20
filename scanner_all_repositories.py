import os
import requests

USER = os.getenv('USER_NAME')
TOKEN = os.getenv('API_TOKEN')
README_PATH = "README.md"

SKIP_SUFFIXES = (
    '-front', '-back', '-docs', 'hub-projects', 'chavesvini', 
    'linguagem-de-programacao-i', 'test-', 'teste-', 'testes-', 
    'projeto-', 'prova-', 'portfolio-bd', 'practice_', 'lpii', 
    'bertoti', 'programação', 'areachecker', 'avaliação', 'start with java'
)

def get_my_repos_by_category():
    url = f"https://api.github.com/users/{USER}/repos?per_page=100"

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Hub-Projects-Scanner"  
    }

    company_assessments = []
    personal_projects = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        repos_data = response.json()
        
        for r in repos_data:
            name = r['name']
            
            if r['fork'] or r.get('private', False) or any(s.lower() in name.lower() for s in SKIP_SUFFIXES):
                continue
                
            desc = (r.get('description') or "").lower()
            repo_url = f"https://github.com/{USER}/{name}"
            repo_data = {"name": name, "url": repo_url}
            
            if "company assessment" in desc:
                company_assessments.append(repo_data)
            else:
                personal_projects.append(repo_data)
        
    except Exception as e:
        return [], []
    
    company_assessments.sort(key=lambda x: x['name'].lower())
    personal_projects.sort(key=lambda x: x['name'].lower())
    
    return company_assessments, personal_projects

def build_table_md(title, repos_list):
    if not repos_list:
        return ""
    
    lines = [
        f"### {title}\n",
        "| Project | Link |",
        "| :---: | :---: |"
    ]
    for r in repos_list:
        lines.append(f"| **{r['name']}** | [View Repository]({r['url']}) |")
        
    return "\n".join(lines) + "\n"

def update_readme(company_list, personal_list):
    company_table = build_table_md("Company Assessments", company_list)
    personal_table = build_table_md("Personal Projects", personal_list)

    readme_template = f"""## Hub-Projects

Welcome! This is a collection of my technical work, including academic projects, personal experiments, and coding challenges for company assessments. Feel free to explore using the links below.

### Academic Projects

| Project | Link |
| :---: | :---: |
| **Avaliação 360** | [View Repository](https://github.com/wiz-fatec/avaliacao-360) |
| **Dom Rock Pipeline Configurator** | [View Repository](https://github.com/wiz-fatec/dom-rock-pipeline-configurator) |
| **GEO-IOT** | [View Repository](https://github.com/manolito-fatec/geo-iot-2024-1) |
| **LuminIA** | [View Repository](https://github.com/new-ge/LuminIA) |
| **TG Manager** | [View Repository](https://github.com/wiz-fatec/api-2BD) |
| **Vision** | [View Repository](https://github.com/new-ge/VISION) |

{company_table}
{personal_table}
"""
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_template)
