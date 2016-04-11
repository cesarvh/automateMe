from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

import sys, getopt


url = "http://www.bankofamerica.com/";
secureURl = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"
failedUrl = "InvalidCredentialsExceptionV2"
successUrl = "homepage"

def getBofa(*args):
	username = args[0][2]
	password = args[0][3]

	driver = webdriver.Firefox()
	
	driver.get(url)
	wait = lambda msg: WebDriverWait(driver, 10).until(EC.title_contains(msg))

	driver.find_element_by_id("onlineId1").send_keys(username)
	driver.find_element_by_id("passcode1").send_keys(password)
	driver.find_element_by_id("hp-sign-in-btn").click()
	wait("Bank of America")

	if (driver.current_url.find(failedUrl) == -1 and driver.current_url.find(successUrl) != -1):
		raise Exception("Your Password or Username were incorrect!")

	if (driver.current_url == secureURl):
		raise Exception("Your identity needs to be verified. Please enter your information and try again")

	wait("Accounts Overview")

	balance = driver.find_element_by_xpath("//*[@id=\"Traditional\"]/li[1]/div[1]/div[1]")
	print "Your Checkings Balance is " + balance.text + "."

	driver.find_element_by_name("onh_sign_off").click
	driver.quit()

if __name__ == "__main__":
  	f = sys.argv[1]
  	if f == "bofa":
		getBofa(sys.argv)
	else:
		raise Exception("No Known Command")




# https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go