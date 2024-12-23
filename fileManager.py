import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox


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
    normalized = re.sub(r"([A-Z]+)(\d+)", r"\1 \2", number.upper())
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
            number = normalize_number(number)
            file_data.append((number, file))
    file_data.sort(key=lambda x: x[0])
    return file_data


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件管理器")

        # 页面#1：选择文件夹
        self.page1 = tk.Frame(self.root)
        self.page1.pack(fill=tk.BOTH, expand=True)

        self.select_label = tk.Label(
            self.page1, text="请选择一个文件夹", font=("Arial", 16))
        self.select_label.pack(pady=20)

        self.select_button = tk.Button(
            self.page1, text="选择文件夹", command=self.select_folder, font=("Arial", 12)
        )
        self.select_button.pack(pady=10)

        # 页面#2：文件显示界面
        self.page2 = tk.Frame(self.root)

        # 搜索框
        self.search_bar = tk.Entry(self.page2, font=("Arial", 14))
        self.search_bar.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.search_button = tk.Button(
            self.page2, text="搜索", command=self.search_file, font=("Arial", 12)
        )
        self.search_button.place(relx=0.7, rely=0.05, anchor=tk.CENTER)

        # 文件显示区域
        self.file_list = tk.Listbox(self.page2, font=("Arial", 12), width=50, height=20)
        self.file_list.place(relx=0.05, rely=0.2)

        self.current_directory = None
        self.file_data = []

    def select_folder(self):
        """
        选择文件夹并切换到文件显示界面。
        """
        folder = filedialog.askdirectory()
        if folder:
            self.current_directory = folder
            self.file_data = read_and_sort_files(folder)

            if not self.file_data:
                messagebox.showerror("错误", "文件夹中没有符合要求的文件。")
                return

            self.show_page2()
        else:
            messagebox.showwarning("警告", "未选择任何文件夹。")

    def show_page2(self):
        """
        显示文件显示界面。
        """
        self.page1.pack_forget()
        self.page2.pack(fill=tk.BOTH, expand=True)

        self.file_list.delete(0, tk.END)
        for number, file in self.file_data:
            self.file_list.insert(tk.END, f"{number} - {file}")

    def search_file(self):
        """
        搜索文件。
        """
        query = self.search_bar.get()
        if not query:
            messagebox.showwarning("警告", "请输入搜索编号。")
            return

        query = normalize_number(query)
        for number, file in self.file_data:
            if number == query:
                messagebox.showinfo("搜索结果", f"找到的文件：{file}")
                return

        messagebox.showinfo("搜索结果", "未找到匹配的文件编号。")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.geometry("800x600")
    root.mainloop()
