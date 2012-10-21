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

class ParametersBoxWidget(PyQt4.QtGui.QWidget):
    def __init__(self, parent=None):
        PyQt4.QtGui.QWidget.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.start_frame_number_label = PyQt4.QtGui.QLabel("Start Frame No.")
        self.start_frame_number_box = PyQt4.QtGui.QSpinBox(parent=self)
        self.start_frame_number_box.setRange(1, 4096)
        self.number_of_spectra_label = PyQt4.QtGui.QLabel("Spectra")
        self.number_of_spectra_box = PyQt4.QtGui.QSpinBox(parent=self)
        self.number_of_spectra_box.setRange(0, 4096)
        self.number_of_spectra_box.setValue(0)
        self.accumlation_frames_label = PyQt4.QtGui.QLabel("Accumlation Frames")
        self.accumlation_frames_box = PyQt4.QtGui.QSpinBox(parent=self)
        self.accumlation_frames_box.setRange(1, 32768)
        self.accumlation_frames_box.setValue(100)
        self.accumlation_axis_label = PyQt4.QtGui.QLabel("Vertical/Horizontal")
        self.accumlation_axis_box = PyQt4.QtGui.QComboBox()
        self.accumlation_axis_box.addItem("Vertical")
        self.accumlation_axis_box.addItem("Horizontal")
        self.activate_dark_label = PyQt4.QtGui.QLabel("Read Dark")
        self.activate_dark_button = PyQt4.QtGui.QPushButton("ON", parent=self)
        self.activate_dark_button.setCheckable(True)
        self.activate_dark_button.setChecked(True)
        self.repeat_blank_and_dark_label = PyQt4.QtGui.QLabel("Repeat Blank and Dark")
        self.repeat_blank_and_dark_button = PyQt4.QtGui.QPushButton("ON", parent=self)
        self.repeat_blank_and_dark_button.setCheckable(True)
        self.repeat_blank_and_dark_button.setChecked(True)

        layout = PyQt4.QtGui.QGridLayout()
        layout.addWidget(self.start_frame_number_label, 0, 0)
        layout.addWidget(self.start_frame_number_box, 0, 1)
        layout.addWidget(self.number_of_spectra_label, 0, 2)
        layout.addWidget(self.number_of_spectra_box, 0, 3)
        layout.addWidget(self.accumlation_frames_label, 0, 4)
        layout.addWidget(self.accumlation_frames_box, 0 ,5)
        layout.addWidget(self.accumlation_axis_label, 1, 0)
        layout.addWidget(self.accumlation_axis_box, 1, 1)
        layout.addWidget(self.activate_dark_label, 1, 2)
        layout.addWidget(self.activate_dark_button, 1, 3)
        layout.addWidget(self.repeat_blank_and_dark_label, 1, 4)
        layout.addWidget(self.repeat_blank_and_dark_button, 1, 5)

        self.setLayout(layout)

class FileDialogBoxWidget(PyQt4.QtGui.QWidget):
    finished = PyQt4.QtCore.pyqtSignal()
    processing = PyQt4.QtCore.pyqtSignal()
    missing = PyQt4.QtCore.pyqtSignal()

    def __init__(self, parent=None):
        PyQt4.QtGui.QWidget.__init__(self, parent=parent)
        self.parent = parent
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

class MainWindow(PyQt4.QtGui.QMainWindow):
    quit = PyQt4.QtCore.pyqtSignal()
    finished = PyQt4.QtCore.pyqtSignal()
    processing = PyQt4.QtCore.pyqtSignal()
    missing = PyQt4.QtCore.pyqtSignal()

    def __init__(self, parent=None):
        PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        panel = PyQt4.QtGui.QWidget()
        self.button_box_widget = ButtonBoxWidget(parent=None)
        self.parameters_box_widget = ParametersBoxWidget(parent=None)
        self.file_dialog_box_widget = FileDialogBoxWidget(parent=None)

        panel_layout = PyQt4.QtGui.QVBoxLayout()
        panel_layout.addWidget(self.file_dialog_box_widget)
        panel_layout.addWidget(self.parameters_box_widget)
        panel_layout.addWidget(self.button_box_widget)
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
        self.file_dialog_box_widget.data_file_button.clicked.connect(self.file_dialog_box_widget.open_data_file)
        self.file_dialog_box_widget.dark_for_data_file_button.clicked.connect(self.file_dialog_box_widget.open_dark_for_data_file)
        self.file_dialog_box_widget.blank_file_button.clicked.connect(self.file_dialog_box_widget.open_blank_file)
        self.file_dialog_box_widget.dark_for_blank_file_button.clicked.connect(self.file_dialog_box_widget.open_dark_for_blank_file)
        self.file_dialog_box_widget.calibration_file_button.clicked.connect(self.file_dialog_box_widget.open_calibration_file)

        self.finished.connect(lambda: self.statusBar().showMessage("Finished! and Ready again!"))
        self.processing.connect(lambda: self.statusBar().showMessage("Processing! Please wait for a while."))
        self.missing.connect(lambda: self.statusBar().showMessage("Missing data file! Please input correct data file paths."))

        self.button_box_widget.start_button.clicked.connect(self.kick)
        #self.button_box_widget.stop_button.clicked.connect()
        self.button_box_widget.quit_button.clicked.connect(lambda: self.close())

        self.about_action.triggered.connect(self.show_about)

    def kick(self):
        self.data_file =  self.file_dialog_box_widget.data_file_box.text()
        self.dark_for_data_file = self.file_dialog_box_widget.dark_for_data_file_box.text()
        self.blank_file = self.file_dialog_box_widget.blank_file_box.text()
        self.dark_for_blank_file = self.file_dialog_box_widget.dark_for_blank_file_box.text()
        self.calibration_file = self.file_dialog_box_widget.calibration_file_box.text()

        self.start_frame_number = self.parameters_box_widget.start_frame_number_box.value()
        self.number_of_spectra = self.parameters_box_widget.number_of_spectra_box.value()
        self.accumlation_frames = self.parameters_box_widget.accumlation_frames_box.value()
        self.accmulation_axis = self.parameters_box_widget.accumlation_axis_box.currentText()
        self.activate_dark = self.parameters_box_widget.activate_dark_button.isChecked()
        self.repeat_black_and_dark = self.parameters_box_widget.repeat_blank_and_dark_button.isChecked()

        if self.data_file and self.dark_for_data_file and self.blank_file and self.dark_for_blank_file and self.calibration_file:
            self.processing.emit()
            convertHIStospectrum(str(self.data_file),
                                 str(self.dark_for_data_file),
                                 str(self.blank_file),
                                 str(self.dark_for_blank_file),
                                 str(self.calibration_file),
                                 self.start_frame_number,
                                 self.number_of_spectra,
                                 self.accumlation_frames,
                                 self.accmulation_axis,
                                 self.activate_dark,
                                 self.repeat_black_and_dark)
            self.finished.emit()
        else:
            self.missing.emit()

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
