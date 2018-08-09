///////////////////////////////////////////////////////////////////////
//  CHALLENGER JENKINS PIPELINE SCRIPT
//
//  The use-case for this pipeline is preparing and packaging a
//  release branch for quality assurance and acceptance testing. It
//  assumes that it is run by a Multibranch Pipeline.
//
//  The pipeline identifies five testing phases:
//
//  Unit:
//    Atomic tests of the application codebase.
//  Integration:
//    Test the application codebase as a whole, with external
//    dependencies (e.g., database servers, HTTP APIs) mocked.
//  System:
//    Test the application as a part of a larger system.
//  Smoke:
//    Runs black box tests in order to identify non-critical
//    issues with the application. Failing smoke tests will result
//    in the build being UNSTABLE, even if the next phase (preliminary
//    quality assurance) succeeds.
//  Preliminary Quality Assurance:
//    Like quality assurance testing, but without a "real" dataset i.e.
//    separated from the live application environment. These are
//    mostly black box tests on HTTP endpoints or application
//    responses to transmission on the Aorta messaging infrastrucure.
//
//  External dependencies that are not maintained within the boundaries
//  of the system being tested, are assumed to be mocked during all
//  test phases.
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
//  - docker-compose
//  - Jenkins Port Allocator plugin
//  - Global Slack Notifier plugin (if Slack is enabled in SG)
//
//  The pipeline assumes that the following ports are allocated by the
//  Jenkins Port Allocator plugin, defined as environment variables:
//
//  HTTP_PORT: Exposes the HTTP API, if applicable.
//  AORTA_ROUTER_PORT: Listen port for the Aorta Router, if applicable.
//  AORTA_BACKEND_PORT: Listen port for the Aorta backend message
//    broker, if applicable.
//
//  The pipeline is further configured by the environment variables
//  listed below:
//
///////////////////////////////////////////////////////////////////////
def image
def image_base
def image_name
def coverage_unit
def coverage_integration
def coverage_system
def workspace
def commit_tag
def tags


pipeline {
  agent any

  stages {
    stage('Setup') {
      steps {
        script {
          workspace = pwd()
          tags = []

          // Ensure that all tags are fetched and assign it to a variable. Note
          // that if the branch contains multiple tags, the last one (as returned
          // by git tag -l) will be used.
          sh 'git fetch --tags'
          commit_tag = sh(returnStdout: true, script: "git tag -l --points-at HEAD | tail -1").trim()
          if (commit_tag) {
            sh "echo 'Commit tag is: ${commit_tag}'"
          }

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

    stage('Lint') {
      steps {
        script {
          image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
            sh 'SQ_TESTING_PHASE=lint ./bin/run-tests'
          }
        }
      }
    }

    stage('Run unit tests') {
      steps {
        script {
          image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
            sh 'SQ_TESTING_PHASE=unit ./bin/run-tests'
            coverage_unit = readFile("./.coverage.unit.${env.BUILD_ID}")
          }
        }
      }
    }

    stage('Run integration tests') {
      steps {
        script {
          image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
            sh 'SQ_TESTING_PHASE=integration ./bin/run-tests'
            coverage_integration = readFile("./.coverage.integration.${env.BUILD_ID}")
          }
        }
      }
    }

    stage('Run system tests') {
      steps {
        script {
          image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
            sh 'SQ_TESTING_PHASE=system ./bin/run-tests'
            coverage_system = readFile("./.coverage.system.${env.BUILD_ID}")
          }
        }
      }
    }

    stage('Run smoke tests') {
      steps {
        script {
          image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
            sh 'SQ_TESTING_PHASE=smoke ./bin/run-tests'
          }
        }
      }
    }

    stage('Run prel. QA tests') {
      steps {
        script {
          image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
            sh 'SQ_TESTING_PHASE=preqa ./bin/run-tests'
          }
        }
      }
    }

    stage('Check coverage') {
      steps {
        script {
          image.inside("--entrypoint='' -v ${workspace}:/app -e BUILD_ID=${env.BUILD_ID}") {
            writeFile file: ".coverage.unit.${env.BUILD_ID}", text: "${coverage_unit}"
            writeFile file: ".coverage.integration.${env.BUILD_ID}", text: "${coverage_integration}"
            writeFile file: ".coverage.system.${env.BUILD_ID}", text: "${coverage_system}"
            sh 'coverage combine . && coverage report --fail-under 0'
          }
        }
      }
    }

    stage('Build final image') {
      steps {
        script {
            sh 'echo "This is a stub"'
        }
      }
    }

    stage('Publish') {
      steps {
        script {
          if (commit_tag) {
            tags.add(commit_tag)
          }

          // Generate a tag based on the commit, commit tags and Quantumfile
          // configuration.
          switch(env.GIT_BRANCH) {
            case 'master':
              tags.add('latest')
              break
            case 'develop':
              tags.add('latest-testing')
              break
            case ~/^(release|version|sprint)\-.*$/:
              tags.add("${env.GIT_BRANCH}-latest")
              break
            case ~/^(hotfix|fix)\-.*$/:
              tags.add("${env.GIT_BRANCH}-latest")
              break
            case ~/^(feature|task)\-.*$/:
              tags.add("${env.GIT_BRANCH}-latest")
              break
            default:
              sh 'echo "Branch is not a candidate for Docker image build."'
          }

          if (tags) {
            for (int i = 0; i < tags.size(); i++) {
              withDockerRegistry([ credentialsId: 'wizards-docker-repo' ]) {
                image.push("${tags[i]}")
              }
            }
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
