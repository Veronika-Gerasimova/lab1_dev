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

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
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

        stage('Setup Frontend') {
            steps {
                echo 'Installing Node.js dependencies for frontend...'
                dir(env.FRONTEND_DIR) {
                    bat 'npm install'
                }
            }
        }

        stage('Run Backend and Frontend in Dev Mode') {
            parallel {
                stage('Run Django Backend') {
                    steps {
                        echo 'Starting Django backend...'
                        bat "start cmd /c \"%VENV_DIR%\\Scripts\\python.exe\" manage.py runserver 0.0.0.0:8000"
                    }
                }

                stage('Run Vue Dev Server') {
                    steps {
                        echo 'Starting Vue frontend dev server...'
                        dir(env.FRONTEND_DIR) {
                            bat "start cmd /c \"npm run dev -- --host 0.0.0.0\""
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '=== DEV ENVIRONMENT RUNNING ==='
            echo 'Django backend: http://<IP_PC>:8000'
            echo 'Vue frontend dev server: http://<IP_PC>:5173'
            echo 'Make sure Windows Firewall allows these ports!'
        }
        failure {
            echo 'Build or deployment failed!'
        }
    }
}
