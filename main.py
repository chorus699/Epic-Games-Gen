import time
import os
import random
import string
import requests
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

def get_proxy():
    with open('proxy.txt', 'r') as file:
        proxy_line = file.readline().strip()
    if proxy_line:
        proxy_parts = proxy_line.split(":")
        if len(proxy_parts) == 4:
            return {
                'host': proxy_parts[0],
                'port': proxy_parts[1],
                'username': proxy_parts[2],
                'password': proxy_parts[3]
            }
    return None


def display_banner():
    banner = r"""
 ____  ____  ____  _      ____    _____  ____  ____  _    
/  __\/  __\/  _ \/ \__/|/  _ \  /__ __\/  _ \/  _ \/ \   
|  \/||  \/|| / \|| |\/||| / \|    / \  | / \|| / \|| |   
|  __/|    /| \_/|| |  ||| \_/|    | |  | \_/|| \_/|| |_/\ 
\_/   \_/\_\\____/\_/  \|\____/    \_/  \____/\____/\____/  V3
                                                          
"""
    print(Fore.CYAN + banner)

os.system("cls" if os.name == "nt" else "clear")
os.system("title 𝙴𝚙𝚒𝚌𝙶𝚊𝚖𝚎𝚜 𝚃𝚘𝚘𝚕 V3/ 𝐃𝐢𝐬𝐜𝐨𝐫𝐝: chorus_699")
display_banner()

API_BASE_URL = "https://api.tempmail.lol/v2"


def create_temp_email():
    url = f"{API_BASE_URL}/inbox/create"
    try:
        response = requests.post(url)
        if response.status_code == 201:  # HTTP Created
            data = response.json()
            email = data.get("address")
            token = data.get("token")
            print(Fore.GREEN + f"✅ Temporary Email Created: {email}")
            return email, token
        else:
            print(Fore.RED + f"❌ Failed to create temporary email. Response: {response.text}")
            return None, None
    except requests.RequestException as e:
        print(Fore.RED + f"❌ Error creating email: {e}")
        return None, None

def check_inbox(token):
    url = f"{API_BASE_URL}/inbox"
    params = {"token": token}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data.get("emails"):
                print(Fore.YELLOW + "📭 Inbox is empty.")
                return []
            else:
                return data["emails"]
        else:
            print(Fore.RED + f"❌ Failed to check inbox. Response: {response.text}")
            return []
    except requests.RequestException as e:
        print(Fore.RED + f"❌ Error checking inbox: {e}")
        return []

def save_email_html(email_data, idx):
    html_content = email_data.get("html", "No HTML content available")
    filename = f"htmlcode_{idx}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(Fore.GREEN + f"✅ HTML content saved to {filename}")
    return filename 

def extract_otp_from_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        otp_match = re.search(r'<tr>\s*<td[^>]*?>\s*(\d+)\s*<br>', html_content)

        # Extract and print the OTP if found
        if otp_match:
            otp = otp_match.group(1)
            print(Fore.CYAN + f"🔑 OTP Extracted: {otp}")
            return otp
        else:
            print(Fore.RED + "❌ No OTP found in the file.")
            return None
    except FileNotFoundError:
        print(Fore.RED + f"❌ File {file_path} not found.")
    except Exception as e:
        print(Fore.RED + f"❌ An error occurred: {e}")
        return None

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(Fore.GREEN + f"✅ File {file_path} deleted successfully.")
    except Exception as e:
        print(Fore.RED + f"❌ Error deleting file {file_path}: {e}")

def save_email_token(email, token):
    with open("saved.txt", "a", encoding="utf-8") as file:
        file.write(f"Email: {email}, Token: {token}\n")
    print(Fore.GREEN + f"✅ Email and Token saved to saved.txt.")

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length))

def input_verification_code(driver, code):

    for i in range(6):
        input_field = driver.find_element(By.NAME, f"code-input-{i}")
        input_field.clear()
        input_field.send_keys(code[i]) 
def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def extract_promo_link_from_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        promo_link_pattern = r'link="([^"]+)"'
        match = re.search(promo_link_pattern, html_content)
        if match:
            link = match.group(1)
            print(Fore.CYAN + f"🔗 Promo Link Found: {link}")
            return link
        else:
            print(Fore.RED + "❌ No promo link found in the HTML content.")
            return None
    except FileNotFoundError:
        print(Fore.RED + f"❌ File {file_path} not found.")
        return None
    except Exception as e:
        print(Fore.RED + f"❌ Error extracting promo link: {e}")
        return None
    proxy = get_proxy()
proxy = get_proxy()
if not proxy:
    print("No proxy found in proxy.txt. Exiting.")
    exit()
print(Fore.CYAN + "                                 -- > Automated EpicGames Promo Maker (V3)") 
print(Fore.CYAN + "                                -- > Features : Emails solver / promo fetcher / proxies") 
print(Fore.RED + "                                    ") 
print(Fore.RED + "                                    ") 
print(Fore.RED + "                                    ")  
print(Fore.RED + "                                    ") 

