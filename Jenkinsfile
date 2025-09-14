
pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Microsoft\\WindowsApps\\python-3.12.4-amd64.exe' // путь к Python на Windows
    }

    stages {
        stage('Test') {
            steps {
                echo 'Jenkinsfile действительно выполняется!'
            }
        }
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'dev', 
                    url: 'https://github.com/Veronika-Gerasimova/lab1_dev', 
                    credentialsId: 'github-token'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up virtual environment...'
                bat "\"%PYTHON_PATH%\" -m venv %VENV_DIR%"
                bat "%VENV_DIR%\\Scripts\\pip.exe install --upgrade pip"
                bat "%VENV_DIR%\\Scripts\\pip.exe install -r requirements.txt"
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
                expression { env.BRANCH_NAME == 'main' } // деплой только из main
            }
            steps {
                echo 'Starting local Django server...'
                bat "start cmd /c \"%VENV_DIR%\\Scripts\\python.exe manage.py runserver 0.0.0.0:8000\""
            }
        }
    }

    post {
        always { echo 'Pipeline finished.' }
        success { echo 'Build and tests succeeded!' }
        failure { echo 'Build or tests failed!' }
    }
}
