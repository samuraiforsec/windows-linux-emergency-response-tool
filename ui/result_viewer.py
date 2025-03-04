from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QTabWidget, QTreeWidget, QTreeWidgetItem, QLabel, QComboBox, QLineEdit, QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

class ResultViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 创建布局
        layout = QVBoxLayout()
        
        # 创建标签页
        self.tabs = QTabWidget()
        
        # 文本视图
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.tabs.addTab(self.text_edit, "文本视图")
        
        # 树形视图
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["项目", "值"])
        self.tree_widget.setColumnWidth(0, 200)
        self.tabs.addTab(self.tree_widget, "树形视图")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def set_text_result(self, text):
        """设置文本结果"""
        self.tabs.setCurrentIndex(0)  # 切换到文本视图
        self.text_edit.setPlainText(text)
    
    def set_tree_result(self, title, data):
        """设置树形结果"""
        self.tabs.setCurrentIndex(1)  # 切换到树形视图
        self.tree_widget.clear()
        
        root = QTreeWidgetItem([title])
        self.tree_widget.addTopLevelItem(root)
        
        def add_items(parent, items):
            if isinstance(items, dict):
                for key, value in items.items():
                    child = QTreeWidgetItem([str(key)])
                    parent.addChild(child)
                    if isinstance(value, (dict, list)):
                        add_items(child, value)
                    else:
                        child.setText(1, str(value))
            elif isinstance(items, list):
                for i, item in enumerate(items):
                    child = QTreeWidgetItem([f"项目 {i+1}"])
                    parent.addChild(child)
                    if isinstance(item, (dict, list)):
                        add_items(child, item)
                    else:
                        child.setText(1, str(item))
        
        add_items(root, data)
        root.setExpanded(True)
    
    def save_results(self):
        """保存结果到文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存结果", "", "文本文件 (*.txt);;所有文件 (*)")
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if self.tabs.currentIndex() == 0:
                    # 保存文本视图内容
                    f.write(self.text_edit.toPlainText())
                else:
                    # 保存树形视图内容
                    def write_items(item, level=0):
                        indent = "  " * level
                        text = f"{indent}{item.text(0)}"
                        if item.text(1):
                            text += f": {item.text(1)}"
                        f.write(text + "\n")
                        for i in range(item.childCount()):
                            write_items(item.child(i), level + 1)
                    
                    root = self.tree_widget.invisibleRootItem()
                    for i in range(root.childCount()):
                        write_items(root.child(i))
        except Exception as e:
            QMessageBox.warning(self, "保存失败", str(e)) 