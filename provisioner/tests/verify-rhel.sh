#!/usr/bin/env bash

set -eu

DEPLOYMENT_NAME=$(grep 'ec2_name_prefix' provisioner/tests/ci-common.yml | cut -d' ' -f2)
ADMIN_PASSWORD=$(grep 'admin_password' provisioner/tests/ci-common.yml | cut -d' ' -f2)

ansible-playbook provisioner/tests/rhel_verify.yml \
  -i provisioner/${DEPLOYMENT_NAME}/instructor_inventory.txt \
  --private-key=provisioner/${DEPLOYMENT_NAME}/${DEPLOYMENT_NAME}-private.pem \
  -e tower_password=${ADMIN_PASSWORD} \
  -e workshop_name=${DEPLOYMENT_NAME}
