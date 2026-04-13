pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'DEMONSTRATE_FAILURE',
            defaultValue: false,
            description: 'Set to true to demonstrate pipeline FAILURE via Stage 5 invalid input'
        )
    }

    environment {
        DOCKER_IMAGE    = 'harshithbcs96/harshith-2022bcs0096-wine-quality:latest'
        CONTAINER_NAME  = "wine-quality-${BUILD_NUMBER}"
        API_URL         = 'http://localhost:8000'
        STUDENT_NAME    = 'Mootha Sri Harshit'
        ROLL_NO         = '2022bcs0096'
    }

    stages {

        stage('Stage 1 - Pull Image') {
            steps {
                script {
                    echo "=== [${STUDENT_NAME} | ${ROLL_NO}] Stage 1: Pull Image ==="
                    sh "docker pull ${DOCKER_IMAGE}"
                    sh "docker images ${DOCKER_IMAGE}"
                    echo "Image pulled successfully: ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Stage 2 - Run Container') {
            steps {
                script {
                    echo "=== [${STUDENT_NAME} | ${ROLL_NO}] Stage 2: Run Container ==="
                    sh "docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${DOCKER_IMAGE}"
                    echo "Container started and exposed on port 8000."
                }
            }
        }

        stage('Stage 3 - Wait for Readiness') {
            steps {
                script {
                    echo "=== [${STUDENT_NAME} | ${ROLL_NO}] Stage 3: Wait for Readiness ==="
                    def ready       = false
                    def maxAttempts = 6
                    def attempt     = 0

                    while (!ready && attempt < maxAttempts) {
                        attempt++
                        try {
                            def code = sh(
                                script: "curl -s -o /dev/null -w '%{http_code}' ${API_URL}/",
                                returnStdout: true
                            ).trim()
                            if (code == '200') {
                                ready = true
                                echo "API is ready (attempt ${attempt}/${maxAttempts}) -- status ${code}"
                            } else {
                                echo "Not ready yet (attempt ${attempt}/${maxAttempts}) -- status ${code}. Waiting 5s..."
                                sh 'sleep 5'
                            }
                        } catch (Exception e) {
                            echo "Connection error (attempt ${attempt}/${maxAttempts}). Waiting 5s..."
                            sh 'sleep 5'
                        }
                    }
                    if (!ready) {
                        error("API did not become ready within 30 seconds -- aborting.")
                    }
                }
            }
        }

        stage('Stage 4 - Valid Inference') {
            steps {
                script {
                    echo "=== [${STUDENT_NAME} | ${ROLL_NO}] Stage 4: Valid Inference ==="

                    def payload = '{"fixed_acidity":7.4,"volatile_acidity":0.70,"citric_acid":0.00,"residual_sugar":1.9,"chlorides":0.076,"free_sulfur_dioxide":11.0,"total_sulfur_dioxide":34.0,"density":0.9978,"pH":3.51,"sulphates":0.56,"alcohol":9.4}'

                    def raw = sh(
                        script: "curl -s -w '\\n%{http_code}' -X POST ${API_URL}/predict -H 'Content-Type: application/json' -d '${payload}'",
                        returnStdout: true
                    ).trim()

                    def lines      = raw.split('\n')
                    def statusCode = lines[-1].trim()
                    def body       = lines[0..-2].join('\n').trim()

                    echo "HTTP Status : ${statusCode}"
                    echo "Response   : ${body}"

                    if (statusCode != '200') {
                        error("Expected HTTP 200 for valid input but got ${statusCode}")
                    }

                    def wineQuality = null
                    def m = (body =~ /"prediction"\s*:\s*([\d.]+)/)
                    if (m) { wineQuality = m[0][1] }
                    if (!wineQuality) {
                        def m2 = (body =~ /"wine_quality"\s*:\s*([\d.]+)/)
                        if (m2) { wineQuality = m2[0][1] }
                    }
                    if (!wineQuality) {
                        error("Could not extract a numeric wine quality value from response: ${body}")
                    }

                    wineQuality.toDouble()

                    echo "============================================================"
                    echo "{ name: 'Mootha Sri Harshit', roll_no: '2022bcs0096', wine_quality: ${wineQuality} }"
                    echo "============================================================"
                }
            }
        }

        stage('Stage 5 - Invalid Input Test') {
            steps {
                script {
                    echo "=== [${STUDENT_NAME} | ${ROLL_NO}] Stage 5: Invalid Input Test ==="

                    def badPayload = '{"fixed_acidity":7.4}'

                    def raw = sh(
                        script: "curl -s -w '\\n%{http_code}' -X POST ${API_URL}/predict -H 'Content-Type: application/json' -d '${badPayload}'",
                        returnStdout: true
                    ).trim()

                    def lines      = raw.split('\n')
                    def statusCode = lines[-1].trim()
                    def body       = lines[0..-2].join('\n').trim()

                    echo "HTTP Status : ${statusCode}"
                    echo "Response   : ${body}"

                    def code = statusCode.toInteger()

                    if (params.DEMONSTRATE_FAILURE) {
                        error("FAILURE DEMO [Mootha Sri Harshit | 2022bcs0096]: Invalid/incomplete request detected (HTTP ${statusCode}). Missing required fields -- pipeline marked FAILED.")
                    } else {
                        if (code >= 400 && code < 600) {
                            echo "API correctly rejected invalid input with status ${statusCode} -- Stage 5 PASSED."
                        } else {
                            error("Expected 4xx/5xx for malformed input but got ${statusCode}.")
                        }
                    }
                }
            }
        }

        stage('Stage 6 - Stop Container') {
            steps {
                script {
                    echo "=== [${STUDENT_NAME} | ${ROLL_NO}] Stage 6: Stop Container ==="
                    sh "docker stop ${CONTAINER_NAME}"
                    sh "docker rm   ${CONTAINER_NAME}"

                    def leftover = sh(
                        script: "docker ps --filter name=${CONTAINER_NAME} --format '{{.Names}}'",
                        returnStdout: true
                    ).trim()

                    if (leftover) {
                        error("Container ${CONTAINER_NAME} is still running after removal!")
                    }
                    echo "Container stopped and removed -- no leftover containers."
                }
            }
        }
    }

    post {
        success {
            echo "================================================================"
            echo "PIPELINE STATUS : SUCCESS"
            echo "Student         : Mootha Sri Harshit"
            echo "Roll No         : 2022bcs0096"
            echo "All 6 stages passed successfully."
            echo "================================================================"
        }
        failure {
            echo "================================================================"
            echo "PIPELINE STATUS : FAILURE"
            echo "Student         : Mootha Sri Harshit"
            echo "Roll No         : 2022bcs0096"
            echo "One or more stages failed -- check console output above."
            echo "================================================================"
            script {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm   ${CONTAINER_NAME} || true"
            }
        }
        always {
            echo "Pipeline run complete -- Mootha Sri Harshit (2022bcs0096)"
        }
    }
}
