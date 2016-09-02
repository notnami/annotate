import logging
import sys

import tqdm
from pathlib import Path

import PyQt5
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QListView)
from PyQt5.QtGui import QStandardItem, QStandardItemModel

import TextSP.ngrams.lyrics_helpers as lyrics_helpers

logging.basicConfig(level=logging.INFO)

class AnnotateWindow(QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        logging.info('initialising...')
        self.setupUI()
        # temporary
        args = app.arguments()
        self.lyrics_path = Path(args[1])
        self.init_artist_list(self.lyrics_path)


    def artist_selected(self):
        selected_index = self.artist_list.selectedIndexes()[0]
        selected_item = selected_index.data()
        self.artist_window = SongListWindow(self.lyrics_path,
                                            selected_item)

    def init_artist_list(self, lyrics_path: Path):
        self.artist_list = QListView()
        self.artist_list.setWindowTitle('Annotate')
        self.artist_list.setMinimumSize(600, 400)
        list_model = QStandardItemModel(self.artist_list)

        artist_names = lyrics_helpers.get_artists(lyrics_path)
        for artist in artist_names:
            artist_item = QStandardItem(artist)
            artist_item.setEditable(False)
            list_model.appendRow(artist_item)

        self.artist_list.setModel(list_model)
        self.artist_list.doubleClicked.connect(self.artist_selected)
        self.artist_list.show()


    def setupUI(self):
        logging.info('setting up the UI...')
        self.setGeometry(500, 500, 800, 600)
        self.setWindowTitle('Annotate')

class SongListWindow(QWidget):
    def __init__(self, lyrics_path, artist_name, **kwargs):
        super(SongListWindow, self).__init__(**kwargs)
        self.lyrics_path = lyrics_path
        self.make_song_list(artist_name)

    def make_song_list(self, artist_name):
        logging.info('initialising the song list for {}'.format(artist_name))
        self.song_list = QListView()
        self.song_list.setWindowTitle(artist_name)

        self.song_list.setMinimumSize(600, 400)
        self.song_list.setGeometry(600, 600, 800, 600)
        list_model = QStandardItemModel(self.song_list)

        songs = lyrics_helpers.get_artist_songs(artist_name, self.lyrics_path)
        for song in songs:
            song_item = QStandardItem(song)
            song_item.setEditable(False)
            list_model.appendRow(song_item)

        self.song_list.setModel(list_model)
        self.song_list.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ann = AnnotateWindow()
    app.exec_()
    sys.exit()




