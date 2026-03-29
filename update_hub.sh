#!/bin/bash

mkdir -p projects
touch README.md

if [ -d ".git/modules/projects/$REPO_NAME" ] || grep -q "path = projects/$REPO_NAME" .gitmodules 2>/dev/null; then
  echo "$REPO_NAME já é um submódulo. Pulando..."
else
  echo "Adicionando submódulo: $REPO_NAME"
  git submodule add "https://github.com/$USER_NAME/$REPO_NAME.git" "projects/$REPO_NAME" || true
fi

if ! grep -q "| $REPO_NAME |" README.md; then
  if ! grep -q "Projeto | Link" README.md; then
    echo -e "\n| Projeto | Link |" >> README.md
    echo "| :---: | :---: |" >> README.md
  fi
  echo "| $REPO_NAME | [Acessar](https://github.com/$USER_NAME/$REPO_NAME) |" >> README.md
fi

if [ "$SKIP_COMMIT" != "true" ]; then
    git add .
    git commit -m ":memo: add $REPO_NAME in README.md and submodule"
    git push origin main
fi