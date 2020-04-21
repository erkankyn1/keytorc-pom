import unittest
from selenium import webdriver
from pages import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class TestPages(unittest.TestCase):

    def setUp(cls):
        cls.driver = webdriver.Chrome("chromedriver.exe")
        cls.driver.get("http://www.n11.com")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_01_search_samsung_add_favorite_remove_favorite_with_login_valid_user(self):
        
        driver=self.driver
        # Homepage Check Page Load! -- MainPage(Change to base)
        Base=MainPage(driver)
        self.assertTrue(Base.check_page_loaded())
        Base.click_sign_in_button()
        
        # Login Page
        Login=LoginPage(driver)
        Login.login_success("yourvalid_user")
        self.assertEqual("https://www.n11.com/",driver.current_url)
        
        # Home Page
        Home=HomePage(driver)
        Home.click_search_item()

        # Search Page
        Search=SearchPage(driver)
        print("Searching Samsung word in the Results...")
        Search.check_product_search(Home.SEARCHED_ITEM)
        Search.go_to_second_page()
        self.assertTrue(Base.check_page_loaded())
        # Return 3rd Item's name.
        returned3rd_item_name=Search.add_favorites_third_product()
        # Print 3rd Item's name
        Search.already_favorites()
        Search.slide_menu()
        
        # Favorites Page
        Favorites=FavoritesPage(driver)
        Favorites.click_favorites_link()
        returned_3rd_item_location=Search.check_product_search(returned3rd_item_name)
        Favorites.delete_product(returned_3rd_item_location)



    def tearDown(cls):
        cls.driver.close()
        cls.driver.quit()
        print("Test finished successfully.")


if __name__ == "__main__":
    unittest.main()
