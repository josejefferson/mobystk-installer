import os
import datetime
import shutil
import subprocess
import zipfile

STEPS = 7
token = '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'
user = 'josejefferson'
repository = 'joystick'
zipURL = f'https://api.github.com/repos/{user}/{repository}/zipball/master'
headers = {'Authorization': 'token ' + token if token else None}
downloadedZIPName = 'mobystk.zip'
updateFolderName = f'{user}-{repository}-'
internalFolder = '.update'
lastUpdateFile = f'{internalFolder}/lastUpdate.txt'

terminalSize = os.get_terminal_size()
terminalWidth = terminalSize[0]
terminalHeight = terminalSize[1]

logo = """
   ▄▄▄▄███▄▄▄▄    ▄██████▄  ▀█████████▄  ▄██   ▄      ▄████████     ███        ▄█   ▄█▄ 
 ▄██▀▀▀███▀▀▀██▄ ███    ███   ███    ███ ███   ██▄   ███    ███ ▀█████████▄   ███ ▄███▀ 
 ███   ███   ███ ███    ███   ███    ███ ███▄▄▄███   ███    █▀     ▀███▀▀██   ███▐██▀   
 ███   ███   ███ ███    ███  ▄███▄▄▄██▀  ▀▀▀▀▀▀███   ███            ███   ▀  ▄█████▀    
 ███   ███   ███ ███    ███ ▀▀███▀▀▀██▄  ▄██   ███ ▀███████████     ███     ▀▀█████▄    
 ███   ███   ███ ███    ███   ███    ██▄ ███   ███          ███     ███       ███▐██▄   
 ███   ███   ███ ███    ███   ███    ███ ███   ███    ▄█    ███     ███       ███ ▀███▄ 
  ▀█   ███   █▀   ▀██████▀  ▄█████████▀   ▀█████▀   ▄████████▀     ▄████▀     ███   ▀█▀ 
                                                                              ▀         
""".strip('\n')

asciiDigits = [
	' ██████ \n██  ████\n██ ██ ██\n████  ██\n ██████ ', # 0
	' ██\n███\n ██\n ██\n ██',                          # 1
	'██████ \n     ██\n █████ \n██     \n███████',      # 2
	'██████ \n     ██\n █████ \n     ██\n██████ ',      # 3
	'██   ██\n██   ██\n███████\n     ██\n     ██',      # 4
	'███████\n██     \n███████\n     ██\n███████',      # 5
	' ██████ \n██      \n███████ \n██    ██\n ██████ ', # 6
	'███████\n     ██\n    ██ \n   ██  \n   ██  ',      # 7
	' █████ \n██   ██\n █████ \n██   ██\n █████ ',      # 8
	' █████ \n██   ██\n ██████\n     ██\n █████ ',      # 9
	'██  ██\n   ██ \n  ██  \n ██   \n██  ██',           # %
	'        \n        \n ██████ \n        \n        '  # -
]


# Limpa o console
def clearConsole():
	command = 'clear'
	if os.name in ('nt', 'dos'):
		command = 'cls'
	os.system(command)


# Retorna uma porcentagem em ASCII Art
def getPercentageAscii(percentage):
	if percentage < 0:
		percentage = [-1]
	else:
		percentage = str(percentage)

	text = ''
	digits = []
	for digit in percentage:
		digits.append(asciiDigits[int(digit)].strip('\n').split('\n'))

	for line in range(5):
		for digit in digits:
			text += digit[line] + ' '
		text += asciiDigits[10].strip('\n').split('\n')[line]
		text += '\n'

	return text


# Mostra o processo no console
def printStep(step, tip = '', status = None):
	text = ''
	lines = logo.split('\n')
	if terminalWidth < len(max(lines, key=len)):
		lines = list(map(lambda l: l[0:terminalWidth], lines))
	lines = list(map(lambda l: l.center(terminalWidth).rstrip(), lines))
	text += '\n'
	for l in lines: text += l + '\n'

	text += '\n'
	stepText = step if step > -1 else '-'
	if status:
		text += status.center(terminalWidth).rstrip() + '\n'
	else:
		text += f'Instalando ({stepText}/{STEPS})'.center(terminalWidth).rstrip() + '\n'
	text += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'.center(terminalWidth).rstrip() + '\n\n'

	percentage = int(step / STEPS * 100)
	percentageAscii = getPercentageAscii(percentage).split('\n')
	for line in percentageAscii:
		text += line.center(terminalWidth).rstrip() + '\n'
	text += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'.center(terminalWidth).rstrip() + '\n'
	for line in tip.split('\n'):
		text += line.center(terminalWidth).rstrip() + '\n'

	clearConsole()
	print(text)


