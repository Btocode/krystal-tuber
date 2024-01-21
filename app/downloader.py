from pytube import YouTube

def download_audio(url, output_path='downloads'):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True)
        filename = audio_stream.download(output_path=output_path)
        # rename the file with an unmatched uuid and a .mp3 extension
        
        
        return {"success": True, "title": yt.title, "filepath": filename}
    except Exception as e:
        return {"error": str(e)}