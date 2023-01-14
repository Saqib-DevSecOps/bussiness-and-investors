def versioning(){
    def ver = sh(script: 'python3 version.py',returnStdout : true ).toString().trim()
    echo "$ver"
    
    return ver
}

def building(String Version)
{
    sh "docker build -t 7150148732291/business-and-investor:$Version -f Dockerfile.prod ."
    withCredentials([usernamePassword(credentialsId: "github-authentication" ,usernameVariable: "USER" , passwordVariable: "PASS")]){
    sh "echo $PASS | docker login -u $USER --password-stdin"
    sh "docker push 7150148732291/business-and-investor:$Version"
    sh "docker image rm 7150148732291/business-and-investor:$Version"
    }
}

def testing(){
    echo "Testing"
}

def deployment()
{
     echo "Deploying"
}

def version_upgraded()
{
    withCredentials([usernamePassword(credentialsId: "github-username-password", usernameVariable: "USER", passwordVariable: "PASS")])
    {
        sh 'git config --global user.email "jenkins@exarth.com"'
        sh 'git global --config user.username "exarth-jenkins"'
        sh "git remote set-url origin https://$USER:$PASSgit@github.com/saqib-devops/bussiness-and-investors.git"
        sh "git add ."
        sh 'git commit -m "Version Bump From exarth jenkins server"'
        sh 'git push origin HEAD:development'
    }
}
return this
