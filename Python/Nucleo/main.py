from PrincipalWindow import *

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon("Imagenes/Icono_Programa2.png"))

	window = PWindow()
	window.setWindowTitle("Creador de grafos y rutas")

	window.show()
	sys.exit(app.exec_())