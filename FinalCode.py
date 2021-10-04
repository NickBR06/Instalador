#!/usr/bin python3
import PySimpleGUI as sg
import os
import paramiko
import shutil
import logging
from stat import S_ISDIR
from datetime import datetime
import schedule
import time

# Tema da interface GUI
sg.theme("Reddit")

# Logging
data_agora = datetime.now()
mes_atual = data_agora.strftime('%m')
print(mes_atual)
try:
    os.makedirs("/home/augusto/VAN_STAGE/logs/{}/".format(mes_atual))
except FileExistsError:
    pass
logging.basicConfig(filename='/home/augusto/VAN_STAGE/logs/{}/logging.log'.format(mes_atual),
                    level=logging.DEBUG, format='%(name)s %(levelname)s %(asctime)s %(message)s',
                    filemode='a')

# Conexao
def Conexao():

    #Variaveis
    ssh = paramiko.SSHClient()
    p_local_rem_processar = '/home/augusto/VAN_STAGE/341/REM/em_processo'
    p_local_rem_processado = '/home/augusto/VAN_STAGE/341/REM/processado'
    p_local_ret_processar = '/home/augusto/VAN_STAGE/341/RET/em_processo'
    p_remote_processar = '/var/www/clients/client1/web1/home/prbrasenior/Dados_ftp/Processos'
    p_remote_processados = '/var/www/clients/client1/web1/home/prbrasenior/Dados_ftp/Retornos/'
    host = 'isp01.ms-01-prod-pr.com.br'
    username = 'prbrasenior'
    password = 'eynG2SK@'
    port = 9823

    # Adicionando host a lista de hosts
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(hostname=host, username=username, password=password, port=port)

    # Upload de Remessa
    sftp = ssh.open_sftp()
    for root, dirs, files in os.walk(p_local_rem_processar):
        cont = len(files)
        while cont > 0:
            for fname in files:
                full_fname = os.path.join(root, fname)
                sftp.put(full_fname, os.path.join(p_remote_processar, fname))
                cont = cont - 1
                logging.info('Operação realizada (remessa enviada) arquivo: {}'.format(fname))

    # Mover REM processado
    for root, dirs, files in os.walk(p_local_rem_processar):
        for file in files:
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(p_local_rem_processado)
            if file in files:
                shutil.move(old_file_path, new_file_path)
    # Download de Retorno
    trans = paramiko.Transport((host, port))
    trans.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(trans)

    def sftp_walk(remotepath):
        path = remotepath
        files = []
        folders = []
        for f in sftp.listdir_attr(remotepath):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        if files:
            yield path, files
        for folder in folders:
            new_path = os.path.join(remotepath, folder)
            for x in sftp_walk(new_path):
                yield x

    for path, files in sftp_walk(p_remote_processados):
        for file in files:
            sftp.get(path + '/' + file, os.path.join(p_local_ret_processar, file))
            logging.info("Operaçao realizada (retorno recebido) nome do arquivo:{} ".format(file))

# Loop de UP. e DOWN. automatico
#def LoopAuto():
 #   schedule.every(10).seconds.do(Conexao)
  #  janela_auto = JanelaBronkenAuto()
   # janela_auto.un_hide()

    #while 1:
     #   schedule.run_pending()
      #  time.sleep(1)
      #  if janela == janela_auto and eventos == 'Parar processo automático':
       #     break

# GUI INTERFACE

    # Layout das janelas
def JanelaLogin():
    estilo = [
        [sg.Text("Usuário"), sg.Input(key='usuario', size=(20, 1))],
        [sg.Text("Senha"), sg.Input(key='senha', password_char='*', size=(20, 1))],
        [sg.Button("Entrar")]
    ]
    return sg.Window("Login", layout=estilo, finalize=True)


