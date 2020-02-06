#!/usr/bin/env groovy

pipeline {

  // Agent Initialization
  agent {
    dockerfile true
  }

  // Parameters
  parameters {
    booleanParam(name: 'RUN_STATIC_CODE_ANALYSIS', defaultValue: true, description: 'Would you like to perform static code analysis?')
    booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Would you like to run unit tests?')
    booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Would you like to deploy?')
  }

  stages {
    // Static Code Analysis
    stage('Static Code Analysis') {
      steps {
        script {
          if (params.RUN_STATIC_CODE_ANALYSIS) {
            sh 'echo "Static Code Analysis"'
            sh 'python manage.py jenkins'
            sh 'su pylint users --output-format=json > ./reports/pylint.report'

            def flake8 = scanForIssues tool: flake8(pattern: '**/reports/flake8.report')
            publishIssues issues:[flake8]

            def pep8 = scanForIssues tool: pep8(pattern: '**/reports/pep8.report')
            publishIssues issues:[pep8]

            def pylint = scanForIssues tool: pyLint(pattern: '**/reports/pylint.report')
            publishIssues issues:[pylint]
          } else {
            sh 'echo "Skipped Static Code Analysis"'
          }
        }
      }
    }

    // Tests
    stage('Tests') {
      steps {
        script {
          if (params.RUN_TESTS) {
            sh 'echo "Tests"'
            sh 'python manage.py test'
          } else {
            sh 'echo "Skipped Tests"'
          }
        }
      }
    }

    // Deployment
    stage('Deployment') {
      steps {
        script {
          if (params.DEPLOY) {
            sh 'echo "Deployment"'
          } else {
            sh 'echo "Skipped Deployment"'
          }
        }
      }
    }
  }

  post {
    always {
      junit '**/reports/junit.xml'
    }
  }
}
