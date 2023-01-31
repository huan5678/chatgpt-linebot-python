# hello.py
"""Simple Hello, World example with PyQt6."""
import sys
# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout, QLineEdit,  QDialog, QDialogButtonBox, QMainWindow, QStatusBar, QToolBar

# 2. Create an instance of QApplication
# app = QApplication([])
# window = QWidget()
# ...# 3. Create your application's GUIwindow = QWidget()
# window.setWindowTitle("PyQt App")
# window.setGeometry(0, 0, 320, 480)
# helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
# helloMsg.move(64, 16)

# horizontal_layout = QHBoxLayout()
# horizontal_layout.addWidget(QPushButton("Left"))
# horizontal_layout.addWidget(QPushButton("Center"))
# horizontal_layout.addWidget(QPushButton("Right"))
# window.setLayout(horizontal_layout)

# vertical_layout = QVBoxLayout()
# vertical_layout.addWidget(QPushButton("Top"))
# vertical_layout.addWidget(QPushButton("Middle"))
# vertical_layout.addWidget(QPushButton("Bottom"))
# window.setLayout(vertical_layout)

# grid_layout = QGridLayout()
# grid_layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
# grid_layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
# grid_layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
# grid_layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
# grid_layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
# grid_layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)
# grid_layout.addWidget(QPushButton("Button (2, 0)"), 2, 0)
# grid_layout.addWidget(
#     QPushButton("Button (2, 1) + 2 Columns Span"), 2, 1, 1, 2
# )
# window.setLayout(grid_layout)

# form_layout = QFormLayout()
# form_layout.addRow(helloMsg)
# form_layout.addRow("First Name:", QLabel("John"))
# form_layout.addRow("Last Name:", QLabel("Doe"))
# form_layout.addRow("Age:", QLineEdit())
# form_layout.addRow("Country:", QLineEdit())
# form_layout.addRow("City:", QLineEdit())
# window.setLayout(form_layout)




# 4. Show your application's GUI
# window.show()
# 5. Run your application's event loop
# sys.exit(app.exec())


# class Window(QDialog):
#   def __init__(self):
#     super().__init__(parent=None)
#     self.setWindowTitle("PyQt App")
#     dialogLayout = QVBoxLayout()
#     formLayout = QFormLayout()
#     formLayout.addRow("Name:", QLineEdit())
#     formLayout.addRow("Age:", QLineEdit())
#     formLayout.addRow("Job:", QLineEdit())
#     formLayout.addRow("Hobbies:", QLineEdit())
#     dialogLayout.addLayout(formLayout)
#     buttons = QDialogButtonBox()
#     buttons.setStandardButtons(
#         QDialogButtonBox.StandardButton.Cancel
#         | QDialogButtonBox.StandardButton.Ok
#     )
#     dialogLayout.addWidget(buttons)
#     self.setLayout(dialogLayout)

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        self.setCentralWidget(QLabel("I'm the Central Widget"))
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
