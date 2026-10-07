from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time


# ============================================================
# CONFIG
# ============================================================

URL = "https://vinme.ge/"
WAIT_TIME = 10

MESSAGE = (
    "👽 👽 👽 👽 👽 👽 👽 "
    "ზუსტად ესეთი გაცნობის საიტია, "
    "ამას ბევრად ჯობია ❤️ "
    "https://gaicani.online/"
)


def log(message):
    print(message, flush=True)


# ============================================================
# CHROMIUM
# ============================================================

log("🚀 BOT STARTED")

options = Options()

options.binary_location = "/usr/bin/chromium"

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Performance
options.add_argument("--disable-extensions")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-sync")
options.add_argument("--disable-translate")
options.add_argument("--disable-default-apps")
options.add_argument("--no-first-run")

log("🔧 Starting Chromium...")

try:
    driver = webdriver.Chrome(options=options)
    log("✅ Chromium started")

except Exception as e:
    log(f"❌ Chromium startup failed: {repr(e)}")
    raise


wait = WebDriverWait(
    driver,
    WAIT_TIME,
    poll_frequency=0.1
)


# ============================================================
# OPEN VINME
# ============================================================

try:

    log("🌐 Opening vinme.ge...")

    driver.get(URL)

    log("✅ Website opened")
    log(f"📄 Title: {driver.title}")
    log(f"🔗 URL: {driver.current_url}")

except Exception as e:

    log(f"❌ Website error: {repr(e)}")

    driver.quit()

    raise


# ============================================================
# START
# ============================================================

try:

    log("🔎 Looking for startButton...")

    start_button = wait.until(
        lambda d: d.find_element(
            By.ID,
            "startButton"
        )
    )

    log("🖱️ Starting chat...")

    driver.execute_script(
        "arguments[0].click();",
        start_button
    )

    log("✅ Chat started")

except Exception as e:

    log(f"❌ Start error: {repr(e)}")

    driver.quit()

    raise


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    try:

        # ----------------------------------------------------
        # FIND NEXT
        # ----------------------------------------------------

        log("🔎 Finding next stranger...")

        next_button = wait.until(
            lambda d: d.find_element(
                By.ID,
                "findNextButton"
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            next_button
        )

        log("🔄 Searching...")


        # ----------------------------------------------------
        # WAIT FOR CHAT TO BECOME READY
        # ----------------------------------------------------

        log("⏳ Waiting for chat...")

        wait.until(
            lambda d: (
                d.find_element(
                    By.ID,
                    "message"
                ).is_enabled()
                and
                d.find_element(
                    By.ID,
                    "submit"
                ).is_enabled()
            )
        )

        log("✅ Chat ready")


        # ----------------------------------------------------
        # GET ELEMENTS
        # ----------------------------------------------------

        message_box = driver.find_element(
            By.ID,
            "message"
        )

        submit_button = driver.find_element(
            By.ID,
            "submit"
        )


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
                    "value"
                ).set;

            setter.call(input, text);

            input.dispatchEvent(
                new Event("input", {
                    bubbles: true
                })
            );

            input.dispatchEvent(
                new Event("change", {
                    bubbles: true
                })
            );
            """,
            message_box,
            MESSAGE
        )


        # ----------------------------------------------------
        # SEND
        # ----------------------------------------------------

        log("📤 Sending...")

        driver.execute_script(
            "arguments[0].click();",
            submit_button
        )

        log("✅ MESSAGE SENT")


        # ----------------------------------------------------
        # VERY SHORT DELAY
        # ----------------------------------------------------

        time.sleep(0.2)


    # ========================================================
    # CHAT TIMEOUT
    # ========================================================

    except TimeoutException:

        log(
            "⏰ Chat did not become ready "
            "within the timeout. Retrying..."
        )

        continue


    # ========================================================
    # OTHER ERROR
    # ========================================================

    except Exception as e:

        log(f"⚠️ LOOP ERROR: {repr(e)}")

        time.sleep(0.5)

        continue
