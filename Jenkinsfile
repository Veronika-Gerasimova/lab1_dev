pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_PATH = 'C:\\Users\\geras\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        NODE_HOME = 'C:\\Program Files\\nodejs'
        PATH = "${NODE_HOME};${env.PATH}"
        FRONTEND_DIR = 'plane'  // Путь к директории фронтенда
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'feature/new-feature', url: 'https://github.com/Veronika-Gerasimova/lab1_dev', credentialsId: 'github-token'
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
                echo 'Building frontend...'
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

        stage('Collect Django Static Files') {
            steps {
                echo 'Collecting Django static files...'
                bat "%VENV_DIR%\\Scripts\\python.exe manage.py collectstatic --noinput"
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Starting both frontend and backend...'
                script {
                    // Запускаем фронтенд в фоновом режиме
                    bat "start \"Frontend\" cmd /k \"cd ${env.FRONTEND_DIR} && npm run dev\""
                    
                    // Ждем немного, чтобы фронтенд успел запуститься
                    sleep(10)
                    
                    // Запускаем бэкенд
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
            echo 'Build and tests succeeded!'
        }
        failure {
            echo 'Build or tests failed!'
        }
    }
}
