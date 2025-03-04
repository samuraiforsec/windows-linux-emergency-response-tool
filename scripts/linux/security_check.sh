#!/bin/bash
# 安全检查脚本

echo "=== 安全检查报告 ==="
date

echo -e "\n=== 系统用户检查 ==="
echo "具有root权限的用户:"
grep -v -E "^#" /etc/passwd | awk -F: '$3 == 0 { print $1 }'
echo "最近登录的用户:"
last | head -n 10

echo -e "\n=== SSH配置检查 ==="
echo "SSH配置:"
grep -v '^#' /etc/ssh/sshd_config | grep -v '^$'
echo "允许SSH登录的用户:"
grep "AllowUsers" /etc/ssh/sshd_config

echo -e "\n=== 防火墙状态 ==="
if command -v ufw > /dev/null; then
    ufw status verbose
elif command -v firewall-cmd > /dev/null; then
    firewall-cmd --list-all
fi

echo -e "\n=== 系统服务检查 ==="
echo "正在运行的服务:"
systemctl list-units --type=service --state=running

echo -e "\n=== 开放端口检查 ==="
netstat -tuln

echo -e "\n=== 系统日志检查 ==="
echo "最近的认证日志:"
grep -i "failed\|invalid\|error" /var/log/auth.log 2>/dev/null | tail -n 10

echo -e "\n=== 可疑进程检查 ==="
ps aux | grep -i "suspicious\|hack\|malware"

echo -e "\n=== 关键文件权限检查 ==="
ls -l /etc/passwd /etc/shadow /etc/group /etc/sudoers

echo -e "\n=== 计划任务检查 ==="
echo "系统计划任务:"
cat /etc/crontab
echo "用户计划任务:"
for user in $(cut -f1 -d: /etc/passwd); do
    crontab -l -u $user 2>/dev/null
done

echo -e "\n===== 安全检查完成 ====="
date 