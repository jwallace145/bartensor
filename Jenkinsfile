#!/usr/bin/env groovy

pipeline {
  // Agent Initialization
  agent {
    dockerfile true
  }

  // Parameters
  parameters {
    booleanParam(name: 'RUN_STATIC_CODE_ANALYSIS', defaultValue: true, description: 'Would you like to perform static code analysis?')
    booleanParam(name: 'RUN_SONARQUBE_ANALYSIS', defaultValue: false, description: 'Would you like to perform a SonarQube analysis?')
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
            sh 'echo SonarQube Analysis'
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
