#!/bin/zsh

echo 'Copying over logs from jenkins server...'
mkdir -p jenkins_local_logs

scp -r -i /Volumes/Encrypted/full_stack_keypair.pem ubuntu@jenkins.n-ws.org:/home/ubuntu/tmp_jenkins_healthchecks/local_cron_job/logs ./jenkins_local_logs

echo 'Copying over logs from remote web server...'
mkdir -p remote_logs

scp -r srv-cslnp8bqf0us7390f4mg@ssh.frankfurt.render.com:/var/data/logs ./remote_logs/
