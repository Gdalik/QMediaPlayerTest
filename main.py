from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QApplication
from PyQt6.QtCore import QObject, QUrl, Qt, QLibraryInfo
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os
import platform


MP3File = 'Audio/MP3_example.mp3'
OGGFile = 'Audio/OGG_example.ogg'
WAVEFile = 'Audio/WAVE_example.wav'

# Uncomment the audio backend you want to use:

AudioBackend = 'ffmpeg'
# AudioBackend = 'native'


class MainWindowView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName('MainWindow')
        self.setWindowTitle('QMediaPlayer Test')
        self.resize(150, 150)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName('centralwidget')
        self.setCentralWidget(self.centralwidget)
        self.VerticalLay = QVBoxLayout(self.centralwidget)
        self.PlayWAVEBut = QPushButton('Play WAVE', self)
        self.PlayMP3But = QPushButton('Play MP3', self)
        self.PlayOGGBut = QPushButton('Play OGG', self)
        self.StopBut = QPushButton('Stop', self)
        self.VerticalLay.addWidget(self.PlayWAVEBut)
        self.VerticalLay.addWidget(self.PlayMP3But)
        self.VerticalLay.addWidget(self.PlayOGGBut)
        self.VerticalLay.addWidget(self.StopBut)
        self._setShortcuts()
        self._showShortcuts()

    def _setShortcuts(self):
        self.PlayWAVEBut.setShortcut(Qt.Key.Key_1)
        self.PlayMP3But.setShortcut(Qt.Key.Key_2)
        self.PlayOGGBut.setShortcut(Qt.Key.Key_3)
        self.StopBut.setShortcut(Qt.Key.Key_Space)

    def _showShortcuts(self):
        buttons = self.findChildren(QPushButton)
        for B in buttons:
            sc = B.shortcut()
            B.setText(f'{B.text()} [Key: {sc.toString()}]')
            B.setShortcut(sc)


class AudioPlayer(QMediaPlayer):
    currentAudio: QUrl
    action: str

    def __init__(self, parent):
        super().__init__()
        self.mw_view = parent.mw_view
        self.audioOutput = QAudioOutput()
        self.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(1)
        self.mediaStatusChanged.connect(self.onPlayerStatusChanged)
        self.mw_view.StopBut.clicked.connect(self.onStopBut_clicked)
        self.errorOccurred.connect(self.onError)

    def setAudioFile(self):
        self.setSource(self.currentAudio)

    def onPlayerStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia and self.action == 'play':
            self.play()

    def onStopBut_clicked(self):
        self.action = 'stop'
        self.stop()

    def playFile(self, file=WAVEFile):
        self.currentAudio = QUrl(file)
        self.playCurrentAudio()

    def playCurrentAudio(self):
        self.action = 'play'
        if self.source() == self.currentAudio:
            self.play()
        else:
            self.setAudioFile()

    @staticmethod
    def onError(err, string):
        print(f'{err}: {string}')


class MainWindowContr(QObject):
    def __init__(self, parent):
        super().__init__()
        self.mw_view = parent
        self.mw_view.show()
        self.player = AudioPlayer(self)
        self.mw_view.PlayMP3But.clicked.connect(lambda: self.player.playFile(MP3File))
        self.mw_view.PlayOGGBut.clicked.connect(lambda: self.player.playFile(OGGFile))
        self.mw_view.PlayWAVEBut.clicked.connect(lambda: self.player.playFile(WAVEFile))


def setAudioBackend():
    native_backend_var = {'Windows': 'windows', 'Darwin': 'darwin', 'Linux': 'gstreamer'}
    value = AudioBackend if AudioBackend != 'native' else native_backend_var[platform.system()]
    os.environ['QT_MEDIA_BACKEND'] = value


def printAudioBackend():
    print(f"Qt multimedia backend: {os.getenv('QT_MEDIA_BACKEND')}")


def printQtVersion():
    print(f"Qt version: {QLibraryInfo.version().toString()}")


if __name__ == '__main__':
    setAudioBackend()
    app = QApplication([])
    mw_view = MainWindowView()
    mw_contr = MainWindowContr(mw_view)
    print(f'OS: {platform.system()}')
    printQtVersion()
    printAudioBackend()
    app.exec()
