import os.path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QMenu, QAction, QHBoxLayout, QCheckBox, QGridLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
import keyboard
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon
import configparser
import time
from pyautogui import click
import ctypes
from ctypes import wintypes
import subprocess

q = "q"
w = "w"
e = "e"

def get_keyboard_layout():
    keyboard_layouts = {
        0x0409: "en",
        0x0419: "ru"
    }
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    GetKeyboardLayout = user32.GetKeyboardLayout
    GetKeyboardLayout.restype = wintypes.HKL
    GetKeyboardLayout.argtypes = [wintypes.DWORD]
    thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
    layout = GetKeyboardLayout(thread_id)
    layout_id = layout & 0xFFFF  # Получаем идентификатор раскладки
    _keyboard = keyboard_layouts.get(layout_id, 'none')
    if _keyboard == "none":
        with open("log.txt", "w") as f:
            f.write("UNEXPECTED KEYBOARD LANGUAGE")
        sys.exit(app.exec_())
    return _keyboard
_lang = get_keyboard_layout()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.css = ("background-color: white; background-image: url(4234)")
        self.setWindowTitle("auto invoka by ask3l")
        self.setGeometry(100, 100, 300, 370)
        self.setFixedSize(300, 370)
        self.setStyleSheet("background-image: url(resourses/background.png)")
        self.transparent_window = TransparentWindow()
        self.setWindowIcon(QIcon("resourses/ico.png"))
        self.settings_window = None
        self.init_ui()
        self.init_tray_icon()
        self.last_cast = 0
        self.binds = {}

        if os.path.exists("resourses/config.ini"):
            config = configparser.ConfigParser()
            config.read("resourses/config.ini")
            self.press1 = int(config["settings"]["press1"])
            self.press2 = int(config["settings"]["press2"])
        else:
            config = configparser.ConfigParser()
            config.add_section("settings")
            config.add_section("keybindings")
            config["settings"] = {"press1": "1", "press2": "0"}
            default_keybindings = {"cold snap": "1", "ghost walk": "2", "ice wall": "3", "emp": "4", "tornado": "5",
                                   "alacrity": "6", "sun strike": "7", "forge spirits": "8", "chaos meteor": "9",
                                   "deafening blast": "0", "refresher": "x", "hex or silence": "c"}

            config["keybindings"] = default_keybindings
            with open("resourses/config.ini", "w") as f:
                config.write(f)
            self.press1 = 1
            self.press2 = 0



    def press(self, letter):
        keyboard.press(letter)
        keyboard.release(letter)

    def cast(self, buttons: list):
        global q
        global w
        global e
        global _lang
        lang = _lang
        if lang == "en":
            print(time.time() - self.last_cast, f" {lang}")
            if time.time() - self.last_cast >= 0.7:
                for i in buttons:
                    self.press(i)
                self.press("r")
                self.last_cast = time.time()
                if self.press1:
                    time.sleep(0.1)
                    self.press("d")
                    if buttons == [w, w, e]:
                        self.press("d")
                    if self.press2 and buttons not in [[q, q, w], [q, q, e], [e, e, q], [w, w, e]]:
                        click(button="left")
        else:
            print(time.time() - self.last_cast, f" {lang}")
            if time.time() - self.last_cast >= 0.7:
                rep = {"q": "й", "w": "ц", "e": "у"}
                for i in buttons:
                    self.press(rep[i])
                self.press("к")
                self.last_cast = time.time()
                if self.press1:
                    time.sleep(0.1)
                    self.press("в")
                    if buttons == [w, w, e]:
                        self.press("в")
                    if self.press2 and buttons not in [[q, q, w], [q, q, e], [e, e, q], [w, w, e]]:
                        click(button="left")



    def init_ui(self):
        self.button1 = QPushButton("Включить")
        self.button1_state = "off"
        self.button1.clicked.connect(self.on_off)
        self.button1.setStyleSheet(self.css)

        self.button2 = QPushButton("Открыть окно подсказок")
        self.button2.clicked.connect(self._transparent_window)
        self.button2.setStyleSheet(self.css)
        self.button2_state = "off"

        self.toggle_drag_button = QPushButton("Закрепить окно")
        self.toggle_drag_button.clicked.connect(self.toggle_dragging)
        self.toggle_drag_button.setEnabled(False)
        self.toggle_drag_button.setStyleSheet(self.css)

        self.button3 = QPushButton("Настройки")
        self.button3.clicked.connect(self.open_settings)
        self.button3.setStyleSheet(self.css)

        # Настраиваем layout для уменьшения расстояния между кнопками
        layout = QVBoxLayout()
        # Добавляем виджеты в layout
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.toggle_drag_button)
        layout.addWidget(self.button3)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def hook_binds(self):
        global q
        global w
        global e
        config = configparser.ConfigParser()
        config.read("resourses/config.ini")
        spells = {"cold snap": [q, q, q], "ghost walk": [q, q, w], "ice wall": [q, q, e], "emp": [w, w, w], "tornado": [w, w, q], "alacrity": [w, w, e], "sun strike": [e, e, e], "forge spirits": [e, e, q], "chaos meteor": [e, e, w], "deafening blast": [q, w, e]}
        for key, value in config["keybindings"].items():
            if key not in ["refresher", "hex or silence"]:
                self.binds[key] = keyboard.add_hotkey(value, self.cast, args=(spells[key],))

            else:
                pass

    def unhook_binds(self):
        for key in self.binds:
            keyboard.remove_hotkey(self.binds[key])
    def on_off(self):
        if self.button1_state == "off":

            self.button1_state = "on"

            self.button3.setEnabled(False)
            self.hook_binds()
            self.button1.setText("Вырубить")
            if self.settings_window:
                self.settings_window.close()
                self.settings_window = None
        else:
            self.button1_state = "off"

            self.unhook_binds()

            self.button3.setEnabled(True)
            self.button1.setText("Включить")

    def _transparent_window(self):
        if self.button2_state == "off":
            self.button2_state = "on"
            self.transparent_window.show()
            self.toggle_drag_button.setEnabled(True)
            self.button2.setText("Закрыть")
        else:
            self.button2_state = "off"
            self.toggle_drag_button.setEnabled(False)
            self.button2.setText("Открыть окно подсказок")
            self.transparent_window.close()



    def toggle_dragging(self):
        self.transparent_window.toggle_dragging()
        self.toggle_drag_button.setText("Открепить окно" if not self.transparent_window.draggable else "Закрепить окно")

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.button3.setEnabled(False)
        self.settings_window.show()
    def init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(QIcon("resourses/ico.png"), self)

        # Создаем контекстное меню для иконки в трее
        tray_menu = QMenu()

        restore_action = QAction("Показать", self)
        restore_action.triggered.connect(self.restore_window)
        tray_menu.addAction(restore_action)

        quit_action = QAction("Отрастить прямые руки", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.icon_activated)

        self.tray_icon.show()

    def closeEvent(self, event):
        # Переопределяем событие закрытия окна, чтобы скрыть его вместо закрытия
        self.hide()
        event.ignore()

    def restore_window(self):
        # Восстанавливаем главное окно при клике на иконку в трее
        self.show()
        self.raise_()
        self.activateWindow()

    def icon_activated(self, reason):
        # Если иконка в трее была кликнута, восстанавливаем окно
        if reason == QSystemTrayIcon.Trigger:
            self.restore_window()

    def quit_application(self):
        # Закрываем приложение при выборе "Quit" в контекстном меню
        QApplication.quit()



