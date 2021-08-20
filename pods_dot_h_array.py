import os
from pods_path_tool import *


class PodsDotHArray(object):

    @staticmethod
    def get_pods_h_files(project_path):
        # 获取pods路径
        pods_path = PodsPathTool.instance().get_pods_path(project_path)
        files = os.listdir(pods_path)

        # 生成一个{'pod名称'=>['xx.h'...]}这样格式的字典
        pods_dot_h = {}
        for dir_name in files:
            if dir_name == 'Headers':
                continue
            dir_path = os.path.join(pods_path, dir_name)

            if os.path.isdir(dir_path) and not dir_name.endswith('xcodeproj'):
                dot_h_array = []
                for _, _, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.h'):
                            dot_h_array.append(file)

                pods_dot_h[dir_name] = dot_h_array

        # 重新整理pods_dot_h字典，将字典转为{'xx.h'=>'pod名称/xx.h'}这样的格式字典
        pods_import = {}
        for key in pods_dot_h:
            for value in pods_dot_h[key]:
                pods_import[value] = f"{key}/{value}"

        return pods_import
