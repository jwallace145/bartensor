#!/usr/bin/env groovy

node {

    if (!installed) {
        stage("Install Python Virtual Enviroment") {
            sh 'virtualenv --no-site-packages .'
        }
    }

    stage ("Get Latest Code") {
        checkout scm
    }

    stage ("Install Application Dependencies") {
        sh '''
            source bin/activate
            pip install -r <relative path to requirements file>
            deactivate
           '''
    }

    stage ("Collect Static files") {
        sh '''
            source bin/activate
            python <relative path to manage.py> collectstatic --noinput
            deactivate
           '''
    }

    stage ("Run Unit/Integration Tests") {
        def testsError = null
        try {
            echo 'unit testing...'
        }
        catch(err) {
            testsError = err
            currentBuild.result = 'FAILURE'
        }
        finally {
            junit 'reports/junit.xml'

            if (testsError) {
                throw testsError
            }
        }
    }
}
