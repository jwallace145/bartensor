#!/usr/bin/env groovy

node {

  def virtual_environment = fileExists 'env/bin/activate'

  if (!virtual_environment) {
    stage("Install Python Virtual Environment") {
      sh 'virtualenv env'
    }
  }
}
