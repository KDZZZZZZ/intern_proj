import random
import os
import hashlib


class FileHandler:
    def __init__(self):
        self.files = {}  # 存储文件名与哈希值

    def add_file(self, filename):
        """将文件名与其哈希值记录下来"""
        file_hash = self.generate_hash(filename)
        self.files[filename] = file_hash

    @staticmethod
    def generate_hash(filename):
        """生成文件的 SHA256 哈希值"""
        hash_object = hashlib.sha256()
        try:
            with open(filename, 'rb') as file:
                for chunk in iter(lambda: file.read(4096), b''):
                    hash_object.update(chunk)
        except FileNotFoundError:
            return None
        return hash_object.hexdigest()

    def select_file(self, random_number):
        """根据哈希值和随机数选择一个文件"""
        if not self.files:
            return None  # 如果没有文件，返回 None

        # 将文件哈希值与随机数映射到一个选择区间
        selection_scores = {
            filename: int(hash_value, 16) % random_number
            for filename, hash_value in self.files.items()
        }

        # 选取得分最小的文件
        selected_file = min(selection_scores, key=selection_scores.get)
        return selected_file


class History:
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text
        self.file_handler = FileHandler()

    def save_text_to_file(self):
        """将文本保存到文件中"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w'):
                pass

        with open(self.filename, 'a') as file:
            file.write(self.text + "\n")

        # 添加文件到 FileHandler
        self.file_handler.add_file(self.filename)
