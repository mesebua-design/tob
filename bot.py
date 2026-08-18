from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()

# Chromium installed by Dockerfile
options.binary_location = "/usr/bin/chromium"

# Headless server settings
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("http://vinme.ge/")

# Start
try:
    start_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "startButton"))
    )
    start_btn.click()
    print("✅ Started")
except Exception as e:
    print("❌ Start error:", e)


while True:
    try:
        # Find next stranger
        next_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "findNextButton"))
        )
        next_btn.click()
        print("🔄 Next stranger")

        # Get message box
        msg_box = wait.until(
            EC.presence_of_element_located((By.ID, "message"))
        )

        # Get send button
        send_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "submit"))
        )

        message = "👽 👽 👽 👽 👽 👽 👽 ზუსტად ესეთი გაცნობის საიტია, ამას ბევრად ჯობია ❤️ https://gaicani.online/"

        # Insert Unicode text using JavaScript
        driver.execute_script("""
            const input = arguments[0];
            const text = arguments[1];

            const setter = Object.getOwnPropertyDescriptor(
                HTMLInputElement.prototype,
                'value'
            )?.set || Object.getOwnPropertyDescriptor(
                HTMLTextAreaElement.prototype,
                'value'
            )?.set;

            if (setter) {
                setter.call(input, text);
            } else {
                input.value = text;
            }

            input.dispatchEvent(
                new Event('input', { bubbles: true })
            );

            input.dispatchEvent(
                new Event('change', { bubbles: true })
            );
        """, msg_box, message)

        # Click send
        send_btn.click()

        print("✅ Message sent")

    except Exception as e:
        print("⚠️ Error:", e)
        continue
