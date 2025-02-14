# 说明
- pyweb助手，封装一些个人常用类函数
- 内置【playwright浏览器类，logger，mysql，config】
- win系统控制隐藏web窗口，需安装pywin32

# 安装使用
`pip install easy-pyweb`

## 试一试 浏览器
```python
from easy_pyweb.wb_helpers import WebHelper

def open_page():
    wb = WebHelper(use_async=False)
    wb.init_browser_sync()
    page = wb.new_page_sync()
    page.goto('https://tool.lu/timestamp/')
    print(page.title())
    print('高度%s' % page.get_height())
    value = page.locator('#jsDatetimeO').input_value()
    print('时间%s' % value)
    page.slide_bottom()
    assert page.title() == '时间戳(Unix timestamp)转换工具 - 在线工具'
```

## 试一试 日志，配置类
```python
from easy_pyweb.more_tool import SingletonLogger, ConfigParser
def log_test():
    logger = SingletonLogger(logdir='logs').get_logger()
    logger.info('This is a test log')
    logger.error('This is a error log')

def conf_test():
    conf = ConfigParser(config_file='config.ini')
    conf.init_config()
    print(conf.get_option('TEST', 'user'))
```

