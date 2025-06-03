import os
import asyncio
from playwright.async_api import async_playwright

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.context = None
        self.page = None

    async def _launch(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox'])
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def login(self):
        await self._launch()
        await self.page.goto("https://www.instagram.com/accounts/login/")

        # Wait for login form
        await self.page.wait_for_selector("input[name='username']")

        # Fill username and password
        await self.page.fill("input[name='username']", self.username)
        await self.page.fill("input[name='password']", self.password)

        # Click login
        await self.page.click("button[type='submit']")

        # Wait and check login success or challenges
        try:
            await self.page.wait_for_selector("nav", timeout=15000)
            return True
        except Exception:
            print("Login failed or blocked.")
            await self.browser.close()
            return False

    async def upload_reel(self, video_path, caption):
        try:
            await self.page.goto("https://www.instagram.com/reels/upload/")

            # Upload video file
            upload_handle = await self.page.query_selector("input[type=file]")
            await upload_handle.set_input_files(video_path)

            # Wait for upload preview & caption box
            await self.page.wait_for_selector("textarea", timeout=30000)

            # Fill caption
            await self.page.fill("textarea", caption[:2200])

            # Click share/post button
            buttons = await self.page.query_selector_all("button")
            for btn in buttons:
                text = await btn.inner_text()
                if "Share" in text or "Post" in text:
                    await btn.click()
                    break

            # Wait some seconds for upload to finish
            await asyncio.sleep(10)
            await self.browser.close()
            return True
        except Exception as e:
            print(f"Upload failed: {e}")
            await self.browser.close()
            return False

    def login(self):
        return asyncio.get_event_loop().run_until_complete(self.login())

    def upload_reel(self, video_path, caption):
        return asyncio.get_event_loop().run_until_complete(self.upload_reel(video_path, caption))
