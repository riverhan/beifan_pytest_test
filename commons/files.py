"""
@Filename:   commons/files
@Author:      北凡
@Time:        2023/1/13 21:26
@Describe:   读取和保存yaml文件
"""
import yaml
from commons.models import CaseInfo


class YamlFile(dict):

    def __init__(self, path):
        super().__init__()  # 让对象按照原来方式完成实例化
        # 接下来完成自定义的代码
        self._path = path  # yaml文件路径
        self.load()  # 实例化时，自动加载yaml内容

    def load(self):
        with open(self._path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)  # 字典

        if data:
            self.update(data)  # 两个字典内容进行合并

    def save(self):
        with open(self._path, "w", encoding="utf-8") as f:
            yaml.dump(dict(self), f, allow_unicode=True)


if __name__ == '__main__':
    path = r"D:\PycharmProjects\TestClass\api_framework\test_2_login.yaml"
    file = YamlFile(path)
    case_info = CaseInfo(**file)
