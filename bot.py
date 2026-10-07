from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# =========================
# Chrome / Chromium options
# =========================

options = Options()

# Chromium installed by Docker
options.binary_location = "/usr/bin/chromium"

# Headless server settings
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")


# =========================
# Start browser
# =========================

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


# =========================
# Open website
# =========================

driver.get("http://vinme.ge/")

print("🌐 Website opened")


# =========================
# Click Start
# =========================

try:
    start_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "startButton"))
    )

    start_btn.click()

    print("✅ Started")

except Exception as e:
    print("❌ Start error:", e)


# =========================
# Main loop
# =========================

while True:

    try:

        # Find next stranger
        next_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "findNextButton"))
        )

        next_btn.click()

        print("🔄 Next stranger")

        # Wait a little for the new chat to load
        time.sleep(1)


        # =========================
        # Find message box
        # =========================

        msg_box = wait.until(
            EC.presence_of_element_located(
                (By.ID, "message")
            )
        )


        # =========================
        # Find send button
        # =========================

        send_btn = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "submit")
            )
        )


        # =========================
        # Message
        # =========================

        message = (
            "👽 👽 👽 👽 👽 👽 👽 "
            "ზუსტად ესეთი გაცნობის საიტია, "
            "ამას ბევრად ჯობია ❤️ "
            "https://gaicani.online/"
        )


        # =========================
        # Insert Unicode text
        # =========================

        driver.execute_script(
            """
            const input = arguments[0];
            const text = arguments[1];

            const inputSetter =
                Object.getOwnPropertyDescriptor(
                    HTMLInputElement.prototype,
                    'value'
                )?.set;

            const textareaSetter =
                Object.getOwnPropertyDescriptor(
                    HTMLTextAreaElement.prototype,
                    'value'
                )?.set;

            const setter =
                inputSetter || textareaSetter;

            if (setter) {
                setter.call(input, text);
            } else {
                input.value = text;
            }

            input.dispatchEvent(
                new Event('input', {
                    bubbles: true
                })
            );

            input.dispatchEvent(
                new Event('change', {
                    bubbles: true
                })
            );
            """,
            msg_box,
            message
        )


        # =========================
        # Send message
        # =========================

        send_btn.click()

        print("✅ Message sent")


        # Small delay before next iteration
        time.sleep(1)


    except Exception as e:

        print("⚠️ Error:", e)

        # Continue to the next iteration
        continue
