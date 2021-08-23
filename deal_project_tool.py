import re
import fileinput
from pods_dot_h_array import *
from pods_path_tool import *


class DealProjectFile(object):

    @staticmethod
    def deal_project(project_path):
        # 预编译正则
        import_dot_hfile = re.compile(r'#import[\s]*["|<][\w\.\+]+\.h["|>]')
        dot_hfile = re.compile(r'[\w]+[\w\.\+]+\.h')

        # 获取pods库数组和项目路径
        pods_import = PodsDotHArray.get_pods_h_files(project_path)
        is_module, search_path = PodsPathTool.instance().search_path()

        # 类文件所在的目录
        if is_module:
            class_path = f"{project_path}/{search_path}/Classes"
        else:
            class_path = ''

        for root, _, files in os.walk(class_path):
            for file in files:
                # 过滤除了.h&.m的文件
                if not file.endswith('.h') and not file.endswith('.m'):
                    continue

                DealProjectFile.deal_file_with_handler(root, file, import_dot_hfile, dot_hfile, pods_import)

        print('文件处理完成')

    @staticmethod
    def deal_file_with_handler(root, file, import_dot_hfile, dot_hfile, pods_import):
        print(f'正在处理：{file}')

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