import unittest
from selenium import webdriver
from pages import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import HtmlTestRunner

class TestPages(unittest.TestCase):

    def setUp(cls):
        cls.driver = webdriver.Chrome("chromedriver.exe")
        cls.driver.get("http://www.n11.com")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_01_search_samsung_add_favorite_remove_favorite_with_login_valid_user(self):

        driver=self.driver

        # homepage - Check Page Load!
        home=HomePage(driver)
        home.check_kvkkmodel_warning()
        self.assertTrue(home.check_page_loaded())
        home.click_sign_in_button()
        
        # Login Page
        login=LoginPage(driver)
        login.login("yourvalid_user")
        self.assertEqual("https://www.n11.com/",driver.current_url)
        
        # Search In home Page!
        home.check_kvkkmodel_warning()
        home.click_search_item()
        
        # Search Page
        search=SearchPage(driver)
        print("Searching 'samsung' word in the Results...")
        home.check_product_search(home.SEARCHED_ITEM)
        search.go_to_second_page()
        # Return 3rd Item's name.
        returned3rd_item_name=search.add_favorites_third_product()
        # Confirm Loaded 2nd Page.
        self.assertEqual("https://www.n11.com/arama?q=samsung&pg=2",driver.current_url)
        # Print 3rd Item's name
        search.already_favorites(home.DISPLAY_NONE)
        search.slide_menu()
        
        # Favorites Page
        favorites=FavoritesPage(driver)
        favorites.click_favorites_link()
        returned_3rd_item_location=home.check_product_search(returned3rd_item_name)
        favorites.delete_product(returned_3rd_item_location)
        # Confirm Fav Page Loaded.
        self.assertEqual("https://www.n11.com/hesabim/favorilerim",driver.current_url)
        home.check_product_search(returned3rd_item_name)

    def tearDown(cls):
        cls.driver.close()
        cls.driver.quit()
        print("Test finished successfully.")


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="./"))
