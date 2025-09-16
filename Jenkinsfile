pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        NODE_HOME = 'C:\\Program Files\\nodejs'
        PATH = "${NODE_HOME};${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'feature/new-feature', 
                    url: 'https://github.com/Veronika-Gerasimova/lab1_dev', 
                    credentialsId: 'github-token'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up virtual environment...'
                bat "\"%PYTHON_PATH%\" -m venv %VENV_DIR%"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install --upgrade pip"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install -r requirements.txt"
            }
        }

        stage('Install Frontend Dependencies') {
            steps {
                dir('plane') {
                    bat 'npm install'
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Django tests...'
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py test"
            }
        }

        stage('Collect Static Files') {
            steps {
                echo 'Collecting Django static files...'
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py collectstatic --noinput"
            }
        }

        stage('Build Frontend') {
            steps {
                echo 'Building frontend for production...'
                dir('plane') {
                    bat 'npm run build'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying backend and frontend...'
                // Запускаем сервер Django с указанием порта
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" manage.py runserver 0.0.0.0:8000"
            }
        }
    }

    post {
        always { echo 'Pipeline finished.' }
        success { echo 'Build and tests succeeded!' }
        failure { echo 'Build or tests failed!' }
    }
}
