#!groovy
pipeline {
  agent {
    dockerfile true
  }

  parameters {
    booleanParam(name: 'STATIC_CODE_ANALYSIS', defaultValue: true, description: 'toggle static code analysis')
    booleanParam(name: 'TEST', defaultValue: true, description: 'toggle tests')
    booleanParam(name: 'DEPLOY', defaultValue: false, description: 'toggle deployment')
  }

  stages {
    stage('Checkout Code') {
      steps {

      }
    }

    stage('Static Code Analysis') {
        if (STATIC_CODE_ANALYSIS) {
          steps {
            sh '''
            python --version
            pip --version
            virtualenv --version
            '''
          }
        } else {
          steps {
            sh 'no static code analysis'
          }
        }
    }

    stage('Test') {
        if (TEST) {
          steps {
            sh 'echo "testing..."'
          }
        } else {
          steps {
            sh 'echo "no tests were performed"'
          }
        }
    }

    stage('Deploy') {
        if (DEPLOY) {
          steps {
            sh 'echo "deploying..."'
          }
        } else {
          steps {
            sh 'echo "no deployment"'
          }
        }
    }
  }

  post {
    always {
      sh 'echo "building reports"'
    }
  }
}
