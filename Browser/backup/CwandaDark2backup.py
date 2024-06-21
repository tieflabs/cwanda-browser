import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLineEdit, QToolBar, QAction, QHBoxLayout, QLabel, QPushButton, QWidget, QMenu
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QMouseEvent

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cwanda")
        self.setGeometry(100, 100, 1200, 800)

        # Remove the native window frame
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # Set the window icon
        self.setWindowIcon(QIcon('fiverr_icon.png'))

        self.browser_tabs = QTabWidget()
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.browser_tabs)

        self.add_new_tab(QUrl('https://www.cwanqa.com'), 'Homepage')

        self.create_navigation_bar()

        # Set initial theme to light mode
        self.is_dark_mode = False
        self.set_light_mode()

        # Create a custom title bar
        self.create_title_bar()

    def create_title_bar(self):
        self.title_bar = QWidget(self)
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setFixedHeight(30)
        self.title_bar.setAutoFillBackground(True)

        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel("Cwanda", self)
        self.title_bar_layout.addWidget(self.title_label)

        self.title_bar_layout.addStretch(1)

        self.minimize_button = QPushButton("-", self)
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.title_bar_layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton("+", self)
        self.maximize_button.setFixedSize(30, 30)
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.title_bar_layout.addWidget(self.maximize_button)

        self.close_button = QPushButton("x", self)
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.close_button)

        self.title_bar.setLayout(self.title_bar_layout)

        # Set the custom title bar
        self.set_menu_bar(self.title_bar)

    def create_navigation_bar(self):
        self.nav_bar = QToolBar("Navigation")
        self.addToolBar(self.nav_bar)

        # Create actions with icons for the navigation buttons
        back_btn = QAction(QIcon('back_icon.png'), "", self)
        back_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().back())
        self.nav_bar.addAction(back_btn)

        forward_btn = QAction(QIcon('forward_icon.png'), "", self)
        forward_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().forward())
        self.nav_bar.addAction(forward_btn)

        reload_btn = QAction(QIcon('reload_icon.png'), "", self)
        reload_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().reload())
        self.nav_bar.addAction(reload_btn)

        home_btn = QAction(QIcon('home_icon.png'), "", self)
        home_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().setUrl(QUrl("https://www.cwanqa.com")))
        self.nav_bar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        new_tab_btn = QAction(QIcon('new_tab_icon.png'), "", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl('https://www.cwanqa.com'), 'New Tab'))
        self.nav_bar.addAction(new_tab_btn)

        # Add settings menu button
        settings_btn = QAction(QIcon('settings_icon.png'), "", self)
        self.settings_menu = QMenu(self)
        
        # Toggle Mode submenu
        toggle_mode_menu = QMenu("Toggle Mode", self)
        toggle_mode_menu.addAction("Sky Blue", lambda: self.set_custom_color_mode("#87CEEB"))
        toggle_mode_menu.addAction("Black", lambda: self.set_custom_color_mode("#000000"))
        toggle_mode_menu.addAction("Lavender", lambda: self.set_custom_color_mode("#E6E6FA"))
        toggle_mode_menu.addAction("Blue", lambda: self.set_custom_color_mode("#0000FF"))
        toggle_mode_menu.addAction("Dark Blue", lambda: self.set_custom_color_mode("#00008B"))
        toggle_mode_menu.addAction("Custom Color", lambda: self.set_custom_color_mode("#252635"))
        
        self.settings_menu.addMenu(toggle_mode_menu)
        self.settings_menu.addAction("History", self.show_history)
        self.settings_menu.addAction("Bookmarks", self.show_bookmarks)
        self.settings_menu.addAction("Incognito", self.start_incognito_mode)
        self.settings_menu.addAction("Help", self.show_help)

        settings_btn.setMenu(self.settings_menu)
        self.nav_bar.addAction(settings_btn)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl("nav_bar")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.urlChanged.connect(self.update_url)

        i = self.browser_tabs.addTab(browser, label)
        self.browser_tabs.setCurrentIndex(i)

    def close_tab(self, i):
        if self.browser_tabs.count() < 2:
            return
        self.browser_tabs.removeTab(i)

    def navigate_to_url(self):
        url = self.url_bar.text()
        q = QUrl(url)
        if q.scheme() == "":
            q.setScheme("https")
        self.browser_tabs.currentWidget().setUrl(q)

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def set_custom_color_mode(self, color):
        custom_style = f"""
        QMainWindow {{
            background-color: {color};
            color: #ffffff;
        }}
        QToolBar {{
            background-color: {color};
            border: none;
        }}
        QLineEdit {{
            background-color: #555555;
            color: #ffffff;
            border: 1px solid #444444;
        }}
        QTabWidget::pane {{
            border: 1px solid #444444;
        }}
        QTabBar::tab {{
            background: #3c3c3c;
            color: #ffffff;
        }}
        QTabBar::tab:selected {{
            background: #555555;
        }}
        QAction {{
            color: #ffffff;
        }}
        QWidget#title_bar {{
            background-color: {color};
        }}
        QLabel {{
            color: #ffffff;
        }}
        QPushButton {{
            background-color: {color};
            color: #ffffff;
            border: none;
        }}
        QPushButton:hover {{
            background-color: #555555;
        }}
        """
        self.setStyleSheet(custom_style)

    def set_dark_mode(self):
        self.set_custom_color_mode("#2e2e2e")

    def set_light_mode(self):
        light_style = """
        QMainWindow {
            background-color: #ffffff;
            color: #000000;
        }
        QToolBar {
            background-color: #f0f0f0;
            border: none;
        }
        QLineEdit {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #cccccc;
        }
        QTabWidget::pane {
            border: 1px solid #cccccc;
        }
        QTabBar::tab {
            background: #f0f0f0;
            color: #000000;
        }
        QTabBar::tab:selected {
            background: #ffffff;
        }
        QAction {
            color: #000000;
        }
        QWidget#title_bar {
            background-color: #f0f0f0;
        }
        QLabel {
            color: #000000;
        }
        QPushButton {
            background-color: #f0f0f0;
            color: #000000;
            border: none;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        """
        self.setStyleSheet(light_style)

    def show_history(self):
        print("History clicked")

    def show_bookmarks(self):
        print("Bookmarks clicked")

    def start_incognito_mode(self):
        print("Incognito mode clicked")

    def show_help(self):
        print("Help clicked")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def set_menu_bar(self, title_bar):
        self.setMenuWidget(title_bar)

app = QApplication(sys.argv)
QApplication.setApplicationName("Cwanqa")
window = Browser()
window.show()
sys.exit(app.exec_())
