import os
from time import sleep

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
def printStep(step, maxStep, tip = ''):
	text = ''
	lines = logo.split('\n')
	if terminalWidth < len(max(lines, key=len)):
		lines = list(map(lambda l: l[0:terminalWidth], lines))
	lines = list(map(lambda l: l.center(terminalWidth).rstrip(), lines))
	text += '\n'
	for l in lines: text += l + '\n'

	text += '\n'
	stepText = step if step > -1 else '-'
	text += f'Instalando ({stepText}/{maxStep})'.center(terminalWidth).rstrip() + '\n'
	text += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'.center(terminalWidth).rstrip() + '\n\n'

	percentage = int(step / maxStep * 100)
	percentageAscii = getPercentageAscii(percentage).split('\n')
	for line in percentageAscii:
		text += line.center(terminalWidth).rstrip() + '\n'
	text += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'.center(terminalWidth).rstrip() + '\n'
	for line in tip.split('\n'):
		text += line.center(terminalWidth).rstrip() + '\n'

	clearConsole()
	print(text)


# Tenta importar os módulos
def importModules():
	try:
		from colorama import init as coloramaInit, Back as B, Fore as F, Style as S
		import datetime
		import os
		import requests
		import shutil
		import zipfile
		return True
	except Exception:
		return False

# if os.path.exists('./MobyStk/'):
	# erro
# else:
	# continuar

# os.mkdir('./MobyStk')
# os.chdir('./MobyStk')



# TODOS:
# Verificar se não há uma instalação existente
# Verificar módulos
# Instalar módulos se necessário
# Criar e entrar na pasta ./mobystk/
# Baixar mobystk.zip
# Extrair
# Escrever arquivo .lastUpdate.txt
# Instalar atalho se Windows
# Abrir atalho na pasta ./mobystk/MobyStk.lnk se Windows