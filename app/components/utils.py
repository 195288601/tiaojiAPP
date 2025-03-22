import os
import json
import pandas as pd
from datetime import datetime
import streamlit as st

# 获取数据目录路径
def get_data_dir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# 获取数据文件路径
def get_data_file():
    return os.path.join(get_data_dir(), 'schools.json')

# 加载数据
@st.cache_data(ttl=60)
def load_data():
    data_file = get_data_file()
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 保存数据
def save_data(data):
    data_file = get_data_file()
    data_dir = get_data_dir()
    # 确保数据目录存在
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 使用 try-except 增强可靠性，防止写入失败破坏数据
    try:
        # 先写入临时文件，成功后再重命名，防止数据损坏
        temp_file = f"{data_file}.temp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # 如果是Windows系统，可能需要先删除原有文件
        if os.path.exists(data_file):
            os.unlink(data_file)
            
        # 重命名临时文件为正式文件
        os.rename(temp_file, data_file)
        return True
    except Exception as e:
        print(f"保存数据时出错: {str(e)}")
        return False

# 添加新学校
def add_school(school_data, schools_data):
    new_school = {
        "id": len(schools_data) + 1,
        "name": school_data["name"],
        "address": school_data["address"],
        "major": school_data["major"],
        "recruitment_count": school_data["recruitment_count"],
        "scores": {
            "2024": {"max": school_data["scores"]["2024"]["max"], "min": school_data["scores"]["2024"]["min"]},
            "2023": {"max": school_data["scores"]["2023"]["max"], "min": school_data["scores"]["2023"]["min"]},
            "2022": {"max": school_data["scores"]["2022"]["max"], "min": school_data["scores"]["2022"]["min"]},
            "2021": {"max": school_data["scores"]["2021"]["max"], "min": school_data["scores"]["2021"]["min"]}
        },
        "contact": {
            "email": school_data["contact"]["email"],
            "phone": school_data["contact"]["phone"]
        },
        "remark": school_data.get("remark", ""),
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    schools_data.append(new_school)
    save_data(schools_data)
    return new_school

# 将JSON数据转换为DataFrame
@st.cache_data(ttl=300)
def json_to_dataframe(schools_data):
    if not schools_data:
        return pd.DataFrame()
        
    return pd.DataFrame([
        {
            "学校名称": school["name"],
            "学校地址": school["address"],
            "调剂专业": school.get("major", ""),
            "招生人数": school["recruitment_count"],
            "2024最高分": school["scores"]["2024"]["max"],
            "2024最低分": school["scores"]["2024"]["min"],
            "2023最高分": school["scores"]["2023"]["max"],
            "2023最低分": school["scores"]["2023"]["min"],
            "2022最高分": school["scores"]["2022"]["max"],
            "2022最低分": school["scores"]["2022"]["min"],
            "2021最高分": school["scores"]["2021"]["max"],
            "2021最低分": school["scores"]["2021"]["min"],
            "邮箱": school["contact"]["email"],
            "电话": school["contact"]["phone"],
            "备注": school.get("remark", "")
        }
        for school in schools_data
    ])

# 创建示例模板数据
@st.cache_data
def create_template_data():
    template_data = {
        "学校名称": ["示例大学", "示例理工大学"],
        "学校地址": ["北京市海淀区XX路XX号", "上海市浦东新区XX路XX号"],
        "调剂专业": ["计算机科学与技术", "软件工程"],
        "招生人数": [20, 15],
        "2024最高分": [380, 370],
        "2024最低分": [350, 340],
        "2023最高分": [375, 365],
        "2023最低分": [345, 335],
        "2022最高分": [370, 360],
        "2022最低分": [340, 330],
        "2021最高分": [365, 355],
        "2021最低分": [335, 325],
        "邮箱": ["example@university.edu.cn", "info@example.edu.cn"],
        "电话": ["010-12345678", "021-87654321"],
        "备注": ["270-310分", "300分左右"]
    }
    return pd.DataFrame(template_data)

# 从Excel/CSV导入数据
def import_from_file(file, schools_data):
    try:
        # 根据文件类型读取数据
        if file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:  # CSV文件
            df = pd.read_csv(file)
        
        # 检查必要的列是否存在
        required_columns = [
            "学校名称", "学校地址", "调剂专业", "招生人数", 
            "2024最高分", "2024最低分", "2023最高分", "2023最低分", 
            "2022最高分", "2022最低分", "2021最高分", "2021最低分", 
            "邮箱", "电话"
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return False, f"上传的文件缺少以下必要列：{', '.join(missing_columns)}", None
        
        # 将NaN值替换为默认值
        df = df.fillna({
            "学校名称": "",
            "学校地址": "",
            "调剂专业": "",
            "招生人数": "0",
            "2024最高分": 0,
            "2024最低分": 0,
            "2023最高分": 0,
            "2023最低分": 0,
            "2022最高分": 0,
            "2022最低分": 0,
            "2021最高分": 0,
            "2021最低分": 0,
            "邮箱": "",
            "电话": "",
            "备注": ""
        })
        
        # 预处理招生人数字段，将其转换为字符串以便保留范围表示
        df["招生人数"] = df["招生人数"].astype(str)
        
        # 将其他数值列转换为整数
        numeric_columns = [
            "2024最高分", "2024最低分", 
            "2023最高分", "2023最低分", 
            "2022最高分", "2022最低分", 
            "2021最高分", "2021最低分"
        ]
        for col in numeric_columns:
            df[col] = df[col].astype(int)
        
        # 将DataFrame数据转换为JSON格式
        new_schools = []
        for _, row in df.iterrows():
            # 跳过空行或名称为空的行
            if not row["学校名称"]:
                continue
            
            # 处理招生人数，尝试转换为整数，如果失败则保留原始字符串
            try:
                recruitment_count = int(row["招生人数"])
            except ValueError:
                # 保留原始字符串格式
                recruitment_count = row["招生人数"]
                
            new_school = {
                "id": len(schools_data) + len(new_schools) + 1,
                "name": row["学校名称"],
                "address": row["学校地址"],
                "major": row["调剂专业"],
                "recruitment_count": recruitment_count,
                "scores": {
                    "2024": {"max": int(row["2024最高分"]), "min": int(row["2024最低分"])},
                    "2023": {"max": int(row["2023最高分"]), "min": int(row["2023最低分"])},
                    "2022": {"max": int(row["2022最高分"]), "min": int(row["2022最低分"])},
                    "2021": {"max": int(row["2021最高分"]), "min": int(row["2021最低分"])}
                },
                "contact": {
                    "email": str(row["邮箱"]),
                    "phone": str(row["电话"])
                },
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 添加备注字段，如果存在
            if "备注" in row:
                new_school["remark"] = str(row["备注"])
            
            new_schools.append(new_school)
        
        if not new_schools:
            return False, "导入文件中没有有效的学校数据", None
            
        return True, f"成功解析 {len(new_schools)} 所学校数据", new_schools
        
    except Exception as e:
        return False, f"导入数据时出错：{str(e)}", None

# 删除学校
def delete_school(school_id, schools_data):
    for i, school in enumerate(schools_data):
        if school["id"] == school_id:
            del schools_data[i]
            save_data(schools_data)
            return True
    return False

# 批量删除学校
def batch_delete_schools(school_ids, schools_data):
    if not school_ids:
        return 0
        
    deleted_count = 0
    indices_to_delete = []
    
    # 先找出要删除的索引
    for i, school in enumerate(schools_data):
        if school["id"] in school_ids:
            indices_to_delete.append(i)
            deleted_count += 1
    
    # 如果没有找到任何匹配的学校，直接返回
    if not indices_to_delete:
        return 0
    
    # 从后往前删除，避免索引变化问题
    for index in sorted(indices_to_delete, reverse=True):
        del schools_data[index]
    
    if deleted_count > 0:
        save_data(schools_data)
    
    return deleted_count

# 删除所有学校
def delete_all_schools():
    # 直接保存空列表，清空所有数据
    save_data([])
    return True 