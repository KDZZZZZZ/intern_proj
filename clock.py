import time

class CallCountClock:
    def __init__(self):
        self.call_count = 0

    def get_time(self):
        self.call_count += 1

        return self.call_count



# 创建时钟对象
clock = CallCountClock()
#每次调用get_time方法时，调用次数会增加1
# 模拟调用时钟方法
for _ in range(10):
    print(clock.get_time())
