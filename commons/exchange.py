"""
@Filename:   commons/exchange.py
@Author:      北凡
@Time:        2023/1/29 20:59
@Describe:    ...
"""
import copy
import json.decoder
import re

import jsonpath
from commons.templates import Template
from commons.files import YamlFile

from commons.models import CaseInfo


class Exchange:

    def __init__(self, path):
        self.file = YamlFile(path)

    def extract(self, resp, var_name, attr, expr: str, index: int):
        # resp中 json是方法，不是属性，需要手动改为属性

        resp = copy.deepcopy(resp)
        try:
            resp.json = resp.json()
        except json.decoder.JSONDecodeError:
            resp.json = {"msg": " is not json data"}

        data = getattr(resp, attr)  #

        if expr.startswith("/"):  # 是 xpath
            res = None
        elif expr.startswith("$"):  # 是jsonpath
            data = dict(data)  # 强转字典
            res = jsonpath.jsonpath(data, expr)
            # print(f"{res=}")
        else:  # 是正则
            res = re.findall(expr, str(data))
        print(f"{res=}")
        if res:  # 如果有数据
            value = res[index]
        else:  # 如果没有数据
            value = "not data"

        self.file[var_name] = value  # 保存变量
        self.file.save()  # 持久化存储到文件

    def replace(self, case_info: CaseInfo):
        # 1. 将case_info 转成字符串
        case_info_str = case_info.to_yaml()

        # 2. 替换字符串
        case_info_str = Template(case_info_str).render(self.file)
        # 3. 将字符串 转成case_info
        new_case_info = case_info.by_yaml(case_info_str)
        return new_case_info


if __name__ == '__main__':
    class MockResponse:
        text = '{"name": "beifan", "age": "18", "data": [3,66,99], "aaa": null}'

        def json(self):
            return json.loads(self.text)


    mock_resp = MockResponse()

    print(mock_resp.text)
    print(mock_resp.json())

    # exchanger = Exchange(r'D:\PycharmProjects\TestClass\api_framework\extract.yaml')
    # exchanger.extract(mock_resp, "name", "text", '"name": "(\w+)"', 0)
    # exchanger.extract(mock_resp, "age", "text", '"age": (\d)', 0)
    # exchanger.extract(mock_resp, "data", "text", '"data": \[(.*)\]', 0)

    exchanger = Exchange(
        r'D:\PycharmProjects\TestClass\api_framework\extract.yaml')
    exchanger.extract(mock_resp, "name", "json", '$.name', 0)
    exchanger.extract(mock_resp, "age", "json", '$.age', 0)
    exchanger.extract(mock_resp, "data", "json", '$.data[2]', 0)
    exchanger.extract(mock_resp, "aaa", "json", '$.aaa', 0)

    case_info = CaseInfo(
        title="单元测试",
        request={
            "data":
                {"name": "${name}", "age": "${int(age)}",
                 "time": "${add(100, 1000)}"}
        },
        extract={},
        validate={}
    )

    new_case_info = exchanger.replace(case_info)
    print(new_case_info)
