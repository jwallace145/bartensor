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
        sh 'pip freeze'
        sh 'pip install -r requirements.txt'
      }
    }

    stage('test') {
      steps {
        sh 'echo "hello world!"'
      }
    }
  }
}
