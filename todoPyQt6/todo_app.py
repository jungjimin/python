import sys
import sqlite3
from plyer import notification
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem, QMenu, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
import time


class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List")
        self.setGeometry(100, 100, 700, 650)
        self.setMinimumSize(400, 300)

        self.conn = sqlite3.connect("todos.db")
        self.c = self.conn.cursor()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY,
                category TEXT,
                task TEXT,
                completed BOOLEAN,
                progress INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

        self.categories = {}
        self.task_timers = {}

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.initUI()
        self.style_ui()

        # 기본 카테고리 생성
        for category in ["현안", "기타", "Today"]:
            if category not in self.categories:
                self.create_category_section(category)

    def initUI(self):
        header_widget = QWidget()
        header_widget.setObjectName("header_widget")
        header_layout = QVBoxLayout(header_widget)

        title = QLabel("📌 Todo List")
        self.stats_label = QLabel("완료된 할 일: 0 / 전체: 0")
        self.stats_label.setObjectName("stats_label")

        header_layout.addWidget(title)
        header_layout.addWidget(self.stats_label)
        self.layout.addWidget(header_widget)

        self.load_from_db()

    def style_ui(self):
        """라이트 모드 스타일"""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', 'Noto Sans KR', sans-serif;
                background-color: #FDFDFD;
                color: #222222;
            }
            QMainWindow { background-color: #FFFFFF; }
            #header_widget {
                background-color: #F5F7FB;
                border-radius: 16px;
                padding: 16px;
                border: 1px solid #DDDDDD;
            }
            /* 카테고리 섹션 스타일 추가 */
            QWidget#category_section {
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 12px;
                border: 1px solid #E0E0E0;
                margin-top: 10px; /* 섹션 상단 여백 추가 */
            }                           
            QLabel#stats_label {
                font-size: 9pt;
                font-weight: 500;
                background-color: #E6F0FF;
                padding: 6px 12px;
                border-radius: 12px;
            }
            QListWidget {
                border: none;
                background-color: transparent;
                padding: 0;
            }
            .todo-item {
                background-color: #FAFAFA;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin: 4px;
                padding: 8px;
            }
            QLabel[completed="true"] {
                text-decoration: line-through;
                color: #888888;
            }
            QPushButton {
                background: transparent;
                border: none;
                font-size: 10pt;
                padding: 4px 6px;
                border-radius: 6px;
                min-width: 24px;
            }
            QPushButton:hover {
                background-color: #E6F0FF;
                color: #2A6BE3;
            }
            QPushButton[class="complete-button"] { color: #28A745; }
            QPushButton[class="delete-button"] { color: #E53935; }
            QPushButton[class="alarm-button"] { color: #FF9800; }
            QLabel[class="alarm-timer"] {
                font-size: 9pt;
                color: #FF9800;
                background-color: #FFF3E0;
                padding: 4px 8px;
                border-radius: 8px;
            }
            QLabel[class="progress-display"] {
                font-size: 9pt;
                padding: 4px 8px;
                border-radius: 8px;
                border: 1px solid #CCCCCC;
                font-family: 'Consolas', 'Monaco', monospace;
                max-width: 200px;
            }
            QLineEdit[class="progress-input"] {
                max-width: 50px;
                border: 1px solid #BBBBBB;
                border-radius: 6px;
                padding: 4px;
                font-size: 9pt;
                background-color: #FFFFFF;
            }
        """)

    def load_from_db(self):
        category_order = ["현안", "기타", "Today"]
        self.c.execute("SELECT * FROM todos ORDER BY category, id")
        todos = self.c.fetchall()

        for category in category_order:
            if category not in self.categories:
                self.create_category_section(category)

        for todo in todos:
            _, category, task, completed, progress = todo
            if category not in self.categories:
                self.create_category_section(category)
            self.add_task(category, task, completed, progress, save_to_db=False)
        self.update_stats()

    def create_category_section(self, category_name):
        section_widget = QWidget()
        # 이 부분을 추가하여 스타일시트에서 참조할 수 있게 합니다.
        section_widget.setObjectName("category_section") 
        section_layout = QVBoxLayout(section_widget)        

        header = QLabel(category_name)

        task_input = QLineEdit()
        task_input.setPlaceholderText(f"{category_name} 할 일 입력")
        task_input.returnPressed.connect(lambda: self.add_task(category_name, task_input.text()))

        add_task_button = QPushButton("+")
        add_task_button.clicked.connect(lambda: self.add_task(category_name, task_input.text()))

        input_layout = QHBoxLayout()
        input_layout.addWidget(task_input)
        input_layout.addWidget(add_task_button)

        task_list = QListWidget()

        section_layout.addWidget(header)
        section_layout.addLayout(input_layout)
        section_layout.addWidget(task_list)

        self.layout.addWidget(section_widget)

        self.categories[category_name] = {
            "task_input": task_input,
            "task_list": task_list
        }

    def add_task(self, category, task_text, completed=False, progress=0, save_to_db=True):
        if not task_text.strip():
            return

        item = QListWidgetItem()
        item_widget = QWidget()
        item_widget.setObjectName("todo-item")
        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(6)

        label = QLabel(task_text)
        label.setProperty("completed", str(completed).lower())
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        if completed:
            label.setStyleSheet("text-decoration: line-through; color: gray;")

        # 진행률 표시
        progress_display = QLabel()
        progress_display.setProperty("class", "progress-display")
        progress_display.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.update_progress_display(progress_display, progress)
        progress_display.mouseDoubleClickEvent = lambda event: self.start_progress_edit(progress_input, progress_display)

        progress_input = QLineEdit(str(progress))
        progress_input.setProperty("class", "progress-input")
        progress_input.hide()
        progress_input.editingFinished.connect(
            lambda: self.finish_progress_edit(task_text, category, progress_input, progress_display)
        )
        progress_input.returnPressed.connect(progress_input.clearFocus)

        complete_button = QPushButton("✓")
        complete_button.setProperty("class", "complete-button")

        delete_button = QPushButton("🗑")
        delete_button.setProperty("class", "delete-button")

        alarm_button = QPushButton("⏰")
        alarm_button.setProperty("class", "alarm-button")

        timer_label = QLabel("")
        timer_label.setProperty("class", "alarm-timer")

        layout.addWidget(label)
        layout.addWidget(progress_display)
        layout.addWidget(progress_input)
        layout.addWidget(timer_label)
        layout.addSpacing(10)

        # 버튼 순서: 알림 → 완료 → 삭제
        if category != "현안":
            layout.addWidget(alarm_button)
        layout.addWidget(complete_button)
        layout.addWidget(delete_button)

        item.setSizeHint(item_widget.sizeHint())
        self.categories[category]["task_list"].addItem(item)
        self.categories[category]["task_list"].setItemWidget(item, item_widget)

        if save_to_db:
            self.c.execute(
                "INSERT INTO todos (category, task, completed, progress) VALUES (?, ?, ?, ?)",
                (category, task_text, completed, int(progress))
            )
            self.conn.commit()

        self.update_stats()

        complete_button.clicked.connect(lambda: self.toggle_complete(label, task_text, category))
        delete_button.clicked.connect(lambda: self.delete_task(item, task_text, category))
        if category != "현안":
            alarm_button.clicked.connect(lambda: self.show_alarm_menu(alarm_button, task_text, timer_label))

        if save_to_db:
            self.categories[category]["task_input"].clear()

    def update_progress_display(self, display_label, progress):
        window_width = self.width()
        total_bars = 20 if window_width >= 650 else 15 if window_width >= 500 else 10
        filled_bars = int((progress / 100) * total_bars)
        empty_bars = total_bars - filled_bars
        progress_bar = "█" * filled_bars + "░" * empty_bars
        display_text = f"{progress_bar} ({progress}%)"
        display_label.setText(display_text)

        if progress >= 100:
            color = "#28A745"
            bg_color = "#D4EDDA"
        elif progress >= 75:
            color = "#2A6BE3"
            bg_color = "#E6F0FF"
        elif progress >= 50:
            color = "#FF9800"
            bg_color = "#FFF3E0"
        elif progress >= 25:
            color = "#FFC107"
            bg_color = "#FFF8E1"
        else:
            color = "#DC3545"
            bg_color = "#F8D7DA"

        display_label.setStyleSheet(f"""
            QLabel[class="progress-display"] {{
                font-size: 9pt;
                color: {color};
                background-color: {bg_color};
                padding: 4px 8px;
                border-radius: 8px;
                border: 1px solid {color}40;
                font-family: 'Consolas', 'Monaco', monospace;
                max-width: 200px;
            }}
            QLabel[class="progress-display"]:hover {{
                opacity: 0.8;
            }}
        """)

    def start_progress_edit(self, input_field, display_label):
        current_text = display_label.text()
        if "(" in current_text and "%" in current_text:
            progress_str = current_text.split("(")[1].split("%")[0]
            input_field.setText(progress_str)
        display_label.hide()
        input_field.show()
        input_field.setFocus()
        input_field.selectAll()

    def finish_progress_edit(self, task_text, category, input_field, display_label):
        try:
            progress = int(input_field.text())
            progress = max(0, min(100, progress))
            self.c.execute(
                "UPDATE todos SET progress=? WHERE task=? AND category=?",
                (progress, task_text, category)
            )
            self.conn.commit()
            self.update_progress_display(display_label, progress)
        except ValueError:
            pass
        input_field.hide()
        display_label.show()

    # 기존 알람, 완료, 삭제 기능 그대로 유지
    def toggle_complete(self, label, task_text, category):
        completed = label.property("completed") == "false"
        label.setProperty("completed", str(completed).lower())
        label.setStyleSheet("text-decoration: line-through; color: gray;" if completed else "")
        self.c.execute(
            "UPDATE todos SET completed=? WHERE task=? AND category=?",
            (completed, task_text, category)
        )
        self.conn.commit()
        self.update_stats()

    def delete_task(self, item, task_text, category):
        if task_text in self.task_timers:
            timer_info = self.task_timers[task_text]
            timer_info['timer'].stop()
            if 'update_timer' in timer_info:
                timer_info['update_timer'].stop()
            del self.task_timers[task_text]
        self.c.execute("DELETE FROM todos WHERE task=? AND category=?", (task_text, category))
        self.conn.commit()
        self.categories[category]["task_list"].takeItem(
            self.categories[category]["task_list"].row(item)
        )
        self.update_stats()

    def show_alarm_menu(self, button, task_text, timer_label):
        menu = QMenu()
        action_5s = menu.addAction("5초 후")
        action_30m = menu.addAction("30분 후")
        action_1h = menu.addAction("1시간 후")
        action = menu.exec_(button.mapToGlobal(button.rect().bottomLeft()))
        if action == action_5s:
            self.set_alarm(task_text, 5, timer_label)
        elif action == action_30m:
            self.set_alarm(task_text, 30 * 60, timer_label)
        elif action == action_1h:
            self.set_alarm(task_text, 60 * 60, timer_label)

    def set_alarm(self, task_text, seconds, timer_label):
        if task_text in self.task_timers:
            self.task_timers[task_text]['timer'].stop()
        end_time = time.time() + seconds
        timer = QTimer()
        self.task_timers[task_text] = {
            'timer': timer,
            'end_time': end_time,
            'label': timer_label
        }
        update_timer = QTimer()
        update_timer.timeout.connect(lambda: self.update_timer_display(task_text))
        update_timer.start(1000)
        self.task_timers[task_text]['update_timer'] = update_timer
        timer.timeout.connect(lambda: self.trigger_alarm(task_text))
        timer.setSingleShot(True)
        timer.start(seconds * 1000)
        self.update_timer_display(task_text)

    def update_timer_display(self, task_text):
        if task_text not in self.task_timers:
            return
        timer_info = self.task_timers[task_text]
        remaining = timer_info['end_time'] - time.time()
        if remaining <= 0:
            timer_info['label'].setText("")
            if 'update_timer' in timer_info:
                timer_info['update_timer'].stop()
            return
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        time_str = f"{minutes}m {seconds}s" if remaining >= 60 else f"{seconds}s"
        timer_info['label'].setText(time_str)
        timer_info['label'].show()

    def trigger_alarm(self, task_text):
        notification.notify(
            title="할 일 알림",
            message=f"⏰ {task_text}",
            timeout=10
        )
        if task_text in self.task_timers:
            timer_info = self.task_timers[task_text]
            timer_info['label'].setText("")
            if 'update_timer' in timer_info:
                timer_info['update_timer'].stop()
            del self.task_timers[task_text]       

    def update_stats(self):
        self.c.execute("SELECT COUNT(*), SUM(completed) FROM todos")
        total, completed = self.c.fetchone()
        completed = completed or 0
        self.stats_label.setText(f"완료된 할 일: {completed} / 전체: {total}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())
