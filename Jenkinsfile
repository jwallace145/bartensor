#!groovy
pipeline {
  agent { docker { image 'python:3.8.0'}}

  stages {
    stage('build') {
      steps {
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
