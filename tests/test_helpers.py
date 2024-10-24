from easy_pyweb.wb_helpers import WebHelper
from easy_pyweb.sql_helpers import MysqlInstance


def test_open_page():
    wb = WebHelper(cookie_path='cookies.txt')
    page = wb.new_page()
    page.goto('https://tool.lu/timestamp/')
    print(page.title())
    print('高度%s' % page.get_height())
    value = page.locator('#jsDatetimeO').input_value()
    print('时间%s' % value)
    page.slide_bottom()
    assert page.title() == '时间戳(Unix timestamp)转换工具 - 在线工具'


def test_mysql():
    con = MysqlInstance('localhost', 'root', 'test', 'build2').init_connect()
    cur = con.cursor()
    cur.execute('select * from log limit 10')
    query = cur.fetchall()
    assert len(query) == 10
