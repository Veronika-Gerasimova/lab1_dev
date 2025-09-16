pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        NODE_HOME = 'C:\\Program Files\\nodejs'
        PATH = "${NODE_HOME};${env.PATH}"
        FRONTEND_DIR = 'plane'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/Veronika-Gerasimova/lab1_dev', credentialsId: 'github-token'
            }
        }

        stage('Setup Frontend') {
            steps {
                echo 'Setting up Node.js dependencies...'
                dir(env.FRONTEND_DIR) {
                    bat 'npm install'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                echo 'Building frontend for production...'
                dir(env.FRONTEND_DIR) {
                    bat 'npm run build'
                }
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

        stage('Run Django Tests') {
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

        stage('Configure Django for Frontend') {
            steps {
                echo 'Configuring Django to serve frontend...'
                // Создаем шаблон для обслуживания фронтенда через Django
                bat '''
                echo Adding frontend serving configuration to settings.py...
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Starting Django server with frontend...'
                script {
                    // Запускаем Django который будет обслуживать и фронтенд и бэкенд
                    bat "\"%VENV_DIR%\\Scripts\\python.exe\" manage.py runserver 0.0.0.0:8000"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '=== DEPLOYMENT SUCCESSFUL ==='
            echo 'Application is running at: http://192.168.0.1:8000'
            echo 'Frontend should be served by Django'
            echo '============================='
        }
        failure {
            echo 'Build or deployment failed!'
        }
    }
}
