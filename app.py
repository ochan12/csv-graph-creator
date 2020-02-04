import matplotlib.pyplot as plt  # Pie chart
from matplotlib import font_manager as fm
import matplotlib as mpl
import csv, random, os
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerPatch
from textwrap import wrap
from constants import MATERIAL_COLORS, get_colors
print(fm._fmcache)
FPATH = os.path.join('.', "fonts/futura/Futura Book font.ttf")
PROP = fm.FontProperties(fname=FPATH)

class HandlerEllipse(HandlerPatch):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        center = 0.5 * width - 0.5 * xdescent, 0.5 * height - 0.5 * ydescent
        p = mpatches.Ellipse(xy=center, width=height + xdescent,
                             height=height + ydescent)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.files = list()
        self.column_colors = dict()
        self.directory = ""
        self.title = ""

        layout = QtWidgets.QVBoxLayout()
        file_layout = QtWidgets.QHBoxLayout()
        self.setWindowTitle("CSV Chart Creator")
        self.setMinimumHeight(400)
        self.setMinimumWidth(600)

        self.create_table_widget()

        file_layout.addWidget(self.tableView)

        self.create_file_buttons()

        file_button_layout = QtWidgets.QVBoxLayout()
        file_button_layout.addWidget(self.addFileButton)
        file_button_layout.addWidget(self.removeFileButton)
        file_button_layout.addWidget(self.removeAll)
        file_layout.addLayout(file_button_layout)

        directory_layout = QtWidgets.QHBoxLayout()
        self.chooseDirectory = QtWidgets.QPushButton(parent=self)
        self.chooseDirectory.setText("¿Dónde guardar?")
        self.chooseDirectory.clicked.connect(self.select_directory)

        self.directory_label = QtWidgets.QLabel(
            "No se seleccionó ningún directorio")
        directory_layout.addWidget(self.chooseDirectory)

        directory_layout.addWidget(self.directory_label)

        self.create_color_table()

        file_layout.addWidget(self.colorTable)

        self.create_label_title()

        self.create_radio_options()

        self.create_label_color()

        self.create_graph_type_combo()

        self.finalGroupButton = QtWidgets.QButtonGroup(self)
        self.processFilesButton = QtWidgets.QPushButton(self)
        self.processFilesButton.setText("Crear imágenes")
        self.processFilesButton.clicked.connect(self.create_images)
        self.finalGroupButton.addButton(self.processFilesButton)

        layout.addLayout(file_layout)
        layout.addLayout(self.radio_options_layout)
        layout.addLayout(self.title_label_layout)
        layout.addLayout(self.graph_type_layout)
        layout.addLayout(self.color_label_layout)
        layout.addLayout(directory_layout)

        layout.addWidget(self.processFilesButton)
        self.setLayout(layout)

    def create_graph_type_combo(self):

        self.graph_type_layout = QtWidgets.QHBoxLayout()
        self.graph_type_combo = QtWidgets.QComboBox()
        self.graph_type_combo.addItems(["Torta", "Barras", "Histograma"])

        self.graph_type_layout.addWidget(QtWidgets.QLabel("Tipo de gráfico: "))
        self.graph_type_layout.addWidget(self.graph_type_combo)
        self.graph_type_layout.addStretch()

    def create_label_color(self):
        self.color_label_layout = QtWidgets.QHBoxLayout()
        self.color_label_layout.addWidget(QtWidgets.QLabel("Color de texto"))
        self.label_color_field = QtWidgets.QLineEdit()
        self.color_label_layout.addWidget(self.label_color_field)

    def create_label_title(self):
        self.title_label_layout = QtWidgets.QHBoxLayout()
        self.title_label_layout.addWidget(QtWidgets.QLabel("Título"))
        self.label_title_field = QtWidgets.QLineEdit()
        self.title_label_layout.addWidget(self.label_title_field)

    def create_radio_options(self):
        self.radio_options_layout = QtWidgets.QHBoxLayout()

        self.file_per_row_btn = QtWidgets.QRadioButton("1 imagen por línea")
        self.file_per_row_btn.setChecked(True)

        self.group_rows_btn = QtWidgets.QRadioButton(
            "Agrupar lineas en una imagen")

        self.radio_options_layout.addWidget(self.file_per_row_btn)
        self.radio_options_layout.addWidget(self.group_rows_btn)

    def create_color_table(self):
        self.colorTable = QtWidgets.QTableWidget(self)
        self.colorTable.setColumnCount(2)
        self.colorTable.setRowCount(0)
        self.colorTable.setHorizontalHeaderLabels(['Columna', 'Color (Hexa)'])
        self.colorTable.itemChanged.connect(self.item_changed)
        color_header = self.colorTable.horizontalHeader()
        color_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def create_file_buttons(self):

        self.fileGroupButton = QtWidgets.QButtonGroup(self)
        self.addFileButton = QtWidgets.QPushButton(parent=self)
        self.addFileButton.setText("Agregar archivo")
        self.addFileButton.clicked.connect(self.select_new_file)

        self.removeFileButton = QtWidgets.QPushButton(parent=self)
        self.removeFileButton.setText("Eliminar archivo")
        self.removeFileButton.clicked.connect(self.remove_row)

        self.removeAll = QtWidgets.QPushButton(parent=self)
        self.removeAll.setText("Eliminar todos")
        self.removeAll.clicked.connect(self.remove_all)

    def create_table_widget(self):
        self.tableView = QtWidgets.QTableWidget(self)
        self.tableView.setColumnCount(1)
        self.tableView.setHorizontalHeaderLabels(['Archivo'])
        self.tableView.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

    def create_pie_chart(self, sizes, colors, file, labels):
        
        fig1, ax1 = plt.subplots()
        patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=None,
                                            autopct='%1.0f%%', pctdistance=1.2, radius=0.4)

        c = [ mpatches.Circle((0.5, 0.5), radius = 0.25, facecolor=colors[i], edgecolor="none" ) for i in range(len(texts))]
        plt.legend(c,labels,handler_map={mpatches.Circle: HandlerEllipse()}, loc='center left', bbox_to_anchor=(1.1,0.5), frameon=False, prop=PROP)
        title = file.replace('.csv', '').replace('_groupped', '').replace('_', ' ').upper()
        
        fig1.suptitle("\n".join(wrap(title, 60)), fontproperties=PROP)
        
        #for text in texts:
         #   text.set_color('white')
         #   text.set_font_properties(PROP)
        for autotext in autotexts:
            autotext.set_color('grey')
            autotext.set_font_properties(PROP)

        ax1.axis('equal')
        plt.tight_layout()
        plt.savefig(self.directory+'/'+file.replace('.csv', '')+'_pie.eps')

    def create_bar_chart(self, sizes, colors, labels, file):
        print("Creating bar chart")
        plt.legend(loc='center', borderpad=0.0, fontproperties=PROP)
        fig, ax = plt.subplots()
        index = np.arange(len(labels))
        bar_width = 0.35
        opacity = 0.8
        plt.bar(index, sizes, bar_width, alpha=opacity, color=colors, fontproperties=PROP)
        plt.title(file.replace('.csv', '').upper())
        plt.xticks(index, labels)
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.directory+'/'+file.replace('.csv', '')+'_bar.eps')
        print("Finished bar chart")

    def create_images(self):
        if len(self.directory) != 0:
            for file in self.files:
                print(file)
                open_file = csv.DictReader(open(file[1]))
                custom_color = [self.column_colors[key]
                                for key in open_file.fieldnames]
                print("fields")
                print(open_file.fieldnames)
                if self.file_per_row_btn.isChecked():
                    i = 1
                    for row in open_file:
                        sizes = [v for k, v in row.items() if int(v) > 0]
                        if self.graph_type_combo.currentIndex() == 0:
                            self.create_pie_chart(
                                sizes=sizes, 
                                colors=custom_color, 
                                labels=open_file.fieldnames, 
                                file=file[0])

                        elif self.graph_type_combo.currentIndex() == 1:
                            self.create_bar_chart(
                                sizes=sizes, colors=custom_color, labels=open_file.fieldnames, file=file[0])
                        i += 1
                else:
                    df = pd.read_csv(file[1])
                    sizes = [df[column].sum() for column in df.columns]
                    if self.graph_type_combo.currentIndex() == 0:
                        self.create_pie_chart(
                            sizes=sizes, 
                            colors=custom_color, 
                            labels=open_file.fieldnames, 
                            file=file[0]+'_groupped')

                    elif self.graph_type_combo.currentIndex() == 1:
                        self.create_bar_chart(
                            sizes=sizes, colors=custom_color, labels=open_file.fieldnames, file=file[0]+'_groupped')
        else:
            self.showDialog()

    def item_changed(self, item):
        if item.column() > 0:
            hexa = item.text()
            item_changed = False
            if len(hexa) == 0:
                hexa = "#FFFFFF"
                item_changed = True
            if len(hexa) > 0:
                if not hexa.startswith("#"):
                    hexa = "#"+hexa
                    item_changed = True
                if len(hexa) < 7:
                    while len(hexa) < 7:
                        hexa = hexa+'0'
                        item_changed = True
            self.colorTable.item(item.row(), 1).setBackground(
                QtGui.QColor(hexa))
            self.colorTable.item(item.row(), 0).setBackground(
                QtGui.QColor(hexa))
            self.column_colors[self.colorTable.item(
                item.row(), 0).text()] = hexa

    def showDialog(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Selecciona donde guardar las imágenes")
        msgBox.setWindowTitle("Imágenes")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            print('OK clicked')

    def select_new_file(self):
        dlg = QtWidgets.QFileDialog(self)
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setViewMode(QtWidgets.QFileDialog.Detail)
        dlg.setNameFilter("Text files (*.csv)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.files.extend((name.split('/')[-1], name)
                              for name in filenames)
            print(self.files)
            self.update_files()
            self.update_color_table()

    def select_directory(self):
        dlg = QtWidgets.QFileDialog(self)
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)

        if dlg.exec_():
            selected_dir = dlg.selectedUrls()[0].toLocalFile()

            print(selected_dir)
            self.directory_label.setText(selected_dir)
            self.directory = selected_dir

    def update_color_table(self):
        for file in self.files:
            csv_file = csv.DictReader(open(file[1]))
            for field in csv_file.fieldnames:
                if not self.column_colors.__contains__(field):
                    self.column_colors[field] = random.choice(MATERIAL_COLORS)

        self.colorTable.setRowCount(len(self.column_colors.keys()))
        i = 0
        for key in self.column_colors.keys():
            self.colorTable.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
            self.colorTable.setItem(
                i, 1, QtWidgets.QTableWidgetItem(self.column_colors[key]))
            self.colorTable.item(i, 0).setBackground(
                QtGui.QColor(self.column_colors[key]))

            i += 1

    def remove_row(self):
        if len(self.files) > 0 and self.tableView.currentRow() >= 0:
            current_row = self.tableView.currentRow()
            self.files.pop(current_row)
            self.update_files()

    def remove_all(self):
        self.files.clear()
        self.column_colors.clear()
        self.update_files()

    def update_files(self):
        i = 0
        self.tableView.setRowCount(len(self.files))
        for file in self.files:
            self.tableView.setItem(i, 0, QtWidgets.QTableWidgetItem(file[0]))
            i += 1
        self.colorTable.setRowCount(len(self.column_colors))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
