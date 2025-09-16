pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Checkout main') {
            steps {
                echo "Cloning repository (main)..."
                git branch: 'main',
                    url: 'https://github.com/Veronika-Gerasimova/lab1_dev',
                    credentialsId: 'github-token'
            }
        }

        stage('Merge feature branch') {
            steps {
                echo "Merging feature/new-feature into main..."
                bat """
                git fetch origin feature/new-feature
                git checkout main
                git merge origin/feature/new-feature --no-edit
                """
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up virtual environment...'
                bat "\"%PYTHON_PATH%\" -m venv %VENV_DIR%"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install --upgrade pip"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install -r requirements.txt"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install django-cors-headers qrcode python-docx openpyxl pyotp djangorestframework Pillow"
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
            steps {
                echo 'Starting local Django server...'
                // запустим на всех интерфейсах, чтобы телефон в сети видел
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" manage.py runserver 0.0.0.0:8000"
            }
        }

        stage('Expose via ngrok') {
            steps {
                echo 'Starting ngrok tunnel...'
                bat "ngrok http 8000"
            }
        }
    }

    post {
        always { echo 'Pipeline finished.' }
        success { echo 'Build and tests succeeded!' }
        failure { echo 'Build or tests failed!' }
    }
}
