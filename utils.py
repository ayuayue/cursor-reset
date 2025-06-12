import webbrowser
import requests
import re
import json
import os
import uuid
import subprocess

# 打开登录链接
def open_login_url(url):
    webbrowser.open(url)

# 删除账户接口
def delete_account(cookie):
    url = 'https://www.cursor.com/api/dashboard/delete-account'
    headers = {'Cookie': cookie}
    response = requests.post(url, headers=headers)
    return response.status_code, response.json()

# 查询用量接口
def query_usage(cookie):
    # 从 cookie 中提取 user 信息
    user_match = re.search(r'user_([A-Z0-9]+)', cookie)
    user = user_match.group(0) if user_match else None
    if not user:
        raise ValueError('无法从 cookie 中提取 user 信息')
    url = 'https://www.cursor.com/api/usage'
    headers = {'Cookie': cookie}
    params = {'user': user}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 查看当前机器码
def get_current_machine_code():
    try:
        # 从注册表获取 MachineGuid
        cmd = 'powershell -Command "(Get-ItemProperty -Path \'HKLM:\\SOFTWARE\\Microsoft\\Cryptography\' -Name MachineGuid).MachineGuid"'
        result = subprocess.check_output(cmd, shell=True).decode().strip()
        return result
    except Exception as e:
        return f"获取机器码失败: {e}"

# 重置机器码
def reset_machine_code():
    try:
        # 生成新的 MachineGuid
        new_guid = str(uuid.uuid4())
        # 使用 PowerShell 更新注册表
        cmd = f'powershell -Command "Set-ItemProperty -Path \'HKLM:\\SOFTWARE\\Microsoft\\Cryptography\' -Name MachineGuid -Value \'{new_guid}\'"'
        subprocess.run(cmd, shell=True, check=True)
        # 保存到本地文件
        with open('machine_code.json', 'w') as f:
            json.dump({'machine_code': new_guid}, f)
        return new_guid
    except Exception as e:
        return f"重置机器码失败: {e}"

# 保存 cookie 到文件
def save_cookie(cookie):
    with open('cookie.json', 'w') as f:
        json.dump({'cookie': cookie}, f)

# 加载 cookie 从文件
def load_cookie():
    if os.path.exists('cookie.json'):
        with open('cookie.json', 'r') as f:
            data = json.load(f)
            return data.get('cookie', '')
    return '' 