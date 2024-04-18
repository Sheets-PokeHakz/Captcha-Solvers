from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import requests

from pydub import AudioSegment
import speech_recognition as sr

def SolveCaptcha(url: str) -> bool:
    # Create the ChromeOptions object
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.executable_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)

    # Add a 10-second delay after opening the URL
    time.sleep(10)

    try:
        captcha_selector = '#recaptcha-anchor > div.recaptcha-checkbox-border'
        audio_selector = '#recaptcha-audio-button'
        download_selector = '#rc-audio > div.rc-audiochallenge-tdownload > a'

        driver.switch_to.default_content()

        # Wait for captcha iframe to be visible
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
        captcha = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, captcha_selector)))

        time.sleep(2)
        captcha.click()

        driver.switch_to.default_content()

        # Wait for challenge to be visible
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")))
        audio_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, audio_selector)))

        time.sleep(2)
        audio_btn.click()

        driver.switch_to.default_content()

        # Wait for audio challenge to be visible
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, download_selector)))

        time.sleep(2)
        download_link = driver.find_element(
            By.CSS_SELECTOR, download_selector).get_attribute("href")

        r = requests.get(download_link)
        with open('sound.mp3', 'wb') as f:
            f.write(r.content)

        sound = AudioSegment.from_mp3("sound.mp3")
        sound.export("sound.wav", format="wav")

        sample_audio = sr.AudioFile('sound.wav')

        recognizer = sr.Recognizer()
        audio = None

        with sample_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        input_box = driver.find_element(By.ID, 'audio-response')

        time.sleep(2)
        input_box.send_keys(text.lower())
        input_box.send_keys(Keys.ENTER)

    except:
        try:
            driver.switch_to.default_content()

            WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#recaptcha-anchor > div.recaptcha-checkbox-checkmark')))

            driver.switch_to.default_content()

            verify_btn = driver.find_element(By.TAG_NAME, "button")

            time.sleep(2)
            verify_btn.click()

            time.sleep(5)
            driver.quit()

            return True

        except:
            driver.quit()
            return False

    try:
        driver.switch_to.default_content()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#rc-audio > div.rc-audiochallenge-error-message')))

        fail_text = driver.find_element(
            By.CSS_SELECTOR, '#rc-audio > div.rc-audiochallenge-error-message').text

        if len(fail_text) > 0:
            driver.quit()
            return False

    except TimeoutException:
        driver.switch_to.default_content()

        verify_btn = driver.find_element(By.TAG_NAME, "button")

        time.sleep(2)
        verify_btn.click()

        time.sleep(5)
        driver.quit()

        return True

def solve(url: str) -> None:
    solved = False

    while solved == False:
        solved = SolveCaptcha(url)

    return

solve('https://verify.poketwo.net/captcha/401365910587179028')

