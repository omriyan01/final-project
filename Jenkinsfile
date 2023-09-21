pipeline {
    agent {
        docker {
            // Use a Docker image with Docker and Docker Compose installed
            image 'docker:20.10-dind'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        DOCKER_REGISTRY = 'https://registry.hub.docker.com'
        DOCKER_HUB_CREDENTIALS = credentials('omri-dockerhub-cred') 
        GITLAB_TOKEN = credentials('omri-gitlab-cred')
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
                    try {
                        echo 'Starting Docker build...'
                        
                        // Clone the Git repository into the workspace
                        git branch: 'feature', credentialsId: 'omri-gitlab-cred', url: 'https://gitlab.com/sela-tracks/1095/students/omriy/application/omri-app/app-backend.git'
                        
                        // Build the Docker image from the current directory
                        sh 'docker build -t omriyan01/flask-app:latest .'
                        echo 'Docker build completed.'
                    } catch (Exception e) {
                        // Print detailed error information
                        echo "Error: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error("Docker build failed")
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
                    withCredentials([usernamePassword(credentialsId: 'omri-dockerhub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh '''
                        echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                        helm package omri-flask-app
                        helm push omri-flask-app-0.1.0.tgz oci://registry-1.docker.io/omriyan01
                        '''
                    }
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