class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ПодсказОЧКА")
        self.setGeometry(200, 200, 400, 300)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")

        self.draggable = True
        layout = QVBoxLayout()
        label = QLabel("*ТУТ ТЕКСТ*")
        label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(label)
        self.setLayout(layout)
        self._start_pos = None

    def _close(self):
        main_window.toggle_drag_button.setEnabled(False)
        self.close()
    def toggle_dragging(self):
        self.draggable = not self.draggable

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self._start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() == Qt.LeftButton and self._start_pos is not None:
            self.move(event.globalPos() - self._start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self._start_pos = None
            event.accept()



class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("настройке(твой батя)")
        self.setGeometry(137, 143, 400, 400)
        self.setWindowIcon(QIcon("resourses/settings.png"))
        self.abilities = [
            "cold snap", "ghost walk", "ice wall", "emp", "tornado",
            "alacrity", "sun strike", "forge spirits", "chaos meteor", "deafening blast", "refresher", "hex or silence"
        ]
        self.default_keybindings = {"cold snap": "1", "ghost walk": "2", "ice wall": "3", "emp": "4", "tornado": "5", "alacrity": "6", "sun strike": "7", "forge spirits": "8", "chaos meteor": "9", "deafening blast": "0", "refresher": "x", "hex or silence": "c"}
        self.keybindings = {}
        config = configparser.ConfigParser()
        config.read("resourses/config.ini")
        if config.has_section("keybindings"):
            for key, value in config["keybindings"].items():
                self.keybindings[key] = value
        else:
            self.keybindings = self.default_keybindings.copy()
            config["keybindings"] = self.keybindings
            config["settings"] = {"press1": str(int(main_window.press1)), "press2": str(int(main_window.press2))}

            with open("resourses/config.ini", "w") as f:
                config.write(f)

        self.current_ability = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        ability_lines = {}
        for ability in self.abilities:
            row_layout = QHBoxLayout()

            label = QLabel(ability.title())
            key_display = QLabel(self.keybindings[ability])  # Показываем назначенную клавишу=
            ability_lines[ability] = key_display
            change_button = QPushButton("Изменить")
            change_button.clicked.connect(lambda checked, a=ability, kd=key_display: self.change_key(a, kd))
            change_button.setStyleSheet(main_window.css)

            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(lambda delete, name=ability: self.edit_key(name))
            delete_button.setStyleSheet(main_window.css)

            reset_button = QPushButton("Ресет")
            reset_button.clicked.connect(lambda reset, name=ability, change=self.default_keybindings[ability]: self.edit_key(name, change))
            reset_button.setStyleSheet(main_window.css)
            row_layout.addWidget(label)
            row_layout.addWidget(key_display)
            row_layout.addWidget(change_button)
            row_layout.addWidget(reset_button)
            row_layout.addWidget(delete_button)
            layout.addLayout(row_layout)
            if ability == "deafening blast":
                line = QFrame()
                line.setFrameShape(QFrame.HLine)  # Горизонтальная линия
                line.setFrameShadow(QFrame.Sunken)  # Оттенок для линии
                line.setLineWidth(2)  # Толщина линии

                line2 = QFrame()
                line2.setFrameShape(QFrame.HLine)
                line2.setFrameShadow(QFrame.Sunken)
                line2.setLineWidth(2)
                # Текст для разделителя
                text_label = QLabel("Ваши бинды на предметы")
                text_label.setAlignment(Qt.AlignCenter)
                # text_label.setStyleSheet(
                #     "background-color: white; padding: 0 10px;")  # Белый фон, чтобы текст был видим на фоне линии

                _line = QVBoxLayout()

                _line.addWidget(line)
                _line.addWidget(text_label)
                _line.addWidget(line2)
                _line.setSpacing(3)
                layout.addLayout(_line)

        self.abilities_lines = ability_lines

        container = QWidget()
        layout2 = QVBoxLayout()

        # Тумблеры (чекбоксы)
        toggle1 = QCheckBox("Прожимать скил")
        # toggle1.setLayoutDirection(Qt.RightToLeft)
        toggle1.setStyleSheet("""
                    QCheckBox::indicator {
                        width: 17px;   /* Ширина чекбокса */
                        height: 17px;  /* Высота чекбокса */
                    }
                """)
        toggle1.setChecked(main_window.press1)
        toggle1.stateChanged.connect(self.state1)



        layout2.addWidget(toggle1)

        self.toggle2 = QCheckBox("Нажимать ЛКМ")
        # toggle2.setLayoutDirection(Qt.RightToLeft)
        self.toggle2.setStyleSheet("""
                    QCheckBox::indicator {
                        width: 17px;   /* Ширина чекбокса */
                        height: 17px;  /* Высота чекбокса */
                    }
                """)

        self.toggle2.setChecked(main_window.press2)
        self.toggle2.stateChanged.connect(self.state2)
        if main_window.press1 == 1:
            self.toggle2.setEnabled(True)
        else:
            self.state2(0)
            self.toggle2.setChecked(False)
            self.toggle2.setEnabled(False)

        # toggle2.setLayoutDirection(Qt.RightToLeft)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Горизонтальная линия
        line.setFrameShadow(QFrame.Sunken)  # Оттенок для линии
        line.setLineWidth(2)  # Толщина линии

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        line2.setLineWidth(2)
        # Текст для разделителя
        text_label = QLabel("Бинды клавиш")
        text_label.setAlignment(Qt.AlignCenter)
        # text_label.setStyleSheet(
        #     "background-color: white; padding: 0 10px;")  # Белый фон, чтобы текст был видим на фоне линии

        _line = QVBoxLayout()

        _line.addWidget(line)
        _line.addWidget(text_label)
        _line.addWidget(line2)
        _line.setSpacing(3)


        layout2.addWidget(self.toggle2)
        layout2.setAlignment(Qt.AlignLeft)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout2)
        main_layout.addLayout(_line)
        main_layout.addLayout(layout)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Запускаем отслеживание клавиш в фоновом потоке
        self._listen_for_keypress()

    def closeEvent(self, a0):
        if main_window.button1_state == "off":
            main_window.button3.setEnabled(True)
    def edit_key(self, ability, change_to="НЕТ"):
        self.keybindings[ability] = change_to
        config = configparser.ConfigParser()
        config.add_section("keybindings")
        config.add_section("settings")
        config["keybindings"] = self.keybindings
        config["settings"] = {"press1": str(int(main_window.press1)), "press2": str(int(main_window.press2))}

        with open("resourses/config.ini", "w") as f:
            config.write(f)
        self.abilities_lines[ability].setText(change_to)
    def change_key(self, ability, key_display):
        """
        Когда нажимается кнопка "Изменить", назначение клавиши сбрасывается
        и окно начинает слушать клавиши.
        """
        self.current_ability = ability
        self.keybindings[ability] = "Нажмите клавишу..."  # Временно ставим надпись
        key_display.setText(self.keybindings[ability])

        # Меняем заголовок окна, чтобы пользователи знали, что они должны нажать клавишу

    def _listen_for_keypress(self):
        """
        Слушаем нажатие клавиш с помощью библиотеки keyboard.
        """
        def on_key_event(e):
            key = e.name
            if self.current_ability is not None and key not in list(self.keybindings.values()):
                  # Получаем название нажатой клавиши
                self.keybindings[self.current_ability] = key
                self.abilities_lines[self.current_ability].setText(key)
                config = configparser.ConfigParser()
                config.add_section("keybindings")
                config.add_section("settings")
                config["settings"] = {"press1": str(int(main_window.press1)), "press2": str(int(main_window.press2))}
                config["keybindings"] = self.keybindings
                with open("resourses/config.ini", "w") as f:
                    config.write(f)
                self.current_ability = None  # Сбрасываем текущую способность

        # Слушаем все клавиши в фоновом режиме
        self.hook = keyboard.hook(on_key_event)
    def state1(self, state):
        main_window.press1 = int(bool(state))
        if main_window.press1 == 1:
            self.toggle2.setEnabled(True)
        else:
            self.state2(0)
            self.toggle2.setChecked(False)
            self.toggle2.setEnabled(False)

        config = configparser.ConfigParser()
        config.add_section("keybindings")
        config.add_section("settings")
        config["settings"] = {"press1": str(main_window.press1), "press2": str(main_window.press2)}
        config["keybindings"] = self.keybindings
        with open("resourses/config.ini", "w") as f:
            config.write(f)
    def state2(self, state):
        main_window.press2 = int(bool(state))
        config = configparser.ConfigParser()
        config.add_section("keybindings")
        config.add_section("settings")

        config["settings"] = {"press1": str(main_window.press1), "press2": str(main_window.press2)}
        config["keybindings"] = self.keybindings

        with open("resourses/config.ini", "w") as f:
            config.write(f)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
