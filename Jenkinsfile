pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        NODE_HOME = 'C:\\Program Files\\nodejs'
        PATH = "${NODE_HOME};${env.PATH}"
    }

    triggers {
        githubPush()  // запуск при пуше
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/Veronika-Gerasimova/lab1_dev', credentialsId: 'github-token'
            }
        }

        stage('Backend Setup') {
            steps {
                echo 'Setting up virtual environment...'
                bat "\"%PYTHON_PATH%\" -m venv %VENV_DIR%"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install --upgrade pip"
                bat "\"%VENV_DIR%\\Scripts\\python.exe\" -m pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py test"
            }
        }

        stage('Frontend Build') {
            steps {
                dir('plane') {
                    bat 'npm install'
                    bat 'npm run build'
                }
            }
        }

        stage('Collect Static') {
            steps {
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py collectstatic --noinput"
            }
        }

        stage('Deploy') {
            steps {
                echo "Restarting backend..."
                // убиваем старый процесс runserver (например через taskkill)
                bat 'taskkill /F /IM python.exe || exit 0'
                // запускаем заново
                bat "start cmd /c %VENV_DIR%\\Scripts\\python.exe manage.py runserver 0.0.0.0:8000"
            }
        }
    }
}
