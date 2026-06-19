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

ACADEMIC_ORGS_REPOS = [
    {"name": "Avaliação 360", "url": "https://github.com/wiz-fatec/avaliacao-360"},
    {"name": "Dom Rock Pipeline Configurator", "url": "https://github.com/wiz-fatec/dom-rock-pipeline-configurator"},
    {"name": "GEO-IOT", "url": "https://github.com/manolito-fatec/geo-iot-2024-1"},
    {"name": "LuminIA", "url": "https://github.com/new-ge/LuminIA"},
    {"name": "TG Manager", "url": "https://github.com/wiz-fatec/api-2BD"},
    {"name": "Vision", "url": "https://github.com/new-ge/VISION"},
]

def get_my_repos_by_category():
    url = f"https://api.github.com/users/{USER}/repos?per_page=100"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    company_assessments = []
    personal_projects = []
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos_data = response.json()

        for r in repos_data:
            name = r['name']
            
            if any(s.lower() in name.lower() for s in SKIP_SUFFIXES) or r['fork'] or r.get('private', False):
                continue
                
            desc = (r.get('description') or "").lower()
            repo_url = f"https://github.com/{USER}/{name}"
            repo_data = {"name": name, "url": repo_url}
            
            if "company assessment" in desc:
                company_assessments.append(repo_data)
            else:
                personal_projects.append(repo_data)
                
        company_assessments.sort(key=lambda x: x['name'].lower())
        personal_projects.sort(key=lambda x: x['name'].lower())
        
        return company_assessments, personal_projects
        
    except Exception as e:
        print(f"Erro ao buscar repositórios: {e}")
        return [], []

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
    print("Gerando o conteúdo completo do README...")
    
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

    print("README.md reescrito com sucesso do zero!")