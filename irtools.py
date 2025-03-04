import sys
import time
import subprocess
import paramiko
from PyQt5 import QtWidgets, QtCore
import json
import threading

class CommandExecutor(QtWidgets.QWidget):

    # Global dictionary to store results from various functions
    results_data = {
        'system_info': {
            'output': None,
            'cmd': None
        },
        'system_integrity': {
            'output': None,
            'cmd': None
        },
        'log_analysis': {
            'output': None,
            'cmd': None
        }
    }

    def __init__(self):
        super().__init__()
        #pywinstyles.apply_style(self, "windows11")  
        self.setWindowTitle("Incident Responser")
        self.setGeometry(100, 100, 800, 800)

        # SSH客户端
        self.ssh_client = None

        # 创建布局
        layout = QtWidgets.QVBoxLayout()

        # 主机名输入
        self.hostname_input = QtWidgets.QLineEdit("166.88.61.176", self)
        self.hostname_input.setPlaceholderText("Host")
        layout.addWidget(self.hostname_input)

        # 用户名输入
        self.username_input = QtWidgets.QLineEdit("root", self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # 密码输入
        self.password_input = QtWidgets.QLineEdit("L6Z3E2d4c5h0s7Kbd5A6", self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        # 连接按钮
        self.connect_button = QtWidgets.QPushButton("Connect", self)
        self.connect_button.clicked.connect(lambda: threading.Thread(target=self.connect_to_host, daemon=True).start())
        layout.addWidget(self.connect_button)

        # 功能按钮
        # Create horizontal layout for buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        self.run_script_button = QtWidgets.QPushButton("Run Script", self)
        self.run_script_button.setFixedWidth(180)
        button_layout.addWidget(self.run_script_button)
        
        self.run_system_info_button = QtWidgets.QPushButton("Basic Info", self)  #进程+端口+服务状态
        self.run_system_info_button.setFixedWidth(180) 
        button_layout.addWidget(self.run_system_info_button)
        
        self.run_memory_info_button = QtWidgets.QPushButton("System Integrity", self)  #历史命令+计划任务+账号+文件修改+基线
        self.run_memory_info_button.setFixedWidth(180)
        button_layout.addWidget(self.run_memory_info_button)
        
        self.run_disk_info_button = QtWidgets.QPushButton("Log Analysis", self)  #应用、系统日志分析
        self.run_disk_info_button.setFixedWidth(180)
        button_layout.addWidget(self.run_disk_info_button)
        
        # Add horizontal button layout to main layout
        layout.addLayout(button_layout)

        # 连接按钮的点击事件
        self.run_script_button.clicked.connect(self.execute_script)
        self.run_system_info_button.clicked.connect(self.get_system_info)
        self.run_memory_info_button.clicked.connect(self.system_integrity)
        self.run_disk_info_button.clicked.connect(self.log_analysis)

        # 添加按钮到布局
        #layout.addWidget(self.run_script_button)
        #layout.addWidget(self.run_system_info_button)
        #layout.addWidget(self.run_memory_info_button)
        #layout.addWidget(self.run_disk_info_button)

        # 结果区域
        #self.result_area = QtWidgets.QTextEdit(self)
        #self.result_area.setReadOnly(True)
        #self.result_area.setAlignment(QtCore.Qt.AlignRight)
        #layout.addWidget(self.result_area)

        # 创建树形控件以展示 JSON 数据
        self.tree_widget = QtWidgets.QTreeWidget(self)
        self.tree_widget.setHeaderLabel("Output")
        layout.addWidget(self.tree_widget)

        # 设置布局
        self.setLayout(layout)

        # 初始禁用功能按钮
        self.set_buttons_enabled(False)

    def set_buttons_enabled(self, enabled):
        """Enable or disable function buttons"""
        self.run_script_button.setEnabled(enabled)
        self.run_system_info_button.setEnabled(enabled)
        self.run_memory_info_button.setEnabled(enabled)
        self.run_disk_info_button.setEnabled(enabled)

    def connect_to_host(self):
        """Connect to remote host"""
        hostname = self.hostname_input.text() 
        username = self.username_input.text() 
        password = self.password_input.text() 

        #self.result_area.clear()
        #self.result_area.append("Connecting to host...")
        #self.result_area.repaint()

        try:
            if self.ssh_client:
                self.ssh_client.close()

            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password)
            
            #self.result_area.append("Successfully connected to host!")
            self.connect_button.setText("Disconnect")
            self.set_buttons_enabled(True)
            
        except Exception as e:
            #self.result_area.append(f"Error connecting to host: {str(e)}")
            self.ssh_client = None
            self.connect_button.setText("Connect")
            self.set_buttons_enabled(False)

    def execute_command(self, command):
        """Helper function to execute a command on the remote server."""
        if not self.ssh_client:
            #self.result_area.append("Not connected to host. Please connect first.")
            return None

        #self.result_area.clear()
        #self.result_area.append("Executing command...")
        #self.result_area.repaint()

        try:
            start_time = time.time()
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000
            #self.result_area.clear()
            #self.result_area.append(f"Command executed in {execution_time:.2f} ms\n")
            
            if output:
                #self.result_area.append(f"Output:\n{output}\n")
                pass
            if error:
                #self.result_area.append(f"Error:\n{error}\n")
                pass

            # Return the command output and error
            return {
                'stdin': command,
                'stdout': output,
                'stderr': error,
                'executiontime':execution_time
            }

        except Exception as e:
            #self.result_area.append(f"Error executing command: {str(e)}\n")
            self.ssh_client = None
            self.connect_button.setText("Connect") 
            self.set_buttons_enabled(False)
            return None
        

    def execute_script(self):
        bash_script = """
        #!/bin/bash
        echo "当前日期和时间:"
        date
        echo "系统信息:"
        uname -a
        echo "磁盘使用情况:"
        df -h
        echo "内存使用情况:"
        free -m
        """
        command = f"echo '{bash_script}' > /tmp/temp_script.sh && chmod +x /tmp/temp_script.sh && /tmp/temp_script.sh"
        result = self.execute_command(command)

        #print(self.results_data['system_info']['processes'])

    def get_system_info(self):
        bash_script = """
        #!/bin/bash
        ps aux 
        systemctl | grep -E "\.service.*running" | awk -F. "{print \$1}"
        """
        command = f"echo '{bash_script}' > /tmp/temp_script.sh && chmod +x /tmp/temp_script.sh && /tmp/temp_script.sh"
        result = self.execute_command(command)
        if result:
            self.results_data['system_info']['ouput'] = result
            self.results_data['system_info']['cmd'] = command
            #self.result_area.clear()
            #self.result_area.append(json.dumps(result, indent=4, ensure_ascii=False))
            # 更新树形控件
            self.display_result(result)

    def system_integrity(self):
        bash_script = """
        #!/bin/bash
        ps aux 
        systemctl | grep -E "\.service.*running" | awk -F. "{print \$1}"
        """
        command = f"echo '{bash_script}' > /tmp/temp_script2.sh && chmod +x /tmp/temp_script2.sh && /tmp/temp_script2.sh"
        result = self.execute_command(command)
        if result:
            self.results_data['system_integrity']['ouput'] = result
            self.results_data['system_integrity']['cmd'] = command
            #self.result_area.clear()
            #self.result_area.append(json.dumps(result, indent=4, ensure_ascii=False))
            # 更新树形控件
            self.display_result(result)

    def log_analysis(self):
        bash_script = """
        #!/bin/bash
        ps aux 
        systemctl | grep -E "\.service.*running" | awk -F. "{print \$1}"
        """
        command = f"echo '{bash_script}' > /tmp/temp_script3.sh && chmod +x /tmp/temp_script3.sh && /tmp/temp_script3.sh"
        result = self.execute_command(command)
        if result:
            self.results_data['log_analysis']['ouput'] = result
            self.results_data['log_analysis']['cmd'] = command
            #self.result_area.clear()
            #self.result_area.append(json.dumps(result, indent=4, ensure_ascii=False))
            # 更新树形控件
            self.display_result(result)

    def display_result(self, result):
        """将 JSON 结果显示在树形控件中"""
        self.tree_widget.clear()  # 清空树形控件
        
        # 创建根节点
        root_item = QtWidgets.QTreeWidgetItem(self.tree_widget, ["Command Execution Result"])
        for key, value in result.items():
            if isinstance(value, str):
                item = QtWidgets.QTreeWidgetItem(root_item, [f"{key}: {value}"])
            else:
                item = QtWidgets.QTreeWidgetItem(root_item, [f"{key}:"])
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        sub_item = QtWidgets.QTreeWidgetItem(item, [f"{sub_key}: {sub_value}"])
            root_item.addChild(item)

        self.tree_widget.expandAll()  # 展开所有节点


    def run_in_thread(self, command):
        if not self.ssh_client:
            #self.result_area.append("Not connected to host. Please connect first.")
            return

        #self.result_area.clear()
        #self.result_area.append("Executing command...")
        #self.result_area.repaint()

        worker = Worker(command, self.ssh_client)
        worker.signals.finished.connect(self.update_result)
        worker.signals.progress.connect(self.update_status)
        self.threadpool.start(worker)

    def closeEvent(self, event):
        """Clean up SSH connection when closing the window"""
        if self.ssh_client:
            self.ssh_client.close()
        event.accept()


class Worker(QtCore.QRunnable):
    """Worker thread for executing commands."""
    def __init__(self, command, ssh_client):
        super().__init__()
        self.command = command
        self.ssh_client = ssh_client
        self.signals = WorkerSignals()

    def run(self):
        try:
            start_time = time.time()
            stdin, stdout, stderr = self.ssh_client.exec_command(self.command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000
            self.signals.finished.emit((output, error, execution_time))

        except Exception as e:
            self.signals.finished.emit(("", str(e), 0))


class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(tuple)
    progress = QtCore.pyqtSignal(int)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    executor = CommandExecutor()
    executor.show()
    sys.exit(app.exec_())