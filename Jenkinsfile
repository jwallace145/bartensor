#!/usr/bin/env groovy

node {

    def installed = fileExists 'bin/activate'

    if (!installed) {
        stage("Install Python Virtual Environment") {
            sh 'virtualenv .'
            }
    }

    stage ("Get Latest Code") {
        checkout scm
    }

    stage ("Install Application Dependencies") {
        sh '''
            source bin/activate
            pip install -r requirements.txt
            deactivate
           '''
    }

    stage ("Collect Static files") {
        sh '''
            source bin/activate
            python manage.py collectstatic
            deactivate
           '''
    }

    stage ("Run Unit/Integration Tests") {
        echo 'testing'
    }
}
