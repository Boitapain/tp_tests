pipeline {
    agent any

    environment {
        // En supposant que le Sonar Scanner est configuré dans Jenkins sous le nom "SonarQubeScanner"
        SCANNER_HOME = tool 'SonarQubeScanner'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup environment & Tests') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest --cov=app --cov-report=xml
                radon cc app -s -a
                '''
            }
        }

        stage('SonarQube analysis') {
            steps {
                // En supposant que le serveur SonarQube est configuré dans Jenkins sous le nom "SonarQubeServer"
                withSonarQubeEnv('SonarQubeServer') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner"
                }
            }
        }
    }
}
