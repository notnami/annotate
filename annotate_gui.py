import functools
import logging
import sys

from pathlib import Path

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QListWidget, QTableWidget,
                             QPushButton, QTableWidgetItem,
                             QProgressBar)
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

import TextSP.ngrams.lyrics_helpers as lyrics_helpers
import TextSP.ngrams.ngram_utils as ngram_utils


class AnnotateWindow(QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        logging.info('initialising...')
        self.setupUI()
        # temporary
        args = app.arguments()
        self.lyrics_path = Path(args[1])
        self.tokens_path = Path(args[2])
        self.init_artist_list(self.lyrics_path)
        self._tokens = None

    @property
    def tokens(self) -> dict:
        if not self._tokens:
            self._tokens = ngram_utils.get_tokens(tokens_path=self.tokens_path,
                                                  lyrics_path=self.lyrics_path)
        return self._tokens

    def artist_selected(self):
        selected_item = self.artist_list.selectedItems()[0]
        selected_artist = selected_item.text()
        self.artist_window = SongListWindow(self.lyrics_path,
                                            selected_artist)

    def init_artist_list(self, lyrics_path: Path):
        self.artist_list = QListWidget()
        self.artist_list.setWindowTitle('Annotate')
        self.artist_list.setMinimumSize(800, 1000)

        artist_names = lyrics_helpers.get_artists(lyrics_path)
        for artist in artist_names:
            self.artist_list.addItem(artist)

        self.artist_list.doubleClicked.connect(self.artist_selected)
        self.artist_list.show()

    def setupUI(self):
        logging.info('setting up the UI...')
        self.setGeometry(500, 500, 1000, 1000)
        self.setWindowTitle('Annotate')

class SongListWindow(QWidget):
    def __init__(self, lyrics_path, artist_name, **kwargs):
        super(SongListWindow, self).__init__(**kwargs)
        self.lyrics_path = lyrics_path
        self.make_song_list(artist_name)

    def display_song_data(self, artist_name, song_name):
        """
        :param song_name:
        :param kind: "lyrics" or "ngrams"
        :return:
        """
        self.song_window = SongView(artist_name, song_name)
        self.song_window.show()

    def song_selected(self, artist_name=None):
        selected_item = self.song_list.selectedItems()[0]
        selected_song = selected_item.text()
        self.display_song_data(artist_name, selected_song)


    def make_song_list(self, artist_name):
        logging.info('initialising the song list for {}'.format(artist_name))
        songs = list(lyrics_helpers.get_artist_songs(artist_name,
                                                     self.lyrics_path))

        self.song_list = QListWidget()

        self.song_list.setWindowTitle(artist_name)
        self.song_list.setMinimumSize(600, 400)
        self.song_list.setGeometry(600, 600, 800, 600)

        for song in songs:
            self.song_list.addItem(song)

            # ngram_button.clicked.connect(show_ngrams)

        song_selected = functools.partial(self.song_selected,
                                          artist_name)
        self.song_list.doubleClicked.connect(song_selected)

        self.song_list.show()

class SongView(QWidget):
    def __init__(self, song_artist, song_name, **kwargs):
        super(SongView, self).__init__(**kwargs)
        self.artist = song_artist
        self.song_name = song_name
        self.setupUI()

    def setupUI(self):
        self.setMinimumSize(600, 800)
        self.make_lyrics_tab()

    def make_lyrics_tab(self):
        # FIXME: this hangs if the tokens need to be computed anew
        # show a progress bar
        progress_bar = QProgressBar(parent=self)
        # make it be a "busy" progress bar
        progress_bar.setRange(0, 0)
        progress_bar.setMinimumWidth(self.minimumWidth())
        progress_bar.show()
        all_tokens = ann.tokens
        song_tokens = all_tokens[self.artist][self.song_name]
        print(song_tokens)
        progress_bar.hide()
        # FIXME: display a table of tokens




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ann = AnnotateWindow()
    app.exec_()
    sys.exit()