# Cria a pasta do MobyStk
def createFolder():
	printStep(0, 'Verificando e criando pasta do MobyStk')
	try:
		if os.path.exists('./MobyStk/'):
			printStep(-1, 'Remova a pasta "MobyStk" depois abra novamente o instalador para prosseguir', 'ERRO: Instalação antiga detectada')
			return input()
		os.mkdir('./MobyStk')
		os.chdir('./MobyStk')
	except Exception as err:
		printStep(-1, str(err), 'ERRO: Ocorreu um erro ao criar pasta do MobyStk')
		input()
		quit()


# Instala os módulos pelo PIP
def installModules():
	printStep(2, 'Instalando módulos')
	input('Pressione ENTER para prosseguir...') #temp
	try:
		commands = [
			'python -m pip install colorama',
			'python -m pip install prompt_toolkit',
			'python -m pip install pynput',
			'python -m pip install pyqrcode',
			'python -m pip install requests',
			'python -m pip install SimpleWebSocketServer'
		]
		for c in commands: subprocess.check_output(c.replace('python -m', f'"{sys.executable}" -m'))
	except Exception as err:
		printStep(-1, str(err), 'ERRO: Falha na instalação dos módulos')


# Importa os módulos
def importModules(showError = False):
	try:
		global requests
		import requests
		return True
	except:
		if not showError: return False
		printStep(-1, 'Tente reiniciar o instalador', 'ERRO: Falha na importação dos módulos')
		input()
		quit()


# Verifica e corrige módulos
def verifyAndFixModules():
	printStep(1, 'Verificando módulos instalados')
	modulesImported = importModules()
	if not modulesImported:
		installModules()
		importModules(True)


# Baixa o MobyStk
def download():
	printStep(3, 'Baixando o MobyStk')
	try:
		response = requests.get(zipURL, headers=headers)
		if response.status_code != 200: raise BadStatusCode(response)
		with open(downloadedZIPName, 'wb') as file:
			file.write(response.content)
	except Exception as err:
		printStep(-1, str(err), 'ERRO: Falha ao baixar o MobyStk')
		input()
		quit()


# Extrair o arquivo ZIP
def extract():
	printStep(4, 'Extraindo arquivos')
	try:
		with zipfile.ZipFile(downloadedZIPName, 'r') as file:
			file.extractall()
		dirList = os.listdir('.')
		extractFolderName = [d for d in dirList if d.startswith(updateFolderName)][0]
		return extractFolderName
	except Exception as err:
		printStep(-1, str(err), 'ERRO: Falha ao extrair arquivos')
		input()
		quit()


# Copia os arquivos extraídos para a pasta
def copyFiles(extractFolderName):
	printStep(5, 'Copiando arquivos')
	try:
		for item in os.listdir(extractFolderName):
			srcPath = os.path.join(extractFolderName, item)
			destPath = os.path.join('.', item)
			if os.path.isdir(srcPath):
				shutil.copytree(srcPath, destPath)
			else:
				shutil.copy2(srcPath, destPath)
	except Exception as err:
		printStep(-1, str(err), 'ERRO: Falha ao copiar os arquivos')
		input()
		quit()


def cleanAndFinalize(extractFolderName):
	printStep(6, 'Finalizando')
	try:
		shutil.rmtree(extractFolderName)
		if os.path.exists(downloadedZIPName):
		  os.remove(downloadedZIPName)
		if not os.path.exists('.update'):
			os.makedirs('.update')
		with open(lastUpdateFile, 'w') as file:
			file.write(datetime.datetime.now().isoformat())
	except Exception as err:
		printStep(-1, str(err), 'ERRO: Falha ao finalizar')
		input()
		quit()


# INÍCIO!!!	
verifyAndFixModules()
createFolder()
download()
extractFolderName = extract()
copyFiles(extractFolderName)
cleanAndFinalize(extractFolderName)

printStep(7, 'O MobyStk foi instalado com sucesso!', 'Instalação finalizada')
# ainda falta os atalhos!

# TODOS:
# Verificar módulos
# Verificar se não há uma instalação existente
# Instalar módulos se necessário
# Criar e entrar na pasta ./mobystk/
# Baixar mobystk.zip
# Extrair
# Escrever arquivo .lastUpdate.txt
# Instalar atalho se Windows
# Abrir atalho na pasta ./mobystk/MobyStk.lnk se Windows