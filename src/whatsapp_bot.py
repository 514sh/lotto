from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class WhatsAppBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=C:/Users/mjmba/AppData/Local/Google/Chrome/User Data/Default/Cookies")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) 
        self.driver.get("https://web.whatsapp.com/")
        self.wait = WebDriverWait(self.driver, 100)


    # def wait_for_login(self):
    #     input("Log in to WhatsApp Web and press Enter once logged in...")
    #     time.sleep(2)

    def send_messages_from_file(self, contact_name, file_path):
        try:
            x_arg = '//span[contains(@title,' + contact_name + ')]'
            contact_title = self.wait.until(EC.presence_of_element_located((
                By.XPATH, x_arg)))
            contact_title.click()

            inp_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
            message_box = self.wait.until(EC.presence_of_element_located((
                By.XPATH, inp_xpath)))
            # Read and send messages from the file
            with open(file_path, "r", encoding="utf-8") as file:
                messages = file.readlines()
                print(messages)
                for message in messages:
                    message = message.strip()
                    message_box.send_keys(message)
                    message_box.send_keys(Keys.SHIFT, Keys.ENTER)
            time.sleep(1)
            message_box.send_keys(Keys.ENTER)
            time.sleep(1)
            print("Messages sent successfully!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def close(self):
        # Close the Chrome WebDriver
        self.driver.quit()

# Example usage:
if __name__ == "__main__":
    whatsapp_bot = WhatsAppBot()
    contact_name = '"Mcmc"'
    file_path = "kabo/09-14-2023-kabo-laban_bryan.txt"  # Replace with the path to your message file
    whatsapp_bot.send_messages_from_file(contact_name, file_path)
    whatsapp_bot.close()




