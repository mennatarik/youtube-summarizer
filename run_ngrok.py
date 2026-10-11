"""Launch the Streamlit app and expose it publicly through ngrok.

Usage:
    export NGROK_AUTHTOKEN=your_token   # https://dashboard.ngrok.com/get-started/your-authtoken
    python run_ngrok.py
"""
import os
import subprocess
import sys
import time

from pyngrok import conf, ngrok

PORT = 8501


def main():
    token = os.getenv("NGROK_AUTHTOKEN")
    if not token:
        sys.exit("Set the NGROK_AUTHTOKEN environment variable first.")
    conf.get_default().auth_token = token

    proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", str(PORT),
            "--server.headless", "true",
        ]
    )
    time.sleep(5)  # give Streamlit a moment to start

    tunnel = ngrok.connect(PORT)
    print(f"\n🌍 Public URL: {tunnel.public_url}\n")

    try:
        proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        ngrok.kill()
        proc.terminate()


if __name__ == "__main__":
    main()
