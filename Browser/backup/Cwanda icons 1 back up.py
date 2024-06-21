import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon  # Import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cwanda")
        self.setGeometry(100, 100, 1200, 800)

        # Set the window icon
        self.setWindowIcon(QIcon('fiverr_icon.png'))  # Add this line

        self.browser_tabs = QTabWidget()
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.browser_tabs)

        self.add_new_tab(QUrl('https://www.cwanqa.com'), 'Homepage')

        self.create_navigation_bar()

    def create_navigation_bar(self):
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        # Create actions with icons for the navigation buttons
        back_btn = QAction(QIcon('back_icon.png'), "", self)
        back_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().back())
        nav_bar.addAction(back_btn)

        forward_btn = QAction(QIcon('forward_icon.png'), "", self)
        forward_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().forward())
        nav_bar.addAction(forward_btn)

        reload_btn = QAction(QIcon('reload_icon.png'), "", self)
        reload_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().reload())
        nav_bar.addAction(reload_btn)

        home_btn = QAction(QIcon('home_icon.png'), "", self)
        home_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().setUrl(QUrl("https://www.cwanqa.com")))
        nav_bar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        new_tab_btn = QAction(QIcon('new_tab_icon.png'), "", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl('https://www.cwanqa.com'), 'New Tab'))
        nav_bar.addAction(new_tab_btn)

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

app = QApplication(sys.argv)
QApplication.setApplicationName("Cwanqa")
window = Browser()
window.show()
sys.exit(app.exec_())
