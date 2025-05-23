from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>IG + X Downloader</title>
</head>
<body>
    <h2>Instagram / Twitter Video Downloader</h2>
    <form method="POST" action="/download">
        <input type="text" name="url" placeholder="Paste video URL" size="50" required>
        <button type="submit">Download</button>
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get("url")
    if not url:
        return "No URL provided", 400

    filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': filename,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Error downloading video: {e}", 500

    response = send_file(filename, as_attachment=True)
    os.remove(filename)
    return response

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5051))
    app.run(host="0.0.0.0", port=port)