pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        NODE_HOME = 'C:\\Program Files\\nodejs'
        PATH = "${NODE_HOME};${env.PATH}"
    }

    triggers {
        githubPush() // автозапуск на каждый коммит
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/Veronika-Gerasimova/lab1_dev', credentialsId: 'github-token'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat "\"%PYTHON_PATH%\" -m venv %VENV_DIR%"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install --upgrade pip"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install -r requirements.txt"
            }
        }

        stage('Run Django Tests') {
            steps {
                echo 'Running Django tests...'
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py test"
            }
        }

        stage('Deploy Backend as Daemon') {
            steps {
                echo 'Starting Django backend as daemon...'
                // Логи бэкенда будут сохраняться в backend.log
                bat "start /B %VENV_DIR%\\Scripts\\python.exe manage.py runserver 0.0.0.0:8000 > backend.log 2>&1"
            }
        }

        stage('Deploy Frontend as Daemon') {
            steps {
                dir('plane') {
                    echo 'Installing frontend dependencies...'
                    bat "npm install"

                    echo 'Starting frontend dev-server as daemon...'
                    // Логи фронта в frontend.log
                    bat "start /B npm run dev > frontend.log 2>&1"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Build and deploy succeeded!'
        }
        failure {
            echo 'Build or tests failed!'
        }
    }
}
