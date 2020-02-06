#!/usr/bin/env groovy

pipeline {

  // Agent Initialization
  agent {
    docker {
      image 'python:3.8.0'
    }
  }

  // Parameters
  parameters {
    booleanParam(name: 'RUN_STATIC_CODE_ANALYSIS', defaultValue: true, description: 'Would you like to perform static code analysis?')
    booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Would you like to run unit tests?')
    booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Would you like to deploy?')
  }

  stages {
    // Virtual Environment Initialization
    stage('Virtual Environment Initialization') {
      steps {
        sh 'echo "Virtual Environment Initialization"'
        sh 'pip install virtualenv'
        sh 'virtualenv --version'
      }
    }

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
          if (params.DEPLOY) {
            sh 'echo "Deployment"'
          } else {
            sh 'echo "Skipped Deployment"'
          }
        }
      }
    }
  }
}
