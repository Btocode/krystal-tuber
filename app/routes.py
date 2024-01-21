from math import isnan
from flask import Blueprint, jsonify, request, send_file
from pytube import YouTube
from flask_cors import CORS
import json
import os 
import threading

bp = Blueprint("main", __name__)
CORS(
    bp,
    origins=["http://localhost:3000", "https://youtube-downloader-frontend.vercel.app"],
    methods=["GET", "POST"],
    supports_credentials=True
    
)


def get_video_and_audio_streams(url):
    yt = YouTube(url)
    
    info = {
        "title": yt.title,
        "thumbnail_url": yt.thumbnail_url,
        "length": yt.length,
        "author": yt.author,
    }
    
    audio_streams = []
    video_streams = []

    try:
        audio_streams = yt.streams.filter(only_audio=True)
    except Exception as e:
        audio_streams = []

    try:
        video_streams = yt.streams.filter(progressive=True)
    except Exception as e:
        video_streams = []
        
    

    return audio_streams, video_streams, info

def delete_file_after_delay(file_path, delay):
    def delete_file():
        try:
            # Wait for the specified delay
            threading.Event().wait(delay)

            # Delete the file
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {e}")

    # Start a new thread for the deletion task
    threading.Thread(target=delete_file, daemon=True).start()

@bp.route('/', methods=['GET'])
def health_check():
    return jsonify({"success": True}), 200

@bp.route('/suggest_formats', methods=['POST'])
def suggest_formats():
    data = request.get_json()

    if 'url' not in data:
        return jsonify({"error": "Please provide a 'url' parameter in the request"}), 400

    url = data['url']
    audio_streams, video_streams, info = get_video_and_audio_streams(url)
        

    if len(audio_streams) == 0 and len(video_streams) == 0:
        return jsonify({"error": "No streams found"}), 404

    response = {
        "info": info,
        "formats": {
            "audio": [stream.abr for stream in audio_streams if stream.abr is not None],
            "video": [stream.resolution for stream in video_streams]
        }
    }
    
    with open('/tmp/formats.json', 'w') as f:
        json.dump(response, f)
        
    
    

    return jsonify(response), 200

@bp.route('/download', methods=['POST'])
def download():
    data = request.get_json()

    if 'url' not in data or 'quality' not in data:
        return jsonify({"error": "Please provide 'url' and 'quality' parameters in the request"}), 400

    url = data['url']
    quality = data['quality']

    yt = YouTube(url)

    stream_to_download = None
    is_audio = False
    
    with open('formats.json', 'r') as f:
        formats = json.load(f)
        audio_formats = formats['formats']['audio']
        video_formats = formats['formats']['video']
        
        if quality in audio_formats:
            is_audio = True
            stream_to_download = yt.streams.filter(only_audio=True, abr=quality).first()
        elif quality in video_formats:
            is_audio = False
            stream_to_download = yt.streams.filter(progressive=True, resolution=quality).first()
        else:
            return jsonify({"error": f"No matching stream found for quality: {quality}"}), 404
        
        
    if stream_to_download:
        file_name = stream_to_download.default_filename
        # Define the directory where you want to save the file
        tmp_directory = '/tmp'

        # Construct the full path for the file in the /tmp directory
        file_path = os.path.join(tmp_directory, file_name)

        # Download the file to the specified path
        stream_to_download.download(output_path=tmp_directory, filename=file_name)

        suggested_filename = f"{file_name}.mp3" if is_audio else f"{file_name}.mp4"
        
        # Schedule the file for deletion after 1 minute
        delete_file_after_delay(file_path, delay=20)

        # Set the Content-Disposition header with the suggested filename
        return send_file(file_path, as_attachment=True, download_name=suggested_filename)
    else:
        return jsonify({"error": f"No matching stream found for quality: {quality}"}), 404
