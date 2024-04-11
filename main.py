from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from qdarktheme import setup_theme
from backEnd import BackEnd
from qrcode import QRCode
from webbrowser import open_new_tab as on

class GQR:
    def __init__(self, App: QApplication):
        self.back = BackEnd()
        setup_theme('dark')
        self.loginWin = loadUi('src/ui/login.ui')
        self.mainWin = loadUi('src/ui/main.ui')
        
        self.loginWin.show()

        self.mainWin.btn_gerar.clicked.connect(
            lambda: self.gerar(
                self.mainWin.entry_cr.text(),
                self.mainWin.igualORlike.currentText(),
                self.mainWin.op_nivel.currentText(),
                self.mainWin.op_nivel2.currentText(),
                self.mainWin.op_empresas.currentText(),
                self.mainWin.op_tipos.currentText()
            )
        )

        self.loginWin.btn_login.clicked.connect(
            lambda: self.realizar_login(
                self.loginWin.entry_user.text(),
                self.loginWin.entry_senha.text(),
                )
            )
        
        self.loginWin.btn_ajuda.clicked.connect(self.abrir_gitHub)

        App.exec()

    def abrir_gitHub(self):
        on('https://github.com/foxtec198/Desktop_GQR/issues/new')

    def msg(self, win, message, tipo = 0, titulo = 'Gerador QR'):
        match tipo:
            case 0: QMessageBox.information(win, titulo, message)
            case 1: QMessageBox.about(win, titulo, message)
            case 2: QMessageBox.warning(win, titulo, message)

    def realizar_login(self, uid, pwd):
        self.msg(self.loginWin, 'Logando...')
        login = self.back.connect_db(uid, pwd)
        self.qr = QRCode(uid, pwd)
        if login == 'Conectado':
            self.mainWin.show()
            self.loginWin.close()
            self.msg(self.mainWin, f'{login}, Seja bem-vindo', 1)
        else: self.msg(self.loginWin, 'Login Incorreto', 2)

    def gerar(self, cr, op_cr, nivel, op_nivel, op_empresas, tipos):
        if cr and op_cr and nivel and op_nivel and op_empresas:
            if op_nivel == '0 - CR': nv = 3
            else: nv = int(op_nivel) + 3
            self.msg(self.mainWin, 'Gerando...')
            self.qr.gerar(cr, op_cr, nivel, nv, op_empresas, tipos)
            self.msg(self.mainWin, f'QRCodes Gerados! - {self.qr.nomeCR}', 1)
            path = self.qr.definir_cor(self.qr.nomeCR)
            img = QPixmap(path)
            self.mainWin.img_molde.setPixmap(img)
        else: self.msg(self.mainWin, 'Dados Invalidos, Confira')

if __name__ == '__main__':
    GQR(QApplication([]))