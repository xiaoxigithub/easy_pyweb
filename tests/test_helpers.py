from easy_pyweb.wb_helpers import WebHelper
from easy_pyweb.hello import hi


def test_open_page():
    wb = WebHelper(cookie_path='cookies.txt')
    page = wb.new_page()
    page.goto('https://tool.lu/timestamp/')
    assert page.title() == '时间戳(Unix timestamp)转换工具 - 在线工具'


def test_hi():
    assert hi("World") == "Hello, World!"
    assert hi("Python") == "Hello, Python!"
