import pandas as pd

# 載入分配前與分配後的 CSV 檔案
before_allocation_df = pd.read_csv('分配前.csv')
after_allocation_df = pd.read_csv('分配後.csv')

# 1. 檢查分配後是否有重複的名字（基於班級、座號、姓名）
duplicates_in_after_allocation = after_allocation_df.duplicated(subset=["班級", "座號", "姓名"])

# 篩選出重複的行
duplicates = after_allocation_df[duplicates_in_after_allocation]

# 2. 檢查分配前的名單是否都在分配後裡，確認是否有名字遺漏
# 建立分配前與分配後的唯一標識集合（班級、座號、姓名）
before_allocation_set = set(before_allocation_df[["班級", "座號", "姓名(請寫全名)"]].itertuples(index=False, name=None))
after_allocation_set = set(after_allocation_df[["班級", "座號", "姓名"]].itertuples(index=False, name=None))

# 找出分配後缺少的名字
missing_in_after_allocation = before_allocation_set - after_allocation_set

# 顯示結果
print("分配後的重複名字：")
print(duplicates)  # 若為空表示沒有重複

print("\n分配後缺少的名字：")
print(missing_in_after_allocation)  # 若為空表示沒有遺漏
