import sys

from cocoapodstool import *


class PodsPathTool(object):
    __search_paths = []  # 当前处理的模块名称

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
            directors = [x for x in files if os.path.isdir(os.path.join(project_path, x)) is True]
            print(directors)

            pass
        else:
            podspec_file = [x for x in files if x.find('.podspec') != -1]
            if podspec_file is None or len(podspec_file) == 0:
                raise FileNotFoundError('未找到当前项目的Podfile或者.podspec文件')

            # 处理模块包
            podspec_array = podspec_file[0].split('.')

            self.__search_paths.append(podspec_array[0])

            # 获取pods所有库文件
            pods_path = f"{project_path}/Example/Pods"
            profile_path = f'{project_path}/Example'

        # 如果没有发现Pods库，执行以下pod update操作
        if not os.path.exists(pods_path):
            pod_update_succeed = CocoaPodsTool.pod_update_with_path(profile_path)
            if not pod_update_succeed:
                raise ValueError('pod update不成功，请检查一下Podfile是否正确')

        return pods_path

    def search_path(self):
        """
        返回需要边路的路径
        :return: 返回一个元祖，第一个参数表示是否是模块，第二个参数表示查找路径
        """
        if len(self.__search_paths) > 1:
            return True, self.__search_paths
        else:
            return False, self.__search_paths
