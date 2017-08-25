def label = "job-pga-ads"
def imageName
def branch
podTemplate(label: "${label}", containers: [
    containerTemplate(name: 'jnlp', image: 'harborbj01.jcloud.com/iaas/jenkins-jnlp-slave:latest'),
    containerTemplate(name: 'dind', image: 'harborbj01.jcloud.com/iaas/jenkins-slave-dind:17.03',privileged: true),
    containerTemplate(name: 'mysql', image: 'harborbj01.jcloud.com/iaas/mysql:5.6.37', envVars: [
            containerEnvVar(key: 'MYSQL_ROOT_PASSWORD', value: 'password'),
            containerEnvVar(key: 'MYSQL_ROOT_HOST', value: '%'),
        ]),
    containerTemplate(name: 'rabbitmq', image: "harborbj01.jcloud.com/iaas/rabbitmq:3.6.11"),
    containerTemplate(name: 'python', image: 'harborbj01.jcloud.com/iaas/jenkins-slave-python:2.7.13.4',ttyEnabled: true,command:'cat')
  ]) {
    node("${label}") {
        stage('checkout code') {
            git(branch:'master',credentialsId:'git-iaas-jcloud-com-credentials',url:'ssh://git@172.19.12.69:80/iaas-ops/pga-ads.git')
            commit = sh(returnStdout:true, script:"git rev-parse HEAD"); commit = commit.trim()
            branch = sh(returnStdout:true, script:"git branch -a --contains ${commit} | grep remotes | grep -v master | tail -1"); branch = branch.trim()
        }
        stage('test and package') {
            container('python') {
                sh """
                    bash unittest.sh
                """
            }
        }
        stage('build docker image') {
            imageTag = sh(returnStdout:true, script:"git show HEAD --pretty='format:%ci-%h' | head -1 |sed 's/+[0-9][0-9][0-9][0-9]//g' | sed 's/[ :]/-/g' | sed 's/--/-/g'")
            imageTag.trim()
            container('dind') {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'harborbj01-jcloud-com-credentials',
                    usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
                    imageName = "harborbj01.jcloud.com/iaas/pga-ads:${imageTag}"
                    imageName = imageName.trim()
                    sh """
                        docker login -u ${USERNAME} -p ${PASSWORD} harborbj01.jcloud.com
                        docker build -t ${imageName} .
                        docker push ${imageName}
                        docker tag ${imageName} harborbj01.jcloud.com/iaas/pga-ads:latest
                        docker push harborbj01.jcloud.com/iaas/pga-ads:latest
                    """
                }
            }
        }
    }
    stage("triggering test job for ${env.JOB_NAME}") {
        if (branch == '') {
            build(job:'pga-ads-test', propagate: false, parameters: [[$class: 'StringParameterValue', name: 'IMAGE', value: imageName]])
        }
    }
}
