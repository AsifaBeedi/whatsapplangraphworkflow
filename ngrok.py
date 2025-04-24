from pyngrok import ngrok

def start_ngrok():
    url = ngrok.connect(5000).public_url
    print(f"Ngrok Tunnel URL: {url}")
    return url