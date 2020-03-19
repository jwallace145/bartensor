import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WEBSITE_URL = 'http://localhost:8000'


class ChromeSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def test_bartensor_link(self):
        self.driver.get(WEBSITE_URL)
        bartensor = self.driver.find_element_by_link_text('Bartensor')
        bartensor.click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'search-bar')))
            self.assertTrue(True)
        except:
            print('bartensor link timed out')
            self.assertTrue(False)

    def test_proposals_link(self):
        self.driver.get(WEBSITE_URL)
        proposals = self.driver.find_element_by_link_text('Proposals')
        proposals.click()
        self.driver.implicitly_wait(5)
        print(self.driver.current_url)
        self.assertTrue(self.driver.current_url ==
                        (WEBSITE_URL + '/timeline/'))

    def test_about_link(self):
        self.driver.get(WEBSITE_URL)
        about = self.driver.find_element_by_link_text('About')
        about.click()
        self.driver.implicitly_wait(5)
        self.assertTrue(self.driver.current_url ==
                        (WEBSITE_URL + '/about/'))

    def test_login_link(self):
        self.driver.get(WEBSITE_URL)
        about = self.driver.find_element_by_link_text('Login')
        about.click()
        self.driver.implicitly_wait(5)
        self.assertTrue(self.driver.current_url ==
                        (WEBSITE_URL + '/login/'))

    def test_login_link(self):
        self.driver.get(WEBSITE_URL)
        about = self.driver.find_element_by_link_text('Register')
        about.click()
        self.driver.implicitly_wait(5)
        self.assertTrue(self.driver.current_url ==
                        (WEBSITE_URL + '/register/'))

    def test_search_rum_and_coke(self):
        self.driver.get(WEBSITE_URL)
        self.assertIn('Bartensor', self.driver.title)
        search_bar = self.driver.find_element_by_id('search-bar')
        search_bar.clear()
        search_bar.send_keys('rum and coke')
        search_bar.send_keys(Keys.RETURN)
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, 'result_container')))
            first_response = self.driver.find_element_by_xpath(
                '//*[@id="1"]/div[1]/h2/button')
            self.assertTrue(first_response.text == 'Rum & Coke')
        except:
            print('search rum and coke failed')
            self.assertTrue(False)

    def tearDown(self):
        try:
            self.driver.close()
        except:
            pass


if __name__ == '__main__':
    unittest.main()
