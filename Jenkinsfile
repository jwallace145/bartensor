#!/usr/bin/env groovy

node {

  stage("Checkout Latest Code") {
    checkout scm
  }

  stage("Install Application Dependencies") {
    sh 'sudo pip3 install -r requirements.txt'
  }
}
