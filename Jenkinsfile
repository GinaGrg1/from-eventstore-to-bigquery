#!groovy
import hudson.AbortException

node {

    TOWER_TEST_ID = 10344

    stage("Checkout") {
        cleanWs()
        checkout scm
    }

    stage('Get tag') {
        def shortHash = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
        sh "echo '${env.BRANCH_NAME.replaceAll(/\//, '.')}.${BUILD_NUMBER}.${shortHash}' > .git/commit-id"
        def commit_id = readFile('.git/commit-id').trim()
        currentBuild.displayName = commit_id
    }

    try {
        def dockerTag = readFile('.git/commit-id').trim()

        stage ("cleanup") {
            sh "docker-compose stop"
            sh "docker-compose down"
            sh "docker-compose rm -vf"
            sh "rm -rf test-results"
        }
        stage ("build") {
            sh "docker-compose build data-river"
        }
        stage ("unit test") {
            sh "docker-compose run data-river entrypoint data-river-run-jenkins"
        }
        stage ("push&deploy") {
            if( env.BRANCH_NAME == "master") {
                sh "docker tag data-river docker.made.com/analytics/data-river:${dockerTag}"
                sh "docker push docker.made.com/analytics/data-river:${dockerTag}"

                sh "docker tag data-river docker.made.com/analytics/data-river:latest"
                sh "docker push docker.made.com/analytics/data-river:latest"

                echo "Deploying ${dockerTag} to test"
                tower(TOWER_TEST_ID, [
                    env: 'test',
                    docker_image_tag: dockerTag,
                ])
            }
        }

    }
    catch(Exception ex) {
        echo "Exception caught: " + ex
        throw new AbortException("I Failed")
    }
    finally {
        stage ("cleanup") {
            sh "docker-compose stop"
            sh "docker-compose down"
            sh "docker-compose rm -avf"
            sh "docker network prune -f"
        }
    }
}
