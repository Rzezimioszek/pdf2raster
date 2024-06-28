import os.path

from pdf2image import convert_from_path
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = 933120000
import pathlib as ph
import sys

from tkinter import messagebox as msg
from tkinter import filedialog


# #### ## Kod dla UI

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QStyle
)
from PyQt5.uic import loadUi

from PyQt5.QtGui import QIcon

extform = {'jpg': 'JPEG',
           'tiff': 'TIFF'}

from pdf2raster_ui import Ui_MainWindow

# #### ##

# pdf2raster 0.1


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

        self.pdf = ''
        self.save = ''
        self.dpi = 0

        ### icons
        self.btnRun.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))

    def connectSignalsSlots(self):
        self.btnRun.clicked.connect(lambda x: self.convert())
        self.btnOpen.clicked.connect(lambda x: self.open_file())
        self.btnSave.clicked.connect(lambda x: self.open_dir())

    def open_file(self):

        filetypes_option = (("pliki pdf", "*.pdf"), ("Wszystkie pliki", "*.*"))
        path = filedialog.askopenfilenames(title="Wybierz plik lub pliki", filetypes=filetypes_option)
        if path is not None:
            self.pdf = path
            i = len(path)
            self.linePDF.setText(f"Załadowano: {i}")

    def open_dir(self):
        path = filedialog.askdirectory(title="Wybierz folder")

        if path is not None:
            self.lineSave.setText(path)
            self.save = path

    def convert(self):

        pdfs = self.pdf
        path = self.save


        dpi = 0


        sdpi = str(self.lineDPI.text())

        if sdpi == '':
            dpi = 0
        elif sdpi.isdecimal():
            dpi = int(sdpi)
        else:
            dpi = 0

        print(pdfs, path, dpi)


        ext = 'jpg'
        format = 'JPEG'

        if self.rTIFF.isChecked():
            ext = 'tiff'
            format = 'TIFF'

        try:
            for pdf in pdfs:
                print(pdf)
                pdf_to_raster(save_path=path, pdf_path=pdf, ext=ext, format=format, dpi=dpi)
            msg.showinfo("Wynik konwersji", "Konwersja z pdf do formatu rastrowego wykonana poprawnie")
        except:
            msg.showerror("Błąd konwersji", "Nieznany błąd konwersji")


def main():
    ...
    # convert()


def pdf_to_raster(save_path = '', pdf_path='MPZT.pdf', ext='jpg', format='JPEG', dpi=0):

    path = ph.Path(pdf_path)
    name = str(path.name).replace(path.suffix, '')


    if dpi == 0:
        images = convert_from_path(pdf_path=pdf_path, poppler_path=r'poppler-24.02.0\Library\bin') #, dpi=100)
    else:
        images = convert_from_path(pdf_path=pdf_path, poppler_path=r'poppler-24.02.0\Library\bin', dpi=dpi)

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save(f"{save_path}/{name} ({i}).{ext}", format=format)


if __name__ == "__main__":
    # main()
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())