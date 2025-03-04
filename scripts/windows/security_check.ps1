# 安全检查脚本

Write-Host "=== 安全检查报告 ===" -ForegroundColor Green
Get-Date

Write-Host "`n=== 系统用户检查 ===" -ForegroundColor Green
Write-Host "本地用户列表:"
Get-LocalUser | Format-Table Name, Enabled, LastLogon
Write-Host "管理员组成员:"
Get-LocalGroupMember -Group "Administrators" | Format-Table Name, PrincipalSource

Write-Host "`n=== 系统服务检查 ===" -ForegroundColor Green
Get-Service | Where-Object {$_.Status -eq "Running"} | Format-Table Name, DisplayName, Status

Write-Host "`n=== 防火墙状态 ===" -ForegroundColor Green
Get-NetFirewallProfile | Format-Table Name, Enabled
Write-Host "开放的入站端口:"
Get-NetFirewallRule | Where-Object {$_.Enabled -eq $true -and $_.Direction -eq "Inbound"} | Format-Table DisplayName, Profile, Action

Write-Host "`n=== 网络连接检查 ===" -ForegroundColor Green
Get-NetTCPConnection | Where-Object State -eq "Listen" | Format-Table LocalAddress, LocalPort, State

Write-Host "`n=== 启动项检查 ===" -ForegroundColor Green
Get-CimInstance Win32_StartupCommand | Format-Table Name, Command, Location

Write-Host "`n=== 计划任务检查 ===" -ForegroundColor Green
Get-ScheduledTask | Where-Object {$_.State -ne "Disabled"} | Format-Table TaskName, State, LastRunTime

Write-Host "`n=== 系统更新状态 ===" -ForegroundColor Green
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10 | Format-Table HotFixID, Description, InstalledOn

Write-Host "`n=== 安全审计策略 ===" -ForegroundColor Green
auditpol /get /category:*

Write-Host "`n=== 共享文件夹检查 ===" -ForegroundColor Green
Get-SmbShare | Format-Table Name, Path, Description

Write-Host "`n=== 可疑进程检查 ===" -ForegroundColor Green
Get-Process | Where-Object {$_.CPU -gt 50 -or $_.WorkingSet -gt 500MB} | Format-Table Name, Id, CPU, WorkingSet

Write-Host "`n===== 事件日志检查 ====="
Write-Host "失败登录尝试 (过去24小时):"
try {
    Get-EventLog -LogName Security -InstanceId 4625 -After (Get-Date).AddHours(-24) | 
        Select-Object TimeGenerated, 
            @{Name="User";Expression={$_.ReplacementStrings[5]}}, 
            @{Name="Source";Expression={$_.ReplacementStrings[13]}} | 
        Format-Table -AutoSize
} catch {
    Write-Host "无法获取事件日志或没有失败登录记录"
}

Write-Host "`n===== 运行服务检查 ====="
Write-Host "第三方服务:"
Get-CimInstance Win32_Service | 
    Where-Object {$_.PathName -notlike "*windows*" -and $_.State -eq "Running"} | 
    Select-Object Name, DisplayName, State, StartMode, PathName | 
    Format-Table -AutoSize

Write-Host "`n===== 域环境检查 ====="
if ((Get-WmiObject Win32_ComputerSystem).PartOfDomain) {
    Write-Host "此计算机是域成员"
    $domain = (Get-WmiObject Win32_ComputerSystem).Domain
    Write-Host "域名: $domain"
    
    Write-Host "`n域控制器:"
    try {
        Get-ADDomainController -DomainName $domain -Filter * | 
            Select-Object Name, IPv4Address, Site, Forest, OperatingSystem | 
            Format-Table -AutoSize
    } catch {
        Write-Host "无法获取域控制器信息，可能需要安装AD PowerShell模块"
    }
} else {
    Write-Host "此计算机不是域成员"
}

Write-Host "`n===== 安全检查完成 ====="
Get-Date 