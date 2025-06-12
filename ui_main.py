from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import utils

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cursor账户管理工具')
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 1. 标题
        title = QLabel('Cursor账户管理工具')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(title)

        # 2. 登录链接
        login_btn = QPushButton('点击跳转浏览器登录')
        login_btn.clicked.connect(lambda: utils.open_login_url('https://www.cursor.com/cn/dashboard'))
        layout.addWidget(login_btn)

        # 3. 输入 Cookie
        cookie_label = QLabel('请输入从浏览器获取到的 Cookie:')
        self.cookie_input = QTextEdit()
        self.cookie_input.setPlaceholderText('在此粘贴 Cookie...')
        # 加载保存的 cookie
        self.cookie_input.setText(utils.load_cookie())
        # 监听输入变化，保存 cookie
        self.cookie_input.textChanged.connect(self.save_cookie)
        layout.addWidget(cookie_label)
        layout.addWidget(self.cookie_input)

        # 4. 删除账户
        del_btn = QPushButton('删除账户')
        del_btn.setStyleSheet('background-color: #ff6b6b; color: white;')
        del_btn.clicked.connect(self.delete_account)
        layout.addWidget(del_btn)

        # 5. 重置机器码
        reset_btn = QPushButton('一键重置机器码')
        reset_btn.clicked.connect(self.reset_machine_code)
        layout.addWidget(reset_btn)

        # 6. 查询用量
        usage_btn = QPushButton('查询用量')
        usage_btn.clicked.connect(self.query_usage)
        layout.addWidget(usage_btn)

        # 7. 一键查询机器码
        query_machine_btn = QPushButton('一键查询机器码')
        query_machine_btn.clicked.connect(self.query_machine_code)
        layout.addWidget(query_machine_btn)

        # 结果显示
        self.result_label = QLabel('')
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet('font-family: monospace;')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def save_cookie(self):
        cookie = self.cookie_input.toPlainText().strip()
        utils.save_cookie(cookie)

    def get_cookie(self):
        return self.cookie_input.toPlainText().strip()

    def delete_account(self):
        cookie = self.get_cookie()
        if not cookie:
            QMessageBox.warning(self, '提示', '请先输入 Cookie')
            return
        QMessageBox.warning(self, '提示', '请先关闭 Cursor 后再尝试删除账户，否则可能不生效。')
        try:
            status_code, result = utils.delete_account(cookie)
            if status_code == 200:
                QMessageBox.information(self, '提示', '删除账户成功，请重新登录获取 Cookie')
                self.cookie_input.clear()
            else:
                self.result_label.setText(f'删除账户失败: {result}')
        except Exception as e:
            self.result_label.setText(f'删除账户失败: {e}')

    def query_usage(self):
        cookie = self.get_cookie()
        if not cookie:
            QMessageBox.warning(self, '提示', '请先输入 Cookie')
            return
        try:
            result = utils.query_usage(cookie)
            # 美化输出
            formatted_result = '查询用量结果:\n'
            for model, data in result.items():
                if model != 'startOfMonth':
                    formatted_result += f'\n{model}:\n'
                    for key, value in data.items():
                        formatted_result += f'  {key}: {value}\n'
            formatted_result += f'\n开始时间: {result.get("startOfMonth", "N/A")}'
            self.result_label.setText(formatted_result)
        except Exception as e:
            self.result_label.setText(f'查询用量失败: {e}')

    def reset_machine_code(self):
        QMessageBox.warning(self, '提示', '请先关闭 Cursor 后再尝试重置，否则可能不生效。')
        try:
            new_machine_code = utils.reset_machine_code()
            self.result_label.setText(f'重置机器码成功，新机器码: {new_machine_code}')
            QMessageBox.information(self, '提示', '重置成功，请退出账户重新登录。')
        except Exception as e:
            self.result_label.setText(f'重置机器码失败: {e}')

    def query_machine_code(self):
        try:
            current_machine_code = utils.get_current_machine_code()
            self.result_label.setText(f'当前机器码: {current_machine_code}')
        except Exception as e:
            self.result_label.setText(f'查询机器码失败: {e}') 