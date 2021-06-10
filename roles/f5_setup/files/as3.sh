#!/bin/bash
# F5 Networks - Install Latest AS3 Package
# https://github.com/ArtiomL/f5networks
# Artiom Lichtenstein
# v1.0.3, 01/09/2018

# Download and unzip
cd /var/config/rest/downloads/
curl -fLOs https://github.com/F5Networks/f5-appsvcs-extension/archive/master.zip
unzip -joq master.zip "f5-appsvcs-extension-master/dist/f5-appsvcs*noarch.rpm*"

# Integrity verification
sha2Repo=$(cat f5-appsvcs-*.sha256 | awk '{print $1}')
strFile=$(cat f5-appsvcs-*.sha256 | awk '{print $2}')
sha2Real=$(sha256sum $strFile | awk '{print $1'})

# RPM install
if [ "$sha2Real" == "$sha2Repo" ] ; then
  touch /var/config/rest/iapps/enable
  strData="{\"operation\":\"INSTALL\",\"packageFilePath\":\"/var/config/rest/downloads/$strFile\"}"
  restcurl -X POST "shared/iapp/package-management-tasks" -d $strData
fi

# Cleanup
rm -f master.zip
