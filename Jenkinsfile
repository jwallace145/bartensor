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
