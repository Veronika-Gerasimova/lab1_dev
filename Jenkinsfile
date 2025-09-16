pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Test') {
            steps {
                echo 'Jenkinsfile start'
            }
        }

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
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install django-cors-headers qrcode python-docx openpyxl pyotp djangorestframework"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install Pillow"
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
                echo 'Collecting static files...'
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py collectstatic --noinput"
            }
        }

        stage('Deploy Locally') {
            when {
                branch 'main'
            }
            steps {
                echo 'Starting local Django server...'
                bat "start cmd /c \"%VENV_DIR%\\Scripts\\python.exe manage.py runserver 192.168.0.102:8000\""
            }
        }
    }

    post {
        always { echo 'Pipeline finished.' }
        success { echo 'Build and tests succeeded!' }
        failure { echo 'Build or tests failed!' }
    }
}
