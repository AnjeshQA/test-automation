// =============================================================================
// Jenkinsfile - CI pipeline for the NEETprep Playwright test framework
//
// Jenkins setup (one time):
//   New Item -> Pipeline (or Multibranch Pipeline)
//   Pipeline -> Definition: "Pipeline script from SCM" -> Git -> this repo
//   Script Path: Jenkinsfile
//
// Optional Jenkins plugins (the pipeline still runs without them, it just skips that report):
//   - HTML Publisher  -> "Playwright HTML Report" link on the build page
//   - Allure          -> "Allure Report" link on the build page (also configure the
//                        Allure commandline under Manage Jenkins -> Tools, name it "allure")
//   JUnit (test results/trends) and archiving are built into Jenkins.
//
// Build result:
//   SUCCESS  -> all tests passed
//   UNSTABLE -> some tests failed (reports are still published)
//   FAILURE  -> setup problem or pytest could not run
// =============================================================================

pipeline {
    // Any agent with python3 (3.10+) and internet access. Linux or macOS.
    agent any

    // Values the user can choose with "Build with Parameters"
    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run the tests in')
        string(name: 'TEST_PATH', defaultValue: 'TestCases', description: 'Tests to run, e.g. TestCases or TestCases/test_login_bdd.py')
        string(name: 'PYTEST_ARGS', defaultValue: '', description: 'Extra pytest options, e.g. -k login  or  -m sanity')
        booleanParam(name: 'INSTALL_BROWSER_DEPS', defaultValue: false, description: 'Linux agents only: also install browser system libraries (needs sudo)')
    }

    options {
        // Stop a hung build
        timeout(time: 45, unit: 'MINUTES')
        // Keep the last 20 builds (and their reports)
        buildDiscarder(logRotator(numToKeepStr: '20'))
        // Never run two builds of this job at the same time (they share the test account)
        disableConcurrentBuilds()
    }

    environment {
        // Folder of the framework inside the repo
        PROJECT_DIR = 'NEETprep_Web_Test_Automation'
        // Unbuffered Python output so logs appear live in the console
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Setup') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh '''
                        set -e
                        # 1. Python virtual environment (re-used between builds on the same agent)
                        python3 -m venv .venv
                        . .venv/bin/activate

                        # 2. Python dependencies
                        pip install --upgrade pip
                        pip install -r requirements.txt

                        # 3. Playwright browser (cached on the agent after the first build)
                        if [ "$INSTALL_BROWSER_DEPS" = "true" ]; then
                            python -m playwright install --with-deps "$BROWSER"
                        else
                            python -m playwright install "$BROWSER"
                        fi

                        # 4. Remove reports from the previous build
                        rm -rf allure-results test-results reports
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                dir("${PROJECT_DIR}") {
                    script {
                        // Headless by default (never pass --headed in CI).
                        // returnStatus: a test failure should not stop the pipeline before reports are published
                        def status = sh(returnStatus: true, script: '''
                            . .venv/bin/activate
                            python -m pytest "$TEST_PATH" --browser "$BROWSER" $PYTEST_ARGS \
                                --alluredir=allure-results \
                                --html=reports/report.html --self-contained-html \
                                --junitxml=reports/junit.xml
                        ''')
                        // pytest exit codes: 0 = all passed, 1 = some tests failed, other = error
                        if (status == 1) {
                            unstable('Some tests failed - see the reports')
                        } else if (status != 0) {
                            error("pytest could not run the tests (exit code ${status})")
                        }
                    }
                }
            }
        }
    }

    post {
        // Runs whether the build passed or failed, so reports are always available
        always {
            dir("${PROJECT_DIR}") {
                // Test results table + trend graph (built-in JUnit plugin)
                junit(testResults: 'reports/junit.xml', allowEmptyResults: true)

                // Downloadable files: HTML report, Allure data, Playwright traces/screenshots, logs
                archiveArtifacts(artifacts: 'reports/**, allure-results/**, test-results/**, Logs/**',
                                 allowEmptyArchive: true, fingerprint: false)

                script {
                    // pytest-html report as a link on the build page (HTML Publisher plugin)
                    try {
                        publishHTML(target: [reportDir: 'reports', reportFiles: 'report.html',
                                             reportName: 'Playwright HTML Report',
                                             keepAll: true, alwaysLinkToLastBuild: true, allowMissing: true])
                    } catch (err) {
                        echo "HTML Publisher plugin not available - report is in the build artifacts (reports/report.html). ${err}"
                    }

                    // Allure report as a link on the build page (Allure plugin)
                    try {
                        allure(includeProperties: false, results: [[path: 'allure-results']])
                    } catch (err) {
                        echo "Allure plugin not available - raw data is in the build artifacts (allure-results/). ${err}"
                    }
                }
            }
        }
    }
}
