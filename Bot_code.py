from tkinter import filedialog, messagebox
import customtkinter as ctk
from tkinter import messagebox
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random
from selenium.webdriver.support.ui import Select
import undetected_chromedriver as uc
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
import requests
import string
from selenium.webdriver.chrome.options import Options
import os
import threading
import pandas as pd
from datetime import datetime
from seleniumwire import webdriver
import zipfile
import tkinter as tk



proxies = [
"rotating.proxyempire.io:9000:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9001:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9002:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9003:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9004:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9005:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9006:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9007:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9008:xiCHkg8CgVwtXA2i:wifi;;;;",
"rotating.proxyempire.io:9009:xiCHkg8CgVwtXA2i:wifi;;;;"
]

is_email_created = False
count = 0
def get_rental_id_and_number(api_key, activation_id):
    """
    Fetches the rental ID and phone number from the API.

    Args:
        api_key (str): The API key for authentication.
        activation_id (str): The activation ID to fetch data for.

    Returns:
        tuple: A tuple containing the rental ID and phone number, or None if the response format is unexpected.
    """
    url = f"https://daisysms.com/stubs/handler_api.php?api_key={api_key}&action=getExtraActivation&activationId={activation_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        response_text = response.text.strip()

        if response_text.startswith("ACCESS_NUMBER:"):
            _, rental_id, phone_number = response_text.split(":")
            return rental_id, phone_number
        else:
            print("Unexpected response format")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

API_KEY = "6DvCFEslwIHpySGaWFQeVepXfXTloH"


def cancel_rental(api_key,id):
    url = f"https://daisysms.com/stubs/handler_api.php?api_key={api_key}&action=setStatus&id={id}&status=8"
    try:
        # Send the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return True
    except:
        pass
    return False
def get_number(api_key):
    # Construct the URL with the provided API key
    url = f"https://daisysms.com/stubs/handler_api.php?api_key={api_key}&action=getNumber&service=go&max_price=5.5"
    
    try:
        # Send the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Process the API response
        response_text = response.text.strip()
        if response_text.startswith("ACCESS_NUMBER"):
            # Successful response with number details
            parts = response_text.split(":")
            rental_id = parts[1]
            number = parts[2]
            return rental_id, number
        elif response_text == "MAX_PRICE_EXCEEDED":
            return "Error: Max price exceeded."
        elif response_text == "NO_NUMBERS":
            return "Error: No numbers left."
        elif response_text == "TOO_MANY_ACTIVE_RENTALS":
            return "Error: Need to finish some rentals before renting more."
        elif response_text == "NO_MONEY":
            return "Error: Not enough balance left."
        else:
            return f"Unexpected response: {response_text}"

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        return f"An error occurred: {e}"
    
def get_code(api_key, rental_id):
    # Construct the URL with the provided API key and rental ID
    url = f"https://daisysms.com/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={rental_id}"
    
    try:
        # Send the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Process the API response
        response_text = response.text.strip()
        
        if response_text.startswith("STATUS_OK"):
            # Successful response with code details
            parts = response_text.split(":")
            code = parts[1]
            return f"{code}"
        elif response_text == "NO_ACTIVATION":
            return "Error: Wrong ID. No activation found."
        elif response_text == "STATUS_WAIT_CODE":
            return "Status: Waiting for SMS."
        elif response_text == "STATUS_CANCEL":
            return "Status: Rental cancelled."
        else:
            return f"Unexpected response: {response_text}"

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        return f"An error occurred: {e}"


def mark_done(api_key, rental_id):
    """
    Marks a rental as done by setting its status to 6.

    Args:
        api_key (str): The API key for authentication.
        rental_id (str): The rental ID to mark as done.

    Returns:
        str: A message indicating the result of the operation.
    """
    # Construct the URL with the provided API key and rental ID
    url = f"https://daisysms.com/stubs/handler_api.php?api_key={api_key}&action=setStatus&id={rental_id}&status=6"
    
    try:
        # Send the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Process the API response
        response_text = response.text.strip()
        
        if response_text == "ACCESS_ACTIVATION":
            return "Success: The rental was successfully marked as done."
        elif response_text == "NO_ACTIVATION":
            return "Failure: Rental ID is missing or invalid."
        else:
            return f"Unexpected response: {response_text}"

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        return f"An error occurred: {e}"
def human_typing(element, text):
    """
    Simulates human typing by sending keys one by one with random delays.
    """
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.4))  # Random delay between keystrokes

