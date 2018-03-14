#!/usr/bin/groovy
@Library('github.com/stakater/fabric8-pipeline-library@master')

def utils = new io.fabric8.Utils()
String gitUsername = "stakater-user"
String gitEmail = "stakater@gmail.com"

// TODO: should be fetched dynamically; and one shouldn't need to specify manually
String thisRepo = "git@github.com:stakater/RestfulDistributedLockManager"
String thisRepoBranch = "master"
String thisRepoDir = "RestfulDistributedLockManager"
String dockerImageName = "restful-distributed-lock-manager"

controllerNode(clientsImage: 'stakater/pipeline-tools:1.3.0') {

    container(name: 'clients') {
        String workspaceDir = WORKSPACE
        def git = new io.stakater.vc.Git()

        stage('Checkout') {
            checkout scm
        }

        stage('Download Dependencies') {
            sh """
                pip install -r pip-requirements.txt
                pip install nose
            """
        }

        if (utils.isCI()) {
            stage('CI: Test') {
                sh """
                    make clean install
                    make test
                """
            }
            stage('CI: Publish Dev Image') {
                sh """
                    docker build -t docker.io/stakater/${dockerImageName}:dev .
                    docker push docker.io/stakater/${dockerImageName}:dev
                """
            }
        } else if (utils.isCD()) {
            stage('CD: Build') {
                sh """
                    make clean install
                    make test
                """
            }

            stage('CD: Tag and Push') {
                print "Checkout current Repo for pushing version"

                git.setUserInfo(gitUsername, gitEmail)
                git.addHostsToKnownHosts()
                // We need to checkout again because we can't commit and push changes to the repo that is checkout via scm
                git.checkoutRepo(thisRepo, thisRepoBranch, thisRepoDir)

                git.addHostsToKnownHosts()
                print "Generating New Version"
                sh """
                    cd ${WORKSPACE}/${thisRepoDir}

                    chmod 600 /root/.ssh-git/ssh-key
                    eval `ssh-agent -s`
                    ssh-add /root/.ssh-git/ssh-key

                    VERSION=\$(jx-release-version)
                    echo "VERSION := \${VERSION}" > Makefile
		        """

                def version = new io.stakater.Common().shOutput """
                    cd ${WORKSPACE}/${thisRepoDir}

                    chmod 600 /root/.ssh-git/ssh-key > /dev/null
                    eval `ssh-agent -s` > /dev/null
                    ssh-add /root/.ssh-git/ssh-key > /dev/null

                    jx-release-version
                """

                git.commitChanges(thisRepoDir, "Bump Version")

                print "Pushing Tag ${version} to Git"
                sh """
                    cd ${WORKSPACE}/${thisRepoDir}

                    chmod 600 /root/.ssh-git/ssh-key
                    eval `ssh-agent -s`
                    ssh-add /root/.ssh-git/ssh-key

                    git tag ${version}
                    git push --tags
                """

                print "Pushing Tag ${version} to DockerHub"
                sh """
                    cd ${WORKSPACE}
                    docker build -t docker.io/stakater/${dockerImageName}:${version} .
                    docker tag docker.io/stakater/${dockerImageName}:${version} docker.io/stakater/${dockerImageName}:latest
                    docker push docker.io/stakater/${dockerImageName}:${version}
	                docker push docker.io/stakater/${dockerImageName}:latest
                """
            }
        }

    }
}
