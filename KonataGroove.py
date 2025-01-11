import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QMessageBox, QGraphicsOpacityEffect

class KonataGroove(QMainWindow):
    def __init__(self, dance_gif_path, shadow_gif_path, icon_path):
        super().__init__()

        # Set the icon for the window
        self.setWindowIcon(QIcon(icon_path))

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.movie = QMovie(dance_gif_path)
        self.label.setMovie(self.movie)
        self.movie.start()
        gif_size = self.movie.frameRect().size()
        self.setFixedSize(gif_size)
        self.label.setFixedSize(gif_size)
        self._drag_pos = None

        self.shadow_effect = None
        self.shadow_enabled = False
        self.transparency_enabled = False
        self.dance_gif_path = dance_gif_path
        self.shadow_gif_path = shadow_gif_path
        self.window_mode = 'Always on Top'  # Default window mode

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        close_action = context_menu.addAction("Close")
        shadow_action = context_menu.addAction("Toggle Shadow")
        transparency_action = context_menu.addAction("Toggle Transparency")
        top_action = context_menu.addAction("Always on Top")
        below_action = context_menu.addAction("Always Below")
        standard_action = context_menu.addAction("Standard")
        about_action = context_menu.addAction("About")

        action = context_menu.exec_(pos)
        if action == close_action:
            self.close_program()
        elif action == shadow_action:
            self.toggle_shadow()
        elif action == transparency_action:
            self.toggle_transparency()
        elif action == top_action:
            self.set_window_mode('Always on Top')
        elif action == below_action:
            self.set_window_mode('Always Below')
        elif action == standard_action:
            self.set_window_mode('Standard')
        elif action == about_action:
            self.show_about()

    def toggle_shadow(self):
        if self.shadow_enabled:
            self.label.setGraphicsEffect(None)
            self.label.setMovie(QMovie(self.dance_gif_path))
            self.shadow_enabled = False
        else:
            self.label.setMovie(QMovie(self.shadow_gif_path))
            self.shadow_enabled = True
        self.label.movie().start()
        gif_size = self.label.movie().frameRect().size()
        self.setFixedSize(gif_size)
        self.label.setFixedSize(gif_size)

    def toggle_transparency(self):
        if self.transparency_enabled:
            self.label.setGraphicsEffect(None)
            self.transparency_enabled = False
        else:
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.80)  # TRANSPARENCY HERE!!
            self.label.setGraphicsEffect(opacity_effect)
            self.transparency_enabled = True

    def set_window_mode(self, mode):
        self.window_mode = mode
        if mode == 'Always on Top':
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        elif mode == 'Always Below':
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
            self.lower()
        elif mode == 'Standard':
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.show()  # Necessary to reapply the window flags

    def close_program(self):
        self.close()
        os._exit(0)

    def show_about(self):
        QMessageBox.about(self, "About KonataGroove", "KonataGroove Application\nVersion 1.0\nDeveloped by Nixietab")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_path = "Konata.ico"
    app.setWindowIcon(QIcon(icon_path))  # Set the application icon
    dance_gif_path = "konata-dance.gif" # this too, its awfull
    shadow_gif_path = "konata-dance.gif" # Replace this please
    window = KonataGroove(dance_gif_path, shadow_gif_path, icon_path)
    window.show()
    sys.exit(app.exec_())