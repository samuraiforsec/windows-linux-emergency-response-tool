from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QTreeWidget, 
                             QTreeWidgetItem, QLabel, QComboBox, QLineEdit, 
                             QDialog, QFileDialog, QMessageBox, QGroupBox,
                             QSplitter, QStatusBar, QAction, QMenu)
from PyQt5.QtCore import Qt, QSize
import os
import tempfile

from core.server_connector import ServerConnector
from core.linux_analyzer import LinuxAnalyzer
from core.windows_analyzer import WindowsAnalyzer
from ui.login_dialog import LoginDialog
from ui.result_viewer import ResultViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Windows和Linux应急响应工具 v1.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化服务器连接器和分析器
        self.server_connector = ServerConnector()
        self.linux_analyzer = LinuxAnalyzer(self.server_connector)
        self.windows_analyzer = WindowsAnalyzer(self.server_connector)
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 添加永久消息（作者信息）
        author_label = QLabel("作者: Andy | 邮箱: andyforsec@gmail.com")
        self.status_bar.addPermanentWidget(author_label)
        
        # 添加临时消息区域
        self.status_message = QLabel("就绪")
        self.status_bar.addWidget(self.status_message)
        
        # 创建分割器
        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)
        
        # 左侧控制面板
        self.control_panel = QWidget()
        self.control_layout = QVBoxLayout(self.control_panel)
        
        # 连接状态
        self.connection_group = QGroupBox("连接状态")
        self.connection_layout = QVBoxLayout()
        self.connection_status = QLabel("未连接")
        self.connection_info = QLabel("")
        self.connection_layout.addWidget(self.connection_status)
        self.connection_layout.addWidget(self.connection_info)
        self.connection_group.setLayout(self.connection_layout)
        self.control_layout.addWidget(self.connection_group)
        
        # 命令执行区域
        self.command_group = QGroupBox("命令执行")
        self.command_layout = QVBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("输入命令...")
        self.command_input.returnPressed.connect(self.execute_command)  # 按回车执行命令
        self.execute_button = QPushButton("执行")
        self.execute_button.clicked.connect(self.execute_command)
        self.command_layout.addWidget(self.command_input)
        self.command_layout.addWidget(self.execute_button)
        self.command_group.setLayout(self.command_layout)
        self.control_layout.addWidget(self.command_group)
        
        # 功能按钮区域
        self.function_group = QGroupBox("服务器分析功能")
        self.function_layout = QVBoxLayout()
        
        # 基本信息按钮
        self.basic_info_button = QPushButton("获取基本信息")
        self.basic_info_button.clicked.connect(self.get_basic_info)
        self.function_layout.addWidget(self.basic_info_button)
        
        # 用户信息按钮
        self.user_info_button = QPushButton("获取用户信息")
        self.user_info_button.clicked.connect(self.get_user_info)
        self.function_layout.addWidget(self.user_info_button)
        
        # 网络信息按钮
        self.network_info_button = QPushButton("获取网络信息")
        self.network_info_button.clicked.connect(self.get_network_info)
        self.function_layout.addWidget(self.network_info_button)
        
        # 进程信息按钮
        self.process_info_button = QPushButton("获取进程信息")
        self.process_info_button.clicked.connect(self.get_process_info)
        self.function_layout.addWidget(self.process_info_button)
        
        # 启动项信息按钮
        self.startup_info_button = QPushButton("获取启动项信息")
        self.startup_info_button.clicked.connect(self.get_startup_info)
        self.function_layout.addWidget(self.startup_info_button)
        
        # Web服务信息按钮
        self.web_info_button = QPushButton("获取Web服务信息")
        self.web_info_button.clicked.connect(self.get_web_service_info)
        self.function_layout.addWidget(self.web_info_button)
        
        # 域信息按钮（仅Windows）
        self.domain_info_button = QPushButton("获取域信息")
        self.domain_info_button.clicked.connect(self.get_domain_info)
        self.function_layout.addWidget(self.domain_info_button)
        
        # 预定义脚本区域
        self.script_group = QGroupBox("预定义脚本")
        self.script_layout = QVBoxLayout()
        
        # 系统信息脚本按钮
        self.system_info_script_button = QPushButton("运行系统信息脚本")
        self.system_info_script_button.clicked.connect(self.run_system_info_script)
        self.script_layout.addWidget(self.system_info_script_button)
        
        # 安全检查脚本按钮
        self.security_check_script_button = QPushButton("运行安全检查脚本")
        self.security_check_script_button.clicked.connect(self.run_security_check_script)
        self.script_layout.addWidget(self.security_check_script_button)
        
        # 上传脚本按钮
        self.upload_script_button = QPushButton("上传并运行自定义脚本")
        self.upload_script_button.clicked.connect(self.upload_script)
        self.script_layout.addWidget(self.upload_script_button)
        
        self.script_group.setLayout(self.script_layout)
        self.function_layout.addWidget(self.script_group)
        
        self.function_group.setLayout(self.function_layout)
        self.control_layout.addWidget(self.function_group)
        
        # 添加拉伸因子
        self.control_layout.addStretch(1)
        
        # 添加控制面板到分割器
        self.splitter.addWidget(self.control_panel)
        
        # 右侧结果显示区域
        self.result_viewer = ResultViewer()
        self.splitter.addWidget(self.result_viewer)
        
        # 设置分割器比例
        self.splitter.setSizes([300, 900])
        
        # 初始禁用所有功能按钮
        self.set_buttons_enabled(False)

    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 连接动作
        connect_action = QAction("连接", self)
        connect_action.setShortcut("Ctrl+N")
        connect_action.triggered.connect(self.show_login_dialog)
        file_menu.addAction(connect_action)
        
        # 断开连接动作
        disconnect_action = QAction("断开连接", self)
        disconnect_action.setShortcut("Ctrl+D")
        disconnect_action.triggered.connect(self.disconnect)
        file_menu.addAction(disconnect_action)
        
        file_menu.addSeparator()
        
        # 保存结果动作
        save_action = QAction("保存结果", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        
        # 刷新动作
        refresh_action = QAction("刷新", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_current_view)
        view_menu.addAction(refresh_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        # 关于动作
        about_action = QAction("关于", self)
        about_action.setShortcut("F1")  # 添加快捷键
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar("主工具栏")
        toolbar.setIconSize(QSize(16, 16))
        
        # 连接按钮
        connect_action = QAction("连接", self)
        connect_action.triggered.connect(self.show_login_dialog)
        toolbar.addAction(connect_action)
        
        # 断开连接按钮
        disconnect_action = QAction("断开连接", self)
        disconnect_action.triggered.connect(self.disconnect)
        toolbar.addAction(disconnect_action)
        
        toolbar.addSeparator()
        
        # 刷新按钮
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.refresh_current_view)
        toolbar.addAction(refresh_action)
        
        # 保存按钮
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_results)
        toolbar.addAction(save_action)

    def show_login_dialog(self):
        """显示登录对话框"""
        dialog = LoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            server_type = dialog.server_type_combo.currentText()
            hostname = dialog.hostname_input.text()
            port_text = dialog.port_input.text()
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            
            # 验证输入
            if not hostname:
                QMessageBox.warning(self, "输入错误", "请输入主机名/IP")
                return
                
            if not username:
                QMessageBox.warning(self, "输入错误", "请输入用户名")
                return
                
            if not password:
                QMessageBox.warning(self, "输入错误", "请输入密码")
                return
                
            # 设置默认端口
            if not port_text:
                if server_type == "Linux":
                    port = 22
                else:
                    port = 3389
            else:
                try:
                    port = int(port_text)
                except ValueError:
                    QMessageBox.warning(self, "输入错误", "端口必须是数字")
                    return
            
            # 执行连接
            self.set_status_message(f"正在连接到 {hostname}...")
            if server_type == "Linux":
                success, message = self.server_connector.connect_ssh(hostname, username, password, port)
            else:
                success, message = self.server_connector.connect_rdp(hostname, username, password, port)
                
            if success:
                self.set_status_message(f"已连接到 {hostname}")
                self.connection_status.setText(f"已连接 ({server_type})")
                self.connection_info.setText(f"主机名: {hostname}\n用户名: {username}")
                self.set_buttons_enabled(True)
                
                # 根据服务器类型启用/禁用特定功能
                if server_type == "Windows":
                    # 对于Windows，启用域信息按钮
                    self.domain_info_button.setEnabled(True)
                    # 对于Windows，可能需要禁用一些Linux特有功能
                    pass  # 没有特定的Linux功能需要禁用
                # 对于Linux，禁用Windows特有功能
                else:
                    self.domain_info_button.setEnabled(False)
            else:
                QMessageBox.critical(self, "连接失败", message)

    def disconnect(self):
        """断开连接"""
        success, message = self.server_connector.disconnect()
        if success:
            self.set_status_message("已断开连接")
            self.connection_status.setText("未连接")
            self.connection_info.setText("")
            self.set_buttons_enabled(False)
        else:
            QMessageBox.warning(self, "断开失败", message)

    def set_buttons_enabled(self, enabled):
        """启用或禁用功能按钮"""
        self.execute_button.setEnabled(enabled)
        self.basic_info_button.setEnabled(enabled)
        self.user_info_button.setEnabled(enabled)
        self.network_info_button.setEnabled(enabled)
        self.process_info_button.setEnabled(enabled)
        self.startup_info_button.setEnabled(enabled)
        self.web_info_button.setEnabled(enabled)
        self.domain_info_button.setEnabled(enabled)
        self.upload_script_button.setEnabled(enabled)
        self.system_info_script_button.setEnabled(enabled)
        self.security_check_script_button.setEnabled(enabled)

    def execute_command(self):
        """执行命令"""
        command = self.command_input.text()
        if not command:
            return
        
        self.set_status_message(f"执行命令: {command}")
        success, result = self.server_connector.execute_command(command)
        if success:
            output = result.get("output", "")
            error = result.get("error", "")
            
            if output:
                self.result_viewer.set_text_result(output)
            if error:
                current_text = self.result_viewer.text_edit.toPlainText()
                self.result_viewer.set_text_result(current_text + "\n\n错误输出:\n" + error)
            
            self.set_status_message("命令执行完成")
        else:
            QMessageBox.warning(self, "命令执行失败", result)
            self.set_status_message("命令执行失败")

    def upload_script(self):
        """上传脚本"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择脚本文件", "", "所有文件 (*)")
        if not file_path:
            return
        
        remote_path, ok = QtWidgets.QInputDialog.getText(self, "远程路径", "请输入远程路径:")
        if not ok or not remote_path:
            return
        
        self.set_status_message(f"正在上传脚本...")
        success, message = self.server_connector.upload_script(file_path, remote_path)
        if success:
            self.set_status_message("脚本上传成功")
            
            # 询问是否执行脚本
            reply = QMessageBox.question(self, "执行脚本", "是否执行上传的脚本?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.run_uploaded_script(remote_path)
        else:
            self.set_status_message("脚本上传失败")
            QMessageBox.warning(self, "上传失败", message)

    def run_uploaded_script(self, script_path):
        """运行已上传的脚本"""
        if self.server_connector.server_type == "linux":
            # 为Linux脚本添加执行权限
            self.server_connector.execute_command(f"chmod +x {script_path}")
            success, result = self.server_connector.execute_command(script_path)
        else:
            # 执行Windows脚本
            if script_path.lower().endswith('.ps1'):
                success, result = self.server_connector.execute_command(f"powershell -ExecutionPolicy Bypass -File {script_path}")
            else:
                success, result = self.server_connector.execute_command(script_path)
        
        if success:
            output = result.get("output", "")
            error = result.get("error", "")
            
            if output:
                self.result_viewer.set_text_result(output)
            if error:
                current_text = self.result_viewer.text_edit.toPlainText()
                self.result_viewer.set_text_result(current_text + "\n\n错误输出:\n" + error)
            
            self.set_status_message("脚本执行完成")
        else:
            QMessageBox.warning(self, "脚本执行失败", result)
            self.set_status_message("脚本执行失败")

    def run_system_info_script(self):
        """运行系统信息脚本"""
        if not self.server_connector.server_type:
            QMessageBox.warning(self, "错误", "请先连接到服务器")
            return
        
        # 创建远程目录用于存放脚本
        remote_dir = "/tmp" if self.server_connector.server_type == "linux" else "C:\\Windows\\Temp"
        
        if self.server_connector.server_type == "linux":
            script_name = "system_info.sh"
            remote_path = f"{remote_dir}/{script_name}"
            with open("scripts/linux/system_info.sh", "r") as f:
                script_content = f.read()
        else:  # Windows
            script_name = "system_info.ps1"
            remote_path = f"{remote_dir}\\{script_name}"
            with open("scripts/windows/system_info.ps1", "r") as f:
                script_content = f.read()
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.'+script_name.split('.')[-1]) as temp:
            temp.write(script_content)
            temp_file_path = temp.name
        
        # 上传脚本
        self.set_status_message(f"正在上传系统信息脚本...")
        success, message = self.server_connector.upload_script(temp_file_path, remote_path)
        
        # 删除临时文件
        os.unlink(temp_file_path)
        
        if success:
            self.set_status_message("系统信息脚本已上传，准备执行...")
            self.run_uploaded_script(remote_path)
        else:
            self.set_status_message("系统信息脚本上传失败")
            QMessageBox.warning(self, "上传失败", message)

    def run_security_check_script(self):
        """运行安全检查脚本"""
        if not self.server_connector.server_type:
            QMessageBox.warning(self, "错误", "请先连接到服务器")
            return
        
        # 创建远程目录用于存放脚本
        remote_dir = "/tmp" if self.server_connector.server_type == "linux" else "C:\\Windows\\Temp"
        
        if self.server_connector.server_type == "linux":
            script_name = "security_check.sh"
            remote_path = f"{remote_dir}/{script_name}"
            with open("scripts/linux/security_check.sh", "r") as f:
                script_content = f.read()
        else:  # Windows
            script_name = "security_check.ps1"
            remote_path = f"{remote_dir}\\{script_name}"
            with open("scripts/windows/security_check.ps1", "r") as f:
                script_content = f.read()
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.'+script_name.split('.')[-1]) as temp:
            temp.write(script_content)
            temp_file_path = temp.name
        
        # 上传脚本
        self.set_status_message(f"正在上传安全检查脚本...")
        success, message = self.server_connector.upload_script(temp_file_path, remote_path)
        
        # 删除临时文件
        os.unlink(temp_file_path)
        
        if success:
            self.set_status_message("安全检查脚本已上传，准备执行...")
            self.run_uploaded_script(remote_path)
        else:
            self.set_status_message("安全检查脚本上传失败")
            QMessageBox.warning(self, "上传失败", message)

    def save_results(self):
        """保存结果"""
        self.result_viewer.save_results()

    def refresh_current_view(self):
        """刷新当前视图"""
        # 获取当前显示的信息类型并重新获取
        if not self.server_connector.server_type:
            return
            
        current_tab = self.result_viewer.tabs.currentWidget()
        current_tab_text = self.result_viewer.tabs.tabText(self.result_viewer.tabs.currentIndex())
        
        if current_tab_text == "文本视图":
            # 如果是命令输出，重新执行上一次的命令
            command = self.command_input.text()
            if command:
                self.execute_command()
        else:
            # 根据当前视图内容重新获取相应信息
            title = "刷新成功"
            if "基本信息" in title:
                self.get_basic_info()
            elif "用户信息" in title:
                self.get_user_info()
            elif "网络信息" in title:
                self.get_network_info()
            elif "进程信息" in title:
                self.get_process_info()
            elif "启动项信息" in title:
                self.get_startup_info()
            elif "Web服务信息" in title:
                self.get_web_service_info()
            elif "域信息" in title:
                self.get_domain_info()
                
        self.set_status_message("视图已刷新")

    def show_about_dialog(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于", 
                         "Windows和Linux应急响应工具 v1.0\n\n"
                         "作者: Andy\n"
                         "邮箱: andyforsec@gmail.com\n\n"
                         "一个用于快速分析Windows和Linux服务器安全状况的工具。\n"
                         "支持远程登录服务器，执行安全检查，分析系统状态，\n"
                         "适用于应急响应场景。")

    def get_basic_info(self):
        """获取基本信息"""
        self.set_status_message("获取基本信息中...")
        if self.server_connector.server_type == "linux":
            results = self.linux_analyzer.get_basic_info()
        else:
            results = self.windows_analyzer.get_basic_info()
        
        self.result_viewer.set_tree_result("基本信息", results)
        self.set_status_message("基本信息获取完成")

    def get_user_info(self):
        """获取用户信息"""
        self.set_status_message("获取用户信息中...")
        if self.server_connector.server_type == "linux":
            results = self.linux_analyzer.get_user_info()
        else:
            results = self.windows_analyzer.get_user_info()
        
        self.result_viewer.set_tree_result("用户信息", results)
        self.set_status_message("用户信息获取完成")

    def get_network_info(self):
        """获取网络信息"""
        self.set_status_message("获取网络信息中...")
        if self.server_connector.server_type == "linux":
            results = self.linux_analyzer.get_network_info()
        else:
            results = self.windows_analyzer.get_network_info()
        
        self.result_viewer.set_tree_result("网络信息", results)
        self.set_status_message("网络信息获取完成")

    def get_process_info(self):
        """获取进程信息"""
        self.set_status_message("获取进程信息中...")
        if self.server_connector.server_type == "linux":
            results = self.linux_analyzer.get_process_info()
        else:
            results = self.windows_analyzer.get_process_info()
        
        self.result_viewer.set_tree_result("进程信息", results)
        self.set_status_message("进程信息获取完成")

    def get_startup_info(self):
        """获取启动项信息"""
        self.set_status_message("获取启动项信息中...")
        if self.server_connector.server_type == "linux":
            results = self.linux_analyzer.get_startup_info()
        else:
            results = self.windows_analyzer.get_startup_info()
        
        self.result_viewer.set_tree_result("启动项信息", results)
        self.set_status_message("启动项信息获取完成")

    def get_web_service_info(self):
        """获取Web服务信息"""
        self.set_status_message("获取Web服务信息中...")
        if self.server_connector.server_type == "linux":
            results = self.linux_analyzer.get_web_service_info()
        else:
            results = self.windows_analyzer.get_web_service_info()
        
        self.result_viewer.set_tree_result("Web服务信息", results)
        self.set_status_message("Web服务信息获取完成")

    def get_domain_info(self):
        """获取域信息（仅Windows）"""
        if self.server_connector.server_type == "windows":
            self.set_status_message("获取域信息中...")
            results = self.windows_analyzer.get_domain_info()
            self.result_viewer.set_tree_result("域信息", results)
            self.set_status_message("域信息获取完成")
        else:
            QMessageBox.information(self, "提示", "此功能仅适用于Windows服务器")

    def closeEvent(self, event):
        """关闭窗口时断开连接"""
        if self.server_connector.ssh_client or self.server_connector.rdp_process:
            reply = QMessageBox.question(self, "确认退出", 
                                        "是否断开当前连接并退出?",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.server_connector.disconnect()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def set_status_message(self, message):
        """更新状态栏临时消息"""
        self.status_message.setText(message) 