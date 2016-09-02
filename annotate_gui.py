import sys

from pathlib import Path

import PyQt5
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel,
                             QListView)
from PyQt5.QtGui import QStandardItem, QStandardItemModel

# temporary
lyrics_path = Path('lyrics')

class AnnotateWindow(QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.setupUI()
        self.init_artist_list(lyrics_path)

    def __get_artist_list(self, lyrics_path: Path):
        for item in lyrics_path.iterdir():
            if item.is_dir():
                yield item.name

    def init_artist_list(self, lyrics_path: Path):
        list_view = QListView(parent=self)
        list_view.setMinimumSize(600, 400)
        list_model = QStandardItemModel(list_view)

        artist_names = self.__get_artist_list(lyrics_path)
        for artist in artist_names:
            artist_item = QStandardItem(artist)
            list_model.appendRow(artist_item)

        list_view.show()


    def setupUI(self):
        self.setGeometry(500, 500, 800, 600)
        self.setWindowTitle('Annotate')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ann = AnnotateWindow()
    app.exec_()
    sys.exit()




