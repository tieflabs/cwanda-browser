import sys
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLineEdit, QToolBar, QAction, QHBoxLayout, QLabel, QPushButton, QWidget, QMenu, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QMouseEvent, QPixmap, QKeySequence


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cwanda")
        self.setGeometry(100, 90, 1200, 700)

        # Remove the native window frame
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # Set the window icon
        self.setWindowIcon(QIcon('fiverr_icon.png'))

        self.browser_tabs = QTabWidget()
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.browser_tabs)

        self.add_new_tab(QUrl('http://localhost:3000/cwanda.html'), 'New Tab')

        # Shortcut key to open a new tab
        QShortcut(QKeySequence('Ctrl+T'), self, lambda: self.add_new_tab(QUrl('http://localhost:3000/cwanda.html'), 'New Tab'))

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
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)  # Ensure no margins

        self.window_icon_label = QLabel(self)
        self.window_icon_label.setPixmap(QPixmap('fiverr_icon.png').scaled(30, 30))

        self.title_bar_layout.addWidget(self.window_icon_label)

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

        # Shortcut for closing window / all browser
        QShortcut(QKeySequence('Ctrl+W'), self).activated.connect(self.close)

        self.title_bar_layout.addWidget(self.close_button)

        self.title_bar.setLayout(self.title_bar_layout)

        # Add the title bar as a widget above the navigation bar
        self.nav_and_title_layout = QVBoxLayout()
        self.nav_and_title_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_and_title_layout.setSpacing(0)
        self.nav_and_title_layout.addWidget(self.title_bar)
        self.nav_and_title_layout.addWidget(self.browser_tabs)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.nav_and_title_layout)
        self.setCentralWidget(self.central_widget)

    def create_navigation_bar(self):
        self.nav_bar = QToolBar("Navigation")
        self.addToolBar(Qt.TopToolBarArea, self.nav_bar)
        self.nav_bar.setFixedHeight(30)

        # Remove any margins
        self.nav_bar.setContentsMargins(0, 0, 0, 0)

        # Create actions with icons for the navigation buttons
        back_btn = QAction(QIcon('back_icon.png'), "Back", self)
        back_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().back())
        self.nav_bar.addAction(back_btn)

        # Shortcut for back
        QShortcut(QKeySequence('Ctrl+left'), self, lambda: self.browser_tabs.currentWidget().back())

        forward_btn = QAction(QIcon('forward_icon.png'), "Forward", self)
        forward_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().forward())
        self.nav_bar.addAction(forward_btn)

        reload_btn = QAction(QIcon('reload_icon.png'), "Reload", self)
        reload_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().reload())
        self.nav_bar.addAction(reload_btn)

        home_btn = QAction(QIcon('home_icon.png'), "Home", self)
        home_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().setUrl(QUrl("http://localhost:3000/cwanda.html")))
        self.nav_bar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        new_tab_btn = QAction(QIcon('new_tab_icon.png'), "New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl('http://localhost:3000/cwanda.html'), 'New Tab'))
        self.nav_bar.addAction(new_tab_btn)

        # Add settings menu button
        settings_btn = QAction(QIcon('settings_icon.png'), "Settings", self)
        self.settings_menu = QMenu(self)

        # Toggle Mode submenu
        toggle_mode_menu = QMenu("Mode", self)
        toggle_mode_menu.addAction("White", lambda: self.set_custom_color_mode("#fff"))
        toggle_mode_menu.addAction("Lavender", lambda: self.set_custom_color_mode("#E6E6FA"))
        toggle_mode_menu.addAction("Normal", lambda: self.set_custom_color_mode("#3c3c3c"))
        toggle_mode_menu.addAction("Custom Color", lambda: self.set_custom_color_mode("#252635"))
        toggle_mode_menu.addAction("Dark", lambda: self.set_custom_color_mode("#333"))

        self.settings_menu.addMenu(toggle_mode_menu)
        self.settings_menu.addAction("History", self.show_history)
        self.settings_menu.addAction("Bookmarks", self.show_bookmarks)
        self.settings_menu.addAction("Incognito", self.start_incognito_mode)
        self.settings_menu.addAction("Help", self.show_help)

        settings_btn.setMenu(self.settings_menu)
        self.nav_bar.addAction(settings_btn)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl("")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.urlChanged.connect(self.update_url)
        browser.titleChanged.connect(lambda title: self.update_tab_title(browser, title))
        browser.iconChanged.connect(lambda icon: self.update_tab_icon(browser, icon))

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
            background-color: #f0f0f0;
            color: #000000;
        }
        QToolBar {
            background-color: #e0e0e0;
            border: none;
        }
        QLineEdit {
            color: #000000;
            border: 1px solid #cccccc;  
        }
        QTabWidget::pane {
            background: red;
            border: 1px solid #cccccc;
        }
        QTabBar::tab {
            background: #f0f0f0;
            color: #000000;
        }
        QTabBar::tab:selected {
            background: #d0d0d0;
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

    def show_help(self):
        pass

    def show_history(self):
        pass

    def show_bookmarks(self):
        pass

    def start_incognito_mode(self):
        pass

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if hasattr(self, 'drag_pos'):
            diff = event.globalPos() - self.drag_pos
            new_pos = self.pos() + diff
            self.move(new_pos)
            self.drag_pos = event.globalPos()
        super().mouseMoveEvent(event)

    def update_tab_title(self, browser, title):
        index = self.browser_tabs.indexOf(browser)
        if index != - -1:
            self.browser_tabs.setTabText(index, title)

    def update_tab_icon(self, browser, icon):
        index = self.browser_tabs.indexOf(browser)
        if index != -1:
            self.browser_tabs.setTabIcon(index, icon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Browser()
    window.show()
    sys.exit(app.exec_())
