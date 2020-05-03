pipeline {

    agent { label 'jenkins-jnlp-agent' }

    options {
        timestamps()
        timeout(time: 3, unit: 'HOURS')
        buildDiscarder(logRotator(daysToKeepStr: '10'))
    }

    parameters {
        choice(
            name: 'TOWER_VERSION',
            description: 'Tower version to deploy',
            choices: ['devel', '3.6.4']
        )
        choice(
            name: 'ANSIBLE_VERSION',
            description: 'Ansible version to use to deploy the lab',
            choices: ['devel', 'stable-2.9']
        )
         string(
            name: 'WORKSHOP_FORK',
            description: 'Workshop fork to deploy from',
            defaultValue: 'ansible'
        )
        string(
            name: 'WORKSHOP_BRANCH',
            description: 'Workshop branch to deploy',
            defaultValue: 'devel'
        )
    }

    stages {

        stage('Build Information') {
            steps {
                echo """Tower Version under test: ${params.TOWER_VERSION}
Ansible version under test: ${params.ANSIBLE_VERSION}
Workshop branch under test: ${params.WORKSHOP_BRANCH}
${AWX_NIGHTLY_REPO_URL}"""
            }
        }

        stage('Retrieve ansible/workshops') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.WORKSHOP_BRANCH}" ]],
                    userRemoteConfigs: [
                        [
                            url: "https://github.com/${params.WORKSHOP_FORK}/workshops.git"
                        ]
                    ]
                ])
            }
        }

        stage('Prep Environment') {
            steps {
                withCredentials([file(credentialsId: 'workshops_tower_license', variable: 'TOWER_LICENSE')]) {
                    sh 'cp ${TOWER_LICENSE} provisioner/tower_license.json'
                }
                sh 'pip install netaddr pywinrm requests requests-credssp boto'
                sh 'yum -y install sshpass'
                sh "pip install git+https://github.com/ansible/ansible.git@${params.ANSIBLE_VERSION}"
                sh 'ansible --version | tee ansible_version.log'
                archiveArtifacts artifacts: 'ansible_version.log'
                script {
                    ADMIN_PASSWORD = sh(
                        script: "cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1",
                        returnStdout: true
                    ).trim()
                    DOTLESS_TOWER_VERSION = TOWER_VERSION.replace('.', '').trim()
                    SHORTENED_ANSIBLE_VERSION = ANSIBLE_VERSION.replace('stable-', '').replace('.', '').trim()
                    ANSIBLE_WORKSHOPS_URL = "https://github.com/${params.WORKSHOP_FORK}/workshops.git"

                    if (params.TOWER_VERSION == 'devel') {
                        tower_installer_url = "${AWX_NIGHTLY_REPO_URL}/${params.TOWER_VERSION}/setup/ansible-tower-setup-latest.tar.gz"
                        gpgcheck = 0
                        aw_repo_url = "${AWX_NIGHTLY_REPO_URL}/${params.TOWER_VERSION}"
                    } else {
                        tower_installer_url = "https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-${params.TOWER_VERSION}-1.tar.gz"
                        gpgcheck = 1
                        aw_repo_url = "https://releases.ansible.com/ansible-tower"
                    }
                }

                sh """tee provisioner/tests/ci-common.yml << EOF
tower_installer_url: ${tower_installer_url}
gpgcheck: ${gpgcheck}
aw_repo_url: ${aw_repo_url}
admin_password: ${ADMIN_PASSWORD}
ansible_workshops_url: ${ANSIBLE_WORKSHOPS_URL}
ansible_workshops_version: ${params.WORKSHOP_BRANCH}
ec2_name_prefix: tqe-{{ workshop_type }}-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}
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
                                        sh '''ansible-playbook provisioner/provision_lab.yml \
                                               -e @provisioner/tests/vars.yml \
                                               -e @provisioner/tests/ci-common.yml \
                                               -e @provisioner/tests/ci-rhel.yml 2>&1 | tee rhel.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                            }
                        }
                        script {
                            stage('RHEL-verify') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/tests/rhel_verify.yml \
                                                -i provisioner/tqe-rhel-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}/instructor_inventory.txt \
                                                --private-key=provisioner/tqe-rhel-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}/tqe-rhel-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}-private.pem \
                                                -e tower_password=${ADMIN_PASSWORD} -e workshop_name=tqe-rhel-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}"""
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
                                        sh '''ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-rhel.yml 2>&1 | tee -a rhel.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                                archiveArtifacts artifacts: 'rhel.log'
                                RHEL_DEPRECATED_WARNINGS = sh(
                                    script: 'grep -c \'DEPRECATION WARNING\' rhel.log || true',
                                    returnStdout: true
                                ).trim()
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
                                        sh '''ansible-playbook provisioner/provision_lab.yml \
                                               -e @provisioner/tests/vars.yml \
                                               -e @provisioner/tests/ci-common.yml \
                                               -e @provisioner/tests/ci-networking.yml 2>&1 | tee networking.log && exit ${PIPESTATUS[0]}'''
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
                                        sh '''ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-networking.yml 2>&1 | tee -a networking.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                                archiveArtifacts artifacts: 'networking.log'
                                NETWORKING_DEPRECATED_WARNINGS = sh(
                                    script: 'grep -c \'DEPRECATION WARNING\' networking.log || true',
                                    returnStdout: true
                                ).trim()
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
                                        sh '''ansible-playbook provisioner/provision_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-f5.yml 2>&1 | tee f5.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                            }
                        }
                        script {
                            stage('F5-exercises') {
                                sh "cat provisioner/tqe-f5-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}/student1-instances.txt | grep -A 1 control | tail -n 1 | cut -d' ' -f 2 | cut -d'=' -f2 | tee control_host"
                                CONTROL_NODE_HOST = readFile('control_host').trim()
                                RUN_ALL_PLAYBOOKS = 'find . -name "*.yml" -o -name "*.yaml" | grep -v "2.0" | sort | xargs -I {} bash -c "echo {} && ANSIBLE_FORCE_COLOR=true ansible-playbook {}"'
                                sh "sshpass -p '${ADMIN_PASSWORD}' ssh -o StrictHostKeyChecking=no student1@${CONTROL_NODE_HOST} 'cd f5-workshop && ${RUN_ALL_PLAYBOOKS}'"
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
                                        sh '''ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-f5.yml 2>&1 | tee -a f5.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                                archiveArtifacts artifacts: 'f5.log'
                                F5_DEPRECATED_WARNINGS = sh(
                                    script: 'grep -c \'DEPRECATION WARNING\' f5.log || true',
                                    returnStdout: true
                                ).trim()
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
                                        sh '''ansible-playbook provisioner/provision_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-security.yml 2>&1 | tee security.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                            }
                        }
                        script {
                            stage('security-verify') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/tests/security_verify.yml \
                                                -i provisioner/tqe-security-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}/instructor_inventory.txt \
                                                --private-key=provisioner/tqe-security-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}/tqe-security-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}-private.pem"""
                                    }
                                }
                            }
                        }
                        script {
                            stage('security-exercises') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh """ansible-playbook provisioner/tests/security_exercise_21.yml \
                                                -i provisioner/tqe-security-tower${DOTLESS_TOWER_VERSION}-${env.BUILD_ID}-${SHORTENED_ANSIBLE_VERSION}/student1-instances.txt"""
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
                                        sh '''ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-security.yml 2>&1 | tee -a security.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                                archiveArtifacts artifacts: 'security.log'
                                SECURITY_DEPRECATED_WARNINGS = sh(
                                    script: 'grep -c \'DEPRECATION WARNING\' security.log || true',
                                    returnStdout: true
                                ).trim()
                            }
                        }
                    }
                }

                stage('windows') {
                    steps {
                        script {
                            stage('windows-deploy') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh '''ansible-playbook provisioner/provision_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-windows.yml 2>&1 | tee windows.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                            }
                        }
                        script {
                            stage('windows-teardown') {
                                withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                                 string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                                    withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                             "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                             "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                             "ANSIBLE_FORCE_COLOR=true"]) {
                                        sh '''ansible-playbook provisioner/teardown_lab.yml \
                                                -e @provisioner/tests/vars.yml \
                                                -e @provisioner/tests/ci-common.yml \
                                                -e @provisioner/tests/ci-windows.yml 2>&1 | tee -a windows.log && exit ${PIPESTATUS[0]}'''
                                    }
                                }
                                archiveArtifacts artifacts: 'windows.log'
                                SECURITY_DEPRECATED_WARNINGS = sh(
                                    script: 'grep -c \'DEPRECATION WARNING\' windows.log || true',
                                    returnStdout: true
                                ).trim()
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
                stage('Cleaning up in case of failure') {
                    withCredentials([string(credentialsId: 'workshops_aws_access_key', variable: 'AWS_ACCESS_KEY'),
                                     string(credentialsId: 'workshops_aws_secret_key', variable: 'AWS_SECRET_KEY')]) {
                        withEnv(["AWS_SECRET_KEY=${AWS_SECRET_KEY}",
                                 "AWS_ACCESS_KEY=${AWS_ACCESS_KEY}",
                                 "ANSIBLE_CONFIG=provisioner/ansible.cfg",
                                 "ANSIBLE_FORCE_COLOR=true"]) {
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-common.yml -e @provisioner/tests/ci-rhel.yml"
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-common.yml -e @provisioner/tests/ci-networking.yml"
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-common.yml -e @provisioner/tests/ci-f5.yml"
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-common.yml -e @provisioner/tests/ci-security.yml"
                            sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e @provisioner/tests/ci-common.yml -e @provisioner/tests/ci-windows.yml"
                        }
                    }
                }
            }
        }
        failure {
            slackSend(
                botUser: false,
                color: "#922B21",
                teamDomain: "ansible",
                channel: "#workshops-events",
                message: "*Tower version: ${params.TOWER_VERSION}* | Ansible version: `${params.ANSIBLE_VERSION}` | Workshop branch: ${params.WORKSHOP_BRANCH} | Integration State: FAIL | <${env.RUN_DISPLAY_URL}|Link>"
            )
        }
        success {
            slackSend(
                botUser: false,
                color: "good",
                teamDomain: "ansible",
                channel: "#workshops-events",
                message: """
*Tower version: ${params.TOWER_VERSION}* | Ansible version: `${params.ANSIBLE_VERSION}` | Workshop branch: ${params.WORKSHOP_BRANCH} | Integration State: OK | <${env.RUN_DISPLAY_URL}|Link> \
Deprecation Warnings: *${RHEL_DEPRECATED_WARNINGS}* in RHEL lab - *${NETWORKING_DEPRECATED_WARNINGS}* in Networking lab - *${F5_DEPRECATED_WARNINGS}* in F5 lab
"""
            )
        }
    }
}
