from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import undetected_chromedriver as uc
import time
import random
import requests

from pydub import AudioSegment
import speech_recognition as sr
from selenium_stealth import stealth

def SolveCaptcha(url: str) -> bool:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-maximize')
    chrome_options.add_argument(f'user-agent={generate_user_agent()}')

    chrome = uc.Chrome(browser_executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",
                       use_subprocess=True, chrome_options=chrome_options)

    # Apply Selenium Stealth to bypass detection
    stealth(chrome,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    chrome.get(url)
    time.sleep(10)

    try:
        captcha_selector = '#recaptcha-anchor > div.recaptcha-checkbox-border'
        audio_selector = '#recaptcha-audio-button'
        download_selector = '#rc-audio > div.rc-audiochallenge-tdownload > a'

        chrome.switch_to.default_content()

        # Wait for captcha iframe to be visible
        WebDriverWait(chrome, 20).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
        captcha = WebDriverWait(chrome, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, captcha_selector)))

        time.sleep(random.uniform(1, 3))
        captcha.click()

        chrome.switch_to.default_content()

        # Wait for challenge to be visible
        WebDriverWait(chrome, 20).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")))
        audio_btn = WebDriverWait(chrome, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, audio_selector)))

        time.sleep(random.uniform(1, 3))
        audio_btn.click()

        chrome.switch_to.default_content()

        # Wait for audio challenge to be visible
        WebDriverWait(chrome, 20).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")))
        WebDriverWait(chrome, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, download_selector)))

        time.sleep(random.uniform(1, 3))
        download_link = chrome.find_element(
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

        input_box = chrome.find_element(By.ID, 'audio-response')

        time.sleep(random.uniform(1, 3))
        input_box.send_keys(text.lower())
        input_box.send_keys(Keys.ENTER)

    except:
        try:
            chrome.switch_to.default_content()

            WebDriverWait(chrome, 20).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
            WebDriverWait(chrome, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#recaptcha-anchor > div.recaptcha-checkbox-checkmark')))

            chrome.switch_to.default_content()

            verify_btn = chrome.find_element(By.TAG_NAME, "button")

            time.sleep(random.uniform(1, 3))
            verify_btn.click()

            time.sleep(5)
            chrome.quit()

            return True

        except:
            chrome.quit()
            return False

    try:
        chrome.switch_to.default_content()

        WebDriverWait(chrome, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#rc-audio > div.rc-audiochallenge-error-message')))

        fail_text = chrome.find_element(
            By.CSS_SELECTOR, '#rc-audio > div.rc-audiochallenge-error-message').text

        if len(fail_text) > 0:
            chrome.quit()
            return False

    except TimeoutException:
        chrome.switch_to.default_content()

        verify_btn = chrome.find_element(By.TAG_NAME, "button")

        time.sleep(random.uniform(1, 3))
        verify_btn.click()

        time.sleep(5)
        chrome.quit()

        return True

def generate_user_agent():
    """
    Generate a random user agent string.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
    ]
    return random.choice(user_agents)

def solve(url: str) -> None:
    solved = False

    while solved == False:
        solved = SolveCaptcha(url)

    return
solve('https://verify.poketwo.net/captcha/401365910587179028')
