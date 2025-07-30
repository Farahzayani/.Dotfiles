import sys
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Country code mapping
COUNTRY_CODES = {
    "tunisia": "+216",
    "morocco": "+212",
    "algeria": "+213",
    "france": "+33",
    "germany": "+49",
    "usa": "+1",
    "canada": "+1",
    "uk": "+44",
    "egypt": "+20",
    "india": "+91",
    # Add more as needed
}

# Read CLI arguments
if len(sys.argv) != 4:
    print("Usage: python script.py <country_name> <phone_number> <password>")
    sys.exit(1)

country_name = sys.argv[1].lower()
phone_number = sys.argv[2]
password = sys.argv[3]

if country_name not in COUNTRY_CODES:
    print(f"❌ Country '{country_name}' not found in database.")
    sys.exit(1)

country_code = COUNTRY_CODES[country_name]

# Appium capabilities
options = UiAutomator2Options().load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "emulator-5554",
    "appium:appPackage": "com.blockchainvault",
    "appium:appActivity": ".MainActivity",
    "appium:noReset": True,
    "appium:dontStopAppOnReset": True,
    "appium:autoGrantPermissions": True
})

driver = webdriver.Remote('http://127.0.0.1:4723', options=options)

def select_country():
    time.sleep(2)
    continue_button = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='Continue with phone number']")
    continue_button.click()
    time.sleep(5)
    print("✅ Clicked 'Continue with phone number'")

    try:
        country_dropdown = driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Country:']/following-sibling::android.view.View")
        country_dropdown.click()
        print("✅ Opened country selector.")
    except Exception as e:
        print("❌ Could not locate country dropdown.")
        print(e)
        driver.quit()
        sys.exit(1)

    try:
        input_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText"))
        )
        input_field.clear()
        input_field.send_keys(country_name.capitalize())
        time.sleep(1)

        option_xpath = f"//*[@text='{country_name.capitalize()} ({country_code})']"
        option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, option_xpath))
        )
        option.click()
        print(f"✅ Country selected: {country_name} -> {country_code}")
    except Exception as e:
        print("❌ Failed to select country from dropdown.")
        print(e)
        driver.quit()
        sys.exit(1)

def enter_phone_and_submit():
    try:
        phone_input = driver.find_element(
            AppiumBy.XPATH,
            '//android.widget.TextView[@text="Phone number:"]/following-sibling::android.view.View/android.widget.EditText'
        )
        phone_input.click()
        phone_input.clear()
        phone_input.send_keys(phone_number)
        print(f"✅ Entered phone number: {phone_number}")
    except Exception as e:
        print("❌ Could not find or enter phone number.")
        print(e)
        driver.quit()
        sys.exit(1)

    try:
        submit_button = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="Submit"]')
        submit_button.click()
        print("✅ Phone number submit button clicked.")
    except Exception as e:
        print("❌ Submit button not found or not clickable.")
        print(e)

def enter_password_and_submit():
    try:
        # Wait for password input field to appear
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.EditText'))
        )
        password_field.click()
        password_field.send_keys(password)
        print("✅ Password entered.")
    except Exception as e:
        print("❌ Could not find or enter password.")
        print(e)
        driver.quit()
        sys.exit(1)

    try:
        submit_button = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="Submit"]')
        submit_button.click()
        print("✅ Password submit button clicked.")
    except Exception as e:
        print("❌ Password Submit button not found or not clickable.")
        print(e)

# Execute flow
select_country()
enter_phone_and_submit()
time.sleep(5)
enter_password_and_submit()

time.sleep(2)
driver.quit()
print("✅ Done.")