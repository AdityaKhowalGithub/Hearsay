# from flask import Flask, request, send_file, render_template, jsonify  # Import jsonify here

# import requests
# from bs4 import BeautifulSoup
# from gtts import gTTS
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
    # return render_template('index.html')

# @app.route('/summarize', methods=['POST'])
# def summarize():
    # url = request.form['url']
    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # print('soup')
    # print(soup) 
    # text = ' '.join(p.text.strip() for p in soup.find_all('p'))
    # print("Extracted Text:", text)  # Debug print to check what text is being extracted
    
    # if not text:
        # error_message = "No text found on the page to speak."
        # print(error_message)  # Optionally log this error
        # return jsonify({'error': error_message}), 400

    # tts = gTTS(text=text, lang='en')
    # audio_file = 'static/summary.mp3'
    # tts.save(audio_file)
    # return send_file(audio_file, as_attachment=True)


# if __name__ == '__main__':
    # app.run(debug=True)
from flask import Flask, request, send_file, render_template, jsonify
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from gtts import gTTS
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.form['url']

    # Setup Selenium with headless Chrome
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the JavaScript to render

        # Using Selenium to fetch the page source after JavaScript execution
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        text = ' '.join(p.text.strip() for p in soup.find_all('p'))
        print("Extracted Text:", text)  # Debug print to check what text is being extracted

        if not text:
            error_message = "No text found on the page to speak."
            print(error_message)  # Optionally log this error
            return jsonify({'error': error_message}), 400

        # Proceed if text is found
        tts = gTTS(text=text, lang='en')
        audio_file = 'static/summary.mp3'
        tts.save(audio_file)
        return send_file(audio_file, as_attachment=True)

    finally:
        driver.quit()  # Make sure to quit the driver to free resources

if __name__ == '__main__':
    app.run(debug=True)

