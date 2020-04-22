import users
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

class Base():
    
    def __init__(self,driver):
        self.driver = driver
        self.PRODUCT_LIST      = '//*[contains(@class,"productName")]'

    def check_product_search(self,item):
        productlist=self.driver.find_elements_by_xpath(self.PRODUCT_LIST)
        if len(productlist)>0:
            for i in range(0,len(productlist)):
                try:
                    print(productlist[i].text.lower())
                    assert item.lower() in productlist[i].text.lower()
                    print("Row: "+str(i)+" Matches Found!")
                    return i
                    break
                except AssertionError:
                    print("Row: "+str(i)+" No matches found!")
        else:
            print("This Page is Clear!")


class HomePage(Base):

    def __init__(self, driver):
        # self.driver           = driver
        super().__init__(driver)
        self.SEARCH           = 'searchData'
        self.SEARCH_BUTTON    = 'searchBtn'
        self.SEARCHED_ITEM    = 'samsung'
        self.LOGO             = 'logo'
        self.SIGN_IN          = 'btnSignIn'
        self.HOMEPAGE_DISPLAY = 'userKvkkModal' 
        self.DISPLAY_NONE     = "arguments[0].setAttribute('style','display:allow;');"

    def check_kvkkmodel_warning(self):
        try:
            element=self.driver.find_element_by_id(self.HOMEPAGE_DISPLAY)
            self.driver.execute_script(self.DISPLAY_NONE,element)
        except:
            pass

    def click_search_item(self):
        self.driver.find_element_by_id(self.SEARCH).send_keys(self.SEARCHED_ITEM)
        self.driver.find_element_by_class_name(self.SEARCH_BUTTON).click()
    
    def check_page_loaded(self):
        if self.driver.find_element_by_class_name(self.LOGO):
            return True
        else:
            return False

    def click_sign_in_button(self):
        self.driver.find_element_by_class_name(self.SIGN_IN).click()

class LoginPage(Base):

    def __init__(self, driver):
        self.driver    = driver
        self.EMAIL     = 'email'
        self.PASSWORD  = 'password'
        self.LOGIN     = 'loginButton'
        self.ERROR     = 'errorText'

    def write_email(self,username):
        self.driver.find_element_by_id(self.EMAIL).clear()
        self.driver.find_element_by_id(self.EMAIL).send_keys(users.get_user(username)["email"])

    def write_password(self,username):
        self.driver.find_element_by_id(self.PASSWORD).clear()
        self.driver.find_element_by_id(self.PASSWORD).send_keys(users.get_user(username)["password"])
        self.driver.find_element_by_id(self.PASSWORD).send_keys(Keys.ENTER)

    # We created this function for single login step
    def login(self,username):
        self.write_email(username)
        self.write_password(username)

class SearchPage(Base):

    def __init__(self, driver):
        self.driver = driver
        self.PAGE2             = '//*[@class="pagination"]//*[text()="2"]'
        self.TARGET            = '//*[@id="view"]/ul/li[3]/div/div[1]/a/h3'
        self.ADDFAVORITES      = '//*[@id="view"]/ul/li[3]/div/div[1]/span'
        self.ERROR_MESSAGE     = 'message'
        self.ERROR_CLICK       = 'btn btnBlack confirm'
        self.ACCOUNT           = '//*[@id="header"]/div/div/div[2]/div[2]/div[2]/div[1]'
        self.MENU              = '//*[@class="customMenu"]/div[2]/div[2]/div/a[2]'
        self.FAVORITES_DISPLAY = "lightBox"

    def go_to_second_page(self):
        self.driver.find_element_by_xpath(self.PAGE2).click()
    
    def add_favorites_third_product(self):
        self.driver.execute_script("window.scrollTo(0, 1000)")
        product=self.driver.find_element_by_xpath(self.TARGET).text
        print("Target: "+product)
        try:
            self.driver.find_element_by_xpath(self.ADDFAVORITES).click()
            print("Clicked Add to Favorites button!")
        except ElementClickInterceptedException:
            add_favorites_third_product()

        return product

    def already_favorites(self,display_script):
        try:
            print(self.driver.find_element_by_class_name(self.ERROR_MESSAGE).text)
            element=self.driver.find_element_by_class_name(self.FAVORITES_DISPLAY)
            self.driver.execute_script(display_script,element)

        except NoSuchElementException:
            pass

    def slide_menu(self):
        element=self.driver.find_element_by_xpath(self.ACCOUNT)
        drag=ActionChains(self.driver).move_to_element(element)
        drag.perform()
        self.driver.find_element_by_xpath(self.MENU).click()

class FavoritesPage(Base):

    # Search target item in favorites menu
    def __init__(self, driver):
        self.driver = driver
        self.FAVORITES = '//*[@id="myAccount"]/div[3]/ul/li[1]/div/a/h4'
        self.DELETE = 'deleteProFromFavorites'

    def click_favorites_link(self):
        self.driver.find_element_by_xpath(self.FAVORITES).click()

    def delete_product(self,returned_value):
        print("Returned Value is: "+str(returned_value))
        try:
            returned_value=int(returned_value)
        except TypeError:
            print("NoneType, Returned Value changed to '0'")
            returned_value=0
        print(returned_value)
        try:
            self.driver.find_elements_by_class_name(self.DELETE)[int(returned_value)].click()
            print("Delete Successful!")
        except IndexError:
            print("Nothing Here!")
        self.driver.refresh()
