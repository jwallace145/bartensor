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
      steps {
        if (STATIC_CODE_ANALYSIS) {
          sh '''
          python --version
          pip --version
          virtualenv --version
          '''
        } else {
          sh 'no static code analysis'
        }
      }
    }

    stage('Test') {
      steps {
        if (TEST) {
          sh 'echo "testing..."'
        } else {
          sh 'echo "no tests were performed"'
        }
      }
    }

    stage('Deploy') {
      steps {
        if (DEPLOY) {
          sh 'echo "deploying..."'
        } else {
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
