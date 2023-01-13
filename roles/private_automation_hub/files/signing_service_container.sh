#!/usr/bin/env bash

set -u
# This GPG_TTY variable might be needed on a container image that is not running as root.
#export GPG_TTY=$(tty)
# Create a file with passphrase only if the key is password protected.
# echo "Galaxy2022" > /tmp/key_password.txt
# pulp_container SigningService will pass the next 3 variables to the script.
MANIFEST_PATH=$1
IMAGE_REFERENCE="$REFERENCE"
SIGNATURE_PATH="$SIG_PATH"
# Create container signature using skopeo
# Include --passphrase-file option if the key is password protected.
skopeo standalone-sign \
  $MANIFEST_PATH \
  $IMAGE_REFERENCE \
  $PULP_SIGNING_KEY_FINGERPRINT \
  --output $SIGNATURE_PATH
# Check the exit status
STATUS=$?
if [ $STATUS -eq 0 ]; then
  echo {\"signature_path\": \"$SIGNATURE_PATH\"}
else
  exit $STATUS
fi
