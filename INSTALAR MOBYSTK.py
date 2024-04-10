import os
import datetime
import importlib.util
import shutil
import subprocess
from sys import executable
import zipfile

token = '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'
user = 'josejefferson'
repository = 'mobystk'
zipURL = f'https://api.github.com/repos/{user}/{repository}/zipball/main'
headers = {'Authorization': 'token ' + token if token else None}
downloadedZIPName = 'mobystk.zip'
updateFolderName = f'{user}-{repository}-'
internalFolder = '.update'
lastUpdateFile = f'{internalFolder}/lastUpdate.txt'

# Módulos necessários para a utilização do MobyStk
modules = [
	'colorama',
	'prompt_toolkit',
	'pynput',
	'pyqrcode',
	'requests',
	'SimpleWebSocketServer'
]

steps = 9 if os.name == 'nt' else 8
currentStep = None
terminalSize = os.get_terminal_size()
terminalWidth = terminalSize[0]
terminalHeight = terminalSize[1]

logos = ["""
   ▄▄▄▄███▄▄▄▄    ▄██████▄  ▀█████████▄  ▄██   ▄      ▄████████     ███        ▄█   ▄█▄ 
 ▄██▀▀▀███▀▀▀██▄ ███    ███   ███    ███ ███   ██▄   ███    ███ ▀█████████▄   ███ ▄███▀ 
 ███   ███   ███ ███    ███   ███    ███ ███▄▄▄███   ███    █▀     ▀███▀▀██   ███▐██▀   
 ███   ███   ███ ███    ███  ▄███▄▄▄██▀  ▀▀▀▀▀▀███   ███            ███   ▀  ▄█████▀    
 ███   ███   ███ ███    ███ ▀▀███▀▀▀██▄  ▄██   ███ ▀███████████     ███     ▀▀█████▄    
 ███   ███   ███ ███    ███   ███    ██▄ ███   ███          ███     ███       ███▐██▄   
 ███   ███   ███ ███    ███   ███    ███ ███   ███    ▄█    ███     ███       ███ ▀███▄ 
  ▀█   ███   █▀   ▀██████▀  ▄█████████▀   ▀█████▀   ▄████████▀     ▄████▀     ███   ▀█▀ 
                                                                              ▀         
""".strip('\n'),

"""

 ███████ ██████  ██████   ██████          ██ 
 ██      ██   ██ ██   ██ ██    ██     ██ ██  
 █████   ██████  ██████  ██    ██        ██  
 ██      ██   ██ ██   ██ ██    ██     ██ ██  
 ███████ ██   ██ ██   ██  ██████          ██ 

""",

"""

 ██████  ██████   ██████  ███    ██ ████████  ██████         ██  
 ██   ██ ██   ██ ██    ██ ████   ██    ██    ██    ██     ██  ██ 
 ██████  ██████  ██    ██ ██ ██  ██    ██    ██    ██         ██ 
 ██      ██   ██ ██    ██ ██  ██ ██    ██    ██    ██     ██  ██ 
 ██      ██   ██  ██████  ██   ████    ██     ██████         ██  

"""]

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


# Centraliza um texto no console
def center(text):
	if type(text) == list:
		text = '\n'.join(text)
	text = text.split('\n')

	allChunks = []
	for line in text:
		chunkLen = terminalWidth - 1
		chunks = [line[i:i+chunkLen] for i in range(0, len(line), chunkLen)]
		if len(chunks):
			for chunk in chunks:
				allChunks.append(chunk.center(terminalWidth).rstrip())
		else:
			allChunks.append('')

	return '\n'.join(allChunks)


# Retorna uma barra de progresso
def getProgressBar(percentage):
	text = '▓' * int(percentage / 100 * terminalWidth)
	text = text.ljust(terminalWidth, '░')
	return text


