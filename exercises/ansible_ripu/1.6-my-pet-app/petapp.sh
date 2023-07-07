#!/bin/bash
#
# Script to install Spring Pet Clinic on a RHEL pet app server
#
# Usage: curl -s https://people.redhat.com/bmader/petapp.sh | bash
#

# Don't run as root!
if [[ $USER == root ]]; then
  echo 'This script must run by non-root user.'
  exit 1
fi

# Install 3rd-party JDK runtime
distver=$(sed -r 's/([^:]*:){4}//;s/(.).*/\1/' /etc/system-release-cpe)
sudo yum-config-manager --add-repo=https://packages.adoptium.net/artifactory/rpm/rhel/$distver/x86_64
sudo yum-config-manager --save --setopt=\*adoptium\*.gpgkey=https://packages.adoptium.net/artifactory/api/gpg/key/public
sudo yum -y install mariadb mariadb-server temurin-17-jdk

# Verify JDK runtime installed
rpm -q temurin-17-jdk
if [[ $? -ne 0 ]]; then
  echo 'Install of JDK failed! Try installing manually.'
  exit 1
fi

# Download the app
cd $HOME
rm -rf spring-petclinic app.log .m2 .config/jgit
git clone https://github.com/spring-projects/spring-petclinic.git

# Verify app download
if [[ ! -x spring-petclinic/mvnw ]]; then
  echo 'App download failed! Review output above for clues.'
  exit 1
fi

# Open firewall rules
if [[ -x /usr/bin/firewall-cmd ]]; then
  sudo firewall-cmd --add-port=8080/tcp
  sudo firewall-cmd --add-port=8080/tcp --permanent
fi

# Set up the database
sudo systemctl enable --now mariadb
mysql --user root <<EOF
CREATE DATABASE IF NOT EXISTS petclinic;
ALTER DATABASE petclinic
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON petclinic.* TO 'petclinic'@'localhost' IDENTIFIED BY 'petclinic';
FLUSH PRIVILEGES;
EOF
if [[ $? -ne 0 ]]; then
  echo 'Database config failed! Review output above for clues.'
  exit 1
fi

# Start app web service
kill $(pidof java) 2> /dev/null
echo 'Starting the app web service. Please wait patiently...'
echo 'cd $HOME/spring-petclinic && ./mvnw spring-boot:run -Dspring-boot.run.profiles=mysql >> $HOME/app.log 2>&1' | at now

# Verify app started
retry=300
touch app.log
until grep -q 'Started PetClinic' app.log; do
  sleep 1
  if [[ $((retry--)) -le 0 ]]; then
    echo 'Timeout waiting for app to start. Check ~/app.log for clues.'
    exit 1
  fi
done

# Declare success!
cat <<EOF

The Spring Pet Clinic web app installed and started successfully.

Access the application at http://$(curl -s ifconfig.me):8080

Have a nice day!
EOF

exit
