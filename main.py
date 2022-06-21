from PyQt5 import QtWidgets, QtCore, QtGui
import webbrowser
import cryptocode
import threading
import pyautogui
import random
import socket
import time
import sys

title_font = QtGui.QFont()
title_font.setFamily('Segoe UI')
title_font.setPixelSize(25)

hint_buttons_font = QtGui.QFont()
hint_buttons_font.setFamily('Segoe UI')
hint_buttons_font.setPixelSize(17)

fields_font = QtGui.QFont()
fields_font.setFamily('Segoe UI')
fields_font.setPixelSize(15)

ground_buttons = QtGui.QFont()
ground_buttons.setFamily('Segoe UI')
ground_buttons.setPixelSize(12)

login_shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
login_shadow_effect.setBlurRadius(9)
login_shadow_effect.setColor(QtGui.QColor(225, 225, 225, 255))
login_shadow_effect.setXOffset(0)
login_shadow_effect.setYOffset(6)

password_shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
password_shadow_effect.setColor(QtGui.QColor(225, 225, 225, 255))
password_shadow_effect.setBlurRadius(9)
password_shadow_effect.setXOffset(0)
password_shadow_effect.setYOffset(6)

translate = QtCore.QCoreApplication.translate


class MainWindow(QtWidgets.QWidget):

    # Buttions functions
    def instruction(self: object) -> None:
        if not self.messagebox_frame.graphicsEffect().opacity() and not self.notification_frame.graphicsEffect().opacity() and not self.loading_frame.graphicsEffect().opacity():
            self.messagebox_frame_label.setText(translate('', 'Для получения вашего Discord-ID введите ">>id" боту.\nДля получения проверочного ключа введите ">>key" боту.\nДля успешной отправки сообщений боту вы должны:\n1. Разрешить отправшу сообщений членам сервера в дискорде.\n2. Находиться на дискоре сервере "Буст Контора".\nDiscord логин бота: Reflect Solutions bot#7166'))
            self.infobox_frame.show()
            self.frames_group = QtCore.QParallelAnimationGroup()
            self.frames_group.addAnimation(self.fade(self.auth_frame, 300, 0.9995, 0.6000))
            self.frames_group.addAnimation(self.fade(self.picture_frame, 300, 0.9995, 0.6000))
            self.frames_group.start()

            self.unfade(self.messagebox_frame, 300, 0.0, 0.9995).start()

    def warn(self: object, warn_text: str) -> None:
        pass

    def close_infobox(self: object) -> None:
        if (self.messagebox_frame.graphicsEffect().opacity() >= 0.9995 or self.notification_frame.graphicsEffect().opacity() >= 0.9995) and not self.loading_frame.graphicsEffect().opacity():
            self.frames_group = QtCore.QParallelAnimationGroup()
            self.frames_group.addAnimation(self.unfade(self.auth_frame, 300, 0.6000, 0.9995))
            self.frames_group.addAnimation(self.unfade(self.picture_frame, 300, 0.6000, 0.9995))
            self.frames_group.start()

            self.fade(self.messagebox_frame, 300, 0.9995, 0.0).start()
            self.infobox_frame.hide()

    def open_discord(self: object) -> None:
        webbrowser.open('https://discord.gg/hYrsuZDch3')

    # Window movement
    def mousePressEvent(self: object, evt: object) -> None:
        self.first_pos = (evt.globalPos().x(), evt.globalPos().y())

    def mouseMoveEvent(self: object, evt: object):
        try:
            delta = (evt.globalPos().x() - self.first_pos[0], evt.globalPos().y() - self.first_pos[1])
            self.move_frame.move(self.move_frame.x() + delta[0], self.move_frame.y() + delta[1])
            self.first_pos = (evt.globalPos().x(), evt.globalPos().y())
        except Exception:
            pass

    # Singleshot functions
    def application_is_running(self):
        while True:
            if not self.isVisible():
                client.send(b'stop')
                break
            time.sleep(0.01)

    # Animations
    def fade(self: object, widget: object, duration: int, start_value: float, stop_value: float) -> object:
        self.fade_effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QtCore.QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(duration)
        self.fade_animation.setStartValue(start_value)
        self.fade_animation.setEndValue(stop_value)
        return self.fade_animation

    def unfade(self: object, widget: object, duration: int, start_value: float, stop_value: float) -> object:
        self.unfade_effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.unfade_effect)
        self.unfade_animation = QtCore.QPropertyAnimation(self.unfade_effect, b"opacity")
        self.unfade_animation.setDuration(duration)
        self.unfade_animation.setStartValue(start_value)
        self.unfade_animation.setEndValue(stop_value)
        return self.unfade_animation

    def __init__(self: object) -> None:
        super().__init__()

        window_title = ''
        for _ in range(4, 16):
            window_title += random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789')
        self.setWindowTitle(window_title)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setGeometry((pyautogui.size()[0] // 2) - 400, (pyautogui.size()[1] // 2) - 300, 800, 600)
        self.setStyleSheet('QWidget{\nbackground-color: black;}')

        self.move_frame = self

        self.auth_frame = QtWidgets.QFrame(self)
        self.auth_frame.setGeometry(0, 0, 350, 600)
        self.auth_frame.setStyleSheet('QFrame{\nbackground-color: white;}')

        self.name_title = QtWidgets.QLabel(self.auth_frame)
        self.name_title.setGeometry(0, 175, self.auth_frame.width(), 55)
        self.name_title.setStyleSheet('QLabel{\ncolor: rgb(0, 0, 128);}')
        self.name_title.setText(translate('', 'Reflect Solutions'))
        self.name_title.setFont(title_font)
        self.name_title.setAlignment(QtCore.Qt.AlignCenter)

        self.login_lineedit = QtWidgets.QLineEdit(self.auth_frame)
        self.login_lineedit.setGeometry(50, 250, 250, 35)
        self.login_lineedit.setGraphicsEffect(login_shadow_effect)
        self.login_lineedit.setStyleSheet('QLineEdit{\nbackground-color: none; border-radius: 8px; border: none;}')
        self.login_lineedit.setFont(fields_font)
        self.login_lineedit.setPlaceholderText("Discord-ID")

        self.password_lineedit = QtWidgets.QLineEdit(self.auth_frame)
        self.password_lineedit.setGeometry(50, 295, 250, 35)
        self.password_lineedit.setGraphicsEffect(password_shadow_effect)
        self.password_lineedit.setStyleSheet('QLineEdit{\nbackground-color: none; border-radius: 8px; border: none;}')
        self.password_lineedit.setFont(fields_font)
        self.password_lineedit.setPlaceholderText("Discord ключ")
        self.password_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.auth_button = QtWidgets.QPushButton(self.auth_frame)
        self.auth_button.setGeometry(50, 370, 250, 35)
        self.auth_button.setStyleSheet('QPushButton{\nbackground-color: rgb(0, 0, 128); color: white; border-radius: 8px; border: none;}QPushButton::hover{background-color: rgb(0, 0, 205);}')
        self.auth_button.setFont(fields_font)
        self.auth_button.setText(translate('', 'Вход'))
        self.auth_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.instruction_button = QtWidgets.QPushButton(self.auth_frame)
        self.instruction_button.setGeometry(140, 420, 70, 20)
        self.instruction_button.setStyleSheet('QPushButton{\nbackground-color: none; color: rgb(150, 150, 150);  border: none;}QPushButton::hover{color: rgb(0, 0, 205);}')
        self.instruction_button.setFont(ground_buttons)
        self.instruction_button.setText(translate('', 'Инструкция'))
        self.instruction_button.clicked.connect(self.instruction)
        self.instruction_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.forget_password_button = QtWidgets.QPushButton(self.auth_frame)
        self.forget_password_button.setGeometry(135, 450, 80, 20)
        self.forget_password_button.setStyleSheet('QPushButton{\nbackground-color: none; color: rgb(150, 150, 150);  border: none;}QPushButton::hover{color: rgb(0, 0, 205);}')
        self.forget_password_button.setFont(ground_buttons)
        self.forget_password_button.setText(translate('', 'Discord сервер'))
        self.forget_password_button.clicked.connect(self.open_discord)
        self.forget_password_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.picture_frame = QtWidgets.QFrame(self)
        self.picture_frame.setGeometry(350, 0, 450, 600)
        self.picture_frame.setStyleSheet('QFrame{\nbackground-color: none; background-image: url(rs_images/background_image.png);}')
        self.picture_frame.mousePressEvent = self.mousePressEvent
        self.picture_frame.mouseMoveEvent = self.mouseMoveEvent

        self.close_button = QtWidgets.QPushButton(self.picture_frame)
        self.close_button.setGeometry(self.picture_frame.width() - 40, 10, 30, 30)
        self.close_button.setStyleSheet('QPushButton{\nbackground-color: none; color: white; border-radius: 10px;}')
        self.close_button.setText(translate('', 'X'))
        self.close_button.setFont(hint_buttons_font)
        self.close_button.clicked.connect(lambda: self.close())
        self.close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.minimize_button = QtWidgets.QPushButton(self.picture_frame)
        self.minimize_button.setGeometry(self.picture_frame.width() - 75, 10, 30, 30)
        self.minimize_button.setStyleSheet('QPushButton{\nbackground-color: none; color: white; border-radius: 10px;}')
        self.minimize_button.setText(translate('', '—'))
        self.minimize_button.setFont(hint_buttons_font)
        self.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.minimize_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # infoboxes
        self.infobox_frame = QtWidgets.QPushButton(self)
        self.infobox_frame.setStyleSheet('QPushButton{\nbackground-color: none; border: none;}')
        self.infobox_frame.setGeometry(0, 0, self.width(), self.height())
        self.infobox_frame.clicked.connect(self.close_infobox)

        # ====================
        self.messagebox_frame = QtWidgets.QFrame(self.infobox_frame)
        self.messagebox_frame.setGeometry(self.width() // 2 - 250, self.height() // 2 - 100, 500, 200)
        self.messagebox_frame.setStyleSheet('QFrame{\nbackground-color: white;}')

        self.messagebox_frame_label = QtWidgets.QLabel(self.messagebox_frame)
        self.messagebox_frame_label.setGeometry(20, 20, self.messagebox_frame.width() - 40, self.messagebox_frame.height() - 40)
        self.messagebox_frame_label.setStyleSheet('QLabel{\nbackground-color: none; color: rgb(150, 150, 150);}')
        self.messagebox_frame_label.setText(translate('', ''))
        self.messagebox_frame_label.setFont(fields_font)
        self.messagebox_frame_label.setAlignment(QtCore.Qt.AlignCenter)

        self.fade(self.messagebox_frame, 0, 0.0, 0.0).start()

        # ====================
        self.notification_frame = QtWidgets.QFrame(self.infobox_frame)
        self.notification_frame.setGeometry(self.width() // 2 - 250, self.height() // 2 - 100, 500, 200)
        self.notification_frame.setStyleSheet('QFrame{\nbackground-color: white;}')

        self.notification_message_label = QtWidgets.QLabel(self.notification_frame)
        self.notification_message_label.setGeometry(190, 20, self.notification_frame.width() - 210, self.notification_frame.height() - 40)
        self.notification_message_label.setStyleSheet('QLabel{\nbackground-color: none; color: rgb(150, 150, 150);}')
        self.notification_message_label.setText(translate('', ''))
        self.notification_message_label.setAlignment(QtCore.Qt.AlignCenter)

        self.notification_message_frame_picture = QtWidgets.QFrame(self.notification_frame)
        self.notification_message_frame_picture.setGeometry(20, 20, self.notification_frame.width() - 350, self.notification_frame.height() - 40)
        self.notification_message_frame_picture.setStyleSheet('QFrame{\nbackground-color: none; background-image: url(rs_images/warning.png);}')

        self.fade(self.notification_frame, 0, 0.0, 0.0).start()

        # ====================
        self.loading_gif = QtGui.QMovie('rs_gifs\\spinner.gif')
        self.loading_gif.start()

        self.loading_frame = QtWidgets.QFrame(self.infobox_frame)
        self.loading_frame.setGeometry(self.width() // 2 - 250, self.height() // 2 - 100, 500, 200)
        self.loading_frame.setStyleSheet('QFrame{\nbackground-color: white;}')

        self.loading_frame_label = QtWidgets.QLabel(self.loading_frame)
        self.loading_frame_label.setGeometry(190, 20, self.loading_frame.width() - 210, self.loading_frame.height() - 40)
        self.loading_frame_label.setStyleSheet('QLabel{\nbackground-color: none; color: rgb(150, 150, 150);}')
        self.loading_frame_label.setText(translate('', ''))
        self.loading_frame_label.setAlignment(QtCore.Qt.AlignCenter)

        self.loading_frame_gif = QtWidgets.QLabel(self.loading_frame)
        self.loading_frame_gif.setGeometry(20, 20, self.loading_frame.width() - 350, self.loading_frame.height() - 40)
        self.loading_frame_gif.setStyleSheet('QFrame{\nbackground-color: none;}')
        self.loading_frame_gif.setMovie(self.loading_gif)

        self.fade(self.loading_frame, 0, 0.0, 0.0).start()

        self.infobox_frame.hide()

        # Timer
        QtCore.QTimer.singleShot(0, lambda: threading.Thread(target=self.application_is_running).start())


def start_server() -> None:
    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('178.250.158.150', 4075))

    while True:
        server_data = client.recv(1024).decode('utf-8')
        if server_data:

            if server_data == 'stop':
                print('Socket client stoped...')
                break

        time.sleep(0.01)


application = QtWidgets.QApplication(sys.argv)
window = MainWindow()
threading.Thread(target=start_server).start()
window.show()
application.exec()
