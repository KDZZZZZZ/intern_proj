import hashlib
import os
import gen_plot
import random

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

def add_file_to_folder_and_dict(state_instance, content):
    """将文件添加到指定文件夹并加入全局字典"""
    n = state_instance.get_state()
        
        # 生成文件列表
    file_path = os.path.join('history', f'stage_{n}.txt')

    with open(file_path, 'a') as f:
        f.write('\n'+content)
    file_hash = generate_hash(file_path)
    if file_hash is not None:
        global_files[file_path] = file_hash
        print(f"文件 {file_path} 已添加到全局字典中。")
    else:
        print(f"无法生成文件 {file_path} 的哈希值。")

def select_file(stage: int) -> str:
    """随机选择从stage_1到stage_n中的一个文件"""
    if stage < 1:
        return None
        
    # 获取所有存在的文件
    valid_files = []
    for i in range(1, stage + 1):
        file_path = os.path.join('history', f'stage_{i}.txt')
        if os.path.exists(file_path):
            valid_files.append(file_path)
    
    if not valid_files:
        return None
    
    # 随机选择一个文件
    return random.choice(valid_files)