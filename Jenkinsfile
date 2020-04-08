#!/usr/bin/env groovy

pipeline {

  agent {
    dockerfile true
  }

  environment {
    BARTENSOR_EMAIL_USERNAME = 'bartensor@gmail.com'
    BARTENSOR_EMAIL_PASSWORD = 'iupeqdduwlekqjrj'
    WATSON_DISCOVERY_API_KEY = 'Q48Xgoo6dGAAOSNjdUdho8uwprTEbwgXOBUspsEaTDO2'
    WATSON_SPEECH_TO_TEXT_API_KEY = 'GUyb9Y0-25JUO7_fZtyLvlDipUAMzROb2vxadUiWJEMX'
  }

  stages {
    stage('Checkout Latest Code') {
      steps {
        checkout scm
      }
    }

    stage('Create Python Virtual Environment') {
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }

    stage('Install Python Application Dependencies') {
      steps {
        sh 'sudo source env/bin/activate'
      }
    }
  }

}
