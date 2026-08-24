import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações do Servidor de E-mail 
SMTP_SERVER = "://example.com"  # Altere para o SMTP real se for testar
SMTP_PORT = 587
EMAIL_REMETENTE = "suporte@suaempresa.com"
EMAIL_SENHA = "sua_senha_secreta"  


def enviar_email(destinatario, assunto, corpo_html):
    """Função responsável por conectar ao servidor e disparar o e-mail"""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(corpo_html, "html"))

    # Para testar de verdade, descomente as linhas abaixo com dados válidos:
    # with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    #     server.starttls()
    #     server.login(EMAIL_REMETENTE, EMAIL_SENHA)
    #     server.send_message(msg)

    print(f" Simulação: E-mail enviado para {destinatario} | Assunto: {assunto}")


# 1. Ler os templates de e-mail
with open("template_postagem.html", "r", encoding="utf-8") as f:
    html_postagem = f.read()

with open("template_conclusao.html", "r", encoding="utf-8") as f:
    html_conclusao = f.read()

# 2. Ler o arquivo CSV gerado pelo ERP
with open("dados_exemplo.csv", "r", encoding="utf-8") as arquivo_csv:
    leitor = csv.DictReader(arquivo_csv)

    for linha in leitor:
        tipo = linha["tipo_notificacao"]
        email = linha["email_cliente"]
        nome = linha["nome_cliente"]
        pedido = linha["id_pedido"]
        rastreio = linha["codigo_rastreio"]

        # 3. Lógica de Decisão 
        if tipo == "postagem":
            assunto = f"Instruções para Devolução - Pedido #{pedido}"
            # Substitui as marcações {nome}, {pedido} pelos dados reais da linha
            corpo = html_postagem.format(
                nome=nome, pedido=pedido, rastreio=rastreio
            )

        elif tipo == "conclusao":
            assunto = f"Devolução Concluída - Pedido #{pedido}"
            corpo = html_conclusao.format(nome=nome, pedido=pedido)

        else:
            print(f"Tipo desconhecido para o cliente {nome}. Pulando...")
            continue

        # 4. Disparar
        enviar_email(email, assunto, corpo)
