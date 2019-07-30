def jobs = [:]
def ansibleVersions = ['devel', 'stable-2.8']
def towerVersions = ['devel', '3.5.1']


ansibleVersions.each { ansibleVersion ->
    towerVersions.each { towerVersion ->
        jobs["Tower ${towerVersion} - Ansible ${ansibleVersion}"] = {

            node('jenkins-jnlp-agent') {
                build(
                    job: 'testing-new-pipeline',
                    parameters: [
                        string(name: 'TOWER_VERSION', value: towerVersion),
                        string(name: 'ANSIBLE_VERSION', value: ansibleVersion),
                        string(name: 'WORKSHOP_BRANCH', value: env.BRANCH_NAME),
                        string(name: 'CHANGE_ID', value: env.CHANGE_ID),
                    ]
                )
            }

        }
    }
}

jobs
