import mp3_webscraper
import GUI2
import fourier



def main_func():
    """
    Main function to run the entire program:
    - Scrapes MP3 files.
    - Automates GUI interactions to export spectrum data.
    - Performs Fourier analysis and collects the results.
    """
    print("Starting MP3 scraping...")
    mp3_webscraper.scrape_mp3()

    print("Automating GUI interactions...")
    GUI2.automate_gui()

    print("Performing Fourier analysis...")
    fourier.fourier_analysis()




if __name__ == "__main__":
    # Run the main function
    main_func()

