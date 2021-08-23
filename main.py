#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created on 2021年08月20日
@author: hejian
@contact: 1048891020@qq.com
"""
from choose_path_tool import *
from deal_project_tool import *


if __name__ == '__main__':
    project_dir = ChoosePathTool.choose_path()
    DealProjectFile.deal_project(project_dir)