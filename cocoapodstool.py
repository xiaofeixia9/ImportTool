import os


class CocoaPodsTool(object):

    @staticmethod
    def pod_update_with_path(pod_dir):
        os.chdir(pod_dir)
        os.system('pod update')

        # 检查Podfile.lock文件是否生成，如果生成标明操作成功
        podfile_lock_exist = os.path.isfile(os.path.join(pod_dir, 'Podfile.lock'))
        return podfile_lock_exist
