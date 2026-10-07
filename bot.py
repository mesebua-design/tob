while True:
    try:
        # Find next
        next_button = driver.find_element(By.ID, "findNextButton")
        driver.execute_script("arguments[0].click();", next_button)

        # Wait only until chat becomes usable
        wait.until(
            lambda d:
            d.find_element(By.ID, "message").is_enabled()
            and d.find_element(By.ID, "submit").is_enabled()
        )

        msg_box = driver.find_element(By.ID, "message")
        send_button = driver.find_element(By.ID, "submit")

        # Insert immediately
        driver.execute_script("""
            const input = arguments[0];
            const text = arguments[1];

            const setter =
                Object.getOwnPropertyDescriptor(
                    HTMLInputElement.prototype,
                    'value'
                ).set;

            setter.call(input, text);

            input.dispatchEvent(
                new Event('input', {bubbles: true})
            );
            input.dispatchEvent(
                new Event('change', {bubbles: true})
            );
        """, msg_box, MESSAGE)

        # Send immediately
        send_button.click()

        print("✅ Sent", flush=True)

    except TimeoutException:
        print("⏳ Match took too long, trying again...", flush=True)
        continue

    except Exception as e:
        print("⚠️", repr(e), flush=True)
        time.sleep(0.5)
