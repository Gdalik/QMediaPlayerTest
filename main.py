from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QApplication
from PyQt6.QtCore import QObject, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os
import platform


MP3File = 'Audio/MP3_example.mp3'
OGGFile = 'Audio/OGG_example.ogg'
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
        self.PlayMP3But = QPushButton('Play MP3', self)
        self.PlayOGGBut = QPushButton('Play OGG', self)
        self.StopBut = QPushButton('Stop', self)
        self.VerticalLay.addWidget(self.PlayMP3But)
        self.VerticalLay.addWidget(self.PlayOGGBut)
        self.VerticalLay.addWidget(self.StopBut)


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

    def playCurrentAudio(self):
        if self.source() == self.currentAudio:
            self.play()
        else:
            self.setAudioFile()

    def onError(self, err, string):
        print(f'{err}: {string}')


class MainWindowContr(QObject):
    def __init__(self, parent):
        super().__init__()
        self.mw_view = parent
        self.mw_view.show()
        self.player = AudioPlayer(self)
        self.mw_view.PlayMP3But.clicked.connect(self.onPlayMP3But_clicked)
        self.mw_view.PlayOGGBut.clicked.connect(self.onPlayOGGBut_clicked)

    def onPlayMP3But_clicked(self):
        self.player.action = 'play'
        self.player.currentAudio = QUrl(MP3File)
        self.player.playCurrentAudio()

    def onPlayOGGBut_clicked(self):
        self.player.action = 'play'
        self.player.currentAudio = QUrl(OGGFile)
        self.player.playCurrentAudio()


def setAudioBackend():
    native_backend_var = {'Windows': 'windows', 'Darwin': 'darwin', 'Linux': 'gstreamer'}
    value = AudioBackend if AudioBackend != 'native' else native_backend_var[platform.system()]
    os.environ['QT_MEDIA_BACKEND'] = value


if __name__ == '__main__':
    setAudioBackend()
    app = QApplication([])
    mw_view = MainWindowView()
    mw_contr = MainWindowContr(mw_view)
    app.exec()
