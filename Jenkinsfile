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
            // 每天凌晨 2 点执行回归测试
            cron('H 2 * * *')

            // 每 5 分钟检查一次 GitHub 是否有新提交
            pollSCM('H/5 * * * *')
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

        stage('Select Test Suite') {
            steps {
                script {
                    env.ACTIVE_SUITE = params.TEST_SUITE

                    if (currentBuild.getBuildCauses(
                        'hudson.triggers.TimerTrigger$TimerTriggerCause'
                    )) {
                        env.ACTIVE_SUITE = 'regression'
                    } else if (currentBuild.getBuildCauses(
                        'hudson.triggers.SCMTrigger$SCMTriggerCause'
                    )) {
                        env.ACTIVE_SUITE = 'smoke'
                    }

                    echo "Test suite: ${env.ACTIVE_SUITE}"
                }
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
                        if (env.ACTIVE_SUITE == 'all') {
                            sh '"$VENV/bin/python" -m pytest'
                        } else {
                            sh '"$VENV/bin/python" -m pytest -m "$ACTIVE_SUITE"'
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

