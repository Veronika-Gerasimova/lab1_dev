pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        NODE_HOME = 'C:\\Program Files\\nodejs'
        PATH = "${NODE_HOME};${env.PATH}"
    }

    triggers {
        // Автозапуск на каждый коммит (при настройке GitHub Webhook)
        githubPush()
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

        stage('Build Frontend') {
            steps {
                dir('plane') {
                    echo 'Installing frontend dependencies...'
                    bat "npm install"
                    echo 'Building frontend...'
                    bat "npm run build"
                }
                // копируем билд во фронт-статик Django
                bat "xcopy /E /I /Y plane\\dist static\\frontend"
            }
        }

        stage('Collect Django Static Files') {
            steps {
                echo 'Collecting Django static files...'
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py collectstatic --noinput"
            }
        }

        stage('Deploy Backend') {
            steps {
                echo 'Starting Django backend...'
                // запускаем как демон, чтобы пайплайн не блокировался
                bat "start /B %VENV_DIR%\\Scripts\\python.exe manage.py runserver 0.0.0.0:8000"
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '✅ Build and deploy succeeded!'
        }
        failure {
            echo '❌ Build or tests failed!'
        }
    }
}
