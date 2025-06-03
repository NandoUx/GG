import subprocess, os
from playwright.sync_api import sync_playwright

def download_video(url, out_file):
    cmd = ["yt-dlp", "-f", "mp4", "-o", out_file, "--no-warnings", url]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0

def repost_video(video_path, caption, account_cookie_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=f"accounts/{account_cookie_file}.json")
        page = context.new_page()
        page.goto("https://www.tiktok.com/upload", timeout=60000)
        
        try:
            page.set_input_files("input[type='file']", video_path)
            page.locator("textarea").fill(caption[:2200])
            page.click("button:has-text('Post')")
            page.wait_for_timeout(8000)  # adjust if needed
            return True
        except Exception as e:
            print("Upload error:", e)
            return False
        finally:
            context.close()
            browser.close()

def extract_caption(url):
    return f"Reposted via bot 🤖\n📽 {url}"  # or parse caption from TikTok if needed

def process_tiktok_link(url, video_name, account_cookie_file):
    if not download_video(url, video_name):
        return False, None
    
    caption = extract_caption(url)
    success = repost_video(video_name, caption, account_cookie_file)

    if os.path.exists(video_name):
        os.remove(video_name)

    return success, caption
