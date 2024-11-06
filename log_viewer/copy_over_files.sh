#!/bin/zsh

# copy over jenkins local file
mkdir jenkins_local_logs

scp -r -i full_stack_keypair.pem ubuntu@jenkins.n-ws.org:/home/ubuntu/test-dir/logs ./jenkins_local_logs

# copy over file from remote server
mkdir remote_logs

scp -r srv-cslnp8bqf0us7390f4mg@ssh.frankfurt.render.com:/var/data/logs ./remote_logs/
