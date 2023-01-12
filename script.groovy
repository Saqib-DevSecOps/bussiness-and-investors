def versioning(){
    def ver = sh(script: 'python3 version.py',returnStdout : true ).toString().trim()
    echo "$ver"
    withCredentials([usernamePassword
    (credentialsId : "github-authentication" , usernameVariable : "USER" , passwordVariable : "PASS")
                    ])
    {
    sh 'git config --global user.email "jenkins@gmail.com"'
    sh 'git config --global user.username "devops-jenkins"'
    sh "git remote set-url origin https://${USER}:${PASS}@github.com/saqib-devops/devops.git"
    sh 'git add .'
    sh 'git commit -m "Version : Version Increase $ver"'
    sh 'git push origin HEAD:development'
    }
    return ver
}

def building(String Version)
{
    withCredentials([usernamePassword
    (credentialsId : 'docker-hub' , usernameVariable : 'USER' , passwordVariable : 'PASS')
    ])
    {
    sh "docker build -t 7150148732291/devops:$Version -f Dockerfile.prod ."
    sh "echo $PASS | docker login  -u $USER --password-stdin"
    sh "docker push 7150148732291/business-investor:$Version"
    sh "docker image rm 7150148732291/business-investor:$Version"

    }
}
def deploying(String Version)
{
    def IMAGE_NAME = "7150148732291/devops:$Version"
    def server = "bash ./server_commands.sh ${IMAGE_NAME}"
    def ec2instance =  "ec2-user@3.222.34.1"
    sshagent(['pms-ec2']) {
    sh "scp docker-compose.prod.yml ${ec2instance}:/home/ec2-user"
    sh "scp server_commands.sh ${ec2instance}:/home/ec2-user"
    sh "scp .env.nginix-proxy ${ec2instance}:/home/ec2-user"
    sh "scp -r nginx ${ec2instance}:/home/ec2-user"
    sh "scp .env.prod ${ec2instance}:/home/ec2-user"
    sh "scp entrypoint.sh ${ec2instance}:/home/ec2-user"
    sh "ssh -o StrictHostKeyChecking=no ${ec2instance} ${server}"
    }
}
return this
