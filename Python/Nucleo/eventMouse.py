from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*

class hoverButton(QPushButton):
    def __init__(self, parent=None,objectLabel=None):
        QPushButton.__init__(self, parent)
        self.objectLabel = objectLabel
        self.cssLeaveEvent = """
			background-color:darkgreen;
			color:white;
			font-size: 150;
			border-style: none;
			border-radius: 7;
			padding: 5px;
			padding-left: 7px;
			padding-right: 30px;
			border-color: black;
			border-width: 2px;
			font-family:Georgia;
            """
        
        self.cssEnterEvent = """
            background-color:darkred
            """
        
        self.setMouseTracking(True)
        self.fuente = self.font()

        self.posicionX = int
        self.posicionY = int

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        self.posicionY = self.pos().y()
        self.setStyleSheet(self.cssEnterEvent)
        #self.objectLabel.setVisible(False)

        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX, self.posicionY, 200, 68))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)
        self.setFixedSize(215,67)
        self.fuente.setPointSize(11)
        self.setFont(self.fuente)

    def leaveEvent(self, event):
        self.fuente.setPointSize(10)
        #self.objectLabel.setVisible(True)
        self.setFont(self.fuente)
        self.setStyleSheet(self.cssLeaveEvent)
        #self.setGeometry(120,580,212,60)
        self.setFixedSize(210,60)
        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 200, 68))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)

