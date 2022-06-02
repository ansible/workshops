#!/usr/bin/env bash

FILE_PATH=$1
SIGNATURE_PATH="$1.asc"
          
ADMIN_ID="$PULP_SIGNING_KEY_FINGERPRINT"
PASSWORD="password"
          
# Create a detached signature
gpg --quiet --batch --yes --passphrase \
   $PASSWORD --homedir ~/.gnupg/ --detach-sign --default-key $ADMIN_ID \
   --armor --output $SIGNATURE_PATH $FILE_PATH
          
# Check the exit status
STATUS=$?
if [ $STATUS -eq 0 ]; then
   echo {\"file\": \"$FILE_PATH\", \"signature\": \"$SIGNATURE_PATH\"}
else
   exit $STATUS
fi
