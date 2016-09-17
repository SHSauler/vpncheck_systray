from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QMessageBox, QMenu, QSystemTrayIcon)
from PyQt5.QtCore import QTimer
import psutil

class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.create_actions()
        self.create_tray_icon()
        self.set_icon()
        self.trayIcon.show()
        timer = QTimer(self)
        timer.timeout.connect(self.set_icon)
        timer.start(5000)

    def create_actions(self):
        self.quitAction = QAction("&Quit", self, triggered=QApplication.instance().quit)

    def create_tray_icon(self):
         self.trayIconMenu = QMenu(self)
         self.trayIconMenu.addAction(self.quitAction)

         self.trayIcon = QSystemTrayIcon(self)
         self.trayIcon.setContextMenu(self.trayIconMenu)

    def set_icon(self):

        net_interfaces = psutil.net_if_addrs().keys()
        result = any("tun" in interface for interface in net_interfaces)

        if result == True:
            icon = QIcon('./images/icon-green.png')
        else:
            icon = QIcon('./images/icon-red.png')
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray", "No Systray available. Quitting.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    sys.exit(app.exec_())
