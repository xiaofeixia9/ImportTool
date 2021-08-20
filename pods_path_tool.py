import sys

from cocoapodstool import *


class PodsPathTool(object):
    __module_name = ''  # 当前处理的模块名称

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(PodsPathTool, "_instance"):
            PodsPathTool._instance = PodsPathTool(*args, **kwargs)
        return PodsPathTool._instance

    def get_pods_path(self, project_path):
        # 获取项目地址

        if not os.path.exists(project_path):
            raise FileNotFoundError('请选择一个已存在的项目')

        try:
            files = os.listdir(project_path)
        except FileNotFoundError:
            print('请选择一个已存在的项目')
            sys.exit()

        podfile = [x for x in files if x.find('Podfile') != -1]
        if podfile is not None and len(podfile) > 0:
            # 工程项目包
            pods_path = f"{project_path}/Pods"
            profile_path = project_path

            pass
        else:
            podspec_file = [x for x in files if x.find('.podspec') != -1]
            if podspec_file is None or len(podspec_file) == 0:
                raise ValueError('未找到当前项目的Podfile或者.podspec文件')

            # 处理模块包
            podspec_array = podspec_file[0].split('.')

            self.__module_name = podspec_array[0]

            if self.__module_name not in files:
                raise ValueError(f"请选择{self.__module_name}模块的项目")

            # 获取pods所有库文件
            pods_path = f"{project_path}/Example/Pods"
            profile_path = f'{project_path}/Example'

        # 如果没有发现Pods库，执行以下pod update操作
        if not os.path.exists(pods_path):
            pod_update_succeed = CocoaPodsTool.pod_update_with_path(profile_path)
            if not pod_update_succeed:
                raise ValueError('pod update不成功，请检查一下Podfile是否正确')

        return pods_path

    def module_name(self):
        return self.__module_name
