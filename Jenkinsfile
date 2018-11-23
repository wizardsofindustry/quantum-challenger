///////////////////////////////////////////////////////////////////////
//  CHALLENGER JENKINS PIPELINE SCRIPT
//
//  The use-case for this pipeline is preparing and packaging a
//  release branch for quality assurance and acceptance testing. It
//  assumes that it is ran by a Multibranch Pipeline.
//
//  The pipeline identifies three testing phases:
//
//  Unit:
//    Atomic tests of the application codebase.
//  Integration:
//    Test the application codebase as a whole, with external
//    dependencies (e.g., database servers, HTTP APIs) mocked.
//  System:
//    Test the application as a part of a larger system.
//
//  External dependencies that are not maintained within the boundaries
//  of the system being tested, are assumed to be mocked during all
//  test phases. Services such as databases and message brokers are to be
//  mocked during unit and integration testing; during system testing it
//  may be assumed that these services are present on the CI/CD slave.
//
//  A succesful build run may result in the containerized application
//  being published to the Docker registry (specified by $DOCKER_REGISTRY)
//  with the tags specified by the commit or branch-based tag. See the
//  docker.ci.build_branches section in the Quantumfile for more
//  information.
//
//  For the pipeline to function correctly, the following applications
//  and plugins need to be installed in the Jenkins node(s):
//
//  - docker
//  - Jenkins Port Allocator plugin
//  - SSH Agent Plugin
//  - Global Slack Notifier plugin (if Slack is enabled in QSA)
//  - Kubernetes Continuous Deploy (when configured to deploy with Kubernetes)
//  - Pipeline Utility Steps
//
//
//  Suggested plugins:
//  - Google Container Registry Auth Plugin (when publishing to GCR)
//
//  The pipeline is further configured by the environment variables
//  listed below:
//
///////////////////////////////////////////////////////////////////////
def changed_files
def commit_hash
def commit_tag
def coverage_unit
def coverage_integration
def coverage_system
def force_deploy
def image
def image_base
def image_name
def must_deploy
def tags
def workspace


