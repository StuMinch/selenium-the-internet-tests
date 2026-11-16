import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

SAUCE_URL = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub"
now = datetime.now()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def driver(request):
    options = ChromeOptions()
    options.browser_version = "latest"
    options.platform_name = "Windows 11"

    sauce_options = {
        "username": os.environ["SAUCE_USERNAME"],
        "accessKey": os.environ["SAUCE_ACCESS_KEY"],
        "build": os.getenv("SAUCE_BUILD", f"selenium-the-internet-tests {now}"),
        "name": request.node.name,
    }
    options.set_capability("sauce:options", sauce_options)

    driver = webdriver.Remote(command_executor=SAUCE_URL, options=options)
    driver.implicitly_wait(5)
    yield driver

    # Report the result to Sauce Labs so the job isn't left as "complete"
    rep_call = getattr(request.node, "rep_call", None)
    passed = rep_call is not None and rep_call.passed
    driver.execute_script(f"sauce:job-result={'passed' if passed else 'failed'}")
    driver.quit()
