from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from form.mainForm import Ui_Dialog
from MainFormController import MainFormController
from Intermediary import Intermediary
from MatrixShop import kabinetProject
from Model import Model
import numpy as np
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui = Ui_Dialog()
    colors = [Qt.darkCyan, Qt.darkBlue, Qt.yellow, Qt.red, Qt.green, Qt.blue]
    models_name = ['obj3','obj2','obj1', 'obj4']

    figures = []

    project_matrix = kabinetProject()
    model_matrix = np.identity(4)
    for obj_name, color in zip(models_name, colors):
        model = Model().init_with_file(obj_name)
        figures.append(Intermediary(model, project_matrix, model_matrix, color))
        
    axX = Intermediary(Model().init_with_file('x'), np.copy(project_matrix), np.copy(model_matrix), Qt.red)
    axY = Intermediary(Model().init_with_file('y'), np.copy(project_matrix), np.copy(model_matrix), Qt.blue)
    axZ = Intermediary(Model().init_with_file('z'), np.copy(project_matrix), np.copy(model_matrix), Qt.green)

    form = MainFormController(ui, figures, (axX, axY, axZ))
    form.show()

    sys.exit(app.exec_())
