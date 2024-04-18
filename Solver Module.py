from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver


test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")

chrome_options.add_argument("--disable-gpu")
chrome_options.executable_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(options=chrome_options)

solver = RecaptchaSolver(driver=driver)

driver.get('https://verify.poketwo.net/captcha/401365910587179028')

recaptcha_iframe = test_driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

solver.click_recaptcha_v2(iframe=recaptcha_iframe)