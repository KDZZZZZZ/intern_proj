## TODO，用于在main中执行相应py

``` python
import subprocess

# Step 1: 修改 input.txt 文件
new_input = "这是新的提示词"
with open('Oneesan/input.txt', 'w', encoding='utf-8') as f:
    f.write(new_input)

# Step 2: 执行 Oneesan.py
result = subprocess.run(
    ['python', 'Oneesan.py'],  # 执行的命令
    capture_output=True,              # 捕获输出
    text=True                         # 将输出解码为字符串
)

# Step 3: 打印执行结果
print(result.stdout)
```