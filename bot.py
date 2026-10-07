from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# ============================================================
# CONFIGURATION
# ============================================================

URL = "https://vinme.ge/"
WAIT_TIME = 30

MESSAGE = (
    "👽 👽 👽 👽 👽 👽 👽 "
    "ზუსტად ესეთი გაცნობის საიტია, "
    "ამას ბევრად ჯობია ❤️ "
    "https://gaicani.online/"
)


# ============================================================
# LOGGING
# ============================================================

def log(message):
    print(message, flush=True)


# ============================================================
# START
# ============================================================

log("🚀 BOT STARTED")


# ============================================================
# CHROMIUM OPTIONS
# ============================================================

options = Options()

options.binary_location = "/usr/bin/chromium"

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

log("🔧 Chromium options configured")


# ============================================================
# START SELENIUM
# ============================================================

try:
    log("🔧 Starting Chromium...")

    driver = webdriver.Chrome(options=options)

    log("✅ Chromium started successfully")

except Exception as e:
    log(f"❌ Chromium startup failed: {repr(e)}")
    raise


wait = WebDriverWait(driver, WAIT_TIME)


# ============================================================
# OPEN WEBSITE
# ============================================================

try:
    log("🌐 Opening vinme.ge...")

    driver.get(URL)

    log("✅ Website opened")
    log(f"📄 Title: {driver.title}")
    log(f"🔗 URL: {driver.current_url}")

except Exception as e:
    log(f"❌ Website opening failed: {repr(e)}")
    driver.quit()
    raise


# ============================================================
# START CHAT
# ============================================================

try:
    log("🔎 Looking for startButton...")

    start_button = wait.until(
        EC.presence_of_element_located(
            (By.ID, "startButton")
        )
    )

    log("🖱️ Clicking startButton...")

    driver.execute_script(
        "arguments[0].click();",
        start_button
    )

    log("✅ Start button clicked")

except Exception as e:
    log(f"❌ Start error: {repr(e)}")
    driver.quit()
    raise


# ============================================================
# WAIT FOR CHAT UI
# ============================================================

try:
    log("⏳ Waiting for chat controls...")

    wait.until(
        lambda d: (
            d.find_element(By.ID, "message").is_displayed()
        )
    )

    log("✅ Chat UI detected")

except Exception as e:
    log(f"❌ Chat UI did not appear: {repr(e)}")
    driver.quit()
    raise


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    try:

        # ----------------------------------------------------
        # FIND NEXT STRANGER
        # ----------------------------------------------------

        log("🔎 Looking for findNextButton...")

        next_button = wait.until(
            EC.presence_of_element_located(
                (By.ID, "findNextButton")
            )
        )

        log("🖱️ Clicking findNextButton...")

        driver.execute_script(
            "arguments[0].click();",
            next_button
        )

        log("🔄 Next stranger requested")


        # ----------------------------------------------------
        # WAIT FOR MESSAGE INPUT TO BECOME ENABLED
        # ----------------------------------------------------

        log("⏳ Waiting for message box to become enabled...")

        wait.until(
            lambda d: (
                d.find_element(By.ID, "message").is_enabled()
            )
        )

        msg_box = driver.find_element(
            By.ID,
            "message"
        )

        log("✅ Message box is enabled")


        # ----------------------------------------------------
        # WAIT FOR SEND BUTTON TO BECOME ENABLED
        # ----------------------------------------------------

        log("⏳ Waiting for submit button to become enabled...")

        wait.until(
            lambda d: (
                d.find_element(By.ID, "submit").is_enabled()
            )
        )

        send_button = driver.find_element(
            By.ID,
            "submit"
        )

        log("✅ Submit button is enabled")


        # ----------------------------------------------------
        # INSERT MESSAGE
        # ----------------------------------------------------

        log("📝 Inserting message...")

        driver.execute_script(
            """
            const input = arguments[0];
            const text = arguments[1];

            const setter =
                Object.getOwnPropertyDescriptor(
                    HTMLInputElement.prototype,
                    'value'
                )?.set ||
                Object.getOwnPropertyDescriptor(
                    HTMLTextAreaElement.prototype,
                    'value'
                )?.set;

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
            MESSAGE
        )

        log("✅ Message inserted")


        # ----------------------------------------------------
        # VERIFY VALUE
        # ----------------------------------------------------

        current_value = msg_box.get_attribute("value")

        log(
            f"📝 Message field contains: "
            f"{current_value[:50] if current_value else 'EMPTY'}"
        )


        # ----------------------------------------------------
        # SEND
        # ----------------------------------------------------

        log("📤 Clicking submit...")

        send_button.click()

        log("✅ Message sent")


        # ----------------------------------------------------
        # WAIT
        # ----------------------------------------------------

        time.sleep(2)


    # ========================================================
    # TIMEOUT
    # ========================================================

    except TimeoutException as e:

        log("⏰ Timeout waiting for chat controls")

        try:
            message_enabled = driver.find_element(
                By.ID,
                "message"
            ).is_enabled()

            submit_enabled = driver.find_element(
                By.ID,
                "submit"
            ).is_enabled()

            log(
                f"🔍 Debug: "
                f"message_enabled={message_enabled}, "
                f"submit_enabled={submit_enabled}"
            )

        except Exception as debug_error:
            log(
                f"⚠️ Debug error: "
                f"{repr(debug_error)}"
            )

        time.sleep(3)

        continue


    # ========================================================
    # OTHER ERRORS
    # ========================================================

    except Exception as e:

        log(f"⚠️ LOOP ERROR: {repr(e)}")

        time.sleep(3)

        continue