options = uc.ChromeOptions()
proxy_auth = f"{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
options.add_argument(f"--proxy-server=http://{proxy['host']}:{proxy['port']}")
    

driver = uc.Chrome(options=options)
driver.get('https://www.epicgames.com/id/register/date-of-birth?lang=en-US&redirect_uri=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2Fp%2Fdiscord--discord-nitro&client_id=875a3b57d3a640a6b7f9b4e883463ab4')
print(Fore.GREEN + f"({get_current_time()})          |    Loaded Email Address")
wait = WebDriverWait(driver, 10)
month_element = wait.until(EC.element_to_be_clickable((By.ID, "month")))
month_element.click()
jan_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@data-value='0']//span[contains(text(), 'Jan')]")))
jan_item.click()
day_element = wait.until(EC.element_to_be_clickable((By.ID, "day")))
day_element.click()
day_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@data-value='2']//span[contains(text(), '2')]")))
day_item.click()
year_input = wait.until(EC.element_to_be_clickable((By.ID, "year")))
year_input.clear() 
year_input.send_keys("1971")  
continue_button = wait.until(EC.element_to_be_clickable((By.ID, "continue")))
continue_button.click()
email, token = create_temp_email()
if email and token:
    print(Fore.YELLOW + f"({get_current_time()})          |   Using Temporary Email: {email}")
    email_input = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    email_input.clear() 
    email_input.send_keys(email)
    
    name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='name']")))
    last_name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='lastName']")))
    name_input.clear()
    name_input.send_keys("chorus")
    last_name_input.clear()
    last_name_input.send_keys("chorus")
    
    display_name = generate_random_string()
    display_name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='displayName']")))
    display_name_input.clear()
    display_name_input.send_keys(display_name)
    
    password_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='password']")))
    password_input.clear()
    password_input.send_keys(email)

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btn-submit']")))
    submit_button.click()

    print(Fore.RED + f"({get_current_time()})          |   Please solve CAPTCHA manually") 
    idx = 1
    otp_verified = False
    
    while not otp_verified:
        print(Fore.BLUE + f"🔍 Checking inbox for OTP at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        emails = check_inbox(token)

        if emails:
            for email_data in emails:
                file_path = save_email_html(email_data, idx)
                otp = extract_otp_from_html(file_path)
                if otp:
                    input_verification_code(driver, otp)
                    verify_email_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='continue'][@aria-label='Verify email']")))
                    verify_email_button.click() 

                    print(Fore.GREEN + "✅ Email Verified Successfully!")
                    delete_file(file_path)
                    save_email_token(email, token)
                    
                    otp_verified = True
                    break
        time.sleep(5) 
    

    time.sleep(7)
    

    add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='add-to-cart-cta-button']")))
    add_to_cart_button.click()
    print(Fore.GREEN + "✅ 'Add To Cart' button clicked.")
    

    driver.get("https://store.epicgames.com/en-US/p/discord")
    print(Fore.GREEN + "✅ Redirected to Discord store page.")
    time.sleep(2)

    get_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='purchase-cta-button']")))
    get_button.click()
    print(Fore.GREEN + "✅ 'Get' button clicked.")


    checkbox_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='checkbox'][@aria-checked='false']")))
    checkbox_button.click()
    print(Fore.GREEN + "✅ Checkbox clicked.")
 
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='eds_14hl3lj9 eds_14hl3ljb eds_14hl3ljh eds_1ypbntdc eds_14hl3lja eds_14hl3lj2'][span//text()='Accept']")))
    accept_button.click()
    print(Fore.GREEN + "✅ 'Accept' button clicked.")

    time.sleep(30)

    driver.get("https://store.epicgames.com/en-US/cart/")
    print(Fore.GREEN + "✅ Redirected to Discord store page.")


    checkout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='eds_14hl3lj9 eds_14hl3ljb eds_14hl3ljh eds_1ypbntdc eds_14hl3lja eds_14hl3lj2'][span//text()='Check Out']")))
    checkout_button.click()
    print(Fore.GREEN + "✅ 'Check Out' button clicked.")


    # Promo link checking loop
    while otp_verified:
        print(Fore.BLUE + f"🔍 Checking inbox for new emails at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        emails = check_inbox(token)
        if emails:
            for email_data in emails:
                print(Fore.GREEN + "New email found!")
                file_path = save_email_html(email_data, idx)
                idx += 1 
                promo_link = extract_promo_link_from_html(file_path)
                if promo_link:
                    with open("promo.txt", "a", encoding="utf-8") as promo_file:
                        promo_file.write(f"{promo_link}\n")
                    print(Fore.GREEN + f"✅ Promo link saved to promo.txt.")

        time.sleep(10)

    driver.quit()
else:
    print(Fore.RED + "❌ Unable to proceed. Failed to create a temporary email.")