def random_delay(min_delay=1, max_delay=3):
    """
    Introduces a random delay to mimic human interactions.
    """
    time.sleep(random.uniform(min_delay, max_delay))


# Shared variable to store the selected file path
selected_file_path = None
def generate_email(first_name, last_name):
    # Random grammar options (only period or double period)
    grammar_options = ["."]
    grammar1 = random.choice(grammar_options)
    grammar2 = random.choice(grammar_options)
    
    # Random patterns for name arrangement (using the full first and last name)
    patterns = [
        f"{first_name.lower()}{grammar1}{last_name.lower()}",  # john.doe
        f"{last_name.lower()}{grammar1}{first_name.lower()}",  # doe.john
    ]
    
    # Choose a random pattern
    base_name = random.choice(patterns)
    
    # Append random numbers or letters for uniqueness (using only letters and digits)
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(2, 5)))
    
    # Combine parts with optional additional grammar and domain
    email = f"{base_name}{grammar2}{random_suffix}"
    
    return email





def normalize_date(dob):
    if isinstance(dob, pd.Timestamp):  # If it's a Timestamp object
        return dob.strftime('%d/%m/%Y')  # Convert to DD/MM/YYYY
    elif isinstance(dob, str):  # If it's a string
        try:
            # Try to parse the string as MM/DD/YYYY
            date_obj = datetime.strptime(dob, "%m/%d/%Y")
            return date_obj.strftime('%d/%m/%Y')  # Convert to DD/MM/YYYY
        except ValueError:
            # Handle invalid date formats
            print(f"Invalid date format: {dob}")
            return dob  # Return the original value if invalid
    else:
        return dob  # Return as is if not a recognized type



def parse_date(dob):
    try:
        # Try parsing the date as DD/MM/YYYY
        return datetime.strptime(dob, "%d/%m/%Y")
    except ValueError:
        try:
            # If the above fails, try parsing as MM/DD/YYYY
            return datetime.strptime(dob, "%m/%d/%Y")
        except ValueError:
            # Handle invalid date format
            print(f"Invalid date format: {dob}")
            return None


def append_or_create_txt_file(file_path, generated_password, recovery_mail, email):
    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it and add the headers (optional)
        with open(file_path, 'w') as file:
            file.write("Password, RecoveryEmail, Email\n")  # Optional header line
            file.write(f"{generated_password}, {recovery_mail}, {email}\n")
        print(f"File created: {file_path}")
    else:
        # If the file exists, append the record to the existing file
        with open(file_path, 'a') as file:
            file.write(f"{generated_password}, {recovery_mail}, {email}\n")
        print(f"Record appended to: {file_path}")


def get_proxy_parts(proxy):
    """Extract proxy parts: host, port, username, password."""
    parts = proxy.split(":")
    host = parts[0]
    port = parts[1]
    username = parts[2]
    password = parts[3]
    return host, port, username, password

