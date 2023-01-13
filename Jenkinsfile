def Version
pipeline{
    agent any
        stages{
            stage("Versioning"){
                step{
                    script{
                        src = load "script.groovy"
                        Version = src.versioning()
                    }
                }
            }
            stage("Building"){
                step{
                    script{
                        src.building "Version"
                    }
                }
            }
            stage("Testing"){
                step{
                    script{
                         src.testing()
                    }
                }
            }
            stage("Deployment"){
                step{
                    script{
                        src.deployment()
                    }
                }
            }
            stage("Version Bump to git"){
                step{
                    script{
                        src.version_upgraded()
                    }
                }
            }
        }

}