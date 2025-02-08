import os
import logging
from flask import Flask, send_file

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return send_file('index.html') # Serve index.html from root

def run_app():
    logger.info("Starting Flask app...") # Log app start
    current_working_directory = os.getcwd()
    logger.info(f"Current working directory: {current_working_directory}")
    logger.info("Listing files in current directory:")
    files_in_dir = os.listdir('.') # List files in current directory
    for file in files_in_dir:
        logger.info(f"- {file}")

    app.run(debug=True, port=8080, host='0.0.0.0')

if __name__ == '__main__':
    run_app()