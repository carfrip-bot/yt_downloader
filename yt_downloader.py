import sys
import os
import re
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QComboBox,
                               QLabel, QFileDialog, QTextEdit, QProgressBar)
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon


class DownloadWorker(QThread):
    """Worker in background"""
    log_signal = Signal(str)
    progress_signal = Signal(int)
    finished_signal = Signal(bool, str)

    def __init__(self, url, output_dir, mode):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.mode = mode

    def run(self):
        cmd = ["yt-dlp", "-P", self.output_dir]

        # Selezione dei parametri di qualità
        if self.mode == "Original Quality (MKV)":
            cmd.extend(["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mkv"])
        elif self.mode == "Standard Quality (MP4 - Max 1080p)":
            cmd.extend(["-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]", "--merge-output-format", "mp4"])
        elif self.mode == "Light (MP4 - Max 720p)":
            cmd.extend(["-f", "bestvideo[height<=720]+bestaudio/best[height<=720]", "--merge-output-format", "mp4"])
        elif self.mode == "Audio Only (MP3)":
            cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])

        cmd.append(self.url)

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding='utf-8',
                errors='replace'
            )

            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    clean_line = line.strip()

                    # Regex per intercettare la percentuale di avanzamento (es: [download]  23.5% of...)
                    progress_match = re.search(r"\[download\]\s+(\d+(?:\.\d+)?)%", clean_line)
                    if progress_match:
                        percent = float(progress_match.group(1))
                        self.progress_signal.emit(int(percent))
                        continue  # Salta l'invio al log testuale per non intasarlo

                    self.log_signal.emit(clean_line)

            rc = process.poll()
            if rc == 0:
                self.finished_signal.emit(True, "Download successful!")
            else:
                self.finished_signal.emit(False, f"Error during download process. Error code: {rc}")

        except Exception as e:
            self.finished_signal.emit(False, f"Download start failed: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader GUI")
        self.resize(650, 500)

        self.default_output_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)

        # ---- RIGA 1: URL ----
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube URL here...")
        url_layout.addWidget(QLabel("Video URL:"))
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # ---- RIGA 2: CARTELLA DI DESTINAZIONE ----
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit(self.default_output_dir)
        self.folder_input.setReadOnly(True)
        self.btn_browse = QPushButton("Browse...")
        self.btn_browse.clicked.connect(self.browse_folder)

        folder_layout.addWidget(QLabel("Download folder:"))
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.btn_browse)
        main_layout.addLayout(folder_layout)

        # ---- RIGA 3: PARAMETRI / QUALITÀ ----
        options_layout = QHBoxLayout()
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Original Quality (MKV)",
            "Standard Quality (MP4 - Max 1080p)",
            "Light (MP4 - Max 720p)",
            "Audio Only (MP3)"
        ])
        options_layout.addWidget(QLabel("Quality Settings:"))
        options_layout.addWidget(self.quality_combo)
        options_layout.addStretch()
        main_layout.addLayout(options_layout)

        # ---- RIGA 4: AZIONE ----
        self.btn_download = QPushButton("DOWNLOAD")
        self.btn_download.setObjectName("BtnScarica")
        self.btn_download.clicked.connect(self.start_download)
        main_layout.addWidget(self.btn_download)

        # ---- RIGA 5: BARRA DI PROGRESSIONE ----
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        main_layout.addWidget(self.progress_bar)

        # ---- RIGA 6: LOG / CONSOLE ----
        main_layout.addWidget(QLabel("Log Process:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)

    def apply_dark_theme(self):
        # QSS Dark Theme con dettagli Verde Smeraldo (#10B981)
        dark_qss = """
            QWidget {
                background-color: #121212;
                color: #E0E0E0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 6px;
                color: #FFFFFF;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #10B981;
            }
            QPushButton {
                background-color: #2D2D2D;
                color: #EEEEEE;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #3D3D3D;
                border: 1px solid #10B981;
            }
            QPushButton:pressed {
                background-color: #1A1A1A;
            }
            QPushButton#BtnScarica {
                background-color: #10B981; 
                color: #FFFFFF; 
                font-weight: bold; 
                font-size: 14px;
                border: none;
            }
            QPushButton#BtnScarica:hover {
                background-color: #059669;
            }
            QPushButton#BtnScarica:disabled {
                background-color: #1F2937;
                color: #6B7280;
            }
            QComboBox::drop-down {
                border: none;
            }
            QProgressBar {
                border: 1px solid #333333;
                border-radius: 4px;
                text-align: center;
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-weight: bold;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #10B981;
                border-radius: 3px;
                width: 1px;
            }
        """
        self.setStyleSheet(dark_qss)

    def browse_folder(self):
        selected_dir = QFileDialog.getExistingDirectory(self, "Select destination folder",
                                                        self.folder_input.text())
        if selected_dir:
            self.folder_input.setText(selected_dir)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            self.log_output.setText("Error: Insert a valid URL before downloading.")
            return

        self.log_output.clear()
        self.progress_bar.setValue(0)
        self.log_output.append("Download initialization loading...")
        self.btn_download.setEnabled(False)
        self.btn_browse.setEnabled(False)

        # Istanziazione e avvio del thread worker
        self.worker = DownloadWorker(url, self.folder_input.text(), self.quality_combo.currentText())
        self.worker.log_signal.connect(self.update_log)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.finished_signal.connect(self.download_finished)
        self.worker.start()

    def update_log(self, text):
        self.log_output.append(text)
        self.log_output.ensureCursorVisible()

    def download_finished(self, success, message):
        if success:
            self.progress_bar.setValue(100)
        self.log_output.append("\n" + "=" * 40 + "\n" + message)
        self.btn_download.setEnabled(True)
        self.btn_browse.setEnabled(True)


if __name__ == "__main__":

    if sys.platform == "win32":
        import ctypes

        # Crea un ID univoco per la tua applicazione (Formato: Azienda.Prodotto.Sottoprodotto.Versione)
        myappid = "carfrip.ytdlp.downloadergui.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # ---------------------------------------------------------

    app = QApplication(sys.argv)
    window = MainWindow()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_png = os.path.join(script_dir, "yt_downloader.png")

    if os.path.exists(icon_png):
        window.setWindowIcon(QIcon(icon_png))
        app.setWindowIcon(QIcon(icon_png))

    window.show()
    sys.exit(app.exec())