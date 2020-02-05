#!groovy
pipeline {
  agent {
    docker {
      image 'python:3.8.1-buster'
    }
  }

  stages {
    def installed = fileExists 'bin/activate'

    if (!installed) {
      stage('install python virtual environment') {
        steps {
          sh 'virtualenv --no-site-packages'
        }
      }
    }

    stage('build') {
      steps {
        sh 'sudo -H pip freeze'
        sh 'sudo -H pip install -r requirements.txt'
      }
    }

    stage('test') {
      steps {
        sh 'echo "tesing..."'
      }
    }

    stage('deploy') {
      steps {
        sh 'echo "deploying..."'
      }
    }
  }
}
