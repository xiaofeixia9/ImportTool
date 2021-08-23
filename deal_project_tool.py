#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created on 2021年08月20日
@author: hejian
@contact: 1048891020@qq.com
"""
import re
import fileinput
from pods_dot_h_array import *
from pods_path_tool import *


class DealProjectFile(object):

    @classmethod
    def deal_project(cls, project_path):
        # 预编译正则
        import_dot_hfile = re.compile(r'#import[\s]*["|<][\w\.\+]+\.h["|>]')
        dot_hfile = re.compile(r'[\w]+[\w\.\+]+\.h')

        # 获取pods库数组和项目路径
        pods_import = PodsDotHArray.get_pods_h_files(project_path)
        search_paths = PodsPathTool.instance().search_path()

        if search_paths is None:
            return

        # 处理文件夹
        for path in search_paths:
            DealProjectFile.deal_path(path, import_dot_hfile, dot_hfile, pods_import)

        print('文件处理完成')

    @classmethod
    def deal_path(cls, path, import_dot_hfile, dot_hfile, pods_import):
        for root, _, files in os.walk(path):
            for file in files:
                # 过滤除了.h&.m的文件
                if not file.endswith('.h') and not file.endswith('.m'):
                    continue

                DealProjectFile.deal_file_with_handler(root, file, import_dot_hfile, dot_hfile, pods_import)

    @classmethod
    def deal_file_with_handler(cls, root, file, import_dot_hfile, dot_hfile, pods_import):
        print(f'正在遍历：{file}')

        path_file_name = os.path.join(root, file)
        finput = fileinput.input([path_file_name], inplace=True, backup='.bak')
        try:
            for line in finput:
                match = import_dot_hfile.search(line)
                if match:
                    old_str = match.group()
                    import_name = dot_hfile.search(old_str).group()
                    if import_name in pods_import:
                        new_str = f"#import <{pods_import[import_name]}>"
                        line = line.replace(old_str, new_str)
                sys.stdout.write(line)
        except UnicodeDecodeError:
            # 用备份文件替代原始文件
            rename_file_name = "%s.bak" % path_file_name
            if os.path.exists(rename_file_name):
                os.rename(rename_file_name, path_file_name)
        finally:
            finput.close()

            # 删除备份文件
            rename_file_name = "%s.bak" % path_file_name
            if os.path.exists(rename_file_name):
                os.remove(rename_file_name)