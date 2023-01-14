def Version
pipeline{
    agent any
        stages{
            stage("Versioning"){
                steps{
                    script{
                        src = load "script.groovy"
                        Version = src.versioning()
                    }
                }
            }
            stage("Building"){
                steps{
                    script{
                        src.building "Version"
                    }
                }
            }
            stage("Testing"){
                steps{
                    script{
                         src.testing()
                    }
                }
            }
            stage("Deployment"){
                steps{
                    script{
                        src.deployment()
                    }
                }
            }
            stage("Version Bump to git"){
                steps{
                    script{
                        src.version_upgraded()
                    }
                }
            }
        }

}