"""
A simple DXAFS data converter obtained at BL28B2, SPring-8.

H. Asakura (h.asakura@nusr.nagoya-u.ac.jp)
License: BSD lisence
Any comments or suggestions are welcome!
"""

__author__  = "Hiroyuki Asakura <h.asakura@nusr.nagoya-u.ac.jp>"
__license__ = "BSD license - see LICENSE file"

# Standard library
import sys, os.path

# Additional library
import numpy

# PyQt4 libaray
import PyQt4.QtCore
import PyQt4.QtGui

# Original libarary
from lib.his2spectrum import *

class ButtonBoxWidget(PyQt4.QtGui.QWidget):
    def __init__(self, parent=None):
        PyQt4.QtGui.QWidget.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.start_button = PyQt4.QtGui.QPushButton("Start", parent=self)
        self.stop_button = PyQt4.QtGui.QPushButton("Stop (does not work)", parent=self)
        self.quit_button = PyQt4.QtGui.QPushButton("Quit", parent=self)

        layout = PyQt4.QtGui.QHBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

class FileDialogBoxWidget(PyQt4.QtGui.QWidget):
    finished = PyQt4.QtCore.pyqtSignal()
    processing = PyQt4.QtCore.pyqtSignal()
    missing = PyQt4.QtCore.pyqtSignal()

    def __init__(self, parent=None):
        PyQt4.QtGui.QWidget.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.data_file_label = PyQt4.QtGui.QLabel("Data File")
        self.data_file_box = PyQt4.QtGui.QLineEdit(parent=self)
        self.data_file_button = PyQt4.QtGui.QToolButton(parent=self)
        self.dark_for_data_file_label = PyQt4.QtGui.QLabel("Dark for Data")
        self.dark_for_data_file_box = PyQt4.QtGui.QLineEdit(parent=self)
        self.dark_for_data_file_button = PyQt4.QtGui.QToolButton(parent=self)
        self.blank_file_label = PyQt4.QtGui.QLabel("Blank File")
        self.blank_file_box = PyQt4.QtGui.QLineEdit(parent=self)
        self.blank_file_button = PyQt4.QtGui.QToolButton(parent=self)
        self.dark_for_blank_file_label = PyQt4.QtGui.QLabel("Dark fo Blank")
        self.dark_for_blank_file_box = PyQt4.QtGui.QLineEdit(parent=self)
        self.dark_for_blank_file_button = PyQt4.QtGui.QToolButton(parent=self)
        self.calibration_file_label = PyQt4.QtGui.QLabel("Calibration File")
        self.calibration_file_box = PyQt4.QtGui.QLineEdit(parent=self)
        self.calibration_file_button = PyQt4.QtGui.QToolButton(parent=self)

        self.current_directory = '.'

        self.data_file = ""
        self.dark_for_data_file = ""
        self.blank_file = ""
        self.dark_for_blank_file = ""
        self.calibration_file = ""

        layout = PyQt4.QtGui.QGridLayout()
        layout.addWidget(self.data_file_label, 0, 0)
        layout.addWidget(self.data_file_box, 0, 1)
        layout.addWidget(self.data_file_button, 0, 2)
        layout.addWidget(self.dark_for_data_file_label, 1, 0)
        layout.addWidget(self.dark_for_data_file_box, 1, 1)
        layout.addWidget(self.dark_for_data_file_button, 1, 2)
        layout.addWidget(self.blank_file_label, 2, 0)
        layout.addWidget(self.blank_file_box, 2, 1)
        layout.addWidget(self.blank_file_button, 2, 2)
        layout.addWidget(self.dark_for_blank_file_label, 3, 0)
        layout.addWidget(self.dark_for_blank_file_box, 3, 1)
        layout.addWidget(self.dark_for_blank_file_button, 3, 2)
        layout.addWidget(self.calibration_file_label, 4, 0)
        layout.addWidget(self.calibration_file_box, 4, 1)
        layout.addWidget(self.calibration_file_button, 4, 2)

        self.setLayout(layout)

    def open_data_file(self):
        filename = PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Select data file(s)', self.current_directory)
        self.data_file_box.setText(filename)
        self.current_directory = PyQt4.QtCore.QFileInfo(filename).dir().path()

    def open_dark_for_data_file(self):
        filename = PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Select dark file for data', self.current_directory)
        self.dark_for_data_file_box.setText(filename)
        self.current_directory = PyQt4.QtCore.QFileInfo(filename).dir().path()

    def open_blank_file(self):
        filename = PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Select blank file for data', self.current_directory)
        self.blank_file_box.setText(filename)
        self.current_directory = PyQt4.QtCore.QFileInfo(filename).dir().path()

    def open_dark_for_blank_file(self):
        filename = PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Select dark file for blank', self.current_directory)
        self.dark_for_blank_file_box.setText(filename)
        self.current_directory = PyQt4.QtCore.QFileInfo(filename).dir().path()

    def open_calibration_file(self):
        filename = PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Select calibraiton file (.ex3)', self.current_directory)
        self.calibration_file_box.setText(filename)
        self.current_directory = PyQt4.QtCore.QFileInfo(filename).dir().path()

    def kick(self):
        self.data_file = self.data_file_box.text()
        self.dark_for_data_file = self.blank_file_box.text()
        self.blank_file = self.blank_file_box.text()
        self.dark_for_blank_file = self.dark_for_blank_file_box.text()
        self.calibration_file = self.calibration_file_box.text()
        if self.data_file and self.dark_for_data_file and self.blank_file and self.dark_for_blank_file and self.calibration_file:
            self.processing.emit()
            convertHIStospectrum(str(self.data_file),
                                 str(self.dark_for_data_file),
                                 str(self.blank_file),
                                 str(self.dark_for_blank_file),
                                 str(self.calibration_file))
            self.finished.emit()
        else:
            self.missing.emit()

