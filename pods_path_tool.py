#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created on 2021年08月20日
@author: hejian
@contact: 1048891020@qq.com
"""
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

        if 'Podfile' in files:
            # 工程项目包
            search_directors = []
            for file in files:
                if os.path.isdir(os.path.join(project_path, file)) and file.find('.') == -1 and file.find('Pods') == -1:
                    search_path = f"{project_path}/{file}"
                    search_directors.append(search_path)

            self.__search_paths = search_directors

            # 获取pods所有库文件
            pods_path = f"{project_path}/Pods"
            profile_path = project_path
        else:
            podspec_file = [x for x in files if x.find('.podspec') != -1]
            if podspec_file is None or len(podspec_file) == 0:
                raise FileNotFoundError('未找到当前项目的Podfile或者.podspec文件')

            # 处理模块包
            podspec_array = podspec_file[0].split('.')

            search_path = f"{project_path}/{podspec_array[0]}/Classes"
            self.__search_paths.append(search_path)

            # 获取pods所有库文件
            pods_path = f"{project_path}/Example/Pods"
            profile_path = f'{project_path}/Example'

        PodsPathTool.update_pods(pods_path, profile_path)

        return pods_path

    @classmethod
    def update_pods(cls, pods_path, profile_path):
        # 如果没有发现Pods库，执行以下pod update操作
        if not os.path.exists(pods_path):
            pod_update_succeed = CocoaPodsTool.pod_update_with_path(profile_path)
            if not pod_update_succeed:
                raise ValueError('pod update不成功，请检查一下Podfile是否正确')

    def search_path(self):
        """
        返回需要边路的路径
        :return: 需要遍历的路径
        """
        return self.__search_paths
