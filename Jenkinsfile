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
        sh '''
        python --version
        pip --version
        sudo pip install virtualenv
        virtualenv --version
        '''
      }
    }

    stage('test') {
      steps {
        sh 'echo "run tests"'
      }
    }
  }

  post {
    always {
      sh 'echo "test results"'
    }
  }
}
