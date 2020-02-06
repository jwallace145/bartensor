#!/usr/bin/env groovy

pipeline {
  // Agent Initialization
  agent {
    dockerfile true
  }

  // Parameters
  parameters {
    booleanParam(name: 'RUN_STATIC_CODE_ANALYSIS', defaultValue: true, description: 'Would you like to perform static code analysis?')
    booleanParam(name: 'RUN_SONARQUBE_ANALYSIS', defaultVale: false, description: 'Would you like to perform a SonarQube analysis?')
    booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Would you like to run unit tests?')
    choice(name: 'DEPLOY', choices: ['NO', 'DEV', 'QA', 'PROD'], description: 'Which environment would you like to deploy to?')
  }

  stages {
    // Static Code Analysis
    stage('Static Code Analysis') {
      steps {
        script {
          if (params.RUN_STATIC_CODE_ANALYSIS) {
            sh 'echo "Static Code Analysis"'

            // creates flake8 and pep8 reports
            sh 'python manage.py jenkins'

            // creates pylint reports
            withEnv(['PYLINTHOME=.']) {
              sh 'pylint --output-format=parseable --exit-zero --rcfile=pylint.cfg --reports=no users/ > ./reports/pylint.log'
              sh 'pylint --output-format=parseable --exit-zero --rcfile=pylint.cfg --reports=no gnt/ >> ./reports/pylint.log'
            }

            // scans and publishes flake8 report
            def flake8 = scanForIssues tool: flake8(pattern: '**/reports/flake8.report')
            publishIssues issues:[flake8]

            // scans and publishes pep8 report
            def pep8 = scanForIssues tool: pep8(pattern: '**/reports/pep8.report')
            publishIssues issues:[pep8]

            // scans and publishes pylint report
            def pylint = scanForIssues tool: pyLint(pattern: '**/reports/pylint.log')
            publishIssues issues:[pylint]
          } else {
            sh 'echo "Skipped Static Code Analysis"'
          }
        }
      }
    }

    // SonarQube Analysis
    stage('SonarQube Analysis') {
      steps {
        script {
          if (params.RUN_SONARQUBE_ANALYSIS) {
            withSonarQubeEnv('sonarqube') {
            }
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

            // creates junit test report
            sh 'python manage.py test'

            // publishes junit test report
            junit '**/reports/junit.xml'
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
          // does not deploy
          if (params.DEPLOY == 'NO') {
            sh 'echo "skipping deployment"'

          // deploy to dev environment
          } else if (params.DEPLOY == 'DEV'){
            sh 'echo "deploying to dev..."'

          // deploy to qa environment
          } else if (params.DEPLOY == 'QA') {
            sh 'echo "deploying to qa..."'

          // deploy to prod environment
          } else if (params.DEPLOY == 'PROD') {
            sh 'echo "deploying to prod..."'

          }
        }
      }
    }
  }
}