# Retorna um número de porcentagem em ASCII Art
def getPercentageAscii(percentage):
	if percentage < 0: percentage = [-1]
	else: percentage = str(percentage)

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
def printStep(step, tip = '', status = None, logo = 0):
	# Atualiza o passo atual
	global currentStep
	if not currentStep or step > currentStep: currentStep = step
	
	# Retorna a porcentagem do progresso
	percentage = int(step / steps * 100)

	# Variável contendo o texto a ser mostrado
	text = ''

	# Barra de progresso
	text += getProgressBar(percentage) + '\n\n'

	# Logo "MobyStk"
	lines = logos[logo].split('\n')
	if terminalWidth < len(max(lines, key=len)):
		lines = list(map(lambda l: l[0:terminalWidth - 1], lines))
	lines = list(map(center, lines))
	text += '\n'
	for l in lines: text += l + '\n'
	text += '\n'

	# Texto informativo do passo atual/total
	stepText = int(step) if step > -1 else '-'
	if status:
		text += center(status) + '\n'
	else:
		text += center(f'Instalando ({stepText}/{steps})') + '\n'

	text += center('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━') + '\n\n'

	# Porcentagem
	percentageAscii = getPercentageAscii(percentage).split('\n')
	text += center(percentageAscii) + '\n'

	text += center('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━') + '\n'

	# Dica ou texto explicativo
	text += center(tip)

	# Mostra todo o conteúdo
	clearConsole()
	print(text)


# Exibe um erro
def error(title = None, description = None, details = None, stop = True):
	text = ''
	if description and details:
		text += description + '\n\n[DETALHES DO ERRO] ' + str(details)
	elif details:
		text += '[DETALHES DO ERRO] ' + str(details)
	elif description:
		text += description
	text += '\a'
	printStep(-1, text, '[ERRO] ' + title if title else None, logo=1)
	
	# Para a instalação ou pergunta se quer continuar
	if stop:
		# Exclui a pasta do MobyStk caso tenha ocorrido um erro
		if currentStep >= 4:
			os.chdir('../')
			try: shutil.rmtree('./MobyStk/')
			except: pass
		input()
		quit()
	else:
		input(center('\nPressione ENTER para continuar...'))


# Instala os módulos pelo PIP
def installModules():
	printStep(2, 'Instalando módulos')
	errors = 0
	try:
		for i in range(len(modules)):
			module = modules[i]
			errorText = '' if errors == 0 else f' - {errors} erro(s)'
			printStep(2 + (i / len(modules)), f'Instalando módulos ({module} - {i + 1}/{len(modules)}{errorText})')
			code = subprocess.call(
				[executable, '-m', 'pip', '--disable-pip-version-check', 'install', module],
				stdout = subprocess.DEVNULL,
				stderr = subprocess.DEVNULL
			)
			if code != 0: errors += 1
	except Exception as err:
		error('Falha na instalação dos módulos', details=err)


# Importa os módulos
def importModules(showError = False):
	try:
		global requests
		import requests
		for module in modules:
			if not importlib.util.find_spec(module):
				raise Exception(f'Cannot find module "{module}"')
		return True
	except Exception as err:
		if not showError: return False
		error('Falha na importação dos módulos', 'Alguns módulos podem não estar instalados, verifique sua conexão com a internet e tente novamente', err, stop=False)


# Verifica e corrige módulos
def verifyAndFixModules():
	printStep(1, 'Verificando módulos instalados')
	modulesImported = importModules()
	if not modulesImported:
		installModules()
		importModules(True)


# Cria a pasta do MobyStk
def createFolder():
	printStep(3, 'Verificando e criando pasta do MobyStk')
	try:
		if os.path.exists('./MobyStk/'):
			error('Instalação antiga detectada', 'Remova a pasta "MobyStk" depois abra novamente o instalador para prosseguir')
		os.mkdir('./MobyStk')
		os.chdir('./MobyStk')
	except Exception as err:
		error('Falha ao criar pasta do MobyStk', details=err)


