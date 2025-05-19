import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox,
    QPushButton, QTextBrowser, QLabel, QGroupBox, QScrollArea,
    QDialog, QLineEdit, QHBoxLayout, QMessageBox, QListWidget, QComboBox
)
from PyQt5.QtCore import Qt


class RuleManagerDialog(QDialog):
    """规则管理对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("规则管理")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # 规则输入框
        self.rule_input = QLineEdit()
        self.rule_input.setPlaceholderText("按“特征1 特征2 …，结论”格式输入规则")
        layout.addWidget(QLabel("输入规则："))
        layout.addWidget(self.rule_input)

        # 按钮区域
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancel")
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        # 规则列表
        self.rule_list = QListWidget()
        layout.addWidget(QLabel("现有规则："))
        layout.addWidget(self.rule_list)

        self.setLayout(layout)


class AnimalRecognitionSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("动物识别系统 - 产生式规则实验")
        self.setGeometry(100, 100, 1000, 800)  # 增大窗口尺寸

        # 初始化知识库
        self.rules = [
            {"if": ["有毛发"], "then": "哺乳类"},
            {"if": ["产奶"], "then": "哺乳类"},
            {"if": ["有羽毛"], "then": "鸟类"},
            {"if": ["会下蛋", "不会飞"], "then": "鸟类"},
            {"if": ["哺乳类", "吃肉"], "then": "食肉类"},
            {"if": ["有犬齿", "有爪", "眼盯前方"], "then": "食肉类"},
            {"if": ["哺乳类", "有蹄"], "then": "蹄类"},
            {"if": ["哺乳类", "反刍"], "then": "蹄类"},
            # 动物识别规则
            {"if": ["食肉类", "黄褐色", "哺乳类", "有斑点"], "then": "金钱豹"},
            {"if": ["食肉类", "黄褐色", "哺乳类", "有黑色条纹"], "then": "虎"},
            {"if": ["有黑色条纹", "蹄类"], "then": "斑马"},
            {"if": ["有斑点", "蹄类", "长脖", "长腿"], "then": "长颈鹿"},
            {"if": ["鸟类", "不会飞", "长脖", "长腿"], "then": "鸵鸟"},
            {"if": ["鸟类", "不会飞", "会游泳", "黑白二色"], "then": "企鹅"},
            {"if": ["鸟类", "善飞"], "then": "信天翁"}
        ]

        self.features = {
            '1': '有毛发', '2': '产奶', '3': '有羽毛', '4': '不会飞',
            '5': '会下蛋', '6': '吃肉', '7': '有犬齿', '8': '有爪',
            '9': '眼盯前方', '10': '有蹄', '11': '反刍', '12': '黄褐色',
            '13': '有斑点', '14': '有黑色条纹', '15': '长脖', '16': '长腿',
            '17': '不会飞', '18': '会游泳', '19': '黑白二色', '20': '善飞'
        }

        self.animal_targets = ["金钱豹", "虎", "斑马", "长颈鹿", "鸵鸟", "企鹅", "信天翁"]

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 标题
        title = QLabel("动物类型产生式推理系统")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 推理模式选择
        mode_group = QGroupBox("推理模式")
        mode_layout = QHBoxLayout()

        self.mode_combo = QComboBox()
        self.mode_combo.addItem("正向推理")
        self.mode_combo.addItem("反向推理")
        mode_layout.addWidget(QLabel("选择推理模式:"))
        mode_layout.addWidget(self.mode_combo)

        # 反向推理目标选择（初始隐藏）
        self.target_combo = QComboBox()
        self.target_combo.addItems(self.animal_targets)
        self.target_combo.setVisible(False)
        mode_layout.addWidget(QLabel("目标动物:"))
        mode_layout.addWidget(self.target_combo)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # 模式切换信号连接
        self.mode_combo.currentTextChanged.connect(self.toggle_reasoning_mode)

        # 规则管理区域
        rule_group = QGroupBox("规则管理")
        rule_layout = QVBoxLayout()

        self.btn_view_rules = QPushButton("查看规则库")
        self.btn_add_rule = QPushButton("添加规则")
        self.btn_del_rule = QPushButton("删除规则")

        self.btn_view_rules.clicked.connect(self.show_rules)
        self.btn_add_rule.clicked.connect(self.add_rule_dialog)
        self.btn_del_rule.clicked.connect(self.delete_rule)

        rule_layout.addWidget(self.btn_view_rules)
        rule_layout.addWidget(self.btn_add_rule)
        rule_layout.addWidget(self.btn_del_rule)
        rule_group.setLayout(rule_layout)
        layout.addWidget(rule_group)

        # 特征选择区域
        feature_group = QGroupBox("选择动物特征")
        feature_layout = QVBoxLayout()

        self.checkboxes = {}
        for key, text in self.features.items():
            cb = QCheckBox(f"{key}: {text}")
            cb.key = key
            self.checkboxes[key] = cb
            feature_layout.addWidget(cb)

        feature_group.setLayout(feature_layout)
        scroll = QScrollArea()
        scroll.setWidget(feature_group)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        # 推理按钮
        self.btn_reason = QPushButton("开始推理")
        self.btn_reason.setStyleSheet("background-color: #4CAF50; color: white;")
        self.btn_reason.clicked.connect(self.start_reasoning)
        layout.addWidget(self.btn_reason)

        # 结果显示区域
        self.result_display = QTextBrowser()
        self.result_display.setStyleSheet("""
            font-family: Consolas; 
            font-size: 32px;
            line-height: 1.5;
        """)
        layout.addWidget(self.result_display)

    def toggle_reasoning_mode(self, mode):
        """切换推理模式"""
        if mode == "反向推理":
            self.target_combo.setVisible(True)
            # 禁用特征选择区域
            for cb in self.checkboxes.values():
                cb.setEnabled(False)
        else:
            self.target_combo.setVisible(False)
            # 启用特征选择区域
            for cb in self.checkboxes.values():
                cb.setEnabled(True)

    def backward_reasoning(self, target):
        """反向推理"""
        self.result_display.clear()
        self.result_display.append(f"=== 反向推理: 证明目标 '{target}' ===")

        required_features = set()
        visited_rules = set()
        queue = [target]

        while queue:
            current = queue.pop(0)

            # 如果是基本特征，直接加入所需特征集
            if current in self.features.values():
                required_features.add(current)
                continue

            # 查找能推导出当前结论的规则
            applicable_rules = [rule for rule in self.rules if rule["then"] == current]

            if not applicable_rules:
                self.result_display.append(f"⚠️ 错误: 没有规则可以推导出 '{current}'")
                continue

            # 使用第一个找到的规则（简化处理）
            rule = applicable_rules[0]
            if str(rule) in visited_rules:
                continue

            visited_rules.add(str(rule))

            self.result_display.append(f"需要满足: {' ∧ '.join(rule['if'])} → {rule['then']}")

            # 将前提条件加入队列
            for cond in rule["if"]:
                if cond not in required_features:
                    queue.append(cond)

        # 显示最终结果
        self.result_display.append("\n=== 反向推理结果 ===")
        if required_features:
            self.result_display.append(f"要证明 '{target}'，需要以下特征:")
            for feature in sorted(required_features):
                self.result_display.append(f" - {feature}")
        else:
            self.result_display.append(f"无法确定证明 '{target}' 所需的特征")

    def show_rules(self):
        """显示所有规则"""
        self.result_display.clear()
        self.result_display.append("=== 当前规则库 ===")
        for i, rule in enumerate(self.rules, 1):
            conditions = " ∧ ".join(rule["if"])
            self.result_display.append(f"{i}. 如果 {conditions} → {rule['then']}")

    def add_rule_dialog(self):
        """添加规则对话框"""
        dialog = RuleManagerDialog(self)
        dialog.btn_ok.clicked.connect(lambda: self.add_rule(dialog))
        dialog.btn_cancel.clicked.connect(dialog.reject)

        # 显示现有规则
        dialog.rule_list.clear()
        for rule in self.rules:
            conditions = " ∧ ".join(rule["if"])
            dialog.rule_list.addItem(f"{conditions} → {rule['then']}")

        dialog.exec_()

    def add_rule(self, dialog):
        """添加新规则"""
        text = dialog.rule_input.text().strip()
        if not text:
            QMessageBox.warning(self, "错误", "请输入规则！")
            return

        if "，" not in text:
            QMessageBox.warning(self, "格式错误", "请使用中文逗号分隔条件和结论！")
            return

        conditions, conclusion = text.split("，", 1)
        conditions = [c.strip() for c in conditions.split()]

        # 检查特征是否存在
        valid_features = list(self.features.values()) + ["哺乳类", "鸟类", "食肉类", "蹄类"]
        for cond in conditions:
            if cond not in valid_features:
                QMessageBox.warning(self, "错误", f"特征 '{cond}' 不在系统中！")
                return

        self.rules.append({"if": conditions, "then": conclusion.strip()})
        QMessageBox.information(self, "成功", "规则已添加！")
        dialog.accept()
        self.show_rules()

    def delete_rule(self):
        """删除规则"""
        if not self.rules:
            QMessageBox.warning(self, "错误", "规则库为空！")
            return

        dialog = RuleManagerDialog(self)
        dialog.setWindowTitle("删除规则")
        dialog.rule_input.setVisible(False)
        dialog.btn_ok.setText("删除选中规则")

        # 显示规则列表
        dialog.rule_list.clear()
        for rule in self.rules:
            conditions = " ∧ ".join(rule["if"])
            dialog.rule_list.addItem(f"{conditions} → {rule['then']}")

        dialog.rule_list.setSelectionMode(QListWidget.SingleSelection)
        dialog.btn_ok.clicked.connect(lambda: self.confirm_delete(dialog))
        dialog.exec_()

    def confirm_delete(self, dialog):
        """确认删除规则"""
        selected = dialog.rule_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "错误", "请选择要删除的规则！")
            return

        del self.rules[selected]
        QMessageBox.information(self, "成功", "规则已删除！")
        dialog.accept()
        self.show_rules()

    def start_reasoning(self):
        """开始推理"""
        mode = self.mode_combo.currentText()

        if mode == "正向推理":
            self.forward_reasoning()
        else:
            target = self.target_combo.currentText()
            self.backward_reasoning(target)

    def forward_reasoning(self):
        """正向推理"""
        selected_features = [
            self.features[cb.key] for cb in self.checkboxes.values() if cb.isChecked()
        ]

        if not selected_features:
            self.result_display.append("⚠️ 请至少选择一个特征！")
            return

        self.result_display.clear()
        self.result_display.append("=== 正向推理过程 ===")
        self.result_display.append(f"初始事实: {' ∧ '.join(selected_features)}")

        # 正向推理
        new_facts = True
        while new_facts:
            new_facts = False
            for rule in self.rules:
                if all(cond in selected_features for cond in rule["if"]) and rule["then"] not in selected_features:
                    selected_features.append(rule["then"])
                    self.result_display.append(f"应用规则: {' ∧ '.join(rule['if'])} → {rule['then']}")
                    new_facts = True

        # 显示最终结果
        self.result_display.append("\n=== 推理结果 ===")
        possible_animals = [fact for fact in selected_features if
                            fact in ["金钱豹", "虎", "斑马", "长颈鹿", "鸵鸟", "企鹅", "信天翁"]]

        if possible_animals:
            self.result_display.append(f"识别结果: {possible_animals[0]}")
        else:
            self.result_display.append("无法确定具体动物类型")
            self.result_display.append(f"推导出的中间结论: {' ∧ '.join(selected_features)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimalRecognitionSystem()
    window.show()
    sys.exit(app.exec_())