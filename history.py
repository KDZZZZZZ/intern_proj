import hashlib
import os

global_files = {}

def generate_hash(file_path):
    """生成文件的 SHA256 哈希值"""
    if not os.path.exists(file_path):
        return None

    hash_object = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hash_object.update(chunk)
        return hash_object.hexdigest()
    except (FileNotFoundError, IOError, OSError):
        return None

def add_file_to_folder_and_dict(folder_path, filename, content):
    """将文件添加到指定文件夹并加入全局字典"""
    file_path = os.path.join(folder_path, filename)
    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
    file_hash = generate_hash(file_path)
    if file_hash is not None:
        global_files[file_path] = file_hash
        print(f"文件 {file_path} 已添加到全局字典中。")
    else:
        print(f"无法生成文件 {file_path} 的哈希值。")

def select_file(random_number):
    """根据哈希值和随机数选择一个文件"""
    if not global_files:
        return None

    # 先过滤出有效的哈希值
    valid_files = {
        filename: hash_value 
        for filename, hash_value in global_files.items() 
        if hash_value is not None
    }

    if not valid_files:
        return None

    try:
        # 计算选择分数
        selection_scores = {
            filename: int(hash_value, 16) % random_number
            for filename, hash_value in valid_files.items()
        }
        
        # 选取得分最小的文件
        return min(selection_scores, key=selection_scores.get)
    except (ValueError, TypeError) as e:
        print(f"Error calculating selection scores: {e}")
        return None