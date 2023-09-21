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

        stage('Build and Push Helm Chart') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'omri-dockerhub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh '''
                        echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                        helm package omri-flask-app
                        helm push omri-flak-app-0.1.0.tgz oci://registry-1.docker.io/omriyan01
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
