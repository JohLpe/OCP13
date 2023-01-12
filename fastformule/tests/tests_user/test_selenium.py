from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User


class RegistrationPage(StaticLiveServerTestCase):

    def setUp(self):
        opts = ChromeOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                       chrome_options=opts)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)
        User.objects.create_user("AnotherUser",
                                 "anotheruser@mail.com",
                                 "thisisatestpssword")
        self.re_user = User.objects.get(username="AnotherUser")

    def test_registration_page(self):

        self.driver.get(self.live_server_url + "/registration/")
        self.wait.until(cond.presence_of_all_elements_located)

        self.driver.find_element(By.XPATH, '//*[@id="id_username"]').send_keys("Testusername")
        self.driver.find_element(By.XPATH, '//*[@id="id_email"]').send_keys("testusername@mail.com")
        self.driver.find_element(By.XPATH, '//*[@id="id_password1"]').send_keys("mytestpssw0rd")
        self.driver.find_element(By.XPATH, '//*[@id="id_password2"]').send_keys("mytestpssw0rd")

        self.driver.find_element(By.ID, "register-btn").submit()
        self.wait.until(cond.url_changes)

        assert self.driver.current_url == self.live_server_url + "/login/"

    def test_login_page(self):

        self.driver.get(self.live_server_url + "/login/")
        self.wait.until(cond.presence_of_all_elements_located)

        self.driver.find_element(By.CSS_SELECTOR, '[name="username"]').send_keys("AnotherUser")
        self.driver.find_element(By.CSS_SELECTOR, '[name="password"]').send_keys("thisisatestpssword")

        self.driver.find_element(By.CSS_SELECTOR, '[name="Login User"]').click()
        self.wait.until(cond.url_changes)

        assert self.driver.current_url == self.live_server_url +\
            "/saisons/actuelle/"

    def tearDown(self):
        self.driver.quit()
