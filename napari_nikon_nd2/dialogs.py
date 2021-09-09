import os

from PyQt5.QtWidgets import QDialogButtonBox, QComboBox, QCheckBox, QWidget
from PyQt5.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from magicgui import magicgui, widgets
'''
choices = ['one', 'two', 'three']
w1 = widgets.ComboBox(choices=choices, value='two', label='ComboBox:')
w2 = widgets.RadioButtons(choices=choices, label='RadioButtons:')
container = widgets.Container(widgets=[w1, w2])
container.show() 
'''

class openWindow(QDialog):
    def __init__(self, filepath, nseries, parent=None):
        super().__init__()
        print(self)
        self.setParent(parent)
        self.setModal(False)
        self.setWindowTitle(f"Opening {os.path.basename(filepath)}")
        self.layout = QVBoxLayout()
        self.series_label= QLabel("Select which series to open")
        series_list = [str(i) for i in list(range(nseries))]
        self.series_combo = QComboBox()
        self.series_combo.addItems(series_list)
        self.layout.addWidget(self.series_label)
        self.layout.addWidget(self.series_combo)
        self.setLayout(self.layout)
        print("Showing now")
         
def open_options(nseries=1):

    dialog = QDialog()
    series_list = list(range(nseries))
    series_combo = QComboBox()
    series_combo.addItems(series_list)
    lazy_check = QCheckBox(False)
    # dialog.add
    # open_button = widgets.PushButton(text="Open", name="Open")
    container = widgets.Container(widgets=[series_combo, lazy_check])#, open_button])
    print("Container created")
    return 1, True