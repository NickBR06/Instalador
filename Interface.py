#!/usr/bin python3
import PySimpleGUI as sg

# Tema da interface GUI
sg.theme("Reddit")

# Layout das janelas

def JanelaLogin():


    estilo = [
        [sg.Text("Usuário"), sg.Input(key='usuario', size=(20, 1))],
        [sg.Text("Senha"), sg.Input(key='senha', password_char='*', size=(20, 1))],
        [sg.Button("Entrar")]
    ]
    return sg.Window("Login", layout=estilo, finalize=True)


def JanelaMenu():

    espacamento = sg.T("                             ")
    espacamento1 = sg.T("                             ")
    espacamento3 = sg.T("                                   ")

    menu = [
        [sg.Button("Configuracoes", size=(20, 7)), espacamento, sg.Button("Relatorio", size=(20, 7))],
        [sg.T("")],
        [sg.Button("Logs", size=(20, 7)), espacamento1, sg.Button("Status dos Processos", size=(20, 7))],
        [sg.T("")],
        [espacamento3, sg.Button("Enviar e Receber", size=(20, 7))],
        [sg.Button("Deslogar")]
    ]
    return sg.Window("Menu", layout=menu, finalize=True)


def JanelaConfig():
    config = [
        [sg.FolderBrowse("Arquivo de Remessa"), sg.Input(), sg.Button("Salvar")],
        [sg.FolderBrowse("Arquivo  de  Retorno"), sg.Input(), sg.Button("Salvar")],
        [sg.FolderBrowse("Pasta    de    Logs   "), sg.Input(), sg.Button("Salvar")],
        [sg.Button("Voltar")]
    ]
    return sg.Window("Configuracoes", layout=config, finalize=True)


def JanelaManual():
    Manual = [
        [sg.Button("Enviar", size=(15, 7))],
        [sg.T("")],
        [sg.Button("Receber", size=(15, 7))],
        [sg.T("")],
        [sg.Button("Extrato", size=(15, 7))],
        [sg.T("")],
        [sg.Button("Voltar")]
    ]
    return sg.Window("Envio Manual", layout=Manual, finalize=True)


def JanelaLogs():
    Logs = [
        [sg.Text('Selecione a data inicial')],
        [sg.In(key='-from-', enable_events=True, visible=True, default_text='AAAA-MM-DD')],
        [sg.Text('Selecione a data final')],
        [sg.In(key='-to-', enable_events=True, visible=True, default_text='AAAA-MM-DD')],
        [sg.Button("Verificar logs"), sg.Button("Voltar")]
    ]
    return sg.Window("Janela de Logs", layout=Logs, finalize=True)


def JanelaStatus():
    Status = [
        [sg.ProgressBar(100)]
    ]
    return sg.Window("Janela de Status", layout=Status, finalize=True)

def JanelaEnvio():
    Env = [
        [sg.T("")],
        [sg.FileBrowse("Escolha o arquivo", key='-me-', enable_events=True), sg.Input()],
        [sg.FolderBrowse("Escolha o destino", key='-from-', enable_events=True), sg.Input()],
        [sg.T("")],
        [sg.Button("Enviar", size=(15,2))],
        [sg.Button("Voltar")]
        ]
    return sg.Window("Janela de Status", layout=Env, finalize=True)

# Janelas
janela1, janela2, janela_con, janela_manual, janela_logs, janela_envio = None, JanelaMenu(), None, None, None, None

# Loop de eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    # Fechar as janelas
    if janela == janela1 and eventos == sg.WIN_CLOSED:
        break
    if janela == janela2 and eventos == sg.WIN_CLOSED:
        break
    if janela == janela_con and eventos == sg.WIN_CLOSED:
        break
    if janela == janela_manual and eventos == sg.WINDOW_CLOSED:
        break
    if janela == janela_logs and eventos == sg.WINDOW_CLOSED:
        break
    if janela == janela_envio and eventos == sg.WIN_CLOSED:
        break

    # Fezendo Login
    if janela == janela1 and eventos == "Entrar":
        if valores["usuario"] == "eduardo" and valores["senha"] == "unigloves":
            janela2 = JanelaMenu()
            janela1.hide()

        elif valores["usuario"] != "eduardo" or valores["senha"] != "unigloves":
            sg.Popup("Nome de usuario e/ou senha incorretos")

    # Deslogar e botões de voltar ao Menu
    if janela == janela2 and eventos == "Deslogar":
        janela2.hide()
        janela1.un_hide()
    if janela == janela_con and eventos == "Voltar":
        janela_con.hide()
        janela2.un_hide()
    if janela == janela_logs and eventos == "Voltar":
        janela_logs.hide()
        janela2.un_hide()
    if janela == janela_manual and eventos == "Voltar":
        janela_manual.hide()
        janela2.un_hide()
    if janela == janela_envio and eventos == "Voltar":
        janela_envio.hide()
        janela2.un_hide()

    # Janela de Configs
        # Entrando na janela
    if janela == janela2 and eventos == "Configuracoes":
        janela_con = JanelaConfig()
        janela_con.un_hide()
        janela2.hide()

    # Janela Enviar e Receber
        # Entrando na janela
    if janela == janela2 and eventos == "Enviar e Receber":
        janela_manual = JanelaManual()
        janela_manual.un_hide()
        janela2.hide()

        # Enviando uma remessa
    if janela == janela_manual and eventos == "Enviar":
        janela_envio = JanelaEnvio()
        janela_envio.un_hide()
        janela_manual.hide()

    if janela == janela_envio and eventos == "Enviar":
        print(valores['-me-'])
        print(valores['-from-'])

    # Janela de Logs

        # Entrando na Janela
    if janela == janela2 and eventos == "Logs":
        janela_logs = JanelaLogs()
        janela_logs.un_hide()
        janela2.hide()

    # Janela de Envio manual

        # Selecionando a data
    if janela == janela_logs and eventos == 'Verificar logs':
       print(1)
