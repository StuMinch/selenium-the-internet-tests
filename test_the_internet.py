from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

BASE_URL = "https://the-internet.herokuapp.com"


def test_basic_auth(driver):
    # Credentials embedded in the URL satisfy the browser's basic auth prompt
    driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")

    message = driver.find_element(By.CSS_SELECTOR, "#content p").text
    assert message == "Congratulations! You must have the proper credentials."


def test_checkboxes(driver):
    driver.get(f"{BASE_URL}/checkboxes")

    checkboxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")
    assert len(checkboxes) == 2

    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()

    assert all(checkbox.is_selected() for checkbox in checkboxes)


def test_dropdown(driver):
    driver.get(f"{BASE_URL}/dropdown")

    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 2")

    assert dropdown.first_selected_option.text == "Option 2"


def test_typos(driver):
    driver.get(f"{BASE_URL}/typos")

    # The page randomly introduces a typo into the second paragraph, so the
    # expected text can legitimately fail intermittently.
    text = driver.find_elements(By.CSS_SELECTOR, "#content p")[1].text
    assert text == "Sometimes you'll see a typo, other times you won't."
