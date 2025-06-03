import subprocess
import re

def download_tiktok_video(url, output_path):
    try:
        result = subprocess.run([
            "yt-dlp",
            "-f", "mp4",
            "-o", output_path,
            url
        ], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Download error: {e}")
        return False

def extract_caption(url):
    # For simplicity, just return a generic caption with link
    return f"Reposted from TikTok: {url}\n#repost #tiktok"
