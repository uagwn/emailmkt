import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import csv


def enviar_email(destinatario, nome, assunto, corpo_html):
    #smtp
    servidor = 'server'
    porta = 000
    remetente_email = 'email'
    remetente_nome = 'Tnome'
    senha = 'senha!'

    #config email
    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr((remetente_nome, remetente_email))
    msg['To'] = destinatario
    msg['Subject'] = assunto

    corpo_html_personalizado = corpo_html.replace('{nome}', nome)
    msg.attach(MIMEText(corpo_html_personalizado, 'html', 'utf-8'))

    #envio do email
    try:
        with smtplib.SMTP_SSL(servidor, porta) as servidor_smtp:
            servidor_smtp.login(remetente_email, senha)
            servidor_smtp.send_message(msg)
            print(f'Email enviado para {destinatario} com nome {nome}')
    except Exception as e:
        print(f'Erro ao enviar email para {destinatario}: {str(e)}')


def carregar_emails_e_enviar():
    try:
        with open('emails.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nome = row.get('nome')
                email = row.get('email')
                if email:
                    #pegando HTML
                    try:
                        with open('email.html', 'r', encoding='utf-8') as file:
                            corpo_html = file.read()
                    except FileNotFoundError:
                        print('Arquivo email.html não encontrado.')
                        return

                    enviar_email(email, nome, "Oferta Curso + Recomendações", corpo_html)
                else:
                    print(f'Email não encontrado para a linha: {row}')
    except FileNotFoundError:
        print('Arquivo emails.csv não encontrado.')


carregar_emails_e_enviar()
