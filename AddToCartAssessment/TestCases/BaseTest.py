import logging
import pytest

# Setting up logging so you can see what's happening in the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

@pytest.mark.flaky(reruns=1)
# IMPORTANT: "setup" must match the function name in conftest.py
# "log_on_failure" handles the automatic screenshots
@pytest.mark.usefixtures("setup", "log_on_failure")
class BaseTest:
    pass