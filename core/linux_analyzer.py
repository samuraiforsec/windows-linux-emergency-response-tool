class LinuxAnalyzer:
    def __init__(self, server_connector):
        self.server_connector = server_connector

    def get_basic_info(self):
        """获取基本系统信息"""
        commands = {
            "主机名": "hostname",
            "操作系统": "cat /etc/os-release",
            "内核版本": "uname -r",
            "CPU信息": "lscpu",
            "内存信息": "free -h",
            "磁盘空间": "df -h"
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
            "当前登录用户": "who",
            "所有用户": "cat /etc/passwd",
            "用户组": "cat /etc/group",
            "sudo权限": "cat /etc/sudoers"
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
            "网络接口": "ip addr",
            "路由表": "ip route",
            "网络连接": "netstat -tuln",
            "防火墙规则": "iptables -L"
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
            "进程列表": "ps aux",
            "系统服务": "systemctl list-units --type=service"
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
            "系统启动项": "ls -l /etc/init.d/",
            "用户启动项": "ls -la /etc/rc*.d/"
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
            "Apache状态": "systemctl status apache2",
            "Nginx状态": "systemctl status nginx",
            "Web配置": "ls -l /etc/apache2/ /etc/nginx/"
        }
        
        results = {}
        for key, cmd in commands.items():
            success, result = self.server_connector.execute_command(cmd)
            if success:
                results[key] = result["output"]
            else:
                results[key] = f"获取失败: {result}"
        return results 