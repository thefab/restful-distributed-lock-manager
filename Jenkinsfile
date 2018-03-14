#!/usr/bin/groovy
@Library('github.com/stakater/fabric8-pipeline-library@master')

def utils = new io.fabric8.Utils()
String gitUsername = "stakater-user"
String gitEmail = "stakater@gmail.com"

String thisRepo = "git@github.com:stakater/RestfulDistributedLockManager"
String thisRepoBranch = "master"
String thisRepoDir = "RestfulDistributedLockManager"

controllerNode(clientsImage: 'stakater/pipeline-tools:1.2.0') {

    container(name: 'clients') {
        String workspaceDir = WORKSPACE
        def git = new io.stakater.vc.Git()

        stage('Checkout') {
            checkout scm
        }

        stage('Download Dependencies') {
            sh """
                pip install -r pip-requirements.txt
            """
        }

        if (utils.isCI()) {
            stage('CI: Test') {
                sh """
                    make test
                """
            }
            stage('CI: Publish Dev Image') {
                sh """
                    docker build -t docker.io/stakater/RestfulDistributedLockManager:dev .
                    docker push docker.io/stakater/RestfulDistributedLockManager:dev
                """
            }
        }
    }
}
