#!/bin/bash
# 系统信息收集脚本

echo "=== 系统基本信息 ==="
echo "主机名: $(hostname)"
echo "操作系统: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "内核版本: $(uname -r)"
echo "系统时间: $(date)"

echo -e "\n=== CPU信息 ==="
lscpu

echo -e "\n=== 内存信息 ==="
free -h

echo -e "\n=== 磁盘信息 ==="
df -h

echo -e "\n=== 网络信息 ==="
echo "IP地址:"
ip addr | grep inet

echo -e "\n=== 系统负载 ==="
uptime

echo -e "\n=== 已安装的重要软件 ==="
if command -v dpkg > /dev/null; then
    dpkg -l | grep -E "apache|nginx|mysql|postgresql|ssh|python|java|php"
elif command -v rpm > /dev/null; then
    rpm -qa | grep -E "apache|nginx|mysql|postgresql|ssh|python|java|php"
fi

echo -e "\n===== 当前登录用户 ====="
who

echo -e "\n===== 最近登录记录 ====="
last | head -10

echo -e "\n===== 开放端口 ====="
netstat -tuln

echo -e "\n===== 运行中的服务 ====="
systemctl list-units --type=service --state=running | head -20

echo -e "\n===== 高CPU占用进程 ====="
ps aux --sort=-%cpu | head -10

echo -e "\n===== 高内存占用进程 ====="
ps aux --sort=-%mem | head -10

echo -e "\n===== 系统日志最新条目 ====="
journalctl -n 20 --no-pager 