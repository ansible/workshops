pipeline {

    agent { label 'jenkins-jnlp-agent' }

    stages {

        stage('Build Information') {
            steps {
                script {
                    TOWER_VERSION = '3.6.2'
                    DOTLESS_TOWER_VERSION = TOWER_VERSION.replace('.', '').trim()
                }
                echo """Tower Version under test: ${TOWER_VERSION}
Workshop branch under test: ${env.BRANCH_NAME} | ${env.CHANGE_NAME}
Build Tag: ${env.BUILD_TAG}"""
            }
        }

        stage('Prep Environment') {
            steps {
                withCredentials([file(credentialsId: 'workshops_tower_license', variable: 'TOWER_LICENSE')]) {
                    sh 'cp ${TOWER_LICENSE} provisioner/tower_license.json'
                }
                sh 'pip install netaddr pywinrm'
                sh 'yum -y install sshpass'
                sh 'ansible --version | tee ansible_version.log'
                archiveArtifacts artifacts: 'ansible_version.log'
                script {
                    ADMIN_PASSWORD = sh(
                        script: "cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1",
                        returnStdout: true
                    ).trim()

                    if (env.CHANGE_ID) {
                        ANSIBLE_WORKSHOPS_REFSPEC = "+refs/pull/${env.CHANGE_ID}/head:refs/remotes/origin/${env.BRANCH_NAME}"
                    } else {
                        ANSIBLE_WORKSHOPS_REFSPEC = "+refs/heads/${env.BRANCH_NAME}:refs/remotes/origin/${env.BRANCH_NAME}"
                    }

                    if (TOWER_VERSION == 'devel') {
                        tower_installer_url = "${AWX_NIGHTLY_REPO_URL}/${TOWER_VERSION}/setup/ansible-tower-setup-latest.tar.gz"
                        gpgcheck = 0
                        aw_repo_url = "${AWX_NIGHTLY_REPO_URL}/${TOWER_VERSION}"
                    } else {
                        tower_installer_url = "https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-${TOWER_VERSION}-1.tar.gz"
                        gpgcheck = 1
                        aw_repo_url = "https://releases.ansible.com/ansible-tower"
                    }
                }

                sh """tee provisioner/tests/ci-common.yml << EOF
tower_installer_url: ${tower_installer_url}
gpgcheck: ${gpgcheck}
aw_repo_url: ${aw_repo_url}
admin_password: ${ADMIN_PASSWORD}
ansible_workshops_refspec: ${ANSIBLE_WORKSHOPS_REFSPEC}
EOF
"""
                sh """tee provisioner/tests/ci-rhel.yml << EOF
workshop_type: rhel
ec2_name_prefix: tower-qe-rhel-tower-${DOTLESS_TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID}
EOF
"""

                sh """tee provisioner/tests/ci-networking.yml << EOF
workshop_type: networking
ec2_region: eu-central-1
ec2_name_prefix: tower-qe-networking-tower-${DOTLESS_TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID}
EOF
"""

                sh """tee provisioner/tests/ci-f5.yml << EOF
workshop_type: f5
ec2_region: ap-northeast-1
ec2_name_prefix: tower-qe-f5-tower-${DOTLESS_TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID}
EOF
"""

                sh """tee provisioner/tests/ci-security.yml << EOF
workshop_type: security
security_console: qradar
windows_password: 'RedHatTesting19!'
ec2_name_prefix: tower-qe-security-workshop-${DOTLESS_TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID}
EOF
"""
            }
        }

        stage('Workshop Type') {
            parallel {
                stage('RHEL') {
                    steps {
                        script {
                            stage('RHEL-deploy') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/provision_lab.yml \
                                               -e @provisioner/tests/vars.yml \
                                               -e @provisioner/tests/ci-common.yml \
                                               -e @provisioner/tests/ci-rhel.yml"""
                                    }
                                }
                            }
                        }
                        script {
                            stage('RHEL-teardown') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-rhel.yml"""
                                    }
                                }
                            }
                        }
                    }
                }

                stage('Networking') {
                    steps {
                        script {
                            stage('networking-deploy') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/provision_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-networking.yml"""
                                    }
                                }
                            }
                        }
                        script {
                            stage('networking-teardown') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-networking.yml"""
                                    }
                                }
                            }
                        }
                    }
                }

                stage('F5') {
                    steps {
                        script {
                            stage('F5-deploy') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/provision_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-f5.yml"""
                                    }
                                }
                            }
                        }
                        script {
                            stage('F5-exercises') {
                                sh "cat provisioner/tower-qe-f5-tower-${DOTLESS_TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID}/student1-instances.txt | grep -A 1 control | tail -n 1 | cut -d' ' -f 2 | cut -d'=' -f2 | tee control_host"
                                CONTROL_NODE_HOST = readFile('control_host').trim()
                                RUN_ALL_PLAYBOOKS = 'find . -name "*.yml" -o -name "*.yaml" | grep -v "2.0" | sort | xargs -I {} bash -c "echo {} && ANSIBLE_FORCE_COLOR=true ansible-playbook {}"'
                                sh "sshpass -p '${ADMIN_PASSWORD}' ssh -o StrictHostKeyChecking=no student1@${CONTROL_NODE_HOST} 'cd networking-workshop && ${RUN_ALL_PLAYBOOKS}'"
                            }
                        }
                        script {
                            stage('F5-teardown') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-f5.yml"""
                                    }
                                }
                            }
                        }
                    }
                }
                stage('security') {
                    steps {
                        script {
                            stage('security-deploy') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/provision_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-security.yml"""
                                    }
                                }
                            }
                        }
                        script {
                            stage('security-teardown') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-security.yml"""
                                    }
                                }
                            }
                        }
                    }
                }

            }
        }
    }

    post {
        cleanup {
            script {
                stage('Cleaning up') {
                    withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                     string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                        withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                 "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                 "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                 "ANSIBLE_FORCE_COLOR=true"]) {
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-rhel.yml"
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-networking.yml"
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-f5.yml"
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-security.yml"
                        }
                    }
                }
            }
        }
    }
}
