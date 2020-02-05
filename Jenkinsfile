#!groovy
pipeline {
  agent {
    docker {
      image 'python:3.8.1-buster'
    }
  }

  stages {
    stage('build') {
      steps {
        sh 'sudo -H pip freeze'
        sh 'sudo -H pip install -r requirements.txt'
      }
    }

    stage('test') {
      steps {
        sh 'echo "hello world!"'
      }
    }

    stage('deploy') {
      steps {
        sh 'echo "deploying"'
      }
    }
  }
}
