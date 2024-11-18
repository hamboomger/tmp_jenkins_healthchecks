#!/bin/zsh

echo 'Copying over logs from jenkins server...'
mkdir -p jenkins_local_logs

scp -r -i /Volumes/Encrypted/full_stack_keypair.pem ubuntu@jenkins.n-ws.org:/home/ubuntu/tmp_jenkins_healthchecks/local_cron_job/logs ./jenkins_local_logs
