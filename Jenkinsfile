pipeline {
    agent any
    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['regression', 'smoke', 'all'],
            description: '请选择测试范围'
        )
    }
    triggers {
        cron('H 2 * * *')
    }

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

        stage('Run Tests') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'restful-booker-credentials',
                        usernameVariable: 'BOOKER_USERNAME',
                        passwordVariable: 'BOOKER_PASSWORD'
                    )
                ]) {
                    script {
                        if (params.TEST_SUITE == 'all') {
                            sh '"$VENV/bin/python" -m pytest'
                        } else {
                            sh '"$VENV/bin/python" -m pytest -m "' +
                            params.TEST_SUITE + '"'
                        }
                    }
                }
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

