import PyInstaller.__main__
import os
import sys

# 获取当前目录的绝对路径
current_dir = os.path.abspath(os.path.dirname(__file__))
scripts_dir = os.path.join(current_dir, 'scripts')

# 确保脚本目录存在
os.makedirs('dist/scripts/windows', exist_ok=True)
os.makedirs('dist/scripts/linux', exist_ok=True)

# 复制脚本文件 - Windows环境使用copy命令
for script in ['system_info.ps1', 'security_check.ps1']:
    os.system(f'copy scripts\\windows\\{script} dist\\scripts\\windows\\{script}')
for script in ['system_info.sh', 'security_check.sh']:
    os.system(f'copy scripts\\linux\\{script} dist\\scripts\\linux\\{script}')

# 设置正确的路径分隔符
separator = ';' if sys.platform.startswith('win') else ':'
scripts_path = f'{scripts_dir}{separator}scripts'

# PyInstaller 配置
PyInstaller.__main__.run([
    'main.py',
    '--name=EmergencyResponseTool',
    '--windowed',
    '--onefile',
    f'--add-data={scripts_path}',    # 使用绝对路径
    '--clean',
    '--noconfirm',
    '--win-private-assemblies',      # 包含私有DLL
    '--win-no-prefer-redirects'      # 不使用重定向
]) 