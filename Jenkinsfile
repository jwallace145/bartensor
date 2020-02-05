#!groovy
pipeline {
  agent {
    docker {
      image 'python:3.8.0'
    }
  }

  stages {
    stage('build') {
      steps {
        sh """
        python --version
        pip --version
        pip install virtualenv
        virtualenv --version
        """
      }
    }
  }
}
