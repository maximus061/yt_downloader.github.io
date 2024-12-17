from flask import Flask, render_template, request, send_file
import os
import logging
from urllib.parse import urlparse, parse_qs
import yt_dlp

app = Flask(__name__)

# Configuration
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Functions
def clean_youtube_url(url):
    """Clean YouTube URL to get the basic video URL."""
    parsed_url = urlparse(url)
    if 'youtu.be' in parsed_url.netloc:
        video_id = parsed_url.path.lstrip('/')
        return f'https://youtube.com/watch?v={video_id}'
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            return f'https://youtube.com/watch?v={query_params["v"][0]}'
    return url

def download_video(url, output_path):
    """Download video using yt_dlp."""
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': True,
        'noprogress': True,
        'nocheckcertificate': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "Invalid URL. Please provide a valid YouTube link.", 400

        try:
            logger.info(f"Original URL: {url}")
            cleaned_url = clean_youtube_url(url)
            logger.info(f"Cleaned URL: {cleaned_url}")

            # Generate a unique filename
            video_filename = "downloaded_video.mp4"
            download_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

            # Download the video
            logger.info("Downloading video...")
            if download_video(cleaned_url, download_path):
                logger.info("Download successful.")
                return send_file(download_path, as_attachment=True, download_name=video_filename)
            else:
                return "Failed to download video. Please check the URL and try again.", 500
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return f"An error occurred: {e}", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
