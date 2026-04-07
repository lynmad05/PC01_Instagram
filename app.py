from flask import Flask, request, jsonify, send_file, render_template_string
import yt_dlp
import os
import uuid
import socket

app = Flask(__name__)

DOWNLOAD_FOLDER = "/tmp/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Instagram Downloader 📸</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0a0a0a;
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .card {
            background: #111;
            border: 1px solid #333;
            border-radius: 16px;
            padding: 40px;
            width: 100%;
            max-width: 500px;
            box-shadow: 0 0 40px rgba(193,53,132,0.2);
        }
        h1 { text-align: center; font-size: 2rem; margin-bottom: 8px; }
        .subtitle { text-align: center; color: #888; margin-bottom: 10px; font-size: 0.9rem; }
        .hostname { text-align: center; color: #555; font-size: 0.75rem; margin-bottom: 24px; }
        input {
            width: 100%;
            padding: 14px 16px;
            border-radius: 10px;
            border: 1px solid #333;
            background: #1a1a1a;
            color: #fff;
            font-size: 1rem;
            margin-bottom: 14px;
            outline: none;
            transition: border 0.2s;
        }
        input:focus { border-color: #c13584; }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #833ab4, #c13584, #e1306c, #fd1d1d);
            color: #fff;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        button:hover { opacity: 0.85; }
        #status {
            margin-top: 20px;
            padding: 14px;
            border-radius: 10px;
            display: none;
            font-size: 0.9rem;
        }
        .success { background: #0f2a1a; color: #4ade80; border: 1px solid #166534; display: block !important; }
        .error   { background: #2a0a0a; color: #f87171; border: 1px solid #991b1b; display: block !important; }
        .loading { background: #1a1a2a; color: #93c5fd; border: 1px solid #1e3a8a; display: block !important; }
        a.dl-link {
            display: block;
            margin-top: 10px;
            text-align: center;
            color: #c13584;
            font-weight: bold;
            text-decoration: none;
        }
        .tip {
            margin-top: 16px;
            font-size: 0.78rem;
            color: #555;
            text-align: center;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>📸 Instagram DL</h1>
        <p class="subtitle">Descarga Reels e IGTV de Instagram</p>
        <p class="hostname">🖥️ Host: {{ hostname }}</p>
        <input type="text" id="url" placeholder="https://www.instagram.com/reel/..." />
        <button onclick="download()">⬇️ Descargar Video</button>
        <div id="status"></div>
        <p class="tip">⚠️ Solo funciona con publicaciones públicas.<br>Formatos soportados: Reels, IGTV, posts con video.</p>
    </div>
    <script>
        async function download() {
            const url = document.getElementById('url').value.trim();
            const status = document.getElementById('status');
            if (!url) {
                status.className = 'error';
                status.textContent = '⚠️ Ingresa una URL válida de Instagram.';
                return;
            }
            status.className = 'loading';
            status.innerHTML = '⏳ Descargando video, por favor espera...';
            try {
                const res = await fetch('/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url })
                });
                const data = await res.json();
                if (res.ok) {
                    status.className = 'success';
                    status.innerHTML = '✅ Video descargado! <a class="dl-link" href="/file/' + data.filename + '" download>📥 Haz clic aquí para guardar el video</a>';
                } else {
                    status.className = 'error';
                    status.textContent = '❌ Error: ' + data.error;
                }
            } catch (e) {
                status.className = 'error';
                status.textContent = '❌ Error de conexión.';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, hostname=socket.gethostname())

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url or 'instagram.com' not in url:
        return jsonify({'error': 'URL inválida. Solo se aceptan URLs de Instagram.'}), 400

    filename = f"{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file/<filename>')
def serve_file(filename):
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return jsonify({'error': 'Archivo no encontrado'}), 404
    return send_file(path, as_attachment=True, download_name='instagram_video.mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)