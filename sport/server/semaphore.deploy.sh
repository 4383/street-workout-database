#!/usr/bin/env bash
ssh-keyscan -H -p <port> <host> >> ~/.ssh/known_hosts
echo -e "Host *\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
git remote rm staging || true
git remote add staging  ssh://staging@<host>:<port>/home/staging/git/swd.git || true
git push --force staging $BRANCH_NAME || true