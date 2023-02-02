"""
@Filename:   commons/models
@Author:      北凡
@Time:        2023/1/13 21:18
@Describe:    声明yaml用例格式
"""

from dataclasses import dataclass, asdict

import yaml


@dataclass
class CaseInfo:
    """用例信息"""

    title: str
    request: dict
    extract: dict
    validate: dict

    def to_yaml(self) -> str:
        """序列化成yaml字符串"""

        yaml_str = yaml.dump(asdict(self))

        return yaml_str

    @classmethod
    def by_yaml(cls, yaml_str):
        """反序列化"""
        obj = cls(**yaml.safe_load(yaml_str))

        return obj

    def assert_all(self):

        if not self.validate:
            return

        for assert_type, assert_data in self.validate.items():
            for msg, data in assert_data.items():
                a, b = data[0], data[1]
                # print(assert_type, a, b, msg)

                match assert_type:
                    case "equals":
                        assert a == b, msg
                    case "not_equals":
                        assert a != b, msg
                    case "contains":
                        assert a in b, msg
                    case "not_contains":
                        assert a not in b, msg


if __name__ == '__main__':
    with open(
            r"D:\PycharmProjects\TestClass\api_framework\testcases\test_2_login.yaml",
            encoding="utf-8") as f:
        data = yaml.safe_load(f)
    print(data)
    case_info = CaseInfo(**data)

    s = case_info.to_yaml()  # 字符串
    # print(s)
    new_case_info = case_info.by_yaml(s)

    print(new_case_info)
