# -*- coding:utf-8 -*-

import os
import sys
import json
import subprocess

icons_floder = "./icons"
toolbox_install_folder = "~/Library/Application\ Support/JetBrains/Toolbox/apps/"

config = {}

with open("./replacement.json", "r") as f:
    config = json.load(f)

# TODO: 自动将最新的ToolBox安装的IDE路径配置到replacement.json中

for path, value in config.items():
    path = path.replace(" ", "\\ ")
    if isinstance(value, str):
        pass
    if isinstance(value, dict):
        for app_name, replacement in value.items():
            # 路径中空格需要转移 空格 -> \空格
            app_name_with_escapes = app_name.replace(" ", "\\ ")
            app_path = f"{path}/{app_name_with_escapes}.app"
            replacement_path = f"{icons_floder}/{replacement}.icns"
            print(f"replacing {app_name} icon ...")

            command = f"sudo fileicon set {app_path} {replacement_path}"
            status, output = subprocess.getstatusoutput(command)
            if status != 0:
                print(f"failed to replace icon for {app_name}, err: {output}")
                print(f"execute command: {command}")
                sys.exit(0)

print("finish")


