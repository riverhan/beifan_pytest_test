import time
import urllib.parse
from requests import Session


session = Session()


def test_1():
    global token
    # 1. 获取csrf
    resp = session.get("http://47.107.116.139/phpwind/")

    token = resp.cookies.get("csrf_token")  # 获取cookies

    assert token


def test_2():
    global back_url
    # 2. 登录
    resp = session.post(
        "http://47.107.116.139/phpwind/index.php?m=u&c=login&a=dorun",
        headers={
            "Accept": "application/json, text/javascript, /; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
        },
        data={
            "username": "beifan",
            "password": "beifan",
            "csrf_token": token,
            "backurl": "http://47.107.116.139/phpwind/",
        },
    )

    assert "success" in resp.text
    back_url = urllib.parse.unquote(resp.json()["referer"])


def test_3():
    # 3. 获取cookies
    resp = session.get(back_url)

    assert "beifan" in resp.text  #  判断登录成功


def test_4():
    # 4. 发帖
    global tid

    content = f"beifan_{time.time()}"  # 动态变化的字符串
    resp = session.post(
        "http://47.107.116.139/phpwind/index.php?c=post&a=doadd&_json=1",
        data={
            "fid": 2,
            "atc_title": content,  # 标题不可重复
            "atc_content": content,  # 内容，不可重复
            "csrf_token": token,
            "reply_notice": 1,  # 非必填参数，可以不填
        },
    )

    print(resp.json())
    assert "success" in resp.text

    url = urllib.parse.unquote(resp.json()["referer"])
    tid = urllib.parse.parse_qs(url)["http://47.107.116.139/phpwind/read.php?tid"][0]


def test_5():
    # 5. 回帖

    time.sleep(4)  # 等待4秒，避免灌水

    resp = session.post(
        "http://47.107.116.139/phpwind/index.php?c=post&a=doreply&_getHtml=1",
        data={
            "atc_content": f"reply_beifan_{time.time()}",
            "csrf_token": token,
            "tid": tid,
        },
    )

    assert "editor_content" in resp.text
