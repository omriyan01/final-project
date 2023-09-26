pipeline {
    agent {
        kubernetes {
            label 'slave-agent'
            yamlFile 'omri-create-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    stages {
        stage('Test Docker') {
            steps {
                script {
                    sh 'docker --version'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Starting Docker build...'

                    // Clone the Git repository into the workspace
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: 'feature']],
                        userRemoteConfigs: [[url: 'https://github.com/omriyan01/final-project.git']]
                    ])

                    // Build the Docker image from the current directory
                    def dockerImage = docker.build('omriyan01/flask-app:latest', '.')
                    echo 'Docker build completed.'
                }
            }
        }

        // Add the pytest stage here
        stage('Run Pytest') {
            steps {
                script {
                    // Run pytest in a Docker container
                    docker.image('omriyan01/flask-app:latest').inside {
                        sh 'pytest test.py'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Starting Docker push...'

                    // Log in to Docker Hub using credentials
                    withCredentials([usernamePassword(credentialsId: 'omri-dockerhub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh '''
                        echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                        docker push omriyan01/flask-app:latest
                        '''
                    }

                    echo 'Docker push completed.'
                }
            }
        }

        stage('Build and Push Helm Chart') {
            steps {
                script {
                    // Log in to Docker Hub using credentials (if needed)
                    withCredentials([usernamePassword(credentialsId: 'omri-dockerhub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh '''
                        echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                        helm package omri-flak-app
                        helm push omri-flak-app-0.1.0.tgz oci://registry-1.docker.io/omriyan01
                        '''
                    }
                    echo 'Helm chart build and push completed.'
                }
            }
        }
    }

    post {
        success {
            echo 'Docker image and Helm chart pushed successfully.'
        }
    }
}
