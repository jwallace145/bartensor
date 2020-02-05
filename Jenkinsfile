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
    // Checkout Code
    stage('Checkout Code') {
      steps {
        sh 'echo "Checkout Code"'
      }
    }

    // Virtual Environment Initialization
    stage('Virtual Environment Initialization') {
      steps {
        sh 'echo "Virtual Environment Initialization"'
      }
    }

    // Static Code Analysis
    stage('Static Code Analysis') {
      steps {
        sh 'echo "Static Code Analysis"'
      }
    }

    // Tests
    stage('Tests') {
      steps {
        sh 'echo "Tests"'
      }
    }

    // Deployment
    stage('Deployment') {
      steps {
        sh 'echo "Deployment"'
      }
    }
  }
}
