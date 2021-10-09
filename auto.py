import os
import paramiko
import shutil
import logging
from stat import S_ISDIR
from datetime import datetime

def Conexao():

    #Variaveis
    Data = datetime.today().strftime('/%y/%m/%d')
    ssh = paramiko.SSHClient()
    p_local_rem_processar_pe = ("/home/augusto/VAN_STAGE/341/PE/REM/em_processo/{}/".format(Data))
    p_local_rem_processado_pe = ("/home/augusto/VAN_STAGE/341/PE/REM/processado/{}".format(Data))
    p_local_ret_processar_pe = ("/home/augusto/VAN_STAGE/341/PE/RET/em_processo/".format(Data))
    p_remote_processar = '/var/www/clients/client1/web1/home/prbrasenior/Dados_ftp/Processos/'
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
    for root, dirs, files in os.walk(p_local_rem_processar_pe):
        cont = len(files)
        logging.info("Walk ok")
        while cont > 0:
            for fname in files:
                full_fname = os.path.join(root, fname)
                logging.info("Peguei o arquivo")
                sftp.put(full_fname, os.path.join(p_remote_processar, fname))
                cont = cont - 1
                logging.info('Operação realizada (remessa enviada) arquivo: {}'.format(fname))

    # Mover REM processado
    for root, dirs, files in os.walk(p_local_rem_processar_pe):
        for file in files:
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(p_local_rem_processado_pe)
            if file in files:
                shutil.move(old_file_path, new_file_path)
                logging.info("Movido para processado")
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
            sftp.get(path + '/' + file, os.path.join(p_local_ret_processar_pe, file))
            logging.info("Operaçao realizada (retorno recebido) nome do arquivo:{} ".format(file))

Conexao()
