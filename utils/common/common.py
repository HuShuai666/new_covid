# coding: utf-8
import datetime
import hashlib
import logging
logger = logging.getLogger('django')


# def append_url_with_domain(url):
#     """
#     对静态资源文件路径进行拼接，返回服务器上资源地址
#     :param url: eg: images/head/123.jpg
#     :return: eg: https://cp1.lxhelper.com/media/images/head/123.jpg
#     """
#     if not url:
#         return ''
#     return DOMAIN + '/media/' + str(url)


def get_ip_address(request):
    """
    从用户请求中获取访问IP地址
    :param request:
    :return:
    """
    if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


def datetime_format(data_time):
    """
    将时间进行格式化
    :param data_time:
    :return:
    """
    return datetime.datetime.strptime(data_time.replace('T', ' ')[:-7], "%Y-%m-%d %H:%M:%S")


def compute_run_time(func):
    """
    计算函数运行时间
    :param func:
    :return:
    """

    def _wrapper(request, *args, **kwargs):
        start_at = datetime.datetime.now()
        result = func(request, *args, **kwargs)
        end_at = datetime.datetime.now()
        print((end_at - start_at).seconds)
        return result

    return _wrapper


def md5(data):
    """md5加密"""
    m2 = hashlib.md5()
    m2.update(data.encode("utf-8"))
    return m2.hexdigest()


def get_today_start_time():
    """取到今天0点0分"""
    now = datetime.datetime.now()
    today_start_time = (now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                                 microseconds=now.microsecond)).strftime("%Y-%m-%d %H:%M:%S")
    return today_start_time
