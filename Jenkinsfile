pipeline {
    agent {
        kubernetes {
            label 'slave-agent'
            yamlFile 'omri-create-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    environment {
        DOCKER_REGISTRY = 'https://registry.hub.docker.com' // Docker Hub URL
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
                        def dockerImage = docker.build('omriyan01/flask-app:latest', '.')
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
                    // Log in to Docker Hub using credentials (if needed)
                    withCredentials([usernamePassword(credentialsId: 'omri-dockerhub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh '''
                        echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                        '''
                    }

                    echo 'Building and pushing Helm chart...'
                    sh '''
                    helm package omri-flask-app
                    helm push omri-flask-app-0.1.0.tgz oci://registry-1.docker.io/omriyan01
                    '''
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
