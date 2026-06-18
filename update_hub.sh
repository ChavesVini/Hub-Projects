#!/bin/bash
touch README.md

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