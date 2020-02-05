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
        sh 'python manage.py jenkins'
      }
    }

    stage('deploy') {
      steps {
        sh 'echo "deploying..."'
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
