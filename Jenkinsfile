pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
    }

    environment {
        PYTEST_ARGS = '--verbose --tb=short --junit-xml=test-results.xml --cov=calculator --cov-report=html:coverage --cov-report=term'
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    echo "=========================================="
                    echo "Build Statistics Report"
                    echo "=========================================="
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Build ID: ${BUILD_ID}"
                    echo "Job Name: ${JOB_NAME}"
                    echo "Build Tag: ${BUILD_TAG}"
                    echo "Workspace: ${WORKSPACE}"
                    echo "=========================================="
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing required packages..."
                    bat 'python -m pip install pytest pytest-cov'
                }
            }
        }

        stage('Run Tests with Coverage') {
            steps {
                script {
                    echo "Running test suite with coverage analysis..."
                    bat "python -m pytest ${PYTEST_ARGS} test_calculator.py"
                }
            }
        }
    }

    post {
        always {
            script {
                echo "=========================================="
                echo "Test Execution Summary"
                echo "=========================================="
                
                // Publish test results
                junit testResults: 'test-results.xml', allowEmptyResults: true
                
                // Archive coverage reports
                archiveArtifacts artifacts: 'coverage/**', allowEmptyArchive: true
                
                echo "Test Results: test-results.xml"
                echo "Coverage Report: coverage/index.html (archived)"
            }
        }

        success {
            script {
                echo "=========================================="
                echo "BUILD SUCCESSFUL"
                echo "=========================================="
                echo "Build completed at: ${new Date()}"
                echo "Build Duration: ${currentBuild.durationString}"
            }
        }

        failure {
            script {
                echo "=========================================="
                echo "BUILD FAILED"
                echo "=========================================="
                echo "Failed at: ${new Date()}"
                echo "Review logs above for details"
            }
        }

        unstable {
            script {
                echo "=========================================="
                echo "BUILD UNSTABLE"
                echo "=========================================="
                echo "Some tests may have failed or warnings detected"
            }
        }
    }
}