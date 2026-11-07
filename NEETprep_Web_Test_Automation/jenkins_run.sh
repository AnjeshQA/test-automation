# =============================================================================
# jenkins_run.sh - CI entry point. Jenkins "Execute shell" step runs:
#     chmod +x jenkins_run.sh && ./jenkins_run.sh
# Steps: update code -> venv -> install deps -> install browser -> run tests (headless)
# Optional job parameters: GIT_BRANCH_TO_TEST, TEST_PATH, BROWSER
# =============================================================================

# 1. Fix Path for Mac binaries (Node, Appium, Python)
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
# Stop the script at the first failing command
set -e

# Optional Jenkins parameters / environment variables (defaults keep the old behaviour)
GIT_BRANCH_TO_TEST="${GIT_BRANCH_TO_TEST:-master}"   # repo has no 'main' branch
TEST_PATH="${TEST_PATH:-TestCases/test_loginpage.py}"
BROWSER="${BROWSER:-chromium}"                        # chromium | firefox | webkit

# 2. Git Integration (discard local changes and match the remote branch)
git fetch origin
git reset --hard "origin/${GIT_BRANCH_TO_TEST}"

# 3. Virtual Environment Setup
if [ ! -d ".venv" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv .venv
fi
# Activate the venv so pip/python below use it
source .venv/bin/activate

# 4. Sync Dependencies using your requirements.txt
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found! Installing core packages manually..."
    pip install pytest pytest-timeout pytest-rerunfailures pytest-bdd pytest-html pytest-playwright allure-pytest openpyxl
fi

# 4b. Playwright browsers (cached in ~/.cache/ms-playwright or ~/Library/Caches/ms-playwright after the first run)
# On a Linux agent use: python -m playwright install --with-deps "$BROWSER"
python -m playwright install "$BROWSER"

# 5. Clean old results (Allure data, Playwright traces/screenshots, HTML report)
rm -rf allure-results test-results reports

# 6. Run Tests (headless: never pass --headed in Jenkins)
# The script exits with pytest's exit code, so failed tests mark the Jenkins build as failed
# Archive in Jenkins: allure-results/**, reports/**, test-results/**, Logs/**
python3 -m pytest "$TEST_PATH" --browser "$BROWSER" --alluredir=allure-results \
    --html=reports/report.html --self-contained-html

#Jenkin Shell Command is given below
#chmod +x jenkins_run.sh
#./jenkins_run.sh
