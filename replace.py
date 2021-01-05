# -*- coding:utf-8 -*-

import os
import sys
import json
import subprocess

icons_floder = "./icons"

replace_config = "./replace.config.json"

# ~ -> /Users/qgaye
def handle_expanduser(path):
    return os.path.expanduser(path)

# 空格 -> \空格
def handle_escape(path):
    return path.replace(" ", "\\ ")

# regex: str
# paths: [str]
def handle_regex(paths):
    has_replaced = False
    new_paths = paths[:]
    for regex in paths:
        start = -1
        end = -1;
        for i in range(len(regex)):
            if regex[i] == '{':
                start = i
            if regex[i] == '}' and start != -1:
                has_replaced = True
                new_paths.remove(regex)
                end = i
                prefix = regex[0 : start]
                replace_place = regex[start : end + 1] 
                suffix = regex[end + 1 : len(regex)]
                solve_replace_place(prefix, replace_place, suffix, new_paths)
    if has_replaced:
        return handle_regex(new_paths)
    return new_paths

def solve_replace_place(prefix, replace_place, suffix, new_paths):
    if replace_place[1 : -1] == "*":
        files = os.listdir(prefix)
        for file in files:
            if os.path.isdir(f"{prefix}{file}"):
                new_paths.append(f"{prefix}{file}{suffix}")

def execute_replace(app_path, replace_icon):
    app_path = f"{handle_escape(app_path)}.app"
    replace_icon_path = f"{icons_floder}/{replace_icon}.icns"
    print(f"replacing {app_name} icon ...")

    command = f"sudo fileicon set {app_path} {replace_icon_path}"
    # print(command)
    status, output = subprocess.getstatusoutput(command)
    if status != 0:
        print(f"failed to replace icon for {app_name}, err: {output}")
        print(f"execute command: {command}")
        sys.exit(0)

if __name__ == "__main__":
    config = {}

    with open(replace_config, "r") as f:
        config = json.load(f)

    for path, value in config.items():
        if isinstance(value, str):
            pass
        if isinstance(value, dict):
            for app_name, replace_icon in value.items():
                app_paths = f"{handle_expanduser(path)}/{app_name}"
                for app_path in handle_regex([app_paths]):
                    execute_replace(app_path, replace_icon)

    print("finish")


