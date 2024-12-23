import os
import re

def extract_number(filename):
    """
    从文件名中提取编号（支持不同格式，例如 XXXX 123、XXXX-123 或 XXX123）。
    """
    match = re.search(r"([A-Z]+[\s\-]?\d+)", filename)
    if match:
        return match.group(0).strip()
    return None

def normalize_number(number):
    """
    标准化编号：将字母与数字分开，字母转换为大写，并在字母和数字之间添加空格。
    """
    # 将字母和数字分开，并统一转换为大写
    normalized = re.sub(r"([A-Z]+)(\d+)", r"\1 \2", number.upper())
    # 将空格和连字符统一为单一空格
    normalized = re.sub(r"[\s\-]+", " ", normalized)
    return normalized.strip()

def read_and_sort_files(directory):
    """
    读取指定目录中的文件，并按照编号排序。
    """
    files = os.listdir(directory)
    file_data = []
    for file in files:
        number = extract_number(file)
        if number:
            number = normalize_number(number)  # 标准化编号
            file_data.append((number, file))
    # 按编号排序
    file_data.sort(key=lambda x: x[0])
    return file_data

def display_files(file_data):
    """
    显示文件编号和对应的完整文件名。
    """
    print("编号 - 文件名")
    for number, file in file_data:
        print(f"{number} - {file}")

def search_by_number(file_data, search_number):
    """
    按照编号查询文件。
    """
    search_number = normalize_number(search_number)  # 标准化用户输入的编号
    for number, file in file_data:
        if number == search_number:
            return file
    return None

def main():
    print("欢迎使用文件管理器")
    directory = input("请输入文件夹路径：")
    
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print("无效的文件夹路径。")
        return
    
    # 读取并排序文件
    file_data = read_and_sort_files(directory)
    if not file_data:
        print("文件夹中没有符合要求的文件。")
        return
    
    # 显示文件
    display_files(file_data)
    
    # 查询功能
    while True:
        search_number = input("\n请输入要查询的编号（或输入 'exit' 退出）：")
        if search_number.lower() == 'exit':
            print("退出文件管理器。")
            break
        result = search_by_number(file_data, search_number)
        if result:
            print(f"找到的文件：{result}")
        else:
            print("未找到匹配的文件编号。")

if __name__ == "__main__":
    main()
