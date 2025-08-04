from PyQt5 import uic, QtWidgets
import mysql.connector

conexao= mysql.connector.connect(

    host = '127.0.0.1',
    user = 'dev',
    password = '1234',
    database = 'cadastros_credito'
)

def inserir_dados():
    nome = cadastro.txtNome.text()
    cpf = cadastro.txtCpf.text()
    idade = cadastro.txtIdade.text()
    renda = cadastro.txtRenda.text()
    situacao = cadastro.txtSituacao.text()

    cursor = conexao.cursor()
    comando_SQL = 'insert into clientes (nome,cpf,idade,renda,situacao) values (%s,%s,%s,%s,%s)'
    dados = (str(nome), str(cpf), str(idade), str(renda), str(situacao))
    cursor.execute(comando_SQL, dados)

    conexao.commit()

    cadastro.txtNome.setText('')
    cadastro.txtCpf.setText('')
    cadastro.txtIdade.setText('')
    cadastro.txtRenda.setText('')
    cadastro.txtSituacao.setText('')
    cadastro.lblAnalise.setText('Clique no Botão Analisar Crédito')


def analise():
    renda = cadastro.txtRenda.text()
    renda = float(renda)
    idade = cadastro.txtIdade.text()
    idade = int(idade)

    if renda>=3500 and idade >=21:
        cadastro.lblAnalise.setText('Cadastro foi pré-aprovado!')
    else:
        cadastro.lblAnalise.setText('Cadastro não foi pré-aprovado!')

def relatorio():
    relatorio.show()


    cursor = conexao.cursor()
    comando_SQL = 'select * from clientes'
    cursor.execute(comando_SQL)
    leitura_clientes = cursor.fetchall()

    relatorio.tableClientes.setRowCount(len(leitura_clientes))
    relatorio.tableClientes.setColumnCount(6)

    for i in range (0, len(leitura_clientes)):
        for j in range(0, 6):
            relatorio.tableClientes.setItem(i,j, QtWidgets.QTableWidgetItem(str(leitura_clientes[i][j])))


def editar_dados():
    dados = relatorio.tableClientes.currentRow()
    cursor = conexao.cursor()
    cursor.execute('select id from clientes')
    leitura_clientes = cursor.fetchall()
    id_ativo = leitura_clientes [dados] [0]
    cursor.execute('select * from clientes where id= '+str(id_ativo))
    leitura_clientes = cursor.fetchall()

    editar.show()


app=QtWidgets.QApplication([])
cadastro=uic.loadUi('cadastro.ui')
cadastro.btnSalvar.clicked.connect(inserir_dados)
cadastro.btnAnalise.clicked.connect(analise)
cadastro.btnRelatorio.clicked.connect(relatorio)


relatorio=uic.loadUi('relatorio.ui')
relatorio.btnEditar.clicked.connect(editar_dados)

editar=uic.loadUi('editar.ui')

cadastro.show()
app.exec()