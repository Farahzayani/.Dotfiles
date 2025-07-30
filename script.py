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
    # add more if needed
}

# Read CLI arguments
if len(sys.argv) != 3:
    print("Usage: python script.py <country_name> <phone_number>")
    sys.exit(1)

country_name = sys.argv[1].lower()
phone_number = sys.argv[2]

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

# Step 1: Select Country
def select_country():
    time.sleep(2)
    continue_button = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='Continue with phone number']")
    continue_button.click()
    time.sleep(5)
    print("✅ Clicked 'Continue with phone number'")

    # Locate and click the country dropdown element instead of hardcoded tap
    try:
        country_dropdown = driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Country:']/following-sibling::android.view.View")
        country_dropdown.click()
        print("✅ Opened country selector.")
    except Exception as e:
        print("❌ Could not locate country dropdown.")
        print(e)
        driver.quit()
        sys.exit(1)

    # Type country name or code into the input field
    try:
        input_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText"))
        )
        input_field.clear()
        input_field.send_keys(country_name.capitalize())
        time.sleep(1)

        # Click the matched result
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

# Step 2: Enter phone number and submit
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

    # Submit
    try:
        submit_button = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="Submit"]')
        submit_button.click()
        print("✅ Submit button clicked.")
    except Exception as e:
        print("❌ Submit button not found or not clickable.")
        print(e)

# Run everything
select_country()
enter_phone_and_submit()

time.sleep(2)
driver.quit()
print("✅ Done.")