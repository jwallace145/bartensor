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

      }
    }

    // Virtual Environment Initialization
    stage('Virtual Environment Initialization') {
      steps {

      }
    }

    // Static Code Analysis
    stage('Static Code Analysis') {
      steps {

      }
    }

    // Tests
    stage('Tests') {
      steps {

      }
    }

    // Deployment
    stage('Deployment') {
      steps {

      }
    }
  }
}
