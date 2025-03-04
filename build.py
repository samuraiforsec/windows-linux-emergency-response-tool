import PyInstaller.__main__
import os
import platform

# 确保脚本目录存在
os.makedirs('dist/scripts/windows', exist_ok=True)
os.makedirs('dist/scripts/linux', exist_ok=True)

# 复制脚本文件 - 使用 macOS 兼容的命令
for script in ['system_info.ps1', 'security_check.ps1']:
    os.system(f'cp scripts/windows/{script} dist/scripts/windows/{script}')
for script in ['system_info.sh', 'security_check.sh']:
    os.system(f'cp scripts/linux/{script} dist/scripts/linux/{script}')

# PyInstaller 配置
PyInstaller.__main__.run([
    'main.py',                          # 主程序文件
    '--name=EmergencyResponseTool',     # 生成的应用名称
    '--windowed',                       # 使用GUI模式
    '--onefile',                        # 打包成单个文件
    '--icon=icon.icns',                 # macOS图标文件
    '--add-data=scripts:scripts',       # macOS使用:分隔符
    '--clean',                          # 清理临时文件
    '--noconfirm',                      # 不确认覆盖
    '--target-arch=universal2'          # 支持 Intel 和 Apple Silicon
]) 