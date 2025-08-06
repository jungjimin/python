import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem,
    QMessageBox, QDialog, QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QDateTime, QObject, pyqtSignal
from PyQt6.QtGui import QFont, QFontDatabase, QFontMetrics, QColor

# 데이터 파일명
DATA_FILE = "todos.json"

class TodoApp(QMainWindow):
    notification_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List 📝")
        self.setFixedSize(480, 700)

        # 폰트 로드: NotoSansKR-VariableFont_wght.ttf 파일이 같은 폴더에 있어야 합니다.
        if QFontDatabase.addApplicationFont("NotoSansKR-VariableFont_wght.ttf") == -1:
            print("폰트 파일 'NotoSansKR-VariableFont_wght.ttf'을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        self.setFont(QFont("Noto Sans KR"))

        # 아이콘 폰트가 깨지는 문제를 해결하기 위해 유니코드 문자로 직접 지정
        self.icon_map = {
            "done": "✔",
            "delete": "🗑",
            "alarm": "⏰",
            "add": "➕"
        }

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_widget.setLayout(self.main_layout)

        self.todos = self.load_todos()
        self.alarms = {}
        
        self.setup_ui()
        self.style_ui()
        self.start_alarms()
        
        self.notification_signal.connect(self.show_notification)

    def setup_ui(self):
        title_label = QLabel("To-Do List 📝")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)

        self.categories = ["반영", "문의", "기타"]
        self.list_widgets = {}

        for category in self.categories:
            self.create_category_box(category)
            
    def apply_shadow(self, widget, color, blur_radius=12, x_offset=0, y_offset=4):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(color))
        shadow.setBlurRadius(blur_radius)
        shadow.setOffset(x_offset, y_offset)
        widget.setGraphicsEffect(shadow)

    def style_ui(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Noto Sans KR';
                background-color: #FAFAFA;
                color: #212529;
            }
            QMainWindow {
                background-color: #FAFAFA;
            }
            QLabel#title_label {
                color: #3F51B5;
                font-size: 26pt;
                font-weight: 700;
                margin-bottom: 25px;
            }
            .category-box {
                background-color: #FFFFFF;
                padding: 18px;
                border-radius: 16px;
                border: 1px solid #E0E0E0;
            }
            .category-box QLabel {
                color: #3F51B5;
                font-size: 18pt;
                font-weight: bold;
                padding-bottom: 8px;
                margin-bottom: 16px;
                border-bottom: 2px solid #F0F0F0;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #DADCE0;
                border-radius: 10px;
                font-size: 12pt;
                background: #FFFFFF;
            }
            #add-icon-button {
                background-color: #3F51B5;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 16pt;
                width: 36px;
                height: 36px;
            }
            #add-icon-button:hover {
                background-color: #303F9F;
            }

            QListWidget {
                border: none;
                background-color: #FFFFFF;
                padding-top: 12px;
            }

            QListWidget::item {
                background-color: transparent;
                padding: 0;
            }

            .todo-item-widget {
                background-color: #FDFDFD;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                margin-bottom: 10px;
            }

            .todo-text {
                font-size: 13pt;
                padding: 0 8px;
                margin-right: 10px;
            }

            #action-button {
                background: transparent;
                border: none;
                font-size: 16pt;
                padding: 0 4px;
                margin: 0;
            }

            #complete-button {
                color: #4CAF50;
            }

            #delete-button {
                color: #F44336;
            }

            #alarm-button {
                color: #FFC107;
            }

            #alarm-timer {
                font-size: 11pt;
                font-weight: 600;
                color: #FF9800;
                padding-right: 5px;
            }

            QLabel[completed="true"] {
                text-decoration: line-through;
                color: #9E9E9E;
            }
        """)

    def create_category_box(self, category):
        category_box = QFrame()
        category_box.setObjectName("category-box")
        category_box_layout = QVBoxLayout()
        category_box.setLayout(category_box_layout)
        self.main_layout.addWidget(category_box)
        self.apply_shadow(category_box, "#000000", 12, 0, 4)

        category_label = QLabel(category)
        category_label.setObjectName("category_label")
        category_box_layout.addWidget(category_label)

        input_layout = QHBoxLayout()
        task_input = QLineEdit()
        task_input.setPlaceholderText("할 일 입력")
        
        add_button = QPushButton(self.icon_map["add"])
        add_button.setObjectName("add-icon-button")

        input_layout.addWidget(task_input)
        input_layout.addWidget(add_button)
        category_box_layout.addLayout(input_layout)

        todo_list = QListWidget()
        todo_list.setObjectName("todo_list")
        category_box_layout.addWidget(todo_list)
        self.list_widgets[category] = todo_list
        
        add_button.clicked.connect(lambda: self.add_todo(category, task_input))
        task_input.returnPressed.connect(lambda: self.add_todo(category, task_input))
        
        self.update_list(category)

    def create_todo_item_widget(self, item_data, category, todo_id):
        widget = QWidget()
        widget.setObjectName("todo-item-widget")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        widget.setLayout(layout)

        text_label = QLabel(item_data['text'])
        text_label.setObjectName("todo-text")
        text_label.setWordWrap(True)
        text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        if item_data['completed']:
            text_label.setProperty("completed", True)
        else:
            text_label.setProperty("completed", False)
        
        layout.addWidget(text_label)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(5)
        
        # 버튼의 투명 배경은 스타일시트로 처리했기 때문에 여기서는 제거
        if item_data.get('alarmTime') and not item_data['completed']:
            timer_label = QLabel()
            timer_label.setObjectName("alarm-timer")
            action_layout.addWidget(timer_label)
        else:
            alarm_button = QPushButton(self.icon_map["alarm"])
            alarm_button.setObjectName("alarm-button")
            alarm_button.clicked.connect(lambda: self.show_alarm_options(category, todo_id))
            alarm_button.setHidden(item_data['completed'])
            action_layout.addWidget(alarm_button)

        complete_button = QPushButton(self.icon_map["done"])
        complete_button.setObjectName("complete-button")
        complete_button.clicked.connect(lambda: self.toggle_complete(category, todo_id))
        complete_button.setHidden(item_data['completed'])
        action_layout.addWidget(complete_button)
        
        delete_button = QPushButton(self.icon_map["delete"])
        delete_button.setObjectName("delete-button")
        delete_button.clicked.connect(lambda: self.delete_todo(category, todo_id))
        action_layout.addWidget(delete_button)
        
        layout.addLayout(action_layout)

        return widget

    def load_todos(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not data or not isinstance(data, dict):
                        return {category: [] for category in ["반영", "문의", "기타"]}
                    return data
            else:
                return {category: [] for category in ["반영", "문의", "기타"]}
        except (IOError, json.JSONDecodeError):
            return {category: [] for category in ["반영", "문의", "기타"]}
            
    def save_todos(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=4)
            
    def add_todo(self, category, input_widget):
        task_text = input_widget.text().strip()
        if not task_text:
            return
        
        new_todo = {
            'id': QDateTime.currentMSecsSinceEpoch(),
            'text': task_text, 
            'completed': False, 
            'alarmTime': None
        }
        self.todos[category].insert(0, new_todo)
        self.save_todos()
        self.update_list(category)
        input_widget.clear()

    def update_list(self, category):
        list_widget = self.list_widgets[category]
        list_widget.clear()
        
        for item_data in self.todos[category]:
            item = QListWidgetItem(list_widget)
            custom_widget = self.create_todo_item_widget(item_data, category, item_data['id'])
            
            # 위젯의 내용에 맞춰 아이템의 높이를 조절
            item.setSizeHint(custom_widget.sizeHint())
            
            list_widget.addItem(item)
            list_widget.setItemWidget(item, custom_widget)

    def find_todo_item(self, category, todo_id):
        for item in self.todos.get(category, []):
            if item['id'] == todo_id:
                return item
        return None

    def find_todo_index(self, category, todo_id):
        for i, item in enumerate(self.todos.get(category, [])):
            if item['id'] == todo_id:
                return i
        return -1

    def toggle_complete(self, category, todo_id):
        item = self.find_todo_item(category, todo_id)
        if item:
            item['completed'] = True
            item['alarmTime'] = None
            if todo_id in self.alarms:
                self.alarms[todo_id]['timer'].stop()
                del self.alarms[todo_id]
            self.save_todos()
            self.update_list(category)

    def delete_todo(self, category, todo_id):
        index = self.find_todo_index(category, todo_id)
        if index != -1:
            del self.todos[category][index]
            if todo_id in self.alarms:
                self.alarms[todo_id]['timer'].stop()
                del self.alarms[todo_id]
            self.save_todos()
            self.update_list(category)

    def show_alarm_options(self, category, todo_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("알림 설정")
        dialog.setFixedSize(200, 150)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        label = QLabel("알림 시간을 선택하세요.")
        label.setStyleSheet("font-size: 11pt; margin-bottom: 10px;")
        layout.addWidget(label)

        times = [("5초 뒤", 5), ("30분 뒤", 1800), ("1시간 뒤", 3600)]
        
        for text, seconds in times:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, s=seconds: self.set_alarm(category, todo_id, s, dialog))
            layout.addWidget(btn)
        
        dialog.exec()

    def set_alarm(self, category, todo_id, seconds, dialog):
        item = self.find_todo_item(category, todo_id)
        if item:
            alarm_time = QDateTime.currentDateTime().addSecs(seconds)
            item['alarmTime'] = alarm_time.toString(Qt.DateFormat.ISODate)
            self.save_todos()
            self.update_list(category)
            self.start_alarms_for_item(category, todo_id)
            dialog.accept()

    def start_alarms(self):
        for category in self.categories:
            for item_data in self.todos.get(category, []):
                if item_data.get('alarmTime') and not item_data['completed']:
                    self.start_alarms_for_item(category, item_data['id'])

    def start_alarms_for_item(self, category, todo_id):
        if todo_id in self.alarms:
            self.alarms[todo_id]['timer'].stop()
            del self.alarms[todo_id]

        timer = QTimer(self)
        timer.timeout.connect(lambda: self.update_alarm_display(category, todo_id))
        self.alarms[todo_id] = {'timer': timer}
        timer.start(1000)

    def update_alarm_display(self, category, todo_id):
        item_data = self.find_todo_item(category, todo_id)
        if not item_data or item_data['completed']:
            if todo_id in self.alarms:
                self.alarms[todo_id]['timer'].stop()
                del self.alarms[todo_id]
            self.update_list(category)
            return

        alarm_time = QDateTime.fromString(item_data['alarmTime'], Qt.DateFormat.ISODate)
        if not alarm_time.isValid():
            return

        remaining_seconds = QDateTime.currentDateTime().secsTo(alarm_time)

        if remaining_seconds <= 0:
            self.notification_signal.emit(item_data['text'], category)
            item_data['alarmTime'] = None
            self.save_todos()
            self.update_list(category)
            return

        minutes, seconds = divmod(remaining_seconds, 60)
        time_text = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"

        list_widget = self.list_widgets[category]
        index = self.find_todo_index(category, todo_id)
        if index != -1:
            item_widget = list_widget.itemWidget(list_widget.item(index))
            if item_widget:
                timer_label = item_widget.findChild(QLabel, "alarm-timer")
                if timer_label:
                    timer_label.setText(time_text)
                
    def show_notification(self, message, category):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("할 일 알림")
        msg_box.setText(f"🚨 **알림:** {message}")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())