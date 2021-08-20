import tkinter as tk
from tkinter import filedialog
import getpass


class ChoosePathTool(object):

    @staticmethod
    def choose_path():
        # 获取项目地址
        root = tk.Tk()
        root.withdraw()

        default_folder = f"/Users/{getpass.getuser()}/Documents"
        project_path = filedialog.askdirectory(initialdir=default_folder, title="选择项目路径")
        return project_path
