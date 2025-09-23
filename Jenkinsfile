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
                git branch: 'feature/new-feature', url: 'https://github.com/Veronika-Gerasimova/lab1_dev', credentialsId: 'github-token'
            }
        }

        stage('Merge Latest Changes') {
            steps {
                echo 'Merging latest changes from main branch...'
                bat 'git config --global user.email "geras-veronika@rambler.ru"'
                bat 'git config --global user.name "veronika"'
                bat 'git fetch origin'
                bat 'git merge origin/main'
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

        stage('Run Frontend') {
            steps {
                echo 'Starting frontend in background...'
                dir('plane') {
                    // Устанавливаем зависимости и запускаем npm dev-сервер в фоне
                    bat 'start /B cmd /c "npm install && npm run dev"'
                }
            }
        }

        stage('Run Django Tests') {
            steps {
                echo 'Running Django tests...'
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py test"
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
                // Запуск backend в фоне, чтобы фронтенд и бэкенд работали одновременно
                bat 'start /B cmd /c "%VENV_DIR%\\Scripts\\python.exe manage.py runserver 0.0.0.0:8000"'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            // Останавливаем все node и python процессы, если нужно
            // bat 'taskkill /F /IM node.exe'
            // bat 'taskkill /F /IM python.exe'
        }
        success {
            echo 'Build and tests succeeded!'
        }
        failure {
            echo 'Build or tests failed!'
        }
    }
}
