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

    if (STATIC_CODE_ANALYSIS) {
      stage('Static Code Analysis') {
        steps {
          sh '''
          python --version
          pip --version
          virtualenv --version
          '''
        }
      }
    }

    if (TEST) {
      stage('Test') {
        steps {
          sh 'python manage.py jenkins'
        }
      }
    }

    if (DEPLOY) {
      stage('Deploy') {
        steps {
          sh 'echo "deploying..."'
        }
      }
    }
  }
  
  post {
    always {
      sh 'echo "building reports"'
      junit 'build/reports/**/*.xml'
    }
  }
}
