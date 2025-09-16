pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'feature/new-feature',
                    url: 'https://github.com/Veronika-Gerasimova/lab1_dev',
                    credentialsId: 'github-token'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat "\"%PYTHON_PATH%\" -m venv %VENV_DIR%"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install --upgrade pip"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install -r requirements.txt"
            }
        }

        stage('Run Django Tests') {
            steps {
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py test"
            }
        }

        stage('Collect Django Static Files') {
            steps {
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py collectstatic --noinput"
            }
        }

         stage('Deploy Backend') {
            steps {
                echo 'Starting Django backend...'
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" manage.py runserver 0.0.0.0:8000"
            }
    }

    post {
        always { echo 'Pipeline finished.' }
        success { echo 'Build and tests succeeded!' }
        failure { echo 'Build or tests failed!' }
    }
}
