#!groovy
pipeline {
  agent {
    docker {
      image 'python:3.8.1-buster'
    }
  }

  stages {
    stage('install python virtual environment') {
      def installed = fileExists 'bin/activate'

      if (!installed) {
        steps {
          sh 'virtualenv --no-site-packages'
        }
      } else {
        steps {
          sh 'virtual environment already installed'
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
