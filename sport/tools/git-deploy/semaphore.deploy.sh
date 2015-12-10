#!/usr/bin/env bash
ssh-keyscan -H -p <port> <host> >> ~/.ssh/known_hosts
echo -e "Host *\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
scp -P <port> sport/tools/git-deploy/post-update.sh staging@<host>:/home/staging/git/staging.swd.git/hooks/post-update
ssh -p <port> staging@<host> 'chmod +x /home/staging/git/staging.swd.git/hooks/post-update'
git remote rm hub || true
git remote add hub  ssh://staging@<host>:<port>/home/staging/git/swd.git || true
git push --force hub staging || true