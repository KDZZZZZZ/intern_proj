import random

# 指定文件名
filename = "texts.txt"

# 打开文件以追加内容，如果文件不存在，将会创建它
with open(filename, 'a') as file:
    while True:
        # 获取用户输入的文本
        text = input("请输入一段文本（输入 'q' 退出）：")
        if text == 'q':
            break
        # 将文本写入文件，并添加换行符
        file.write(text + "\n")

# 打印一条消息表示文件写入完成
print(f"文本已保存到 '{filename}' 文件中。")

# 定义一个字典，用于存储文件名和概率
file_probabilities = {}

# 计算每个文件的概率
with open(filename, 'r') as file:
    lines = file.readlines()
    total_lines = len(lines)
    for line in lines:
        # 假设概率是根据文本长度计算的，您可以根据需要更改算法
        probability = len(line.strip()) / total_lines
        file_probabilities[line.strip()] = probability

# 现在您可以通过文件名来访问概率
# probability_of_file1 = file_probabilities["file1.txt"]
# print("概率 of file1.txt:", probability_of_file1)