class MainWindow(PyQt4.QtGui.QMainWindow):
    quit = PyQt4.QtCore.pyqtSignal()

    def __init__(self, parent=None):
        PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        panel = PyQt4.QtGui.QWidget()
        button_box_widget = ButtonBoxWidget(parent=None)
        file_dialog_box_widget = FileDialogBoxWidget(parent=None)

        panel_layout = PyQt4.QtGui.QVBoxLayout()
        panel_layout.addWidget(file_dialog_box_widget)
        panel_layout.addWidget(button_box_widget)
        panel.setLayout(panel_layout)
        panel.setFixedSize(640, 400)

        self.help_menu = self.menuBar().addMenu("&Help")
        self.about_action = PyQt4.QtGui.QAction("&About", self)
        self.about_action.setShortcut("F1")
        self.help_menu.addAction(self.about_action)


        self.statusBar().showMessage("Ready!")
        self.setWindowTitle("DXAFS Data Converter")
        self.setCentralWidget(panel)

        # connect
        file_dialog_box_widget.data_file_button.clicked.connect(file_dialog_box_widget.open_data_file)
        file_dialog_box_widget.dark_for_data_file_button.clicked.connect(file_dialog_box_widget.open_dark_for_data_file)
        file_dialog_box_widget.blank_file_button.clicked.connect(file_dialog_box_widget.open_blank_file)
        file_dialog_box_widget.dark_for_blank_file_button.clicked.connect(file_dialog_box_widget.open_dark_for_blank_file)
        file_dialog_box_widget.calibration_file_button.clicked.connect(file_dialog_box_widget.open_calibration_file)

        file_dialog_box_widget.finished.connect(lambda: self.statusBar().showMessage("Finished! and Ready again!"))
        file_dialog_box_widget.processing.connect(lambda: self.statusBar().showMessage("Processing! Please wait for a while."))
        file_dialog_box_widget.missing.connect(lambda: self.statusBar().showMessage("Missing data file! Please input correct data file paths."))

        button_box_widget.start_button.clicked.connect(file_dialog_box_widget.kick)
        #button_box_widget.stop_button.clicked.connect()
        button_box_widget.quit_button.clicked.connect(lambda: self.close())

        self.about_action.triggered.connect(self.show_about)

    def show_about(self):
        msg = __doc__
        PyQt4.QtGui.QMessageBox.about(self, "About the DXAFS Data Converter", msg.strip())

def main():
    app = PyQt4.QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.connect(app, PyQt4.QtCore.SIGNAL("lastWindowClosed()"), app, PyQt4.QtCore.SLOT("quit()"))
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
