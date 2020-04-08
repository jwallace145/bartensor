#!/usr/bin/env groovy

node {

  stage("Install Python Virtual Environment") {
    sh 'virtualenv env --python=python3'
  }

  stage("Checkout Latest Code") {
    checkout scm
  }

  stage("Install Application Dependencies") {
    sh '''
      source env/bin/activate
      pip install -r requirements.txt
      deactivate
      '''
  }

  stage("Make Migrations") {

  }

  stage("Migrate") {

  }
}
