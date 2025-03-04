import paramiko
import subprocess
import os
import platform

class ServerConnector:
    def __init__(self):
        self.ssh_client = None
        self.rdp_process = None
        self.server_type = None  # "linux" or "windows"
        
    def connect_ssh(self, hostname, username, password, port=22):
        """连接到Linux服务器"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, port, username, password)
            self.server_type = "linux"
            return True, "连接成功"
        except Exception as e:
            return False, str(e)

    def connect_rdp(self, hostname, username, password, port=3389):
        """连接到Windows服务器"""
        try:
            # 这里需要实现RDP连接逻辑
            # 可以使用pyfreerdp或其他RDP库
            self.server_type = "windows"
            return True, "连接成功"
        except Exception as e:
            return False, str(e)

    def disconnect(self):
        """断开连接"""
        try:
            if self.ssh_client:
                self.ssh_client.close()
                self.ssh_client = None
            if self.rdp_process:
                self.rdp_process.terminate()
                self.rdp_process = None
            self.server_type = None
            return True, "断开连接成功"
        except Exception as e:
            return False, str(e)

    def execute_command(self, command):
        """执行命令"""
        try:
            if self.server_type == "linux":
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                return True, {
                    "output": stdout.read().decode(),
                    "error": stderr.read().decode()
                }
            elif self.server_type == "windows":
                # 这里需要实现Windows命令执行逻辑
                return True, {
                    "output": "Windows command execution not implemented",
                    "error": ""
                }
            else:
                return False, "未连接到服务器"
        except Exception as e:
            return False, str(e)

    def upload_script(self, local_path, remote_path):
        """上传脚本"""
        try:
            if self.server_type == "linux":
                sftp = self.ssh_client.open_sftp()
                sftp.put(local_path, remote_path)
                sftp.close()
                return True, "脚本上传成功"
            elif self.server_type == "windows":
                # 这里需要实现Windows文件上传逻辑
                return True, "Windows file upload not implemented"
            else:
                return False, "未连接到服务器"
        except Exception as e:
            return False, str(e) 