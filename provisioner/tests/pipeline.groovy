pipeline {

    agent { label 'jenkins-jnlp-agent' }

    parameters {
        choice(
            name: 'TOWER_VERSION',
            description: 'Tower version to deploy',
            choices: ['devel', '3.5.1']
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
                            credentialsId: 'd2d4d16b-dc9a-461b-bceb-601f9515c98a',
                            url: "git@github.com:${params.WORKSHOP_FORK}/workshops.git"
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
                sh 'pip install netaddr'
                sh 'yum -y install sshpass'
                script {
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
                                        sh "ansible-playbook provisioner/provision_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=rhel -e ec2_name_prefix=tower-qe-rhel-tower-${params.TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID} -e tower_installer_url=${tower_installer_url} -e gpgcheck=${gpgcheck} -e aw_repo_url=${aw_repo_url} -e ansible_workshops_url=${ANSIBLE_WORKSHOPS_URL} -e ansible_workshops_version=${params.WORKSHOP_BRANCH} 2>&1 | tee rhel.log"
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
                                        sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=rhel -e ec2_name_prefix=tower-qe-rhel-tower-${params.TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID} 2>&1 | tee -a rhel.log"
                                    }
                                }
                                archiveArtifacts artifacts: 'rhel.log'
                                RHEL_DEPRECATED_WARNINGS = sh(
                                    script: 'grep -c \'DEPRECATION WARNING\' rhel.log',
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
                                        sh "ansible-playbook provisioner/provision_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=networking -e ec2_name_prefix=tower-qe-networking-tower-${params.TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID} -e tower_installer_url=${tower_installer_url} -e gpgcheck=${gpgcheck} -e aw_repo_url=${aw_repo_url} -e ansible_workshops_url=${ANSIBLE_WORKSHOPS_URL} -e ansible_workshops_version=${params.WORKSHOP_BRANCH} 2>&1 | tee networking.log"
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
                                        sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=networking -e ec2_name_prefix=tower-qe-networking-tower-${params.TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID} 2>&1 | tee -a networking.log"
                                    }
                                }
                                archiveArtifacts artifacts: 'networking.log'
                                NETWORKING_DEPRECATED_WARNINGS = sh(
                                    script: 'grep -c \'DEPRECATION WARNING\' networking.log',
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
                                        sh "ansible-playbook provisioner/provision_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=f5 -e ec2_name_prefix=tower-qe-f5-tower-${params.TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID} -e tower_installer_url=${tower_installer_url} -e gpgcheck=${gpgcheck} -e aw_repo_url=${aw_repo_url} -e ansible_workshops_url=${ANSIBLE_WORKSHOPS_URL} -e ansible_workshops_version=${params.WORKSHOP_BRANCH} 2>&1 | tee f5.log"
                                    }
                                }
                            }
                        }
                        script {
                            stage('F5-exercises') {
                                sh "cat provisioner/tower-qe-f5-tower-${TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID}/student1-instances.txt | grep -A 1 control | tail -n 1 | cut -d' ' -f 2 | cut -d'=' -f2 | tee control_host"
                                CONTROL_NODE_HOST = readFile('control_host').trim()
                                RUN_ALL_PLAYBOOKS = 'find . -name "*.yml" -o -name "*.yaml" | grep -v "2.0" | sort | xargs -I {} bash -c "echo {} && ansible-playbook {}"'
                                sh "sshpass -p 'ansible' ssh -o StrictHostKeyChecking=no student1@${CONTROL_NODE_HOST} 'cd networking-workshop && ${RUN_ALL_PLAYBOOKS}'"
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
                                        sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=f5 -e ec2_name_prefix=tower-qe-f5-tower-${params.TOWER_VERSION}-${env.BRANCH_NAME}-${env.BUILD_ID} 2>&1 | tee -a f5.log"
                                    }
                                }
                                archiveArtifacts artifacts: 'f5.log'
                                F5_DEPRECATED_WARNINGS = sh(
                                    script: 'grep -c \'DEPRECATION WARNING\' f5.log',
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
        failure {
            slackSend(
                botUser: false,
                color: "#922B21",
                teamDomain: "ansible",
                channel: "#workshops-events",
                message: "*Tower version: ${params.TOWER_VERSION}* | Workshop branch: ${params.WORKSHOP_BRANCH} | Integration State: FAIL | <${env.RUN_DISPLAY_URL}|Link>"
            )
        }
        success {
            slackSend(
                botUser: false,
                color: "good",
                teamDomain: "ansible",
                channel: "#workshops-events",
                message: """
*Tower version: ${params.TOWER_VERSION}* | Workshop branch: ${params.WORKSHOP_BRANCH} | Integration State: OK | <${env.RUN_DISPLAY_URL}|Link> \
Deprecation Warnings: *${RHEL_DEPRECATED_WARNINGS}* in RHEL lab - *${NETWORKING_DEPRECATED_WARNINGS}* in Networking lab - *${F5_DEPRECATED_WARNINGS}* in F5 lab
"""
            )
        }
    }
}
