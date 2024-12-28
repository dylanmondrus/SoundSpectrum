from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time


def scrape_mp3():
    """
    Automates the process of finding and downloading an MP3 file for a given song.
    - Searches YouTube for the song and artist.
    - Extracts the first matching video link.
    - Downloads the MP3 from a YouTube-to-MP3 converter site.
    """
    try:
        # Set up WebDriver
        driver = webdriver.Chrome()

        # Get user input
        user_song = input("Enter your initial song: ").title()
        user_artist = input("Enter the artist: ").title()
        user_track = f"{user_song} by {user_artist} lyrics"

        print(f"Searching for: {user_track}")
        driver.get("https://www.youtube.com/")

        # Search for the song on YouTube
        search = driver.find_element(By.NAME, "search_query")
        search.send_keys(user_track)
        search.send_keys(Keys.RETURN)
        time.sleep(5)

        # Extract video links from search results
        search_results_links = driver.find_elements(By.TAG_NAME, "a")
        hrefs = [link.get_attribute("href") for link in search_results_links if link.get_attribute("href")]
        hrefs = [href for href in hrefs if "www.youtube.com/watch?" in href]

        # Find the first matching video
        first_link = None
        count = 0
        for href in hrefs:
            driver.get(href)
            page_title = driver.title
            print(f"Checking video: {page_title}")
            count += 1
            if user_song in page_title:
                first_link = href
                print(f"Match found: {href}")
                break
            if count > 5:  # Limit iterations to avoid excessive loading
                print("No match found within the first 5 videos.")
                break

        # If a matching video is found, download the MP3
        if first_link:
            print("Navigating to MP3 converter...")
            driver.get("https://ytmp3.la/unLf/")

            # Enter video URL and initiate conversion
            try:
                mp3search = driver.find_element(By.ID, "video")
                mp3search.send_keys(first_link)
                mp3search.send_keys(Keys.RETURN)
                time.sleep(15)

                # Wait for the download button and click
                print("Waiting for the download button...")
                button = driver.find_element(By.XPATH, '//button[@type="button" and text()="Download"]')
                while not button.is_enabled():
                    print("Button not ready, waiting...")
                    time.sleep(60)
                    button = driver.find_element(By.XPATH, '//button[@type="button" and text()="Download"]')
                button.click()
                print("Download initiated.")
                time.sleep(5)

            except NoSuchElementException:
                print("Error: Unable to locate the download button.")
        else:
            print("No matching video found. Exiting.")

    except WebDriverException as e:
        print(f"WebDriver error: {e}")

    finally:
        # Ensure the WebDriver is closed properly
        print("Closing the browser.")
        driver.quit()


