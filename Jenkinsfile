def Version
pipeline{
agent any
   stages{
        stage("Versioning")
        {
            steps
            {
                script
                {
                    src = load "script.groovy"
                    Version = src.versioning()
                    env.IMAGE_NAME = "7150148732291/pms:$Version"
                }
            }
        }
        stage("Building")
        {
            steps
            {
                script
                {
                    src.building "$Version"
                }
            }
        }
        stage("Deploying")
        {
            steps
            {
                script
                {
                    src.deploying "$Version"
                }
            }
        }
    }
}