from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QPicture
from Intermediary import Intermediary
from PyQt5.QtCore import Qt, QTimer

class MainFormController(QWidget):

    def __init__(self, ui, figs, axis: tuple):
        super().__init__()
        
        self._ui = ui
        self._ui.setupUi(self)
        self.figs = figs
        self.axis = axis

        self._ui.sheet.setStyleSheet('background-color:white;')
        self._ui.sheet.paintEvent = self.fakePaintEvent

        self.color_mask_flag = True

        self._ui.button_steps.clicked.connect(self.buttonClicked_steps)
        self._ui.button_colors.clicked.connect(self.buttonClicked_colors)
        self._ui.button_z.clicked.connect(self.buttonClicked_z_mask)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.setInterval(100)

    
    def timerEvent(self):
        try:
            self.z_mask, self.color_mask = next(self.prerender)
            self.color_mask_flag = not self.color_mask_flag
            self._ui.sheet.update()
            self._ui.label_animation.setText(str(self.color_mask_flag))
        except StopIteration:
            self._ui.label_animation.setText('the end')
            self._ui.sheet.paintEvent = self.fakePaintEvent
            self.timer.stop()
            self.animationFrame = None

    def buttonClicked_colors(self) :
        self.color_mask_flag = True
        self._ui.sheet.update()

    def buttonClicked_z_mask(self) :
        self.color_mask_flag = False
        self._ui.sheet.update()

    def buttonClicked_steps(self) :
        try: 
            self.timer.start()

            self.prerender = Intermediary.prerender_all(self.figs, self._ui.sheet)
            self._ui.sheet.paintEvent = self.fakePaintEvent2
            self.color_mask_flag = True
            self._ui.label_animation.setText('ok go')
        except Exception as ex:
            print(ex)

    def fakePaintEvent2(self, e):
        if self.color_mask_flag:
            Intermediary.draw_color_mask(self.color_mask, self._ui.sheet)
        else:
            Intermediary.draw_z_mask(self.z_mask, self._ui.sheet)

    def fakePaintEvent(self, e):
    
        if self.color_mask_flag:
            Intermediary.render_all_colors(self.figs, self._ui.sheet)
        else:
            Intermediary.render_all_z_mask(self.figs, self._ui.sheet)