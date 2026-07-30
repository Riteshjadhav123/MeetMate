# src/bot.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def join_meeting(meeting_url):
    """
    Launches a browser, navigates to the meeting URL, and joins the call.
    """
    # Path to your downloaded chromedriver, assuming it's in the root EUREKA folder
    service = Service(executable_path='chromedriver.exe') 
    
    # Set up Chrome options to handle microphone permissions
    options = webdriver.ChromeOptions()
    options.add_argument("--use-fake-ui-for-media-stream") # Auto-allows microphone
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Go to the meeting URL
        driver.get(meeting_url)
        
        print("Navigated to meeting URL. Waiting for page to load...")
        time.sleep(7) # Increased wait time for slower connections
        
        # This part clicks the "Join now" or "Ask to join" button
        try:
            # Look for a button that contains the text "Join now"
            join_button = driver.find_element(By.XPATH, '//*[contains(text(), "Join now")]')
            join_button.click()
            print("Successfully clicked 'Join now' button.")
        except Exception:
            print("Could not find 'Join now' button. Trying 'Ask to join'.")
            # Look for a button that contains the text "Ask to join"
            ask_to_join_button = driver.find_element(By.XPATH, '//*[contains(text(), "Ask to join")]')
            ask_to_join_button.click()
            print("Successfully clicked 'Ask to join' button.")

        print("Bot has joined the meeting. Holding the line...")
        
        # Keep the browser open for a long time (e.g., for a 1-hour meeting)
        # We will replace this with recording logic later.
        time.sleep(3600) 

    except Exception as e:
        print(f"An error occurred in the bot: {e}")
    finally:
        # Close the browser when done
        driver.quit()

# This part is for testing the bot directly
if __name__ == '__main__':
    test_url = "https://meet.google.com/lookup/your-test-code" # Replace with a real link for testing
    join_meeting(test_url)