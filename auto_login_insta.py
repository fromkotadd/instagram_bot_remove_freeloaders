from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random

def login(username, password, browser):

	try:
		browser.get('https://www.instagram.com')
		time.sleep(random.randrange(3, 5))

		username_input = browser.find_element_by_name('username')
		username_input.clear()
		username_input.send_keys(username)

		time.sleep(2)

		password_imput = browser.find_element_by_name('password')
		password_imput.clear()
		password_imput.send_keys(password)

		password_imput.send_keys(Keys.ENTER)

		time.sleep(5)
		return browser


	except Exception as ex:
		print(ex)
		browser.close()
		browser.quit()

