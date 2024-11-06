import pandas as pd

# 載入 CSV 檔案
csv_file_path = '分配前.csv'
df = pd.read_csv(csv_file_path)

# 定義活動欄位及每個活動的目標人數
activity_columns = df.columns[3:].tolist()  # 假設活動欄位從第四欄開始
total_students = len(df)
target_per_activity = total_students // len(activity_columns)

# 初始化每個活動的分配字典
allocations = {activity: [] for activity in activity_columns}

# 分配函數，依照學生志願順序進行分配，並記錄志願順序
def allocate_students_with_unique_check(df, allocations, target_per_activity):
    assigned_students = set()  # 使用集合追蹤已分配的學生，避免重複

    for priority_level in range(1, 11):  # 志願順序從1到10
        for idx, row in df.iterrows():
            # 定義學生唯一標識（班級、座號、姓名）
            student_identifier = (row["班級"], row["座號"], row["姓名(請寫全名)"])
            student = (row["班級"], row["座號"], row["姓名(請寫全名)"], f"第{priority_level}志願")
            
            # 若學生尚未分配至任何活動，才進行分配
            if student_identifier not in assigned_students:
                for activity in activity_columns:
                    if row[activity] == priority_level:
                        # 若活動人數未達目標且學生未被分配，則進行分配
                        if len(allocations[activity]) < target_per_activity:
                            allocations[activity].append(student)
                            assigned_students.add(student_identifier)  # 標記為已分配
                        break  # 成功分配後，停止檢查其他活動

    return allocations

# 執行分配函數
final_allocations = allocate_students_with_unique_check(df, allocations, target_per_activity)

# 將分配結果轉換為 DataFrame 以便輸出
output_data = []
for activity, students in final_allocations.items():
    for student in students:
        output_data.append({
            "活動": activity,
            "班級": student[0],
            "座號": student[1],
            "姓名": student[2],
            "志願順序": student[3]
        })

output_df = pd.DataFrame(output_data)

# 將結果儲存為 Excel 檔案
output_excel_path = 'student_allocations_with_priority_unique.xlsx'
output_df.to_excel(output_excel_path, index=False)
print(f"分配結果已儲存為 {output_excel_path}")