pipeline {

  agent {
    label 'docker'
  }

  environment {
    CHALLENGER_RDBMS_DSN = 'sqlite:///db.sqlite3'
    GNUPGHOME = "/tmp/build-${env.BUILD_ID}"
  }

  stages {

    stage('Setup') {
      steps {
        script {
          changed_files = sh(
            script: 'git diff --name-only HEAD^1',
            returnStdout: true
          ).trim().tokenize('\n')
          for (i in changed_files) {
            echo "Detected change in ${i}"
          }

          // Ensure that all tags are fetched and assign it to a variable. Note
          // that if the branch contains multiple tags, the last one (as returned
          // by git tag -l) will be used.
          commit_tag = sh(
            returnStdout: true,
            script: "git tag -l --points-at HEAD | tail -1"
          ).trim()
          if (commit_tag) {
            sh "echo 'Commit tag is: ${commit_tag}'"
          }
        }
      }
    }

    stage('Lint') {
      parallel {
        stage('YAML') {
          steps {
            sh('find . -name "*.yml" -type f | xargs python3 -m yamllint --strict')
          }
        }
      } // End linting stages.
    }

    stage('Build') {
      steps {
        script {
          workspace = pwd()
          tags = []

          // Ensure that the base image is up-to-date
          image_base = docker.image('wizardsofindustry/quantum:latest')
          image_base.pull()

          // Build the application Docker image, ensuring that
          // we have the latest version of the sg base image.
          // Put the Jenkins build identifier in the image
          // tag so that we can run concurrent builds.
          image_name = 'wizardsofindustry/quantum-challenger'
          image = docker.build("${image_name}:${env.BUILD_ID}")
        }
      }
    }

    stage('Run tests') {

      parallel {
        stage('Lint') {
          steps {
              script {
                image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
                  sh('pylint challenger --ignore __init__.py')
                }
              }
          }
        }

        stage('Unit') {
          steps {
            script {
              image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
                sh 'QUANTUM_TESTING_PHASE=unit ./bin/run-tests'
                coverage_unit = readFile("./.coverage.unit.${env.BUILD_ID}")
              }
            }
          }
        }

        stage('Integration') {
          steps {
            script {
              image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
                sh 'QUANTUM_TESTING_PHASE=integration ./bin/run-tests'
                coverage_integration = readFile("./.coverage.integration.${env.BUILD_ID}")
              }
            }
          }
        }

        stage('System') {
          steps {
            script {
              image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
                sh 'QUANTUM_TESTING_PHASE=system ./bin/run-tests'
                coverage_system = readFile("./.coverage.system.${env.BUILD_ID}")
              }
            }
          }
        }
      }
    }

    stage('Check coverage') {

      parallel {
        stage('Python') {
          steps {
            script {
              image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
                writeFile file: ".coverage.unit.${env.BUILD_ID}", text: "${coverage_unit}"
                writeFile file: ".coverage.integration.${env.BUILD_ID}", text: "${coverage_integration}"
                writeFile file: ".coverage.system.${env.BUILD_ID}", text: "${coverage_system}"
                sh 'coverage combine . && coverage report --fail-under 100 --omit **/test_*'
              }
            }
          }
        }
      }
    }

    stage('Publish') {
      steps {
        script {
          force_deploy = false
          commit_hash = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
          if (commit_tag) {
            tags.add(commit_tag)
          }

          // The switch/case block below determines the deployment
          // environment and the deployment name based on configuration
          // in Quantumfile.ci.build_branches, so that the pipeline can
          // publish a container and deploy it to a specific environment.
          env.QUANTUM_DEPLOYMENT_NAME = ''
          env.QUANTUM_DEPLOYMENT_ENV = ''
          switch(env.GIT_BRANCH) {
            case 'master':
              tags.add('latest')
              break
            case 'develop':
              env.QUANTUM_DEPLOYMENT_NAME = 'staging'
              env.QUANTUM_DEPLOYMENT_ENV = 'staging'
              force_deploy = true
              tags.add('staging')
              break
            case '^(release|version|sprint)-.*$':
              break
            case '^(hotfix|fix)-.*$':
              break
            case '^(feature|task)-.*$':
              break
            default:
              echo "Branch '${env.GIT_BRANCH}' is not selected for deployment."
          }

          // If the pipeline is configured to always deploy regardless of the presence
          // of a commit tag, create one based on the short commit hash.
          if (!commit_tag && !!env.QUANTUM_DEPLOYMENT_ENV && force_deploy) {
            commit_tag = "${commit_hash}"
            tags.add(commit_tag)
          }

          // Determine the tag of the image that is to be deployed, so that
          // pipeline knows which image to deploy to ${env.QUANTUM_DEPLOYMENT_ENV}.
          // If a tag is defined and the QUANTUM_DEPLOYMENT_ENV environment
          // variable is set, this means we have a green light for deployment.
          if (!!commit_tag && !!env.QUANTUM_DEPLOYMENT_ENV) {
            env.IMAGE_TAG = commit_tag
          }
          must_deploy = (!!commit_tag && !!env.QUANTUM_DEPLOYMENT_ENV)
          if (!!tags) {
            for (int i = 0; i < tags.size(); i++) {
              withDockerRegistry([ credentialsId: 'wizards.dockerhub' ]) {
                image.push("${tags[i]}")
              }
            }
          }
        }
      }
    }

    stage('Configure') {

      // Configuration files are always deployed to the current environment
      // if we detect changes, regardless of an actual container image being
      // built. This ensures that the service, pod and job deploy steps always
      // have access to the configs specified in the VCS.
      when {
        expression {
          def files = findFiles(glob: "k8s/config.*")
          return (files.length > 0) && !!must_deploy
        }
      }

      parallel {

        stage('Global') {
          when {
            expression {
              return fileExists('k8s/config.common.yml')
            }
          }
          steps {
            kubernetesDeploy(
              kubeconfigId: "k8s-${env.QUANTUM_DEPLOYMENT_ENV}",
              configs: "k8s/config.common.yml",
              enableConfigSubstitution: true
            )
          }
        }

        stage('Environment') {
          when {
            expression {
              return fileExists("k8s/config.${env.QUANTUM_DEPLOYMENT_ENV}.yml")
            }
          }
          steps {
            kubernetesDeploy(
              kubeconfigId: "k8s-${env.QUANTUM_DEPLOYMENT_ENV}",
              configs: "k8s/config.${env.QUANTUM_DEPLOYMENT_ENV}.yml",
              enableConfigSubstitution: true
            )
          }
        }
      }
    }

    stage('Deploy') {
      when {
        expression {
          return !!must_deploy
        }
      }

      parallel {

        // Ensure that the Kubernetes Continuous Deploy plugin is installed on
        // the Jenkins master. Additionally, a Kubernetes configuration must
        // be added as a system-wide credential. The naming convention of
        // 'k8s-<deployment environment name>' is used.
        stage('Deploy services') {
          when {
            expression {
              def files = findFiles(glob: "k8s/service.*")
              return (files.length > 0)
            }
          }
          steps {
            kubernetesDeploy(
              kubeconfigId: "k8s-${env.QUANTUM_DEPLOYMENT_ENV}",
              configs: "k8s/service.*",
              enableConfigSubstitution: true
            )
          }
        }
        stage('Deploy pods') {
          when {
            expression {
              def files = findFiles(glob: "k8s/deployment.*")
              return (files.length > 0)
            }
          }
          steps {
            kubernetesDeploy(
              kubeconfigId: "k8s-${env.QUANTUM_DEPLOYMENT_ENV}",
              configs: "k8s/deployment.*",
              enableConfigSubstitution: true
            )
          }
        }
        stage('Deploy jobs') {
          when {
            expression {
              def files = findFiles(glob: "k8s/job.*")
              return (files.length > 0)
            }
          }
          steps {
            kubernetesDeploy(
              kubeconfigId: "k8s-${env.QUANTUM_DEPLOYMENT_ENV}",
              configs: "k8s/job.*",
              enableConfigSubstitution: true
            )
          }
        }
      }
    }
  } // End stages

  post {
    always {
      sh 'make clean'
    }
    success {
      slackSend(
        color: "#2EB886",
        message: "Success: Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (${env.BUILD_URL})")
    }
    failure {
      slackSend(
        color: "#CC0000",
        message: "Failed: Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (${env.BUILD_URL})")
    }
  }

} // End pipeline
