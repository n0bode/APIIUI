#Janela Principal

from PyQt5.QtWidgets import (QWidget, QFrame, QDockWidget, 
							QWidget, QHBoxLayout, QVBoxLayout,
							QToolBar, QLabel, QStackedWidget,
							QPushButton, QButtonGroup)
from PyQt5.Qt import Qt, QSizePolicy
from view.productsscreen import ProductsScreen
from view.salesscreen import SaleScreen
from view.customersscreen import CustomersScreen
from view.categoriesscreen import CategoriesScreen
import loader
import translator

class MainWindow(QWidget):
	def __init__(self, *args):
		super(MainWindow, self).__init__(*args)
		#Muda o Titulo da Janela
		self.setWindowTitle("Finanças")
		#Criar um limitador de tamanho da tela
		self.setMinimumSize(1000, 500)
		#Seta o icon da janela
		self.setWindowIcon(loader.loadIcon("icon_app.png"))
		self._initUI()

	def _initUI(self):
		#Criando a uma Box Horizontal para Criar o NavBar e TopBar
		self.setLayout(QHBoxLayout())
		self.layout().setAlignment(Qt.AlignLeft)
		self.layout().setContentsMargins(0, 0, 0, 0)
		self.layout().setSpacing(0)

		navbar = self._createNavBar()
		central = self._createCentral()
		self.layout().addWidget(navbar)
		self.layout().addLayout(central)

	def _createNavBar(self):
		navbar = QFrame()
		navbar.setFixedWidth(200)
		navbar.setSizePolicy(QSizePolicy(0, 1))
		navbar.setLayout(QVBoxLayout())
		navbar.layout().setContentsMargins(0, 0, 0, 0)
		navbar.layout().setAlignment(Qt.AlignTop)
		navbar.setObjectName("navbar")
		navbar.layout().setSpacing(0)

		logo = self._createNavButton("Finanças", "icon_app.png")
		logo.setObjectName("logo")
		logo.setFixedHeight(50)
		navbar.layout().addWidget(logo)

		#Criando os Botoes da navbar
		#Botao Vendas
		self.sellsBtn = self._createNavButton("Vendas", "sales.png")
		self.sellsBtn.setChecked(True)

		#Botao Produto
		self.productBtn = self._createNavButton("Produtos", "products.png")
		
		#Botao Clients
		self.clientBtn = self._createNavButton("Clientes", "clientes.png")

		#Botao Categoria
		self.tagBtn = self._createNavButton("Categorias", "category.png")

		#GroupButton para criar uma exclusão entre os botoes
		#Para que não fique selecionado dois de uma vez
		group = QButtonGroup(self)
		group.setExclusive(True)
		group.addButton(self.sellsBtn)
		group.addButton(self.productBtn)
		group.addButton(self.clientBtn)
		group.addButton(self.tagBtn)

		#Adicionando os botoes à Layout da NavBar
		navbar.layout().addWidget(self.sellsBtn)
		navbar.layout().addWidget(self.productBtn)
		navbar.layout().addWidget(self.clientBtn)
		navbar.layout().addWidget(self.tagBtn)
		return navbar

	#Funcao pra criar os botoes da NavBar
	def _createNavButton(self, title, icon=""):
		button = loader.buttonIcon(icon, 20, 20)
		button.setText(title)
		button.setFixedHeight(40)
		button.setFlat(True)
		button.setCheckable(True)
		return button

	#Criar o TopBar
	#Barra de cima
	def _createTopBar(self):
		topbar = QFrame()
		topbar.setFixedHeight(50)
		topbar.setLayout(QHBoxLayout())
		topbar.setContentsMargins(10, 0, 0, 0)
		topbar.setSizePolicy(QSizePolicy(1, 0))
		topbar.setObjectName("topbar")

		self.titleText = QLabel("Produtos")
		topbar.layout().addWidget(self.titleText)
		return topbar

	#Criar o espaço onde as "Screens" vao aparecer
	def _createCentral(self):
		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		topbar = self._createTopBar()
		self.stack = self._createStackLayout()

		layout.addWidget(topbar)
		layout.addWidget(self.stack)
		return layout

	#StackLayout é a responsavel por mudar as telas
	def _createStackLayout(self):
		stack = QStackedWidget()
		stack.setContentsMargins(5, 5, 5, 5)

		#Aqui criar as telas
		"""stack.addWidget(ProductsScreen())
		stack.addWidget(SalesScreen())
		stack.addWidget(ClientsScreen())
		stack.addWidget(CategoriesScreen())"""
		return stack