import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget,  QPushButton, QRadioButton
from PySide6.QtWidgets import QTableWidget, QFileDialog, QTableWidgetItem, QInputDialog, QMessageBox

import re
import pickle

eng = dict()
rus = dict()
spa = dict()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.poiner = 0
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 500)
        self.table.setRowCount(0)
        self.table.setColumnWidth(1, 200)
        self.table.setHorizontalHeaderLabels(["Words", "Number"])
        self.curLanguage = QLabel("English")
        self.setWindowTitle("3 Dicts")
        self.unique_words_count = 0
        self.total_words_count = 0
        self.infoLabel = QLabel()
        mainLayout = QVBoxLayout()
        firsLayerLayout = QHBoxLayout()
        fileChooseV = QVBoxLayout()

        fileButton = QPushButton("add text to data")
        fileButton.clicked.connect(self.openFileDialog)

        radioButtonLayout = QHBoxLayout()

        radiobutton = QRadioButton("English")
        radiobutton.setChecked(True)
        radiobutton.type = 0
        radiobutton.toggled.connect(self.onClicked)
        radioButtonLayout.addWidget(radiobutton)

        radiobutton = QRadioButton("RUS")
        radiobutton.type = 1
        radiobutton.toggled.connect(self.onClicked)
        radioButtonLayout.addWidget(radiobutton)

        radiobutton = QRadioButton("Spanish")
        radiobutton.type = 2
        radiobutton.toggled.connect(self.onClicked)
        radioButtonLayout.addWidget(radiobutton)

        font = self.curLanguage.font()
        font.setPointSize(24)
        self.curLanguage.setFont(font)

        self.curLanguage.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        font.setPointSize(16)

        fileChooseV.addWidget(self.curLanguage)
        fileChooseV.addWidget(fileButton)
        firsLayerLayout.addLayout(radioButtonLayout)


        firsLayerLayout.addLayout(fileChooseV)
        mainLayout.addLayout(firsLayerLayout)


