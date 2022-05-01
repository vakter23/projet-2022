#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Volkan AKTER

This program allows to a doctor :
- To create a folder for a patient
- To add symptoms to the history of the patient
- Get recommendations for symptoms entered
- List all the folder he have
- Open the folder of a patient
"""

import sys
import json
from PyQt5.QtCore import pyqtSlot
from paramiko import client
from PyQt5.QtGui import QIntValidator, QPixmap, QFont
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QWidget, QLabel, QRadioButton, QButtonGroup, QPlainTextEdit, QToolTip,
                             QListWidget)


################################################################
# The main window displays :
# - Esthetic :
# - - Logo of the school
# - - The company's name
# - - A welcoming message
# - Two buttons
# - - A button to the creation of a new folder
# - - A button to list all patient folder's
################################################################
class MainWindow:
    class MainView(QWidget):
        def __init__(self):
            super().__init__()

            self.myCtrl = MainWindow.MainController()

            # Initialisation of differents items in the view
            # Logo
            # creating label
            self.labelImage = QLabel(self)
            # loading image
            self.pixmap = QPixmap('logo-episen.jpg')
            # adding image to label
            self.labelImage.setPixmap(self.pixmap)
            # Optional, resize label to image size
            self.labelImage.resize(self.pixmap.width(), self.pixmap.height())

            self.labelNomPlateforme = QLabel(self)
            self.labelNomPlateforme.setText('PARAMEDIVAL')

            self.labelMessageAccueil = QLabel(self)
            self.labelMessageAccueil.setText('Bienvenue')

            self.buttonCreer = QPushButton('Creer', self)
            self.buttonCreer.setStyleSheet("color: blue;"
                                           "background-color: white;"
                                           "selection-color: yellow;"
                                           "selection-background-color: blue;")

            self.buttonCharger = QPushButton('Charger', self)
            self.buttonCharger.setStyleSheet("color: blue;"
                                             "background-color: white;"
                                             "selection-color: yellow;"
                                             "selection-background-color: blue;")

            self.init_ui()
            self.show()

        # Definition of the box
        def init_ui(self):
            h_box_image = QHBoxLayout()
            h_box_image.addWidget(self.labelImage)

            h_box_label = QHBoxLayout()
            h_box_label.addWidget(self.labelNomPlateforme)

            h_box_message = QHBoxLayout()
            h_box_message.addWidget(self.labelMessageAccueil)

            v_box_button = QVBoxLayout()
            v_box_button.addWidget(self.buttonCreer)
            v_box_button.addWidget(self.buttonCharger)

            # Order the different boxs in the view
            v_box = QVBoxLayout()
            v_box.addLayout(h_box_image)
            v_box.addLayout(h_box_label)
            v_box.addLayout(h_box_message)
            v_box.addLayout(v_box_button)

            # Align center the two text
            self.labelNomPlateforme.setAlignment(QtCore.Qt.AlignCenter)
            self.labelMessageAccueil.setAlignment(QtCore.Qt.AlignCenter)

            self.setLayout(v_box)
            self.setWindowTitle('Paramadival')

            # Add the functionality to the buttons
            self.buttonCreer.clicked.connect(self.open_folder_view)
            self.buttonCharger.clicked.connect(self.open_list_patient_view)

        def closeEvent(self, event):
            event.accept()  # let the window close
            self.myCtrl.closeWindow()

        @pyqtSlot()
        def open_folder_view(self):
            self.cams = FolderWindow.FolderView()
            self.close()

        @pyqtSlot()
        def open_list_patient_view(self):
            self.cams = ListPatientWindow.ListPatientView()
            self.close()

    class MainController:
        def __init__(self):
            self.myModel = MainWindow.MainModel()

        def closeWindow(self):
            self.myModel.closeWindow()

    class MainModel:
        def __init__(self):
            print()

        def closeWindow(self):
            print()


################################################################
# The folder window displays :
# - 4 informations about the patient (that can be modified) :
# - - Nom
# - - Prenom
# - - Age
# - - Sexe
# - 3 buttons :
# - - To open the personal history of the patient (if it's exist)
# - - Save button to save a new patient or to save news info about the patient
# - - Close button to return to the main window
# - Two text area :
# - - The left text area is the area where the doctor can write the symptoms about the patient
# - - The right text area can not be written in because it display recommendation medicaments about the symptoms entered
################################################################
class FolderWindow:
    class FolderView(QWidget):
        def __init__(self, file_name=None):
            super().__init__()

            self.myCtrl = FolderWindow.FolderController()

            # Initialisation of differents items in the view

            # Top
            # 1.1 Infos about the patient
            self.labelNom = QLabel(self)
            self.labelNom.setText('Nom :')
            self.lineNom = QLineEdit(self)

            self.labelPrenom = QLabel(self)
            self.labelPrenom.setText('Prenom :')
            self.linePrenom = QLineEdit(self)

            self.labelAge = QLabel(self)
            self.labelAge.setText('Age :')
            self.lineAge = QLineEdit(self)
            self.lineAge.setValidator(QIntValidator(0, 200))

            self.labelSexe = QLabel('Sexe')
            self.rbtnM = QRadioButton('M')
            self.rbtnF = QRadioButton('F')
            self.btnGroupSexe = QButtonGroup()
            self.btnGroupSexe.addButton(self.rbtnM)
            self.btnGroupSexe.addButton(self.rbtnF)
            self.rbtnM.setChecked(True)  # Check the the button M
            # 1.2
            self.buttonHistory = QPushButton('Historique')

            # 2.1
            self.textDoctor = QPlainTextEdit(self)

            # 2.2
            self.textMedicament = QPlainTextEdit(self)
            self.textMedicament.setReadOnly(True)
            self.textMedicament.setStyleSheet("background-color: grey; color: white;")

            # 3.1
            self.setToolTip('Tooltip for <b>QWidget</b>')
            self.buttonSave = QPushButton('Sauvegarder')
            self.buttonSave.setToolTip('<b>Sauvegarder Le fichier</b>')

            # 3.2
            self.buttonClose = QPushButton('Fermer')
            self.buttonClose.setToolTip('<b>Revenir menu principal</b>')

            # If there is a file_name we retrieve the patient datas
            if file_name is not None:
                datas = (file_name.replace(".json", "")).split("_")  # remove the .json and separate the datas
                self.lineNom.setText(datas[0])  # His nom
                self.linePrenom.setText(datas[1])  # His prenom
                self.lineAge.setText(datas[2])  # His age
                if datas[3] == "M":  # His sexe
                    if not self.rbtnM.isChecked():
                        self.rbtnF.setChecked(False)
                        self.rbtnM.setChecked(True)
                else:
                    if self.rbtnM.isChecked():
                        self.rbtnM.setChecked(False)
                        self.rbtnF.setChecked(True)

            self.init_ui()
            self.show()

        # Definition of the box
        def init_ui(self):

            # Top left box #1
            # Box Nom
            h_box_nom = QHBoxLayout()
            h_box_nom.addWidget(self.labelNom)
            h_box_nom.addWidget(self.lineNom)

            # Box Prenom
            h_box_prenom = QHBoxLayout()
            h_box_prenom.addWidget(self.labelPrenom)
            h_box_prenom.addWidget(self.linePrenom)

            # Box Age
            h_box_age = QHBoxLayout()
            h_box_age.addWidget(self.labelAge)
            h_box_age.addWidget(self.lineAge)

            # Box Sexe
            h_box_sexe = QHBoxLayout()
            h_box_sexe.addWidget(self.labelSexe)
            h_box_sexe.addWidget(self.rbtnM)
            h_box_sexe.addWidget(self.rbtnF)

            # Top right box
            h_box_btn_history = QHBoxLayout()
            h_box_btn_history.addWidget(self.buttonHistory)

            # Top left
            v_box_top_left = QVBoxLayout()
            v_box_top_left.addLayout(h_box_nom)
            v_box_top_left.addLayout(h_box_prenom)
            v_box_top_left.addLayout(h_box_age)
            v_box_top_left.addLayout(h_box_sexe)

            h_box_top_right = QHBoxLayout()
            h_box_top_right.addLayout(h_box_btn_history)

            # Top box
            h_box_top = QHBoxLayout()
            h_box_top.addLayout(v_box_top_left)
            h_box_top.addLayout(h_box_top_right)

            # Mid box
            h_box_mid = QHBoxLayout()
            h_box_mid.addWidget(self.textDoctor)
            h_box_mid.addWidget(self.textMedicament)

            # Box Bottom
            h_box_button = QHBoxLayout()
            h_box_button.addWidget(self.buttonSave)
            h_box_button.addWidget(self.buttonClose)

            # Order the different boxs in the view
            v_box = QVBoxLayout()
            v_box.addLayout(h_box_top)
            v_box.addLayout(h_box_mid)
            v_box.addLayout(h_box_button)

            self.setLayout(v_box)
            self.setWindowTitle('Dossier')

            # Add the functionality to the buttons
            self.buttonClose.clicked.connect(self.quitWindow)
            self.buttonSave.clicked.connect(self.save_new_infos_patient)
            self.buttonHistory.clicked.connect(self.change_window_history)
            self.textDoctor.textChanged.connect(self.search_medics)

        def save_new_infos_patient(self):
            nom = self.lineNom.text()
            prenom = self.linePrenom.text()
            age = self.lineAge.text()
            if self.rbtnM.isChecked():
                sexe = "M"
            else:
                sexe = "F"

            symptoms = self.textDoctor.toPlainText()
            medics = self.textMedicament.toPlainText()

            self.myCtrl.save_new_infos_patient(nom, prenom, age, sexe, symptoms, medics)
            self.textDoctor.setPlainText("")
            self.textMedicament.setPlainText("")

        def search_medics(self):
            if " " in self.textDoctor.toPlainText():
                datas = self.textDoctor.toPlainText().split(" ")
                self.myCtrl.search_medics(datas, self.textMedicament)

        @pyqtSlot()
        def change_window_history(self):
            nom = self.lineNom.text()
            prenom = self.linePrenom.text()
            age = self.lineAge.text()
            if self.rbtnM.isChecked():
                sexe = "M"
            else:
                sexe = "F"
            file_name = (nom.upper() + "_" + prenom.lower() + "_" + age + "_" + sexe + ".json")
            # We send the file name to open the history window of the patient
            self.cams = HistoryWindow.HistoryView(file_name)
            self.close()

        @pyqtSlot()
        def quitWindow(self):
            self.cams = MainWindow.MainView()
            self.close()

    class FolderController():
        def __init__(self):
            self.myModel = FolderWindow.FolderModel()

        def save_new_infos_patient(self, nom, prenom, age, sexe, symptoms, medics):
            self.myModel.save_new_infos_patient(nom, prenom, age, sexe, symptoms, medics)

        # We search between the words entered by the doctor
        # if we find a word we display all the medicaments that belong to the word
        def search_medics(self, datas, inputs):
            for terms in datas:
                for key, medicament in self.myModel.medics.items():
                    if terms == key: # if the word entered by the doctor and a word in the list are equal
                        for medic in medicament:
                            sentence = ("Pour " + terms + " prendre " + medic)
                            try:
                                inputs.toPlainText().index(sentence) # Check if the sentence is not already written
                            except ValueError: # if not we append the sentence in the right part text area
                                inputs.appendPlainText(sentence)


        # Trigger an event when the user clicked on close
        def closeWindow(self):
            self.myModel.closeWindow()

    class FolderModel():
        def __init__(self):
            self.medics = {
                'antalgique': {'Doliprane', 'Dafalgan', 'Efferalgan'},
                'douleur': {'Doliprane', 'Dafalgan', 'Efferalgan'},
                'paracétamol': {'Doliprane', 'Dafalgan', 'Efferalgan'},
                'fièvre': {'Doliprane', 'Dafalgan', 'Efferalgan'},
                'anti-agrégant': {'Kardegic'},
                'avc': {'Kardegic'},
                'cardiaque': {'Kardegic'},
                'coeur': {'Kardegic'},
                'cerveau': {'Kardegic'},
                'intestin': {'Spasfon', 'MeteoSpasmyl'},
                'digestif': {'Spasfon', 'MeteoSpasmyl'},
                'biliaires': {'Spasfon', 'MeteoSpasmyl'},
                'estomac': {'Gaviscon'},
                'indigestion': {'Gaviscon'},
                'creme': {'Dexeryl'},
                'irritation': {'Dexeryl'},
                'cutannées': {'Dexeryl'},
                'antiseptique': {'Biseptine'},
                'plaies': {'Biseptine'},
                'lesions': {'Biseptine'},
                'bouche': {'Eludril'},
                'dents': {'Eludril'},
                'gencives': {'Eludril'}
            }

        # Save the patients infos in a Json file named like "DOE_John_99_M.json"
        def save_new_infos_patient(self, nom, prenom, age, sexe, symptoms, medics):
            ssh = Ssh()
            # Create json datas
            if nom != "" and prenom != "" and age != "": # if all the value are fulfilled
                if symptoms != '': # if the patient have symptoms we write in his folder
                    data = {
                        'nom': nom,
                        'prenom': prenom,
                        'age': age,
                        'sexe': sexe,
                        'history': [
                            {'symptoms': symptoms,'medics': medics}
                        ]
                    }
                else:
                    data = {
                        'nom': nom,
                        'prenom': prenom,
                        'age': age,
                        'sexe': sexe,
                        'history': [
                        ]
                    }

                json_string = json.dumps(data) # Dump the python dict into a json object
                file_name = (nom.upper() + "_" + prenom.lower() + "_" + age + "_" + sexe + ".json")

                if ssh.is_sftp_dir_exists(ssh.folderPath + file_name):  # we checked if the patient folder exist
                    if symptoms != "":  # we checked if the doctor write symptoms to append it to the patient folder
                        ssh.add_new_history(file_name, symptoms, medics)
                else: # else we just create the patient folder
                    ssh.send_file(file_name, json_string)

            # close the connection
            ssh.closing()

        def closeWindow(self):
            print()


################################################################
# The history window displays :
# - 3 informations about the patient (that can be modified) :
# - - Nom
# - - Prenom
# - - Age
# - 1 buttons :
# - - Close button to return to the folder window
# - 1 text area :
# - - The text area display the precedent symptoms and recommanded medics of the patient (if the patient have a folder)
################################################################
class HistoryWindow:
    class HistoryView(QWidget):
        def __init__(self, file_name):
            super().__init__()

            self.myCtrl = HistoryWindow.HistoryController(file_name)
            self.datas = self.myCtrl.datas # Check and get patient informations

            # 1.1 Infos about the patient
            self.labelNom = QLabel(self)
            self.labelNom.setText('Nom :')
            self.lineNom = QLineEdit(self)
            self.lineNom.setReadOnly(True)

            self.labelPrenom = QLabel(self)
            self.labelPrenom.setText('Prenom :')
            self.linePrenom = QLineEdit(self)
            self.linePrenom.setReadOnly(True)

            self.labelAge = QLabel(self)
            self.labelAge.setText('Age :')
            self.lineAge = QLineEdit(self)
            self.lineAge.setValidator(QIntValidator(0, 200))
            self.lineAge.setReadOnly(True)

            self.lineSexe = QLineEdit(self)
            self.lineSexe.hide()

            # 2.2
            self.textHistory = QPlainTextEdit(self)
            self.textHistory.setReadOnly(True)
            self.textHistory.setStyleSheet("background-color: grey; color: white;")

            # 3.1
            self.setToolTip('Tooltip for <b>QWidget</b>')
            self.buttonSave = QPushButton('Sauvegarder')
            self.buttonSave.setToolTip('Save <b>Le fichier</b>')

            # 3.2
            self.buttonClose = QPushButton('Fermer')
            self.buttonClose.setToolTip('Revenir <b>menu principal</b>')

            # if the patient exists we display his history
            if self.datas is not None:
                self.lineNom.setText(self.datas['nom'])
                self.linePrenom.setText(self.datas['prenom'])
                self.lineAge.setText(self.datas['age'])
                self.lineSexe.setText(self.datas['sexe'])
                for i in range(len(self.datas['history'])):
                    self.textHistory.appendPlainText(
                        "Symptoms : " + self.datas['history'][i]['symptoms'] + " | " + "Medics : " +
                        self.datas['history'][i]['medics'])

            self.init_ui()
            self.show()

        # Definition of the box
        def init_ui(self):

            # Top left box #1
            # Box Nom
            h_box_nom = QHBoxLayout()
            h_box_nom.addWidget(self.labelNom)
            h_box_nom.addWidget(self.lineNom)

            # Box Prenom
            h_box_prenom = QHBoxLayout()
            h_box_prenom.addWidget(self.labelPrenom)
            h_box_prenom.addWidget(self.linePrenom)

            # Box Age
            h_box_age = QHBoxLayout()
            h_box_age.addWidget(self.labelAge)
            h_box_age.addWidget(self.lineAge)

            # Top right box
            # 2
            h_box_btn_history = QHBoxLayout()
            # h_box_btn_history.addWidget()

            # Top left
            v_box_top_left = QVBoxLayout()
            v_box_top_left.addLayout(h_box_nom)
            v_box_top_left.addLayout(h_box_prenom)
            v_box_top_left.addLayout(h_box_age)

            h_box_top_right = QHBoxLayout()
            h_box_top_right.addLayout(h_box_btn_history)

            # Top box
            h_box_top = QHBoxLayout()
            h_box_top.addLayout(v_box_top_left)
            h_box_top.addLayout(h_box_top_right)

            # Mid box
            h_box_mid = QHBoxLayout()
            h_box_mid.addWidget(self.textHistory)

            # Box Bottom
            h_box_button = QHBoxLayout()
            h_box_button.addWidget(self.buttonClose)

            # Order the different boxs in the view
            v_box = QVBoxLayout()
            v_box.addLayout(h_box_top)
            v_box.addLayout(h_box_mid)
            v_box.addLayout(h_box_button)

            self.setLayout(v_box)
            self.setWindowTitle('Historigramme')

            # Add the functionality to the buttons
            self.buttonClose.clicked.connect(self.changeMainWindow)

        @pyqtSlot()
        def changeMainWindow(self):
            nom = self.lineNom.text()
            prenom = self.linePrenom.text()
            age = self.lineAge.text()
            sexe = self.lineSexe.text()

            file_name = (nom.upper() + "_" + prenom.lower() + "_" + age + "_" + sexe + ".json")
            # We open the folder window of the current patient with the file_name
            self.cams = FolderWindow.FolderView(file_name)
            self.close()

    class HistoryController():
        def __init__(self, file_name):
            self.file_name = file_name
            self.myModel = HistoryWindow.HistoryModel(file_name)
            self.datas = self.myModel.get_infos()

        def closeWindow(self):
            self.myModel.closeWindow()

    class HistoryModel():
        def __init__(self, file_name):  # ,ssh):
            self.ssh = Ssh()
            self.file_name = (file_name)

        # Check if the patient exist and if he exists the model returns the datas of the patient
        def get_infos(self):
            exist = self.ssh.is_sftp_dir_exists(self.ssh.folderPath + self.file_name)
            if exist:
                datas = self.ssh.get_infos_history(self.file_name)
                return datas

        def closeWindow(self):
            print()

################################################################
# The history window displays :
# - 3 informations about the patient (that can be modified) :
# - - Nom
# - - Prenom
# - - Age
# - 1 buttons :
# - - Close button to return to the folder window
# - 1 text area :
# - - The text area display the precedent symptoms and recommanded medics of the patient (if the patient have a folder)
################################################################
class ListPatientWindow():
    class ListPatientView(QWidget):
        def __init__(self):
            super().__init__()

            self.myCtrl = ListPatientWindow.ListPatientController()

            self.list_patient = QListWidget()

            self.buttonClose = QPushButton('Fermer')
            self.buttonClose.setToolTip('<b>Revenir menu principal</b>')

            self.init_ui()
            self.show()

        # Definition of the box
        def init_ui(self):
            # Top right box
            h_box_btn_history = QHBoxLayout()

            h_box_top_right = QHBoxLayout()
            h_box_top_right.addLayout(h_box_btn_history)

            # Top box
            h_box_top = QHBoxLayout()
            h_box_top.addLayout(h_box_top_right)

            # Mid box
            h_box_mid = QHBoxLayout()
            h_box_mid.addWidget(self.list_patient)

            # Box Bottom
            h_box_button = QHBoxLayout()
            h_box_button.addWidget(self.buttonClose)

            # Order the different boxs in the view
            v_box = QVBoxLayout()
            v_box.addLayout(h_box_top)
            v_box.addLayout(h_box_mid)
            v_box.addLayout(h_box_button)

            for patient in self.myCtrl.datas:
                self.list_patient.addItem(patient)

            self.setLayout(v_box)
            self.setWindowTitle('List patient')

            # Add the functionality to the buttons
            self.list_patient.doubleClicked.connect(self.open_patient_folder)
            self.buttonClose.clicked.connect(self.changeMainWindow)

        @pyqtSlot()
        def open_patient_folder(self):
            item = self.list_patient.currentItem()
            # Transfer the file name to open the patient folder
            self.cams = FolderWindow.FolderView(item.text())
            self.close()

        @pyqtSlot()
        def changeMainWindow(self):
            self.cams = MainWindow.MainView()
            self.close()

    class ListPatientController():
        def __init__(self):
            self.myModel = ListPatientWindow.ListPatientModel()
            self.datas = self.myModel.get_list_patient()

        # Trigger an event when the user clicked on close
        def closeWindow(self):
            self.myModel.closeWindow()

    class ListPatientModel():
        def __init__(self):  # ,ssh):
            self.ssh = Ssh()

        def get_list_patient(self):
            return self.ssh.get_list_patient()

        # Close the SSH connection and delete the local file
        def closeWindow(self):
            print('close')


# This class initialize the SSH connexion and the functions
class Ssh:
    client = None

    # Initialize the SSH and SFTP connexion
    def __init__(self):
        try:
            print("Connecting to server.")
            # Connexion to the VM
            hostname = "X"
            username = "X"
            password = "X"
            port = 22
            self.folderPath = "/home/student/patient/"

            self.client = client.SSHClient()
            self.client.set_missing_host_key_policy(client.AutoAddPolicy())
            self.client.connect(hostname, port=port, username=username,
                                password=password)
            # Open the sftp client
            self.sftp = self.client.open_sftp()
            self.create_sftp_dir()
        except:
            print("Exception raised in SSH!")
            raise Exception("La connexion à la VM a échoué")

    # Return true if he find a file or directory pass in parameters in the VM
    def is_sftp_dir_exists(self, folderPath):
        try:
            self.sftp.stat(folderPath)
            return True
        except Exception:
            return False

    # Create the folder patient
    def create_sftp_dir(self):
        try:
            self.sftp.mkdir(self.folderPath)
        except IOError as exc:
            if not self.is_sftp_dir_exists(self.folderPath):
                raise exc

    # Send the patient json file in the VM
    def send_file(self, file_name, data):
        with self.sftp.open((self.folderPath + file_name), 'w') as outfile:
            json.dump(data, outfile)

    def add_new_history(self, file_name, symptoms, medics):
        file = self.sftp.open((self.folderPath + file_name))  # Get the file
        data = json.load(file)  # Turn the file data into a string
        datas = json.loads(data)  # Convert the string in json
        file.close()
        datas['history'].append({'symptoms': symptoms, 'medics': medics})
        json_string = json.dumps(datas)
        with self.sftp.open((self.folderPath + file_name), 'w') as outfile:
            json.dump(json_string, outfile)

    def get_infos_history(self, file_name):
        file = self.sftp.open((self.folderPath + file_name))  # Get the file
        data = json.load(file)  # Turn the file data into a string
        datas = json.loads(data)  # Convert the string in json
        file.close()
        return datas

    def get_list_patient(self):
        return self.sftp.listdir(self.folderPath)

    # Close the sftp and ssh connexion
    def closing(self):
        self.client.close()


print(__name__)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = MainWindow.MainModel()  # ssh)
    ctrl = MainWindow.MainController()  # model)
    view = MainWindow.MainView()  # ctrl)
    sys.exit(app.exec_())
