import functools
import logging
import sys

from pathlib import Path

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QListView, QTableView, QTableWidget,
                             QPushButton, QTableWidgetItem)
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

import TextSP.ngrams.lyrics_helpers as lyrics_helpers


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
        # self.artist_window.show()

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

    def display_song_data(self, song_name, kind):
        """
        :param song_name:
        :param kind: "lyrics" or "ngrams"
        :return:
        """
        print(song_name, kind)

    def make_song_list(self, artist_name):
        logging.info('initialising the song list for {}'.format(artist_name))
        songs = list(lyrics_helpers.get_artist_songs(artist_name,
                                                     self.lyrics_path))

        self.song_table = QTableWidget()
        self.song_table.setRowCount(len(songs))
        self.song_table.setColumnCount(3)
        self.song_table.verticalHeader().hide()

        self.song_table.setMinimumSize(600, 400)
        self.song_table.setGeometry(600, 600, 800, 600)

        for n, song in enumerate(songs):
            song_item = QTableWidgetItem(song)
            song_item.setFlags(song_item.flags() ^ Qt.ItemIsEditable)
            lyrics_button = QPushButton('lyrics')
            ngram_button = QPushButton('n-grams')
            self.song_table.setItem(n, 0, song_item)
            self.song_table.setCellWidget(n, 1, lyrics_button)
            self.song_table.setCellWidget(n, 2, ngram_button)

            show_lyrics = functools.partial(self.display_song_data,
                                            song, 'lyrics')
            show_ngrams = functools.partial(self.display_song_data,
                                            song, 'ngrams')

            lyrics_button.clicked.connect(show_lyrics)
            ngram_button.clicked.connect(show_ngrams)

        self.song_table.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ann = AnnotateWindow()
    app.exec_()
    sys.exit()




