# easy_pyweb/helpers.py
import json
import os
import random
from datetime import datetime, timezone
from typing import Union
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Page as AsyncPage
from playwright.sync_api import sync_playwright, Page as SyncPage


class WebHelper:
    args = [
        '--disable-blink-features=AutomationControlled',
        '--incognito',
        '--enable-automation',
        '--disable-infobars',
        '--disable-impl-side-painting',
    ]
    device = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.71',
        'viewport': {'width': 1280, 'height': 1024},
    }

    def __init__(self, use_async: bool = False, **kwargs):
        self.use_async = use_async
        self.args.extend(kwargs.get('args', []))
        self.device.update(kwargs.get('device', {}))
        self.executable_path = kwargs.get('executable_path', os.path.join('c:\\', 'chrome32'))
        self.headless = kwargs.get('headless', False)
        self.cookie_path = kwargs.get('cookie_path', 'cookies.json')
        self.browser = None
        self.playwright = None
        self._new = False

    # 初始化浏览器
    async def init_browser_async(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch_persistent_context(
            executable_path=os.path.join(self.executable_path, 'chrome.exe'),
            user_data_dir=os.path.join(self.executable_path, 'userdata'),
            headless=self.headless,
            args=self.args,
            user_agent=self.device['user_agent'],
            viewport=self.device['viewport'],
        )
        self._new = False
        # 加载 stealth.min.js
        await self._load_stealth_script_async()

    def init_browser_sync(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(
            executable_path=os.path.join(self.executable_path, 'chrome.exe'),
            user_data_dir=os.path.join(self.executable_path, 'userdata'),
            headless=self.headless,
            args=self.args,
            user_agent=self.device['user_agent'],
            viewport=self.device['viewport'],
        )
        self._new = False
        # 加载 stealth.min.js
        self._load_stealth_script_sync()

    async def _load_stealth_script_async(self):
        js_path = os.path.join(os.path.dirname(__file__), 'js', 'stealth.min.js')
        with open(js_path) as f:
            js = f.read()
        await self.browser.add_init_script(js)

    def _load_stealth_script_sync(self):
        js_path = os.path.join(os.path.dirname(__file__), 'js', 'stealth.min.js')
        with open(js_path) as f:
            js = f.read()
        self.browser.add_init_script(js)

    # 创建页面
    async def new_page_async(self, hide_img: bool = False) -> Union[AsyncPage, 'PageHelper']:
        page = await self.browser.new_page()
        if hide_img:
            await self._disable_images_async(page)
        # 清除默认打开的空白页面
        if not self._new and self.browser.pages:
            await self.browser.pages[0].close()
            self._new = True
        return PageHelper(page, use_async=True)

    def new_page_sync(self, hide_img: bool = False) -> Union[SyncPage, 'PageHelper']:
        page = self.browser.new_page()
        if hide_img:
            self._disable_images_sync(page)
        # 清除默认打开的空白页面
        if not self._new and self.browser.pages:
            self.browser.pages[0].close()
            self._new = True
        return PageHelper(page)

    async def _disable_images_async(self, page: AsyncPage):
        await page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
        await page.route("**/*", lambda route: route.abort()
        if route.request.resource_type == "image" else route.continue_())

    def _disable_images_sync(self, page: SyncPage):
        page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
        page.route("**/*", lambda route: route.abort()
        if route.request.resource_type == "image" else route.continue_())

    # Cookie 管理
    async def load_cookies_async(self, cookie_file: str, domain: str):
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            await self.browser.add_cookies(cookies)

    def load_cookies_sync(self, cookie_file: str, domain: str):
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            self.browser.add_cookies(cookies)

    async def save_cookies_async(self, cookie_file: str):
        cookies = await self.browser.cookies()
        with open(cookie_file, 'w', encoding='utf8') as f:
            json.dump(cookies, f)

    def save_cookies_sync(self, cookie_file: str):
        cookies = self.browser.cookies()
        with open(cookie_file, 'w', encoding='utf8') as f:
            json.dump(cookies, f)

    # 关闭浏览器
    async def close_async(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def close_sync(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


class PageHelper:
    def __init__(self, page: Union[SyncPage, AsyncPage], use_async: bool = False):
        self.page = page
        self.use_async = use_async
        self.setIntervalJS = 'setInterval(function(){document.querySelectorAll("[style*=block], [scrolling=no],{business}").forEach(function(ele){ele.remove();}); document.querySelectorAll("[onclick]").forEach(function(e){e.removeAttribute("onclick");});},1000);'

    def __getattr__(self, name):
        return getattr(self.page, name)

    # 等待随机时间（同步）
    def rand_wait_sync(self, min_time=1, max_time=3):
        self.page.wait_for_timeout(random.randint(min_time, max_time) * 1000)

    # 等待随机时间（异步）
    async def rand_wait_async(self, min_time=1, max_time=3):
        await self.page.wait_for_timeout(random.randint(min_time, max_time) * 1000)

    # 获取页面高度（同步）
    def get_height_sync(self):
        return self.page.evaluate('''() => {
                     return Math.max(
                         document.body.scrollHeight, document.body.offsetHeight,
                         document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight
                     );
                 }''')

    # 获取页面高度（异步）
    async def get_height_async(self):
        return await self.page.evaluate('''() => {
                     return Math.max(
                         document.body.scrollHeight, document.body.offsetHeight,
                         document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight
                     );
                 }''')

    # 滑动到底部（同步）
    def slide_bottom_sync(self, scroll_step=300, wait_time=500):
        current_position = 0
        total_height = self.get_height_sync()
        while current_position < total_height:
            self.page.evaluate(f'window.scrollTo(0, {current_position});')
            current_position += scroll_step
            self.page.wait_for_timeout(wait_time)

    # 滑动到底部（异步）
    async def slide_bottom_async(self, scroll_step=300, wait_time=500):
        current_position = 0
        total_height = await self.get_height_async()
        while current_position < total_height:
            await self.page.evaluate(f'window.scrollTo(0, {current_position});')
            current_position += scroll_step
            await self.page.wait_for_timeout(wait_time)

    # 清除元素（同步）
    def clear_block_sync(self, selector):
        self.page.evaluate(self.setIntervalJS.replace('{business}', selector))

    # 清除元素（异步）
    async def clear_block_async(self, selector):
        await self.page.evaluate(self.setIntervalJS.replace('{business}', selector))

    # 安全获取属性（同步）
    def get_attribute_safe_sync(self, node, selector, inner_text=True, attribute='') -> str:
        try:
            rand_time = random.randint(100, 600)
            node = node.locator(selector).first
            if inner_text:
                return node.inner_text(timeout=rand_time)
            return node.get_attribute(attribute, timeout=rand_time)
        except Exception:
            return ''

    # 安全获取属性（异步）
    async def get_attribute_safe_async(self, node, selector, inner_text=True, attribute='') -> str:
        try:
            rand_time = random.randint(100, 600)
            node = node.locator(selector).first
            if inner_text:
                return await node.inner_text(timeout=rand_time)
            return await node.get_attribute(attribute, timeout=rand_time)
        except Exception:
            return ''

    # 检查页面元素（同步）
    def page_element_check_sync(self, selector, retry_count=3):
        result = False
        for _ in range(retry_count):
            try:
                result = self.page_evaluate_script_sync(selector)
                return result
            except Exception as e:
                print('执行js异常 %s' % e)
        return result

    # 检查页面元素（异步）
    async def page_element_check_async(self, selector, retry_count=3):
        result = False
        for _ in range(retry_count):
            try:
                result = await self.page_evaluate_script_async(selector)
                return result
            except Exception as e:
                print('执行js异常 %s' % e)
        return result

    # 执行 JS 检查元素是否存在（同步）
    def page_evaluate_script_sync(self, selector):
        return self.page.evaluate(f'!!document.querySelector("{selector}")')

    # 执行 JS 检查元素是否存在（异步）
    async def page_evaluate_script_async(self, selector):
        return await self.page.evaluate(f'!!document.querySelector("{selector}")')


# 解析cookie
def parse_cookie_str(ck_str: str, domain: str):
    result = []
    for i in ck_str.split(';'):
        value = i.split('=')
        if not len(value) == 2:
            continue
        # 有效期设置今年12月31号23:59
        now = datetime.now()
        year_end = datetime(now.year, 12, 31, 23, 59, tzinfo=timezone.utc)
        expires_timestamp = year_end.timestamp()  # 转换为时间戳
        result.append({
            'name': value[0].strip(),
            'value': value[1].strip(),
            'domain': urlparse(domain).netloc,
            'path': '/',
            'expires': expires_timestamp,
            'httpOnly': False,
            'secure': True,
            'sameSite': 'Lax'
        })
    return result
