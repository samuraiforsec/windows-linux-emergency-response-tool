class WindowsAnalyzer:
    def __init__(self, server_connector):
        self.connector = server_connector

    def get_basic_info(self):
        """获取Windows服务器基本信息"""
        commands = {
            "hostname": "hostname",
            "ip": "ipconfig | findstr IPv4",
            "os_version": "systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\"",
            "uptime": "net statistics server | findstr Statistics",
            "cpu_info": "wmic cpu get Name, NumberOfCores, NumberOfLogicalProcessors",
            "memory": "wmic OS get TotalVisibleMemorySize, FreePhysicalMemory /Value",
            "disk_space": "wmic logicaldisk get DeviceID, Size, FreeSpace, FileSystem",
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.connector.execute_command(cmd)
            if success:
                results[key] = result.get("output", "")
            else:
                results[key] = f"Error: {result}"
        
        return results

    def get_user_info(self):
        """获取当前登录用户信息"""
        commands = {
            "current_users": "query user",
            "local_users": "net user",
            "admin_users": "net localgroup administrators",
            "last_logins": "wmic netlogin get name, lastlogon",
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.connector.execute_command(cmd)
            if success:
                results[key] = result.get("output", "")
            else:
                results[key] = f"Error: {result}"
        
        return results

    def get_network_info(self):
        """获取网络连接信息"""
        commands = {
            "active_connections": "netstat -ano",
            "listening_ports": "netstat -ano | findstr LISTENING",
            "network_interfaces": "ipconfig /all",
            "routing_table": "route print",
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.connector.execute_command(cmd)
            if success:
                results[key] = result.get("output", "")
            else:
                results[key] = f"Error: {result}"
        
        return results

    def get_process_info(self):
        """获取进程信息"""
        commands = {
            "running_processes": "tasklist /v",
            "service_status": "net start",
            "process_connections": "netstat -anob",
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.connector.execute_command(cmd)
            if success:
                results[key] = result.get("output", "")
            else:
                results[key] = f"Error: {result}"
        
        return results

    def get_startup_info(self):
        """获取系统启动项信息"""
        commands = {
            "startup_programs": "wmic startup get caption,command",
            "scheduled_tasks": "schtasks /query /fo LIST",
            "services": "wmic service where \"startmode='auto'\" get name, startmode, state",
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.connector.execute_command(cmd)
            if success:
                results[key] = result.get("output", "")
            else:
                results[key] = f"Error: {result}"
        
        return results

    def get_domain_info(self):
        """获取域环境信息"""
        # 首先检查是否在域环境中
        success, result = self.connector.execute_command("systeminfo | findstr /B /C:\"Domain\"")
        if success and "Domain" in result.get("output", ""):
            # 在域环境中，获取域控信息
            commands = {
                "domain_name": "echo %USERDOMAIN%",
                "domain_controllers": "nltest /dclist:%USERDOMAIN%",
                "domain_info": "nltest /domain_trusts",
                "user_domain_groups": "net user %USERNAME% /domain",
            }
            
            results = {"is_domain": "Yes"}
            for key, cmd in commands.items():
                success, cmd_result = self.connector.execute_command(cmd)
                if success:
                    results[key] = cmd_result.get("output", "")
                else:
                    results[key] = f"Error: {cmd_result}"
            
            return results
        else:
            return {"is_domain": "No", "message": "此服务器不在域环境中"}

    def get_web_service_info(self):
        """获取Web服务信息"""
        commands = {
            "iis_status": "sc query w3svc",
            "web_sites": "C:\\Windows\\System32\\inetsrv\\appcmd.exe list sites 2>nul || echo 'IIS未安装或appcmd不可用'",
            "web_app_pools": "C:\\Windows\\System32\\inetsrv\\appcmd.exe list apppool 2>nul || echo 'IIS未安装或appcmd不可用'",
            "listening_web_ports": "netstat -ano | findstr :80 | findstr :443",
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.connector.execute_command(cmd)
            if success:
                results[key] = result.get("output", "")
            else:
                results[key] = f"Error: {result}"
        
        return results 