from choose_path_tool import *
from deal_project_tool import *


if __name__ == '__main__':
    project_dir = ChoosePathTool.choose_path()
    DealProjectFile.deal_project(project_dir)