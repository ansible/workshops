pipeline {

    agent { label 'jenkins-jnlp-agent' }

    parameters {
        choice(
            name: 'TOWER_VERSION',
            description: 'Tower version to deploy',
            choices: ['devel', '3.5.0', '3.4.3']
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
                            url: 'git@github.com:Spredzy/workshops.git'
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
                script {
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
                                        sh "ansible-playbook provisioner/provision_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=rhel -e ec2_name_prefix=tower-qe-rhel-tower-${params.TOWER_VERSION} -e tower_installer_url=${tower_installer_url} -e gpgcheck=${gpgcheck} -e aw_repo_url=${aw_repo_url}"
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
                                        sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=rhel -e ec2_name_prefix=tower-qe-rhel-tower-${params.TOWER_VERSION}"
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
                                        sh "ansible-playbook provisioner/provision_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=networking -e ec2_name_prefix=tower-qe-networking-tower-${params.TOWER_VERSION} -e tower_installer_url=${tower_installer_url} -e gpgcheck=${gpgcheck} -e aw_repo_url=${aw_repo_url}"
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
                                        sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=networking -e ec2_name_prefix=tower-qe-networking-tower-${params.TOWER_VERSION}"
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
                                        sh "ansible-playbook provisioner/provision_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=f5 -e ec2_name_prefix=tower-qe-f5-tower-${params.TOWER_VERSION} -e tower_installer_url=${tower_installer_url} -e gpgcheck=${gpgcheck} -e aw_repo_url=${aw_repo_url}"
                                    }
                                }
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
                                        sh "ansible-playbook provisioner/teardown_lab.yml -e @provisioner/tests/vars.yml -e workshop_type=f5 -e ec2_name_prefix=tower-qe-f5-tower-${params.TOWER_VERSION}"
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
        failure {
            slackSend(
                botUser: false,
                color: "#922B21",
                teamDomain: "ansible",
                channel: "#workshops-events",
                message: "*Tower version: ${params.TOWER_VERSION}* | Workshop branch: ${params.WORKSHOP_BRANCH} | Integration State: FAIL | <${env.RUN_DISPLAY_URL}|Link>"
            )
        }
        fixed {
            slackSend(
                botUser: false,
                color: "good",
                teamDomain: "ansible",
                channel: "#workshops-events",
                message: "*Tower version: ${params.TOWER_VERSION}* | Workshop branch: ${params.WORKSHOP_BRANCH} | Integration State: Back to OK | <${env.RUN_DISPLAY_URL}|Link>"
            )
        }
    }
}
