from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication,QFileDialog,QMessageBox
from main import Translator

class MainWindow:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("main.ui")
        
        self.ui.ImportButton.clicked.connect(self.input_explorer)
        self.ui.ExportButton.clicked.connect(self.output_explorer)
        self.ui.RunButton.clicked.connect(self.run)
        
        self.ui.FrontList.addItem('German')
        
        self.translator = Translator()
        self.translator.input_file = ''
        self.translator.output_file = ''
    
    def input_explorer(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self.ui, 'Open File', './', 'Text Files (*.txt);;All Files(*)')
            self.translator.input_file = file_path
            QMessageBox.information(self.ui, 'Success', 'File imported successfully')
        except Exception as e:
            QMessageBox.critical(self.ui, 'Error', str(e))
        
    def output_explorer(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self.ui, 'Save File', './', 'Text Files (*.txt);;All Files(*)')
            self.translator.output_file = file_path
            self.translator.write_file(file_path)
            QMessageBox.information(self.ui, 'Success', 'File exported successfully')
        except Exception as e:
            QMessageBox.critical(self.ui, 'Error', str(e))
    
    def run(self):
        try:
            self.translator.translate()
            for line in self.translator.output_lines:
                self.ui.FrontList.addItem(line.split(';')[0])
            QMessageBox.information(self.ui, 'Success', 'Translation completed successfully')
        except Exception as e:
            QMessageBox.critical(self.ui, 'Error', str(e))
        

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.ui.show()
    app.exec()