#!/bin/bash

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

git fetch origin main
git reset --hard origin/main

if [[ "$REPO_NAME" == *"-front" ]] || [[ "$REPO_NAME" == *"-back" ]] || [[ "$REPO_NAME" == *"-docs" ]]; then
  echo "Repo $REPO_NAME ignorado pelos sufixos."
  exit 0
fi

mkdir -p projects
touch README.md

if ! curl -s -I -f "https://github.com/$USER_NAME/$REPO_NAME" > /dev/null; then
  echo "Erro: O repositório $REPO_NAME não pertence a $USER_NAME ou é privado/org."
  exit 1
fi

echo "Erro: $API_TOKEN $REPO_NAME $USER_NAME"

git remote set-url origin "https://x-access-token:${API_TOKEN}@github.com/${USER_NAME}/Hub-Projects.git"

if [ ! -d "projects/$REPO_NAME" ]; then
  git submodule add "https://github.com/$USER_NAME/$REPO_NAME.git" "projects/$REPO_NAME"
fi

if ! grep -q "$REPO_NAME" README.md; then
  if ! grep -q "Projeto | Link" README.md; then
    echo -e "\n| Projeto | Link |" >> README.md
    echo "| :---: | :---: |" >> README.md
  fi
  echo "| $REPO_NAME | [Acessar](https://github.com/$USER_NAME/$REPO_NAME) |" >> README.md
fi

git add .
git commit -m "auto: link submodule $REPO_NAME and add on README.md" || echo "Nada para commitar"
git pull --rebase -X ours origin main
git push origin main || (sleep 5 && git pull --rebase origin main && git push origin main)
