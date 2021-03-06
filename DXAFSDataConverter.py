"""
A simple converter for DXAFS data obtained at BL28B2, SPring-8.

ASAKURA, Hiroyuki (asakura@moleng.kyoto-u.ac.jp)
License: BSD lisence

"""

__author__  = "ASAKURA, Hiroyuki <asakura@moleng.kyoto-u.ac.jp>"
__license__ = "BSD license - see LICENSE file"

# Standard library
import sys, os.path

# Additional library
import numpy

# PyQt4 libaray
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets

# Original libarary
from lib.his2spectrum import *

class ButtonBoxWidget(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        PyQt5.QtWidgets.QWidget.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.start_button = PyQt5.QtWidgets.QPushButton("Start", parent=self)
        self.stop_button = PyQt5.QtWidgets.QPushButton("Stop (does not work)", parent=self)
        self.quit_button = PyQt5.QtWidgets.QPushButton("Quit", parent=self)

        layout = PyQt5.QtWidgets.QHBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

class ParametersBoxWidget(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        PyQt5.QtWidgets.QWidget.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.start_frame_number_label = PyQt5.QtWidgets.QLabel("Start Frame No.")
        self.start_frame_number_box = PyQt5.QtWidgets.QSpinBox(parent=self)
        self.start_frame_number_box.setRange(1, 4096)
        self.number_of_spectra_label = PyQt5.QtWidgets.QLabel("Spectra")
        self.number_of_spectra_box = PyQt5.QtWidgets.QSpinBox(parent=self)
        self.number_of_spectra_box.setRange(0, 4096)
        self.number_of_spectra_box.setValue(0)
        self.accumlation_frames_label = PyQt5.QtWidgets.QLabel("Accumlation Frames")
        self.accumlation_frames_box = PyQt5.QtWidgets.QSpinBox(parent=self)
        self.accumlation_frames_box.setRange(1, 32768)
        self.accumlation_frames_box.setValue(100)
        self.accumlation_axis_label = PyQt5.QtWidgets.QLabel("Vertical/Horizontal")
        self.accumlation_axis_box = PyQt5.QtWidgets.QComboBox()
        self.accumlation_axis_box.addItem("Vertical")
        self.accumlation_axis_box.addItem("Horizontal")
        self.activate_dark_label = PyQt5.QtWidgets.QLabel("Read Dark")
        self.activate_dark_button = PyQt5.QtWidgets.QPushButton("ON", parent=self)
        self.activate_dark_button.setCheckable(True)
        self.activate_dark_button.setChecked(True)
        self.repeat_blank_and_dark_label = PyQt5.QtWidgets.QLabel("Repeat Blank and Dark")
        self.repeat_blank_and_dark_button = PyQt5.QtWidgets.QPushButton("ON", parent=self)
        self.repeat_blank_and_dark_button.setCheckable(True)
        self.repeat_blank_and_dark_button.setChecked(True)

        layout = PyQt5.QtWidgets.QGridLayout()
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

class FileDialogBoxWidget(PyQt5.QtWidgets.QWidget):
    finished = PyQt5.QtCore.pyqtSignal()
    processing = PyQt5.QtCore.pyqtSignal()
    missing = PyQt5.QtCore.pyqtSignal()

    def __init__(self, parent=None):
        PyQt5.QtWidgets.QWidget.__init__(self, parent=parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.data_file_label = PyQt5.QtWidgets.QLabel("Data File")
        self.data_file_box = PyQt5.QtWidgets.QLineEdit(parent=self)
        self.data_file_button = PyQt5.QtWidgets.QToolButton(parent=self)
        self.dark_for_data_file_label = PyQt5.QtWidgets.QLabel("Dark for Data")
        self.dark_for_data_file_box = PyQt5.QtWidgets.QLineEdit(parent=self)
        self.dark_for_data_file_button = PyQt5.QtWidgets.QToolButton(parent=self)
        self.blank_file_label = PyQt5.QtWidgets.QLabel("Blank File")
        self.blank_file_box = PyQt5.QtWidgets.QLineEdit(parent=self)
        self.blank_file_button = PyQt5.QtWidgets.QToolButton(parent=self)
        self.dark_for_blank_file_label = PyQt5.QtWidgets.QLabel("Dark fo Blank")
        self.dark_for_blank_file_box = PyQt5.QtWidgets.QLineEdit(parent=self)
        self.dark_for_blank_file_button = PyQt5.QtWidgets.QToolButton(parent=self)
        self.calibration_file_label = PyQt5.QtWidgets.QLabel("Calibration File")
        self.calibration_file_box = PyQt5.QtWidgets.QLineEdit(parent=self)
        self.calibration_file_button = PyQt5.QtWidgets.QToolButton(parent=self)

        self.current_directory = '.'

        self.data_file = ""
        self.dark_for_data_file = ""
        self.blank_file = ""
        self.dark_for_blank_file = ""
        self.calibration_file = ""

        layout = PyQt5.QtWidgets.QGridLayout()
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
        filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select data file(s)', self.current_directory)
        self.data_file_box.setText(filename[0])
        self.current_directory = PyQt5.QtCore.QFileInfo(filename[0]).dir().path()

    def open_dark_for_data_file(self):
        filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select dark file for data', self.current_directory)
        self.dark_for_data_file_box.setText(filename[0])
        self.current_directory = PyQt5.QtCore.QFileInfo(filename[0]).dir().path()

    def open_blank_file(self):
        filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select blank file for data', self.current_directory)
        self.blank_file_box.setText(filename[0])
        self.current_directory = PyQt5.QtCore.QFileInfo(filename[0]).dir().path()

    def open_dark_for_blank_file(self):
        filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select dark file for blank', self.current_directory)
        self.dark_for_blank_file_box.setText(filename[0])
        self.current_directory = PyQt5.QtCore.QFileInfo(filename[0]).dir().path()

    def open_calibration_file(self):
        filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Select calibraiton file (.ex3)', self.current_directory)
        self.calibration_file_box.setText(filename[0])
        self.current_directory = PyQt5.QtCore.QFileInfo(filename[0]).dir().path()

class MainWindow(PyQt5.QtWidgets.QMainWindow):
    quit = PyQt5.QtCore.pyqtSignal()
    finished = PyQt5.QtCore.pyqtSignal()
    processing = PyQt5.QtCore.pyqtSignal()
    missing = PyQt5.QtCore.pyqtSignal()

    def __init__(self, parent=None):
        PyQt5.QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        panel = PyQt5.QtWidgets.QWidget()
        self.button_box_widget = ButtonBoxWidget(parent=None)
        self.parameters_box_widget = ParametersBoxWidget(parent=None)
        self.file_dialog_box_widget = FileDialogBoxWidget(parent=None)

        panel_layout = PyQt5.QtWidgets.QVBoxLayout()
        panel_layout.addWidget(self.file_dialog_box_widget)
        panel_layout.addWidget(self.parameters_box_widget)
        panel_layout.addWidget(self.button_box_widget)
        panel.setLayout(panel_layout)
        panel.setFixedSize(640, 400)

        self.help_menu = self.menuBar().addMenu("&Help")
        self.about_action = PyQt5.QtWidgets.QAction("&About", self)
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
        self.button_box_widget.quit_button.clicked.connect(self.close)

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
        PyQt5.QtWidgets.QMessageBox.about(self, "About the DXAFS Data Converter", msg.strip())

def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
