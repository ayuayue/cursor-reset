# 充值账户管理工具

## 功能
- 浏览器登录链接跳转
- 输入 Cookie
- 删除账户
- 查询用量
- 一键重置机器码

## 运行
```bash
pip install -r requirements.txt
python main.py
```

## 打包为 exe
```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --windowed --name cursor-set main.py
```

打包完成后，可执行文件位于 `dist` 目录下，文件名为 `cursor-set.exe`。 