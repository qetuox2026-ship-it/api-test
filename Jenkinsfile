pipeline {
    agent any

    environment {
        PYTHON = '/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13'
        VENV = "${WORKSPACE}/.jenkins-venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '"$PYTHON" -m venv "$VENV"'
                sh '"$VENV/bin/python" -m pip install -r requirements.txt'
            }
        }

        stage('Smoke Test') {
            steps {
                sh '"$VENV/bin/python" -m pytest -m smoke'
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/junit.xml',
                  allowEmptyResults: true

            archiveArtifacts artifacts: 'reports/report.html, logs/automation.log',
                             allowEmptyArchive: true
        }
    }
}