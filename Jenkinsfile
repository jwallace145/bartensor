#!/usr/bin/env groovy

node {

  stage("Checkout Latest Code") {
    checkout scm
  }

  stage("Install Application Dependencies") {
    sh 'pip3 install -r requirements.txt'
  }

  stage("Make Migrations") {
    sh 'python3 manage.py makemigrations'
  }

  stage("Migrate") {
    sh 'python3 manage.py migrate'
  }
}
