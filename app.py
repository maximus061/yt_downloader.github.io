import os
from flask import Flask, request, render_template, send_file
import yt_dlp

app = Flask(__name__)

# Function to clean the input URL
def clean_url(url):
    if "youtu.be" in url:
        video_id = url.split("/")[-1].split("?")[0]
        return f"https://youtube.com/watch?v={video_id}"
    return url

# Function to download the video using yt-dlp with cookies
def download_video(url, download_path, cookies_path):
    ydl_opts = {
        'outtmpl': download_path,     # Path where the video will be saved
        'cookies': cookies_path,      # Path to the cookies.txt file
        'format': 'bestvideo+bestaudio/best',  # Best video and audio quality
        'merge_output_format': 'mp4', # Ensure output is in MP4 format
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise Exception(f"Error occurred: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form.get("url")  # Get the YouTube URL from the form
        if not original_url:
            return "Please provide a valid URL.", 400

        # Clean and process the URL
        cleaned_url = clean_url(original_url)
        print(f"Original URL: {original_url}")
        print(f"Cleaned URL: {cleaned_url}")

        # Specify paths
        download_path = os.path.join("downloads", "downloaded_video.mp4")
        cookies_path = os.path.join("cookies.txt")  # Path to your exported cookies file

        # Ensure the downloads folder exists
        os.makedirs("downloads", exist_ok=True)

        try:
            # Download the video
            download_video(cleaned_url, download_path, cookies_path)
            print(f"Downloaded to: {download_path}")
            return send_file(download_path, as_attachment=True)
        except Exception as e:
            print(f"ERROR: {e}")
            return f"An error occurred: {e}", 500

    return render_template("index.html")  # Render the HTML form for input

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