# Baixa o MobyStk em formato ZIP
def download():
	printStep(4, 'Baixando o MobyStk')
	try:
		response = requests.get(zipURL, headers=headers)
		if response.status_code != 200: raise Exception(response)
		with open(downloadedZIPName, 'wb') as file:
			file.write(response.content)
	except NameError as err:
		error('Falha ao baixar o MobyStk', 'Provavelmente o módulo "requests" não foi instalado. Verifique sua conexão com a internet e tente novamente', err)
	except Exception as err:
		error('Falha ao baixar o MobyStk', 'Verifique sua conexão com a internet e tente novamente', err)


# Extrai o arquivo ZIP
def extract():
	printStep(5, 'Extraindo arquivos')
	try:
		global extractFolderName
		with zipfile.ZipFile(downloadedZIPName, 'r') as file:
			file.extractall()
		dirList = os.listdir('.')
		extractFolderName = [d for d in dirList if d.startswith(updateFolderName)][0]
	except Exception as err:
		error('Falha ao extrair arquivos', details=err)


# Copia os arquivos extraídos para a pasta principal
def copyFiles():
	printStep(6, 'Copiando arquivos')
	try:
		for item in os.listdir(extractFolderName):
			srcPath = os.path.join(extractFolderName, item)
			destPath = os.path.join('.', item)
			if os.path.isdir(srcPath):
				shutil.copytree(srcPath, destPath)
			else:
				shutil.copy2(srcPath, destPath)
	except Exception as err:
		error('Falha ao copiar os arquivos', details=err)


# Remove os arquivos usados na instalação
def cleanAndFinalize():
	printStep(7, 'Finalizando a instalação')
	try:
		shutil.rmtree(extractFolderName)
		if os.path.exists(downloadedZIPName):
		  os.remove(downloadedZIPName)
		if not os.path.exists('.update'):
			os.makedirs('.update')
		with open(lastUpdateFile, 'w') as file:
			file.write(datetime.datetime.now().isoformat())
	except Exception as err:
		error('Falha ao finalizar a instalação', details=err, stop=False)


# Criar atalho
def createShortcuts():
	if os.name != 'nt': return
	printStep(8, 'Criando atalhos')
	try:
		os.system(f"powershell \"$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\\Desktop\\MobyStk.lnk');$s.TargetPath='{os.getcwd()}\\INICIAR.py';$s.Description='Use seu smartphone como controle de videogame para PC';$s.IconLocation='{os.getcwd()}\\web\\img\\icon.ico';$s.Save()\"")
		os.system(f"powershell \"$s=(New-Object -COM WScript.Shell).CreateShortcut('%appdata%\\Microsoft\\Windows\\Start Menu\\MobyStk.lnk');$s.TargetPath='{os.getcwd()}\\INICIAR.py';$s.IconLocation='{os.getcwd()}\\web\\img\\icon.ico';$s.Save()\"")
		os.system(f"powershell \"$s=(New-Object -COM WScript.Shell).CreateShortcut('{os.getcwd()}\\MobyStk.lnk');$s.TargetPath='{os.getcwd()}\\INICIAR.py';$s.IconLocation='{os.getcwd()}\\web\\img\\icon.ico';$s.Save()\"")
	except: pass


try:
	printStep(0, 'Preparando a instalação, aguarde!', 'Preparando')
	verifyAndFixModules()
	createFolder()
	download()
	extract()
	copyFiles()
	cleanAndFinalize()
	createShortcuts()
	printStep(steps, 'O MobyStk foi instalado com sucesso! Você pode fechar esta janela agora\nAbra o MobyStk clicando no arquivo "INICIAR" na pasta "MobyStk"\a', 'Instalação finalizada', logo = 2)
	input()
except KeyboardInterrupt:
	pass
except Exception as err:
	print('Ocorreu um erro, verifique os detalhes abaixo:')
	print(str(err))
	input()
