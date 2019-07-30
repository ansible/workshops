pipeline {

    agent { label 'jenkins-jnlp-agent' }

    stages {
        stage('Scenario') {
            steps {
                script {
                    jobs = load('provisioner/tests/build-scenarios.groovy')
                    parallel jobs
                }
            }
        }
    }
}
