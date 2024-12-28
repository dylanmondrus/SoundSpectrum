# SoundSpectrum
Combines web scraping, GUI automation, and signal processing to achieve the average sound score of a desired song.

SoundSpectrum is a Python-based tool that automates audio spectrum analysis by integrating Youtube scraping, GUI automation with pyautogui package and Audacity, 
and conducts Fourier analysis with the spectrum graph of the song. The user inputs a song title and artist, and the program uses Selenium to open Youtube and find a video with the inputted title. The scraper then takes the link of the video and puts it into a Youtube to mp3 website to get the mp3 file. Then pyautogui opens audacity and uses hotkeys, computer vision, and other GUI tools to automate the process of extracting the spectrum graph. The final part is uploading the graph back to python, where the data is linearized, and the frequency and decibal values are multiplied, and then averaged to produce the average dot product of the graph. 
