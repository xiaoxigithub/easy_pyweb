from easy_pyweb.wb_helpers import WebHelper
from easy_pyweb.more_tool import SingletonLogger, ConfigParser


def open_page():
    wb = WebHelper(cookie_path='cookies.txt')
    page = wb.new_page()
    page.goto('https://tool.lu/timestamp/')
    print(page.title())
    assert page.title() == '时间戳(Unix timestamp)转换工具 - 在线工具'


def log_test():
    logger = SingletonLogger(logdir='logs').get_logger()
    logger.info('This is a test log')
    logger.error('This is a error log')


def conf_test():
    conf = ConfigParser(config_file='config.ini')
    conf.init_config()
    print(conf.get_option('TEST', 'user'))


if __name__ == '__main__':
    # open_page()
    # log_test()
    conf_test()
