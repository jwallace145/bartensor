#!groovy
pipeline {
  agent {
    dockerfile true
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
