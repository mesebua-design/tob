from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# ============================================================
# BOT START
# ============================================================

print("🚀 BOT STARTED", flush=True)


# ============================================================
# CHROMIUM CONFIGURATION
# ============================================================

options = Options()

# Chromium installed by Dockerfile
options.binary_location = "/usr/bin/chromium"

# Render / Docker settings
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

print("🔧 Chromium options configured", flush=True)


# ============================================================
# START SELENIUM
# ============================================================

try:
    print("🔧 Starting Chromium...", flush=True)

    driver = webdriver.Chrome(options=options)

    print("✅ Chromium started successfully", flush=True)

except Exception as e:
    print("❌ Chromium startup failed:", repr(e), flush=True)
    raise


# ============================================================
# WAIT CONFIGURATION
# ============================================================

wait = WebDriverWait(driver, 15)

print("✅ WebDriverWait configured", flush=True)


# ============================================================
# OPEN WEBSITE
# ============================================================

try:
    print("🌐 Opening vinme.ge...", flush=True)

    driver.get("http://vinme.ge/")

    print("✅ vinme.ge opened", flush=True)

except Exception as e:
    print("❌ Failed to open vinme.ge:", repr(e), flush=True)
    driver.quit()
    raise


# ============================================================
# PRINT PAGE INFORMATION
# ============================================================

try:
    print("📄 Page title:", driver.title, flush=True)
    print("🔗 Current URL:", driver.current_url, flush=True)

except Exception as e:
    print("⚠️ Could not read page information:", repr(e), flush=True)


# ============================================================
# CLICK START BUTTON
# ============================================================

try:
    print("🔎 Looking for startButton...", flush=True)

    start_btn = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "startButton")
        )
    )

    print("🖱️ Clicking startButton...", flush=True)

    start_btn.click()

    print("✅ Started", flush=True)

except Exception as e:
    print("❌ Start button error:", repr(e), flush=True)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    try:
        # --------------------------------------------------------
        # FIND NEXT STRANGER
        # --------------------------------------------------------

        print("🔎 Looking for findNextButton...", flush=True)

        next_btn = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "findNextButton")
            )
        )

        print("🖱️ Clicking findNextButton...", flush=True)

        next_btn.click()

        print("🔄 Next stranger", flush=True)

        # Give the website some time to load the new chat
        time.sleep(1)


        # --------------------------------------------------------
        # FIND MESSAGE BOX
        # --------------------------------------------------------

        print("🔎 Looking for message box...", flush=True)

        msg_box = wait.until(
            EC.presence_of_element_located(
                (By.ID, "message")
            )
        )

        print("✅ Message box found", flush=True)


        # --------------------------------------------------------
        # FIND SEND BUTTON
        # --------------------------------------------------------

        print("🔎 Looking for submit button...", flush=True)

        send_btn = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "submit")
            )
        )

        print("✅ Send button found", flush=True)


        # --------------------------------------------------------
        # MESSAGE
        # --------------------------------------------------------

        message = (
            "👽 👽 👽 👽 👽 👽 👽 "
            "ზუსტად ესეთი გაცნობის საიტია, "
            "ამას ბევრად ჯობია ❤️ "
            "https://gaicani.online/"
        )

        print("📝 Preparing message...", flush=True)


        # --------------------------------------------------------
        # INSERT MESSAGE USING JAVASCRIPT
        # --------------------------------------------------------

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

        print("✅ Message inserted", flush=True)


        # --------------------------------------------------------
        # CLICK SEND
        # --------------------------------------------------------

        print("🖱️ Clicking send...", flush=True)

        send_btn.click()

        print("✅ Message sent", flush=True)


        # --------------------------------------------------------
        # WAIT BEFORE NEXT ITERATION
        # --------------------------------------------------------

        time.sleep(1)


    except Exception as e:

        print("⚠️ LOOP ERROR:", repr(e), flush=True)

        # Don't kill the whole worker.
        # Wait briefly and try again.
        time.sleep(2)

        continue
