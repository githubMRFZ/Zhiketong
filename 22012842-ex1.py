import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox,
    QPushButton, QTextBrowser, QLabel, QGroupBox, QScrollArea,
    QDialog, QLineEdit, QHBoxLayout, QMessageBox, QListWidget, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class RuleDialog(QDialog):
    """规则管理对话框（修改了类名）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("规则管理器")
        self.setFixedSize(700, 500)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 规则输入区域
        input_group = QGroupBox("添加新规则")
        input_layout = QVBoxLayout()
        self.rule_input = QLineEdit()
        self.rule_input.setPlaceholderText("输入格式：特征1 特征2...，结论")
        input_layout.addWidget(self.rule_input)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # 按钮区域
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("添加")
        self.cancel_btn = QPushButton("取消")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        # 规则列表
        list_group = QGroupBox("现有规则")
        list_layout = QVBoxLayout()
        self.rule_list = QListWidget()
        list_layout.addWidget(self.rule_list)
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)

        self.setLayout(layout)

        # 连接信号
        self.cancel_btn.clicked.connect(self.reject)


class AnimalSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("动物识别专家系统")
        self.setGeometry(100, 100, 900, 700)

        # 知识库初始化
        self.rule_base = self.init_rules()
        self.feature_map = self.init_features()
        self.animal_list = ["金钱豹", "虎", "斑马", "长颈鹿", "鸵鸟", "企鹅", "信天翁"]
        self.checkbox_dict = {}

        self.setup_ui()

    def init_rules(self):
        """初始化规则库（修改了数据结构）"""
        return [
            {"premise": ["有毛发"], "conclusion": "哺乳类"},
            {"premise": ["产奶"], "conclusion": "哺乳类"},
            {"premise": ["有羽毛"], "conclusion": "鸟类"},
            {"premise": ["会下蛋", "不会飞"], "conclusion": "鸟类"},
            {"premise": ["哺乳类", "吃肉"], "conclusion": "食肉类"},
            {"premise": ["有犬齿", "有爪", "眼盯前方"], "conclusion": "食肉类"},
            {"premise": ["哺乳类", "有蹄"], "conclusion": "蹄类"},
            {"premise": ["哺乳类", "反刍"], "conclusion": "蹄类"},
            {"premise": ["食肉类", "黄褐色", "哺乳类", "有斑点"], "conclusion": "金钱豹"},
            {"premise": ["食肉类", "黄褐色", "哺乳类", "有黑色条纹"], "conclusion": "虎"},
            {"premise": ["有黑色条纹", "蹄类"], "conclusion": "斑马"},
            {"premise": ["有斑点", "蹄类", "长脖", "长腿"], "conclusion": "长颈鹿"},
            {"premise": ["鸟类", "不会飞", "长脖", "长腿"], "conclusion": "鸵鸟"},
            {"premise": ["鸟类", "不会飞", "会游泳", "黑白二色"], "conclusion": "企鹅"},
            {"premise": ["鸟类", "善飞"], "conclusion": "信天翁"}
        ]

    def init_features(self):
        """初始化特征字典（修改了键名）"""
        return {
            'f1': '有毛发', 'f2': '产奶', 'f3': '有羽毛', 'f4': '不会飞',
            'f5': '会下蛋', 'f6': '吃肉', 'f7': '有犬齿', 'f8': '有爪',
            'f9': '眼盯前方', 'f10': '有蹄', 'f11': '反刍', 'f12': '黄褐色',
            'f13': '有斑点', 'f14': '有黑色条纹', 'f15': '长脖', 'f16': '长腿',
            'f17': '不会飞', 'f18': '会游泳', 'f19': '黑白二色', 'f20': '善飞'
        }

    def setup_ui(self):
        """设置界面（修改了布局）"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        # 标题
        title = QLabel("动物识别专家系统")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)

        # 模式选择
        mode_box = QGroupBox("推理模式设置")
        mode_layout = QVBoxLayout()

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["正向推理", "反向推理"])
        mode_layout.addWidget(QLabel("选择推理模式:"))
        mode_layout.addWidget(self.mode_selector)

        self.target_selector = QComboBox()
        self.target_selector.addItems(self.animal_list)
        self.target_selector.setVisible(False)
        mode_layout.addWidget(QLabel("选择目标动物:"))
        mode_layout.addWidget(self.target_selector)

        mode_box.setLayout(mode_layout)
        left_layout.addWidget(mode_box)

        # 规则管理
        rule_box = QGroupBox("规则管理")
        rule_layout = QVBoxLayout()

        self.view_btn = QPushButton("查看规则库")
        self.add_btn = QPushButton("添加规则")
        self.del_btn = QPushButton("删除规则")

        rule_layout.addWidget(self.view_btn)
        rule_layout.addWidget(self.add_btn)
        rule_layout.addWidget(self.del_btn)
        rule_box.setLayout(rule_layout)
        left_layout.addWidget(rule_box)

        # 特征选择
        feature_box = QGroupBox("动物特征选择")
        feature_layout = QVBoxLayout()

        for key, text in self.feature_map.items():
            cb = QCheckBox(f"{key}: {text}")
            cb.feature_key = key
            self.checkbox_dict[key] = cb
            feature_layout.addWidget(cb)

        feature_box.setLayout(feature_layout)
        scroll = QScrollArea()
        scroll.setWidget(feature_box)
        scroll.setWidgetResizable(True)
        left_layout.addWidget(scroll)

        # 推理按钮
        self.reason_btn = QPushButton("开始推理")
        self.reason_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        left_layout.addWidget(self.reason_btn)

        left_panel.setLayout(left_layout)
        main_layout.addWidget(left_panel, stretch=1)

        # 结果显示区域
        result_panel = QWidget()
        result_layout = QVBoxLayout()

        self.result_display = QTextBrowser()
        font = QFont()
        font.setPointSize(24)  # 字体放大3倍（默认8pt×3）
        self.result_display.setFont(font)
        result_layout.addWidget(self.result_display)

        result_panel.setLayout(result_layout)
        main_layout.addWidget(result_panel, stretch=2)

        main_widget.setLayout(main_layout)

        # 连接信号
        self.mode_selector.currentTextChanged.connect(self.change_mode)
        self.view_btn.clicked.connect(self.display_rules)
        self.add_btn.clicked.connect(self.open_rule_dialog)
        self.del_btn.clicked.connect(self.remove_rule)
        self.reason_btn.clicked.connect(self.execute_reasoning)

    def change_mode(self, mode):
        """切换推理模式（修改了实现方式）"""
        is_backward = mode == "反向推理"
        self.target_selector.setVisible(is_backward)

        for cb in self.checkbox_dict.values():
            cb.setEnabled(not is_backward)

    def forward_reason(self):
        """正向推理（修改了实现方式）"""
        selected = [self.feature_map[cb.feature_key]
                    for cb in self.checkbox_dict.values() if cb.isChecked()]

        if not selected:
            self.result_display.append("请至少选择一个特征！")
            return

        self.result_display.clear()
        self.result_display.append("=== 正向推理开始 ===")
        self.result_display.append(f"初始特征: {', '.join(selected)}")

        changed = True
        while changed:
            changed = False
            for rule in self.rule_base:
                if all(pre in selected for pre in rule["premise"]) and rule["conclusion"] not in selected:
                    selected.append(rule["conclusion"])
                    self.result_display.append(f"应用规则: {' + '.join(rule['premise'])} → {rule['conclusion']}")
                    changed = True

        self.result_display.append("\n=== 推理结果 ===")
        animals = [item for item in selected if item in self.animal_list]

        if animals:
            self.result_display.append(f"识别结果: {animals[0]}")
        else:
            self.result_display.append("无法确定具体动物")
            self.result_display.append(f"中间结论: {', '.join(selected)}")

    def backward_reason(self, target):
        """反向推理（修改了实现方式）"""
        self.result_display.clear()
        self.result_display.append(f"=== 反向推理目标: {target} ===")

        needed = set()
        to_check = [target]
        checked = set()

        while to_check:
            current = to_check.pop(0)

            if current in self.feature_map.values():
                needed.add(current)
                continue

            applicable = [r for r in self.rule_base if r["conclusion"] == current]

            if not applicable:
                self.result_display.append(f"无法找到推导 {current} 的规则")
                continue

            rule = applicable[0]
            if str(rule) in checked:
                continue

            checked.add(str(rule))
            self.result_display.append(f"需要满足: {' + '.join(rule['premise'])} → {rule['conclusion']}")

            for pre in rule["premise"]:
                if pre not in needed:
                    to_check.append(pre)

        self.result_display.append("\n=== 推理结果 ===")
        if needed:
            self.result_display.append(f"证明 {target} 需要:")
            for feature in sorted(needed):
                self.result_display.append(f"- {feature}")
        else:
            self.result_display.append(f"无法确定证明 {target} 所需的特征")

    def display_rules(self):
        """显示规则库"""
        self.result_display.clear()
        self.result_display.append("=== 规则库 ===")

        for i, rule in enumerate(self.rule_base, 1):
            self.result_display.append(
                f"{i}. {' ∧ '.join(rule['premise'])} → {rule['conclusion']}"
            )

    def open_rule_dialog(self):
        """打开规则对话框"""
        dialog = RuleDialog(self)
        dialog.add_btn.clicked.connect(lambda: self.add_rule(dialog))

        # 显示现有规则
        for rule in self.rule_base:
            dialog.rule_list.addItem(
                f"{' ∧ '.join(rule['premise'])} → {rule['conclusion']}"
            )

        dialog.exec_()

    def add_rule(self, dialog):
        """添加规则"""
        text = dialog.rule_input.text().strip()
        if not text:
            QMessageBox.warning(self, "错误", "请输入规则内容")
            return

        if "，" not in text:
            QMessageBox.warning(self, "格式错误", "请使用中文逗号分隔条件和结论")
            return

        premises, conclusion = text.split("，", 1)
        premises = [p.strip() for p in premises.split()]

        valid = list(self.feature_map.values()) + ["哺乳类", "鸟类", "食肉类", "蹄类"]
        for p in premises:
            if p not in valid:
                QMessageBox.warning(self, "错误", f"无效特征: {p}")
                return

        self.rule_base.append({
            "premise": premises,
            "conclusion": conclusion.strip()
        })

        QMessageBox.information(self, "成功", "规则已添加")
        dialog.accept()
        self.display_rules()

    def remove_rule(self):
        """删除规则"""
        if not self.rule_base:
            QMessageBox.warning(self, "错误", "规则库为空")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("删除规则")
        dialog.setFixedSize(600, 400)

        layout = QVBoxLayout()

        # 规则列表
        rule_list = QListWidget()
        for rule in self.rule_base:
            rule_list.addItem(f"{' ∧ '.join(rule['premise'])} → {rule['conclusion']}")

        # 按钮区域
        btn_layout = QHBoxLayout()
        del_btn = QPushButton("删除选中规则")
        cancel_btn = QPushButton("取消")

        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addWidget(rule_list)
        layout.addLayout(btn_layout)
        dialog.setLayout(layout)

        # 信号连接
        def do_delete():
            selected = rule_list.currentRow()
            if selected == -1:
                QMessageBox.warning(dialog, "错误", "请选择要删除的规则")
                return

            self.rule_base.pop(selected)
            QMessageBox.information(dialog, "成功", "规则已删除")
            dialog.accept()
            self.display_rules()

        del_btn.clicked.connect(do_delete)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

    def confirm_remove(self, dialog):
        """确认删除"""
        selected = dialog.rule_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "错误", "请选择要删除的规则")
            return

        self.rule_base.pop(selected)
        QMessageBox.information(self, "成功", "规则已删除")
        dialog.accept()
        self.display_rules()

    def execute_reasoning(self):
        """执行推理"""
        mode = self.mode_selector.currentText()

        if mode == "正向推理":
            self.forward_reason()
        else:
            target = self.target_selector.currentText()
            self.backward_reason(target)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    system = AnimalSystem()
    system.show()
    sys.exit(app.exec_())