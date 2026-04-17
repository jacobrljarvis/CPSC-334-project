pipeline {
    agent any

    stages {
        stage('Install Pytest') {
            steps {
                bat 'py -m pip install pytest'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'py -m pytest test_calculator.py'
            }
        }
    }
}