##################################################################################
        secondLayerLayout = QHBoxLayout()

        secondLayerLayout.addWidget(self.table)


        logicL = QVBoxLayout()
        sortAlf = QPushButton()
        sortDescending = QPushButton()
        sortAscending = QPushButton()
        sortReverseAlf = QPushButton()
        hLayouts = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]



        hLayouts[0].addWidget(sortAscending)
        hLayouts[0].addWidget(sortDescending)
        sortAlf.setText("sortAlf")
        sortDescending.setText("sortDescending")
        sortAscending.setText("sortAscending")
        sortReverseAlf.setText("sortReverseAlf")
        info = QLabel("сортировки")
        info.setFixedHeight(30)
        info.setFont(font)
        info.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)



        ###search

        self.lineEd = QLineEdit()
        self.lineEd.setMaximumWidth(100)
        buttonlineEd = QPushButton("Search")
        buttonlineEd.setMaximumWidth(100)
        layoutEdit = QHBoxLayout()
        layoutEdit.addWidget(self.lineEd)
        layoutEdit.addWidget(buttonlineEd)

        info1 = QLabel("поисковик")
        info1.setFont(font)
        info1.setFixedHeight(30)
        info1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        logicL.addSpacing(50)
        logicL.addWidget(info1)

        logicL.addLayout(layoutEdit)

        hLayouts[1].addWidget(sortAlf)
        hLayouts[1].addWidget(sortReverseAlf)
        ####
        logicL.addWidget(info)
        logicL.addSpacing(10)
        logicL.addLayout(hLayouts[0])
        logicL.addLayout(hLayouts[1])

        buttonDEL = QPushButton("DEL Word")
        buttonADD = QPushButton("ADD Word")

        buttonEDIT = QPushButton("Edit word")

        logicL.addSpacing(50)
        info2 = QLabel("манипуляции с словом")
        info2.setFont(font)
        info2.setFixedHeight(30)
        info2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        logicL.addWidget(info2)
        logicL.addWidget(buttonDEL)
        logicL.addWidget(buttonADD)
        logicL.addWidget(buttonEDIT)

        saveButton = QPushButton("Save Dictionary")
        loadButton = QPushButton("Load Dictionary")

        saveButton.clicked.connect(self.saveDictionary)
        loadButton.clicked.connect(self.loadAndMergeDictionary)
        hLayouts[2].addWidget(saveButton)
        hLayouts[2].addWidget(loadButton)
        logicL.addLayout(hLayouts[2])
        logicL.addWidget(self.infoLabel)
        logicL.addSpacing(200)
        secondLayerLayout.addLayout(logicL)
        mainLayout.addLayout(secondLayerLayout)
        container = QWidget()
        container.setLayout(mainLayout)
        self.setMinimumSize(950, 600)
        self.setCentralWidget(container)


        buttonlineEd.clicked.connect(self.searchWords)
        sortAscending.clicked.connect(self.sortExtending)
        sortAlf.clicked.connect(self.sortTable)
        sortReverseAlf.clicked.connect(self.sortReverseAlf)
        sortDescending.clicked.connect(self.sortDescending)
        buttonDEL.clicked.connect(self.deleteWord)
        buttonADD.clicked.connect(self.addWord)
        buttonEDIT.clicked.connect(self.editWord)


        ##### data
    def searchWords(self):
        search_text = self.lineEd.text().strip().lower()
        if not search_text:
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)
            return

        pattern = re.compile(fr'\b{re.escape(search_text)}', re.IGNORECASE)

        for row in range(self.table.rowCount()):
            word_item = self.table.item(row, 0)
            if word_item:
                word = word_item.text().lower()
                if pattern.search(word):
                    self.table.setRowHidden(row, False)
                else:
                    self.table.setRowHidden(row, True)
        self.lineEd.setText("")

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Language is %s" % (radioButton.type))
        if radioButton.type == 1:
            self.curLanguage.setText("Russian")
            self.poiner = 1
        elif radioButton.type == 2:
            self.curLanguage.setText("Spanish")
            self.poiner = 2
        else :
            self.curLanguage.setText("English")
            self.poiner = 0
        self.fillTable()




    def fillTable(self):
        self.table.setRowCount(0)

        if self.poiner == 0:
            word_dict = eng
        elif self.poiner == 1:
            word_dict = rus
        else:
            word_dict = spa

        self.unique_words_count = len(word_dict)
        self.total_words_count = sum(word_dict.values())
        self.updateInfoLabel()
        sorted_word_dict = dict(sorted(word_dict.items(), key=lambda item: item[1], reverse = True))

        # Заполnenie
        for i, (word, count) in enumerate(sorted_word_dict.items()):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(word))
            self.table.setItem(i, 1, QTableWidgetItem(str(count)))


    def openFileDialog(self):
        filename = QFileDialog.getOpenFileName(self,'Open File')
        if filename[0]:
            f = open(filename[0],'r')
            with f:
                data = f.read()
                words = re.findall(r'\b[а-яА-Яa-zA-Záéíóúüñ]+\b', data.lower())
                #print(words[:600])
                if self.poiner == 0:
                    for word in words:
                        if word in eng:
                            eng[word] += 1
                        else:
                            eng[word] = 1
                elif self.poiner == 1:
                    for word in words:
                        if word in rus:
                            rus[word] += 1
                        else:
                            rus[word] = 1
                else:
                    for word in words:
                        if word in spa:
                            spa[word] += 1
                        else:
                            spa[word] = 1
        self.fillTable()

    def sortDescending(self):
        table = self.table

        table.setRowCount(0)

        if self.poiner == 0:
            word_dict = eng
        elif self.poiner == 1:
            word_dict = rus
        else:
            word_dict = spa

        sorted_words = sorted(word_dict.items(), key=lambda item: item[1], reverse = True)

        for word, count in sorted_words:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(word))
            table.setItem(row_position, 1, QTableWidgetItem(str(count)))


    def sortExtending(self):
        table = self.table

        table.setRowCount(0)

        if self.poiner == 0:
            word_dict = eng
        elif self.poiner == 1:
            word_dict = rus
        else:
            word_dict = spa
        sorted_words = sorted(word_dict.items(), key=lambda item: item[1], reverse = True)
        sorted_words.reverse()

        for word, count in sorted_words:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(word))
            table.setItem(row_position, 1, QTableWidgetItem(str(count)))



    def sortTable(self):
        table = self.table

        row_count = table.rowCount()

        table_data = []
        for row in range(row_count):
            word_item = table.item(row, 0)
            count_item = table.item(row, 1)
            if word_item and count_item:
                word = word_item.text()
                count = count_item.text()
                table_data.append((word, count))

        sorted_data = sorted(table_data, key=lambda x: x[0])

        table.setRowCount(0)

        for row, (word, count) in enumerate(sorted_data):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(word))
            table.setItem(row, 1, QTableWidgetItem(count))


    def sortReverseAlf(self):
        table = self.table

        row_count = table.rowCount()

        table_data = []
        for row in range(row_count):
            word_item = table.item(row, 0)
            count_item = table.item(row, 1)
            if word_item and count_item:
                word = word_item.text()
                count = count_item.text()
                table_data.append((word, count))

        sorted_data = sorted(table_data, key=lambda x: x[0])
        sorted_data.reverse()
        table.setRowCount(0)

        for row, (word, count) in enumerate(sorted_data):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(word))
            table.setItem(row, 1, QTableWidgetItem(count))





    def deleteWord(self):
        selected_items = self.table.selectedItems()  # Get selected items (cells)
        if not selected_items:
            return

        words_to_delete = set()

        if self.poiner == 0:
            word_dict = eng
        elif self.poiner == 1:
            word_dict = rus
        else:
            word_dict = spa


        for item in selected_items:
            if item.column() == 0:
                word = item.text()
                words_to_delete.add(word)

        confirmation_message = f"Do you want to delete the selected word(s): {', '.join(words_to_delete)}?"
        reply = QMessageBox.question(self, 'Confirm Deletion', confirmation_message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for word in words_to_delete:
                if word in word_dict:
                    del word_dict[word]
                    self.table.removeRow(item.row())
        else:
            pass






    def addWord(self):
        new_word, ok = QInputDialog.getText(self, "Add Word", "Enter a new word:")

        if ok and new_word:
            new_word = new_word.strip().lower()
            if not new_word:
                return

            if self.poiner == 0:
                word_dict = eng
            elif self.poiner == 1:
                word_dict = rus
            else:
                word_dict = spa

            if new_word in word_dict:
                QMessageBox.warning(self, "Word Already Exists", "The word already exists in the dictionary.")
                return

            word_dict[new_word] = 0
            if self.poiner == 0:
                word_dict = eng
                eng[new_word] = 0
            elif self.poiner == 1:
                word_dict = rus
                rus[new_word] = 0
            else:
                word_dict = spa
                spa[new_word] = 0

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(new_word))
            self.table.setItem(row_position, 1, QTableWidgetItem("0"))




    def editWord(self):
        selected_items = self.table.selectedItems()  # Get selected items (cells)
        if not selected_items:
            return  # No cells selected

        if self.poiner == 0:
            word_dict = eng
        elif self.poiner == 1:
            word_dict = rus
        else:
            word_dict = spa

        for item in selected_items:
            if item.column() == 0:
                old_word = item.text()
                new_word, ok = QInputDialog.getText(self, "Edit Word", f"Edit word '{old_word}' to:")
                if ok and new_word:
                    new_word = new_word.strip().lower()

                    if not new_word:
                        return

                    if new_word in word_dict:
                        word_dict[new_word] += word_dict[old_word]
                        del word_dict[old_word]
                        self.table.removeRow(item.row())

                        options = QFileDialog.Options()
                        file_name, _ = QFileDialog.getOpenFileName(self, "Select Text File for Replacement", "", "Text Files (*.txt);;All Files (*)", options=options)
                        if file_name:
                            with open(file_name, 'r') as file:
                                file_content = file.read()

                            file_content = file_content.replace(old_word, new_word)

                            with open(file_name, 'w') as file:
                                file.write(file_content)

                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)
                        self.table.setItem(row_position, 0, QTableWidgetItem(new_word))
                        self.table.setItem(row_position, 1, QTableWidgetItem(str(word_dict[new_word])))

                    else:
                        word_dict[new_word] = word_dict[old_word]
                        del word_dict[old_word]

                        options = QFileDialog.Options()
                        file_name, _ = QFileDialog.getOpenFileName(self, "Select Text File for Replacement", "", "Text Files (*.txt);;All Files (*)", options=options)
                        if file_name:
                            with open(file_name, 'r') as file:
                                file_content = file.read()

                            file_content = file_content.replace(old_word, new_word)

                            with open(file_name, 'w') as file:
                                file.write(file_content)
                        item.setText(new_word)


        self.fillTable()


    def saveDictionary(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Dictionary", "", "Dictionary Files (*.dict);;All Files (*)")
        if not file_name:
            return  # User canceled the save dialog

        if self.poiner == 0:
            word_dict = eng
        elif self.poiner == 1:
            word_dict = rus
        else:
            word_dict = spa

        try:
            with open(file_name, 'wb') as file:
                pickle.dump(word_dict, file)  # Serialize and save the dictionary to a file
            QMessageBox.information(self, "Dictionary Saved", "Dictionary has been saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the dictionary: {str(e)}")


    def loadAndMergeDictionary(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Dictionary", "", "Dictionary Files (*.dict);;All Files (*)")
        if not file_name:
            return  # User canceled the load dialog

        if self.poiner == 0:
            word_dict = eng
        elif self.poiner == 1:
            word_dict = rus
        else:
            word_dict = spa

        try:
            with open(file_name, 'rb') as file:
                loaded_dict = pickle.load(file)

            for word, count in loaded_dict.items():
                if word in word_dict:
                    word_dict[word] += count
                else:
                    word_dict[word] = count

            QMessageBox.information(self, "Dictionary Loaded", "Dictionary has been loaded and merged successfully.")
            self.fillTable()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while loading the dictionary: {str(e)}")
        self.fillTable()

    def updateInfoLabel(self):
        info_text = f"Unique Words: {self.unique_words_count} | Total Words: {self.total_words_count}"
        self.infoLabel.setText(info_text)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
