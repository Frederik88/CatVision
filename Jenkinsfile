pipeline {
    agent any

    tools {
        // Install the Maven version configured as "M3" and add it to the path.
        maven "maven"
        jdk "jdk"
    }

     node('linux') {
        def maven = docker.image('maven:latest')
        maven.pull() // make sure we have the latest available from Docker Hub
    }

    stages {
        stage('Build') {
            steps {
                git branch: 'master',
                credentialsId: '1d1215a4-46e6-4f7c-9dbf-05daed395d4f',
                url: 'https://github.com/Frederik88/CatVision.git'
                
                dir('catvision-api'){
                    bat "mvn clean test -Dmaven.test.skip=false"
                }
            }

            post {
                // If Maven was able to run the tests, even if some of the test
                // failed, record the test results and archive the jar file.
                success {
                    junit '**/target/surefire-reports/TEST-*.xml'
                    archiveArtifacts 'target/*.jar'
                }
            }
        }
        stage('Deploy'){
            steps{
                echo 'Deployment stage'
                dir('catvision-api'){
                    echo 'Creater docker image'
                    bat "mvnw spring-boot:build-image"
                }
            }
        }
    }
    
}