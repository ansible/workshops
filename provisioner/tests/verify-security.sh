#!/usr/bin/env bash

set -eu

DEPLOYMENT_NAME=$(grep 'ec2_name_prefix' provisioner/tests/ci-common.yml | cut -d' ' -f2)

ansible-playbook provisioner/tests/security_verify.yml \
    -i provisioner/${DEPLOYMENT_NAME}/instructor_inventory.txt \
    --private-key=provisioner/${DEPLOYMENT_NAME}/${DEPLOYMENT_NAME}-private.pem


cat provisioner/${DEPLOYMENT_NAME}/instructor_inventory.txt
cat provisioner/${DEPLOYMENT_NAME}/${DEPLOYMENT_NAME}-private.pem

ansible-playbook -vvv provisioner/tests/security_exercise_21.yml \
    -i provisioner/${DEPLOYMENT_NAME}/student1-instances.txt
