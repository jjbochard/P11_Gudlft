from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class TestClass:
    def test_login_page(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")

        assert driver.title == "GUDLFT Registration"

    def test_happy_login(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")

        email_form = driver.find_element(By.NAME, "email")
        email_form.clear()
        email_form.send_keys("john@simplylift.co")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()
        assert driver.title == "Summary | GUDLFT Registration"

        driver.close()

    def test_sad_login(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")

        email_form = driver.find_element(By.NAME, "email")
        email_form.clear()
        email_form.send_keys("error@test.co")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()
        assert "Please enter a valid secretary email" in driver.page_source

        driver.close()

    def test_see_clubs(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/clubs")

        assert driver.title == "Clubs Summary"

        driver.close()

    def test_goto_book_page(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")

        email_form = driver.find_element(By.NAME, "email")
        email_form.clear()
        email_form.send_keys("john@simplylift.co")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()

        book_link = driver.find_element(By.LINK_TEXT, "Book Places")
        book_link.click()

        assert driver.title == "Booking for Spring Festival || GUDLFT"

        driver.close()

    def test_book_sad(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")

        email_form = driver.find_element(By.NAME, "email")
        email_form.clear()
        email_form.send_keys("john@simplylift.co")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()

        book_link = driver.find_element(By.LINK_TEXT, "Book Places")
        book_link.click()

        email_form = driver.find_element(By.NAME, "places")
        email_form.clear()
        email_form.send_keys("200")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()

        assert (
            "Your club has not enough points to purchase 200 places."
            in driver.page_source
        )
        driver.close()

    def test_book_happy(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")

        email_form = driver.find_element(By.NAME, "email")
        email_form.clear()
        email_form.send_keys("john@simplylift.co")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()

        book_link = driver.find_element(By.LINK_TEXT, "Book Places")
        book_link.click()

        email_form = driver.find_element(By.NAME, "places")
        email_form.clear()
        email_form.send_keys("1")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()

        assert "Great-booking complete" in driver.page_source
        driver.close()

    def test_logout(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")

        email_form = driver.find_element(By.NAME, "email")
        email_form.clear()
        email_form.send_keys("john@simplylift.co")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()

        logout = driver.find_element(By.LINK_TEXT, "Logout")
        logout.click()

        assert driver.title == "GUDLFT Registration"
