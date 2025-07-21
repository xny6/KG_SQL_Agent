import sys
import os

# 添加模块路径到 sys.path
module_path = "/home/NingyuanXiao/LightRAG_test"
if module_path not in sys.path:
    sys.path.append(module_path)

# 打印 sys.path 查看是否添加成功
print("sys.path:", sys.path)

# 尝试导入模块
try:
    from LightRAG_test.attack_final.query_kg import test_query
    print("Module imported successfully!")
except ModuleNotFoundError as e:
    print("ModuleNotFoundError:", e)

import asyncio

asyncio.run(test_query(question='Which earphone devices supports ANC?'))