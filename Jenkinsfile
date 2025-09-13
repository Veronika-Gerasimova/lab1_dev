pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/username/repo.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up virtual environment...'
                sh 'python -m venv ${VENV_DIR}'
                sh '${VENV_DIR}/Scripts/pip install --upgrade pip'
                sh '${VENV_DIR}/Scripts/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Django tests...'
                sh '${VENV_DIR}/Scripts/python manage.py test'
            }
        }

        stage('Collect Static Files') {
            steps {
                echo 'Collecting static files...'
                sh '${VENV_DIR}/Scripts/python manage.py collectstatic --noinput'
            }
        }

        stage('Deploy Locally') {
            when {
                branch 'main'  // Деплой только из ветки main
            }
            steps {
                echo 'Starting local Django server...'
                // для локального теста можно запускать сервер в фоне
                sh '${VENV_DIR}/Scripts/python manage.py runserver 0.0.0.0:8000 &'
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