def JanelaMenu():
    menu = [
        [sg.Button("Configuracoes", size=(15, 5)), sg.Button("Relatorio", size=(15, 5))],
        [sg.Button("Logs", size=(15, 5)), sg.Button("Status dos Processos", size=(15, 5))],
        [sg.Button("Deslogar", size=(15, 5)), sg.Button("Enviar e Receber", size=(15, 5))],
        [sg.Combo(["Automatico", "Manual"], default_value="Automático", enable_events=True, key='auto', size=10)]
    ]
    return sg.Window("Meunu", layout=menu, finalize=True)


def JanelaConfig():
    config = [
        [sg.Text("Arquivo de Remessa"), sg.InputText("Caminho"), sg.Button("Salvar")],
        [sg.Text("Arquivo de Retorno"), sg.InputText("Caminho"), sg.Button("Salvar")],
        [sg.Text("Pasta de Logs     "), sg.InputText("Caminho"), sg.Button("Salvar")],
        [sg.Button("Voltar")]
    ]
    return sg.Window("Configuraçoes", layout=config, finalize=True)


def JanelaEnvRet():
    EnvRet = [
        [sg.Button("Enviar", size=(15, 7))],
        [sg.Button("Receber", size=(15, 7))],
        [sg.Button("Extrato", size=(15, 7))],
        [sg.Button("Voltar")]
    ]
    return sg.Window("Enviar e Receber", layout=EnvRet, finalize=True)


def JanelaLogs():
    Logs = [
        [sg.Text('Selecione o inicio')],
        [sg.In(key='-FROM-', enable_events=True, visible=True, default_text='AAAA-MM-DD')],
        [sg.Text('Selecione o final')],
        [sg.In(key='-TO-', enable_events=True, visible=True, default_text='AAAA-MM-DD')],
        [sg.Button("Verificar logs"), sg.Button("Voltar")]
    ]
    return sg.Window("Janela de Logs", layout=Logs, finalize=True)


def JanelaStatus():
    Status = [
        [sg.ProgressBar(100)]
    ]
    return sg.Window("Janela de Status", layout=Status, finalize=True)

def JanelaBronkenAuto():
    Parar = [
        [sg.Button('Parar processo automático')]
    ]
    return sg.Window("Janela de Status", layout=Parar, finalize=True)


# Janelas
janela1, janela2, janela_con, janela_env_ret, janela_logs, janela_auto = None, JanelaMenu(), None, None, None, None

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
    if janela == janela_env_ret and eventos == sg.WINDOW_CLOSED:
        break
    if janela == janela_logs and eventos == sg.WINDOW_CLOSED:
        break
    if janela == janela_auto and eventos == sg.WINDOW_CLOSED:
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
    if janela == janela_env_ret and eventos == "Voltar":
        janela_env_ret.hide()
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
        janela_env_ret = JanelaEnvRet()
        janela_env_ret.un_hide()
        janela2.hide()

        # Enviando uma remessa
    if janela == janela_env_ret and eventos == "Enviar":
        Env = [
            [sg.popup_get_file(title="Arquivo", message=("Qual seria o arquivo?"))],
            [sg.popup_get_folder(title="Banco", message=("Para qual banco deseja enviar?"))]]
        for valores in janela_env_ret:
            print(valores)

    # Janela de Logs
        # Entrando na Janela
    if janela == janela2 and eventos == "Logs":
        janela_logs = JanelaLogs()
        janela_logs.un_hide()
        janela2.hide()

        # Selecionando a data
    if janela == janela_logs and eventos == 'Verificar logs':
       print(1)

# Iniciando o automatico
    if eventos == 'auto':
        auto_no = valores['auto']
        if auto_no == "Automatico":
            schedule.every(10).seconds.do(Conexao)
            janela_auto = JanelaBronkenAuto()
            janela_auto.un_hide()

            while 1:
                schedule.run_pending()
                time.sleep(1)
                janela, eventos, valores = sg.read_all_windows()

                if janela == janela_auto and eventos == 'Parar processo automático':
                    janela_auto.hide()
                    break
            # Intervalo de execução



        if auto_no == "Manual":
            sg.PopupAutoClose("Em manutenção")

# Iniciando o manual