def create_driver_with_proxy_and_profile(proxy):
    """Create a Selenium WebDriver with proxy and Chrome profile."""
    host, port, username, password = get_proxy_parts(proxy)
    print(f"host={host}, port={port}, username={username}, password={password}")
    

    # Updated manifest.json
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 3,
        "name": "ProxyAuth",
        "permissions": [
            "proxy",
            "webRequest",
            "webRequestAuthProvider",
            "storage",
            "declarativeNetRequest"
        ],
        "host_permissions": ["<all_urls>"],
        "background": {
            "service_worker": "background.js"
        }
    }
    """

    # Dynamically generated background.js
    background_js_template = """
    chrome.proxy.settings.set(
        {{
            value: {{
                mode: "fixed_servers",
                rules: {{
                    singleProxy: {{
                        scheme: "http",
                        host: "{host}",
                        port: {port}
                    }},
                    bypassList: []
                }}
            }},
            scope: "regular"
        }},
        function () {{}}
    );

    chrome.webRequest.onAuthRequired.addListener(
        function (details) {{
            return {{
                authCredentials: {{
                    username: "{username}",
                    password: "{password}"
                }}
            }};
        }},
        {{ urls: ["<all_urls>"] }},
        ["blocking"]
    );
    """
    background_js = background_js_template.format(
        host=host,
        port=port,
        username=username,
        password=password
    )

    # Write the extension files
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_extension(pluginfile)
    # chrome_options.add_argument(f"--user-data-dir={profile_path}")  # Load the Chrome profile

    # Initialize WebDriver
    # service = Service('C:/chromeDriver/chromedriver.exe')  # Replace with your chromedriver path
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# Example usage:
file_path = 'credentials.txt'




def show_message():
    msg_box = tk.Toplevel(root)
    msg_box.title("Trying Again with same credentials")
    msg_box.geometry("400x400")

    label = tk.Label(msg_box, text="Trying Again with same credentials....This message will close in 3 seconds.", padx=20, pady=20)
    label.pack()

    # Automatically close the window after 3000 milliseconds (3 seconds)
    msg_box.after(3000, msg_box.destroy)


driver = None
data = None
is_autmation_start = False

def submit_data():
    global driver
    global is_autmation_start
    global data
    is_autmation_start = True
    global is_email_created
    global file_path
    if not selected_file_path:
        messagebox.showerror("Error","Please select a file first")
        return
    
    
    password = password_entry.get()
    recovery_mail = recovery_mail_entry.get()
    no_of_emails = None
    
    proxy_address = str(proxy_address_entry.get()).strip()
    print(f"fetched procy = {proxy_address}")
    
    try:
        no_of_emails = int(no_of_mails_entry.get())
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Please enter a valid number of emails")
        return

    data = pd.read_excel(selected_file_path)
    for col in ['Done', 'RecoveryEmail', 'Password', 'Email']:
        if col not in data.columns:
            data[col] = ""
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce', dayfirst=True)
        data['Date'] = data['Date'].apply(normalize_date)
        
    if no_of_emails > len(data):
        no_of_emails = len(data)
    
    index = 0
    while  no_of_emails > 0:
        is_email_created = False

        no_of_emails -= 1
        row = data.iloc[index]
        if row['Done'] == 1:
            index += 1
            continue

        name = str(row['Name'])
        surname = str(row['Surname'])
        gender = str(row['Gender'])
        gender.capitalize()
        dob = row['Date']
        if isinstance(dob, pd.Timestamp):
            dob = dob.strftime('%d/%m/%Y')  # Convert to MM/DD/YYYY
        else:
            dob = str(dob)  # Ensure it's a string
        birth_date = parse_date(dob)
      

        # Extract the birth year, month, and day
        biirth_year = str(birth_date.year)
        birth_month = str(birth_date.month)
        birth_day = str(birth_date.day)

        index += 1
        # driver = uc.Chrome()
        # proxy_parts= None
        # host = port = username = password_prox = ""
        # proxy_options = None
        if proxy_address:
            try:
                parts = proxy_address.split(":")
                host = parts[0]
                port = parts[1]
                username = parts[2]
                password_p = parts[3]
            except:
                messagebox.showerror("Proxy", "Invalid proxy address")
            # print(f"if {proxy_address}")
            try:
                driver = create_driver_with_proxy_and_profile(proxy_address)
            except Exception:
                driver = uc.Chrome()
                pass
                # messagebox.showinfo("Error","Other error")
            # try:

            # except:
            #     messagebox.showinfo("Proxy","Add a valid proxy")
                # return
        else:
            driver = uc.Chrome()
        driver.maximize_window()

    

        global count
        count = 1
        is_email_created_or_not = False
        while not is_email_created_or_not:
            try:
                driver.get("http://httpbin.org/ip")
                time.sleep(2)
                # Step 1: Open Gmail website (since this is the current URL in your code)
                GMAIL_URL = "https://www.gmail.com"
                driver.get(GMAIL_URL)
                time.sleep(3)

                # Step 2: Find and click the 'Create account' button
                # create_account = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[2]/div/div/div[1]/div/button')
                create_account = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[2]/div/div/div[1]/div/button'))
    )
                create_account.click()
                time.sleep(3)

                # 
                # personal_use = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[2]/div/div/div[2]/div/ul/li[1]')
                personal_use = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[2]/div/div/div[2]/div/ul/li[1]'))
    )
                personal_use.click()
                time.sleep(3)

                first_name = name

                first_name_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="firstName"]'))
    )
            
                human_typing(first_name_input, first_name)
                time.sleep(3)
                last_name = surname

                
                last_name_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="lastName"]'))
    )
                
                human_typing(last_name_input,last_name)

                
                time.sleep(3)


                next = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="collectNameNext"]/div/button'))
    )
                next.click()

                time.sleep(3)


                year_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="year"]'))
    )
                human_typing(year_input,biirth_year)

                month_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="month"]'))
                )
                select_month = Select(month_dropdown)
                
                time.sleep(3)
                select_month.select_by_value(str(birth_month))  # Select the month by value

            
                day_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="day"]'))
    )
                time.sleep(3)
            
                day_input.clear()
                human_typing(day_input,birth_day)
                gender_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="gender"]'))
                )

                select_gender = Select(gender_dropdown)


                selected_gender = "1"
                if gender == "Male":
                    selected_gender = "1"
                elif gender == "Female":
                    selected_gender = "2"
                elif gender == "Rather not to say":
                    selected_gender = "3"
                else:
                    selected_gender = "4"
                    
                time.sleep(3)

                select_gender.select_by_value(selected_gender)  # Select by the value attribute


                time.sleep(3)


                next = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="birthdaygenderNext"]/div/button'))
    )
                next.click()
                time.sleep(5)


                is_create_own_mail = False

                try:
                    # Wait for the element to appear (maximum wait time: 10 seconds)
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div'))
                    )
                    
                    # Click the element once it appears
                    element.click()
                    is_create_own_mail = True

                    # Optionally, perform other actions after the click
                    print("Element clicked successfully.")

                except Exception as e:
                    print("Element not found or not clickable:", e)

                email = None
                if is_create_own_mail:
                    email = generate_email(name,surname)
                    # Wait for the email input field to be present
                    email_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input'))
                    )

                    # Input the generated email into the field
                    email_input.clear()  # Clear any existing text in the input field
                    # email_input.send_keys(random_email)  # Enter the random email
                    human_typing(email_input,email)


                            
            
                next = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="next"]/div/button'))
    )
                next.click()


                time.sleep(3)
                generated_password = password
                print(f"Generated Password: {generated_password}")
                password_input = None
                

                
                password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input'))
    )
                



                
                human_typing(password_input,generated_password)
                time.sleep(3)
    
                confirm_password_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input'))  # Replace with actual XPath
                )
                human_typing(confirm_password_input,generated_password)

                next = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="createpasswordNext"]/div/button'))
    )
                next.click()
                time.sleep(3)

                
                try:
                    
                    
                    # while not is_done:
                    phone_number_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="phoneNumberId"]'))  # Replace with actual XPath
                )
                    
                    is_done = False
                    id = None
                    phone_number = None
                    
                    id, phone_number = get_number(API_KEY)
                    while not is_done:
                        phone_number_input.clear()
                        human_typing(phone_number_input,f"+{phone_number}")
                        time.sleep(1)
                        next =  WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button'))
        )
                        next.click()
                        time.sleep(2)
                        try:
                            elemen = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[2]/div/div[2]/div[2]/div')
                            is_done = False
                            cancel_rental(API_KEY,id)
                            print("Canceled the rental")
                            time.sleep(1)
                            id, phone_number = get_number(API_KEY)
                            print("new number")
                            time.sleep(2)
                        except:
                            is_done = True
                    time.sleep(2)


                    # time.sleep(2)
                    is_number_not_used = False
                    text = None
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[2]/div/div[2]/div[2]/div')
            # Get the text from the element
                        text = element.text
                        is_number_not_used = True
                    except:
                        pass
                    
                    if is_number_not_used:
                        driver.quit()
                        continue    
                    is_get_code = False
                    while not is_get_code:
                        time.sleep(10)
                        code = str(get_code(API_KEY, id))  # Replace API_KEY and id with actual values
                        print(get_code)
                        if isinstance(code, str) and code[0].isdigit():
                            print("Code starts with a number, breaking the loop.")
                            is_get_code = True
                        else:
                            print(f"Received: {code}. Retrying...")
                                
                    code_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="code"]'))  # Replace with actual XPath
                )
                    
                    
                    # code_input.send_keys(code)
                    human_typing(code_input,code)
                    
                    next = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="next"]/div/button'))
    )
                    next.click()
                    time.sleep(3)

                    print(mark_done(API_KEY,id))
                    recovery_mail_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="recoveryEmailId"]'))  # Replace with actual XPath
                )

                    
                    human_typing(recovery_mail_input,recovery_mail)
                    next =  WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="recoveryNext"]/div/button'))
    )
                    next.click()
                    time.sleep(3)
                    append_or_create_txt_file(file_path,generated_password,recovery_mail,email)
                    
                    element_text = ""
                    is_new_appear = False
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[2]')
        

                        # Get the text of the element
                        element_text = element.text
                        if element_text.startswith('Google'):
                            is_new_appear = True
                        
                    
                        # is_new_appear = True
                    except Exception:
                        pass
                        
                    
                    if is_new_appear:
                        skip_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="recoverySkip"]/div/button'))
    )
                        skip_button.click()
                        time.sleep(3)

                        try:
                            next = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button'))
            )
                        
                            next.click()
                            time.sleep(4)
                        except Exception as e:
                            pass
                        
                        try:
                            click_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/div[1]/div/span/div[1]/div'))
    )
                            click_option.click()
                            time.sleep(3)
                            
                            
                        except Exception:
                            pass
                        try:
                            next = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button'))
    )
                            next.click()
                            time.sleep(3)
                        except Exception as e:
                            pass

                        try:
                            accept_all = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button'))
        )         
                            accept_all.click()
                            time.sleep(3)
                        except Exception as e:
                            pass

                        try:
                            confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button'))
        )         
                            confirm_button.click()
                            time.sleep(3)
                        except Exception as e:
                            pass
                        
                        
                        
                        try:
                            confirm_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[text()="Confirm"]'))
                        )
                            confirm_button.click()
                            time.sleep(2)
                        except Exception as e:
                            pass

                        try:
                            agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[1]/div/div/button'))
        )
                    
                            agree_button.click()
                            time.sleep(4)
                        except Exception as e:
                            pass    
                    else:
                        try:
                            next = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button'))
        )
                            next.click()
                            time.sleep(3)
                        except Exception as e:
                            pass
                        
                        try:
                            confirm_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[text()="Confirm"]'))
                        )
                            confirm_button.click()
                            time.sleep(2)
                        except Exception as e:
                            pass
                        
                        try:
                            agree_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[1]/div/div/button'))
            )
                        
                            agree_button.click()
                            time.sleep(4)
                        except Exception as e:
                            pass
                        try:
                            next = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button'))
            )
                        
                            next.click()
                            time.sleep(4)
                        except Exception as e:
                            pass

                    




                    driver.quit()
                    is_email_created = True
                    data.loc[index-1, 'Done'] = 1
                    data.loc[index-1, 'Password'] = generated_password
                    data.loc[index-1, 'RecoveryEmail'] = recovery_mail
                    data.loc[index-1, 'Email'] = email
                    is_email_created_or_not = True
                    

                    # append_or_create_txt_file(file_path,generated_password,recovery_mail,email)

            

                    # global is_email_created
                    # is_email_created = True


                    
                
                    # messagebox.showinfo("Sucessfully","Created the Mail")
                except Exception as e:
                    is_email_created = False
                    # messagebox.showerror("Failed","could not Created the Mail")
                    pass

            except Exception as e:
                # messagebox.showerror("Failed","could not Created the Mail")
                if not is_email_created:
                    driver.quit()
                # show_message()
                print(e)
        
        
    # output_path =selected_file_path.replace(".xlsx", "_updated.xlsx")
    try:
        data.to_excel(selected_file_path,index=False)
        messagebox.showinfo("Success", "Data submitted and Excel updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to save the updated Excel file.")



def stop_script():
    if is_autmation_start:
        is_autmation_start = False
        
    



def read_excel_file(filepath):
    try:
        data = pd.read_excel(filepath)
        if 'Done' in data.columns:
            print("'Done' column already exists.")
        else:
            print("'Done' column does not exist. Adding it now.")
            # Add the 'Done' column with default value 0
            data['Done'] = 0

        # Iterate over each record to update the 'Done' column
        for index, row in data.iterrows():
            print(f"Processing Record {index + 1}:")
            print(row)
            # Update the 'Done' column for the current record
            data.at[index, 'Done'] = 1

        # Save the updated DataFrame to a new file
        output_path = filepath.replace(".xlsx", "_updated.xlsx")
        data.to_excel(output_path, index=False)
        print(f"Updated file saved as: {output_path}")
        messagebox.showinfo("Success", f"File processed and saved as: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not process the file: {e}")

# Function to browse and read an Excel file
def browse_excel():
    global selected_file_path
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    if file_path:
        selected_file_path = file_path
        messagebox.showinfo("File Selected", f"Selected file: {file_path}")
    else:
        messagebox.showwarning("Warning", "No file selected.")

# Function for thread-safe submission
def submit_thread():
    global is_email_created, count
    global selected_file_path
    if selected_file_path:
        submit_data()
        if is_email_created and count != 0:
            messagebox.showinfo("Success","Emails Created")
            is_email_created = False
    else:
        messagebox.showwarning("Warning", "No file selected. Please browse a file first.")

# Main Window
root = ctk.CTk()
root.title("Interactive User Data Input")
root.geometry("700x400")
root.resizable(False, False)

# Title Label
title_label = ctk.CTkLabel(
    root,
    text="Excel File Input Form",
    font=("Arial", 20, "bold"),
)
title_label.pack(pady=20)

# Input Frame
input_frame = ctk.CTkFrame(root)
input_frame.pack(pady=10, padx=20, fill="both", expand=True)

# File Selection Button
file_browse_button = ctk.CTkButton(
    input_frame,
    text="Browse Excel File",
    command=browse_excel
)
file_browse_button.grid(row=0, column=0, columnspan=2, pady=10)

# Input Fields
fields = [
    ("Password", "Enter password"),
    ("Recovery Mail", "Enter Recovery Mail"),
    ("No of Mails", "Enter no of mails you want to process"),
    ("Proxy", "Enter Proxy Address"),
    
]
password_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter password")
recovery_mail_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter Recovery Mail")
no_of_mails_entry = ctk.CTkEntry(input_frame,placeholder_text="Enter no of mails you want to process")
proxy_address_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter Proxy Address")
entries = [password_entry, recovery_mail_entry,no_of_mails_entry,proxy_address_entry]
for i, (label_text, _) in enumerate(fields):
    ctk.CTkLabel(input_frame, text=label_text, font=("Arial", 14)).grid(row=i + 1, column=0, padx=10, pady=10, sticky="w")
    entries[i].grid(row=i + 1, column=1, padx=10, pady=10)

# Buttons Frame
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=20)

submit_button = ctk.CTkButton(
    button_frame,
    text="Submit",
    command=lambda: threading.Thread(target=submit_thread).start()
)
submit_button.grid(row=0, column=0, padx=10)

# Run the Application
root.mainloop()
