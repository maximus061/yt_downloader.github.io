   import os
   from flask import Flask, render_template, request, send_file
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

   # ... existing code ...

   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       app.run(host='0.0.0.0', port=port)