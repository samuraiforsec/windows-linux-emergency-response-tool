from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QPushButton)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("服务器登录")
        self.setModal(True)
        
        # 创建布局
        layout = QVBoxLayout()
        
        # 服务器类型选择
        type_layout = QHBoxLayout()
        type_label = QLabel("服务器类型:")
        self.server_type_combo = QComboBox()
        self.server_type_combo.addItems(["Linux", "Windows"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.server_type_combo)
        layout.addLayout(type_layout)
        
        # 主机名/IP输入
        host_layout = QHBoxLayout()
        host_label = QLabel("主机名/IP:")
        self.hostname_input = QLineEdit()
        host_layout.addWidget(host_label)
        host_layout.addWidget(self.hostname_input)
        layout.addLayout(host_layout)
        
        # 端口输入
        port_layout = QHBoxLayout()
        port_label = QLabel("端口:")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("SSH:22 / RDP:3389")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)
        
        # 用户名输入
        username_layout = QHBoxLayout()
        username_label = QLabel("用户名:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # 密码输入
        password_layout = QHBoxLayout()
        password_label = QLabel("密码:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.connect_button = QPushButton("连接")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 连接信号
        self.connect_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.server_type_combo.currentTextChanged.connect(self.on_server_type_changed)
        
    def on_server_type_changed(self, server_type):
        """当服务器类型改变时更新端口默认值"""
        if server_type == "Linux":
            self.port_input.setPlaceholderText("22")
        else:
            self.port_input.setPlaceholderText("3389") 