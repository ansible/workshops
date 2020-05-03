#!/usr/bin/env bash

set -eu

DEPLOYMENT_NAME=$(grep 'ec2_name_prefix' provisioner/tests/ci-common.yml | cut -d' ' -f2)
ADMIN_PASSWORD=$(grep 'admin_password' provisioner/tests/ci-common.yml | cut -d' ' -f2)

CONTROL_NODE_HOST=$(grep -A 1 control provisioner/${DEPLOYMENT_NAME}/student1-instances.txt | tail -n 1 | cut -d' ' -f 2 | cut -d'=' -f2)

RUN_ALL_PLAYBOOKS_CMD='find . -name "*.yml" -o -name "*.yaml" | grep -v "2.0" | sort | xargs -I {} bash -c "echo {} && ANSIBLE_FORCE_COLOR=true ansible-playbook {}"'

sshpass -p "${ADMIN_PASSWORD}" ssh -o StrictHostKeyChecking=no student1@${CONTROL_NODE_HOST} "cd f5-workshop && ${RUN_ALL_PLAYBOOKS_CMD}"
