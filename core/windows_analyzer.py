class WindowsAnalyzer:
    def __init__(self, server_connector):
        self.server_connector = server_connector

    def get_basic_info(self):
        """获取基本系统信息"""
        commands = {
            "系统信息": "systeminfo",
            "主机名": "hostname",
            "操作系统版本": "ver",
            "CPU信息": "wmic cpu get caption,name,numberofcores,maxclockspeed",
            "内存信息": "wmic memorychip get capacity,speed",
            "磁盘空间": "wmic logicaldisk get caption,description,freespace,size"
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.server_connector.execute_command(cmd)
            if success:
                results[key] = result["output"]
            else:
                results[key] = f"获取失败: {result}"
        return results

    def get_user_info(self):
        """获取用户信息"""
        commands = {
            "本地用户": "net user",
            "管理员组": "net localgroup administrators",
            "当前登录用户": "query user"
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.server_connector.execute_command(cmd)
            if success:
                results[key] = result["output"]
            else:
                results[key] = f"获取失败: {result}"
        return results

    def get_network_info(self):
        """获取网络信息"""
        commands = {
            "网络配置": "ipconfig /all",
            "路由表": "route print",
            "网络连接": "netstat -ano",
            "防火墙规则": "netsh advfirewall show rule name=all"
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.server_connector.execute_command(cmd)
            if success:
                results[key] = result["output"]
            else:
                results[key] = f"获取失败: {result}"
        return results

    def get_process_info(self):
        """获取进程信息"""
        commands = {
            "进程列表": "tasklist /v",
            "服务列表": "net start"
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.server_connector.execute_command(cmd)
            if success:
                results[key] = result["output"]
            else:
                results[key] = f"获取失败: {result}"
        return results

    def get_startup_info(self):
        """获取启动项信息"""
        commands = {
            "启动项": "wmic startup get caption,command",
            "计划任务": "schtasks /query /fo list"
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.server_connector.execute_command(cmd)
            if success:
                results[key] = result["output"]
            else:
                results[key] = f"获取失败: {result}"
        return results

    def get_web_service_info(self):
        """获取Web服务信息"""
        commands = {
            "IIS状态": "iisreset /status",
            "Web服务": "net start | findstr /i \"iis apache nginx\""
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.server_connector.execute_command(cmd)
            if success:
                results[key] = result["output"]
            else:
                results[key] = f"获取失败: {result}"
        return results

    def get_domain_info(self):
        """获取域信息"""
        commands = {
            "域信息": "systeminfo | findstr /i \"domain\"",
            "域控制器": "netdom query dc",
            "域用户": "net user /domain"
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.server_connector.execute_command(cmd)
            if success:
                results[key] = result["output"]
            else:
                results[key] = f"获取失败: {result}"
        return results 