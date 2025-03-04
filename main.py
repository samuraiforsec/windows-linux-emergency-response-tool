#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows和Linux应急响应工具 v1.0
一个用于快速分析Windows和Linux服务器安全状况的工具

作者: Andy
邮箱: chenxiaodong@chinatelecomglobal.com
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序的主循环
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 