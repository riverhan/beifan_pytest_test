"""
@Filename:   /session
@Author:      北凡
@Time:        2023/1/11 21:55
@Describe:    ...
"""

import logging
from urllib.parse import urljoin

import requests
from requests import PreparedRequest, Response

logger = logging.getLogger("requests.session")


class Session(requests.Session):
    """
    北凡的封装：
    1. 支持BaseURL
    2. 支持日志记录
    """

    def __init__(self, base_url=""):
        super().__init__()  # 先按原有的方式完成实例化
        self.base_url = base_url  # 再按新的方式完成  【额外操作】

    def request(self, method, url, *args, **kwargs):
        if not url.startswith("http"):  # 如果url不是以HTTP开头
            # 就自动添加baseurl
            url = urljoin(self.base_url, url)

        return super().request(method, url, *args, **kwargs)  # 按照原有方式执行

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        logger.info(f"发送请求>>>>>> 接口地址 = {request.method} {request.url}")
        logger.info(f"发送请求>>>>>> 请求头 = {request.headers}")
        logger.info(f"发送请求>>>>>> 请求正文 = {request.body}")

        response = super().send(request, **kwargs)  # 按原有的方式发送请求

        logger.info(f"接收响应      <<<<<< 状态码 = {response.status_code}")
        logger.info(f"接收响应      <<<<<< 响应头 = {response.headers}")
        logger.info(f"接收响应      <<<<<< 响应正文 = {response.content}")

        return response


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    session = Session("http://baidu.com")

    resp = session.get("/123", data={"a": 1})

    print(resp.url)  # 跳转后的结果

    # 实际请求的地址： http://baidu.com/123
