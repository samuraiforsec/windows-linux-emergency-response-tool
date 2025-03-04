# 系统信息收集脚本

Write-Host "=== 系统基本信息 ===" -ForegroundColor Green
$os = Get-WmiObject -Class Win32_OperatingSystem
Write-Host "操作系统: $($os.Caption) $($os.Version)"
Write-Host "主机名: $($env:COMPUTERNAME)"
Write-Host "系统时间: $(Get-Date)"

Write-Host "`n=== CPU信息 ===" -ForegroundColor Green
Get-WmiObject -Class Win32_Processor | ForEach-Object {
    Write-Host "处理器: $($_.Name)"
    Write-Host "核心数: $($_.NumberOfCores)"
    Write-Host "线程数: $($_.NumberOfLogicalProcessors)"
}

Write-Host "`n=== 内存信息 ===" -ForegroundColor Green
$totalMemory = [math]::Round((Get-WmiObject -Class Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)
Write-Host "总内存: $totalMemory GB"
Get-WmiObject -Class Win32_OperatingSystem | ForEach-Object {
    $freeMemory = [math]::Round($_.FreePhysicalMemory / 1MB, 2)
    Write-Host "可用内存: $freeMemory GB"
}

Write-Host "`n=== 磁盘信息 ===" -ForegroundColor Green
Get-WmiObject -Class Win32_LogicalDisk | ForEach-Object {
    $size = [math]::Round($_.Size / 1GB, 2)
    $free = [math]::Round($_.FreeSpace / 1GB, 2)
    Write-Host "驱动器 $($_.DeviceID)"
    Write-Host "总大小: $size GB"
    Write-Host "可用空间: $free GB"
}

Write-Host "`n=== 网络信息 ===" -ForegroundColor Green
Get-NetAdapter | Where-Object Status -eq "Up" | ForEach-Object {
    Write-Host "网卡: $($_.Name)"
    Write-Host "状态: $($_.Status)"
    $ip = Get-NetIPAddress -InterfaceIndex $_.ifIndex -AddressFamily IPv4
    Write-Host "IP地址: $($ip.IPAddress)"
}

Write-Host "`n=== 已安装的软件 ===" -ForegroundColor Green
Get-WmiObject -Class Win32_Product | Select-Object Name, Version | Format-Table -AutoSize 