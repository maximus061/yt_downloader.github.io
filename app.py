from flask import Flask, render_template, request, send_file
import os
import logging
from urllib.parse import urlparse, parse_qs
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def clean_youtube_url(url):
    """Clean YouTube URL to get the basic video URL."""
    parsed_url = urlparse(url)
    
    # Handle youtu.be URLs
    if 'youtu.be' in parsed_url.netloc:
        video_id = parsed_url.path.lstrip('/')
        return f'https://youtube.com/watch?v={video_id}'
    
    # Handle youtube.com URLs
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            return f'https://youtube.com/watch?v={query_params["v"][0]}'
    
    return url

def download_video(url, download_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': download_path,
        'cookiesfrombrowser': ('chrome',),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            url = request.form['url']
            logger.info(f"Original URL: {url}")
            
            # Clean the URL
            cleaned_url = clean_youtube_url(url)
            logger.info(f"Cleaned URL: {cleaned_url}")
            
            # Define download path
            safe_filename = "downloaded_video.mp4"
            download_path = os.path.join(DOWNLOAD_FOLDER, safe_filename)
            
            logger.info(f"Downloading to: {download_path}")
            download_video(cleaned_url, download_path)
            
            if os.path.exists(download_path):
                logger.info("Download successful, sending file")
                return send_file(
                    download_path,
                    as_attachment=True,
                    download_name=safe_filename
                )
            else:
                logger.error("File not found after download")
                return "Download failed - file not found", 500
                
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            return f"An error occurred: {str(e)}", 500
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 