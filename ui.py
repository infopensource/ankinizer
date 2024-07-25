from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication,QFileDialog,QMessageBox
from PySide6.QtGui import QIcon
from main import Translator
import threading

class MainWindow:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("main.ui")
        self.ui.setWindowTitle('Ankinizer')
        self.ui.setWindowIcon(QIcon('./icon.png'))
        self.ui.statusBar().showMessage('Started')
        
        self.ui.actionOpen.triggered.connect(self.input_explorer)
        self.ui.actionSave.triggered.connect(self.output_explorer)
        self.ui.actionAbout.triggered.connect(self.show_about)
        
        self.ui.ImportButton.clicked.connect(self.input_explorer)
        self.ui.ExportButton.clicked.connect(self.output_explorer)
        self.ui.RunButton.clicked.connect(self.run)
        self.ui.AdvancedButton.clicked.connect(self.show_advanced)
        
        # self.ui.FrontList.addItem('German')
        self.ui.FrontList.itemClicked.connect(self.update_list)
        
        self.translator = Translator()
        self.translator.input_file = ''
        self.translator.output_file = ''
        
    def show_about(self):
        self.about_window = AboutWindow()
        self.about_window.ui.show()
    
    def show_advanced(self):
        self.advanced_window = AdvancedWindow()
        self.advanced_window.ui.show()
    
    def input_explorer(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self.ui, 'Open File', './', 'Text Files (*.txt);;All Files(*)')
            self.translator.input_file = file_path
            self.ui.statusBar().showMessage('Input file selected')
            QMessageBox.information(self.ui, 'Success', 'File imported successfully')
            if self.translator.output_file != '':
                self.translator.read_file(file_path, self.translator.output_file)
                self.ui.statusBar().showMessage('Ready')
        except Exception as e:
            QMessageBox.critical(self.ui, 'Error', str(e))
        
    def output_explorer(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self.ui, 'Save File', './', 'Text Files (*.txt);;All Files(*)')
            self.translator.output_file = file_path
            self.ui.statusBar().showMessage('Output file selected')
            QMessageBox.information(self.ui, 'Success', 'File exported successfully')
            if self.translator.input_file != '':
                self.translator.read_file(self.translator.input_file, file_path)
                self.ui.statusBar().showMessage('Ready')
        except Exception as e:
            QMessageBox.critical(self.ui, 'Error', str(e))
    
    def run(self):
        try:
            self.ui.statusBar().showMessage('Please wait...')
            QApplication.processEvents()
            thread = threading.Thread(target=self.translator.translate())
            thread.start()
            while thread.is_alive():
                QApplication.processEvents()
            for line in self.translator.output_lines:
                self.ui.FrontList.addItem(line.split(';')[0])
            QApplication.processEvents()
            self.translator.write_file(self.translator.output_file)
            self.ui.statusBar().showMessage('Done')
            QMessageBox.information(self.ui, 'Success', 'Translation completed successfully')
        except Exception as e:
            QMessageBox.critical(self.ui, 'Error', str(e))
            self.ui.statusBar().showMessage('Failed')
        
            
    def update_list(self):
        self.ui.BackEdit.clear()
        for i in self.translator.output_lines:
            if i.split(';')[0] == self.ui.FrontList.currentItem().text():
                self.ui.BackEdit.setHtml(i.split(';')[1])

class AdvancedWindow:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("Advanced.ui")
        self.ui.setWindowTitle('Ankinizer - Advanced')
        self.ui.CancelButton.clicked.connect(self.close)
        self.ui.ApplyButton.clicked.connect(self.apply)
    
    def close(self):
        self.ui.close()
    
    def apply(self):
        pass

class AboutWindow:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("About.ui")
        self.ui.setWindowTitle('Ankinizer - About')

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.ui.show()
    app.exec()