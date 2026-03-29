#!/bin/bash

mkdir -p projects
touch README.md

if [ -d ".git/modules/projects/$REPO_NAME" ] || grep -q "path = projects/$REPO_NAME" .gitmodules 2>/dev/null; then
  echo "Skipping: $REPO_NAME is already registered as a submodule."
else
  echo "Adding submodule: $REPO_NAME"
  git submodule add "https://github.com/$USER_NAME/$REPO_NAME.git" "projects/$REPO_NAME" || true
fi

if ! grep -qi "|.*$REPO_NAME.*|" README.md; then
  if ! grep -q "Project | Link" README.md; then
    echo -e "\n| Project | Link |" >> README.md
    echo "| :---: | :---: |" >> README.md
  fi

  echo "| **$REPO_NAME** | [View Repository](https://github.com/$USER_NAME/$REPO_NAME) |" >> README.md
  echo "Added $REPO_NAME to README."
else
  echo "Skipping: $REPO_NAME already exists in README."
fi