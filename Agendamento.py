import streamlit as st
import datetime
from PIL import Image
import smtplib
import email.message
import pandas as pd
import re
import locale
import email.utils
from email.utils import formataddr
import time

# Configuração da página
st.set_page_config(
    page_title="Agendamento",
    page_icon=":bar_chart:",
    layout="wide"
)

# Estilos CSS
progress_bar_style = """
    <style>
    .stProgress > div > div {
        background-image: linear-gradient(45deg, #ff6c00, #ff9933);
        animation: gradient-animation 5s ease infinite;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }

    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes hide-progress {
        0% { opacity: 1; }
        100% { opacity: 0; }
    }

    .hide-progress {
        display: none;
    }

    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #dddddd;
        background-color: #ffffff;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }

    h1 {
        font-size: 28px;
        font-weight: bold;
        color: #ff99cc; /* Título rosa bebê */
        margin-bottom: 20px;
    }

    p {
        font-size: 16px;
        margin-bottom: 15px;
    }

    strong {
        font-weight: bold;
        color: #ff6c00; /* Cor laranja */
    }

    .footer {
        text-align: center;
        margin-top: 30px;
        border-top: 1px solid #dddddd;
        padding-top: 15px;
    }

    .footer p {
        font-size: 14px;
        color: #888888;
    }

    </style>
"""

st.markdown(progress_bar_style, unsafe_allow_html=True)

# Barra de progresso customizada
progress_bar_html = """
    <style>
    .custom-progress-bar {
        background-image: linear-gradient(45deg, #ff6c00, #ff9933);
        animation: gradient-animation 5s ease infinite;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
    </style>
"""
st.markdown(progress_bar_html, unsafe_allow_html=True)

# Carrega imagem do logo
image = Image.open('logo.jpeg')
st.sidebar.image(image)

# Sidebar
st.sidebar.markdown('## Menu:')
menu = st.sidebar.radio(
    "Selecione:",
    ("Agendamento")
)

# Horários disponíveis
horarios_disponiveis = [
    datetime.time(8, 0),
    datetime.time(9, 0),
    datetime.time(10, 0),
    datetime.time(11, 0),
    datetime.time(14, 0),
    datetime.time(15, 0),
    datetime.time(16, 0),
    datetime.time(17, 0)
]

horarios_formatados = [horario.strftime("%H:%M") for horario in horarios_disponiveis]


# Config Menu ==========================================================================================================
if menu == 'Agendamento':

    st.title('\n\nAgende sua consulta\n\n\n\n')

    nome = st.text_input("Nome e Sobrenome")
    if not nome:
        st.warning("Por favor, preencha o campo de nome.")
    else:
        st.success("Olá, " + nome + "! Seu nome foi salvo com sucesso.")

    e = st.text_input("E-mail")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", e):
        st.warning("Por favor, insira um endereço de e-mail válido.")
    else:
        st.success("O endereço de e-mail " + e + " é válido.")

    numero_celular = st.text_input("Numero do celular (Somente números com DDD) Ex: 75981999999", max_chars=11)
    ddd = numero_celular[:2]
    numero_formatado = '({}) {}-{}'.format(ddd, numero_celular[2:7], numero_celular[7:])
    if len(numero_celular) != 11:
        st.warning("Por favor, insira um numero de celular válido.")
    else:
       st.success('Seu número de celular é: ' + numero_formatado + '')

    option = st.selectbox(
        'Deseja agendar para qual especialidade?',
        ('Terapeuta Erika', 'Terapeuta Mavyane', 'Psicóloga Marcela', ''))

    st.write('Você escolheu:', option)


    def limitar_para_datas_futuras(data):
        hoje = datetime.date.today()
        if data < hoje:
            return hoje
        else:
            return data


    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    d = st.date_input(
        "Selecione para que data deseja agendar",
        min_value=datetime.date.today(), max_value=None)
    data_limite = limitar_para_datas_futuras(d)
    data_formatada = d.strftime("%d/%m/%Y")
    st.write('A data selecionada é:', data_formatada)



    hoje=datetime.date.today()

    t = st.selectbox('Escolha um dos horários disponíveis', horarios_formatados)
    st.write('Horario escolhido', t)

    confirma = st.success(f'''Você confirma seus dados?
                          
                          Nome: {nome}
    Número: {numero_formatado}
    Email: {e}''')

    if nome and e and numero_celular:
        button_enabled = st.button('Confirmar')

    else:
        st.warning('Aguardando confirmação')
        button_enabled = False

    if button_enabled:
        # Definindo o estilo da barra de progresso
        progress_bar_style = """
            <style>
            .stProgress > div > div {
                background-image: linear-gradient(45deg, #f6d365, #fda085); /* Cor rosa bebê */
                animation: gradient-animation 5s ease infinite;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }

            @keyframes gradient-animation {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            @keyframes hide-progress {
                0% { opacity: 1; }
                100% { opacity: 0; }
            }
            </style>
        """

        # Aplicando o estilo da barra de progresso
        st.markdown(progress_bar_style, unsafe_allow_html=True)

        # Cria uma barra de progresso
        progress_bar = st.progress(0)

        # Atualiza a barra de progresso em intervalos de 10%
        for i in range(10):
            # Atualiza o valor da barra de progresso
            progress_bar.progress((i + 1) / 10)
            # Adiciona um pequeno atraso para simular algum processamento
            time.sleep(0.5)


        # Adiciona a animação de desaparecimento ao atingir 100%
        progress_bar_html = """
                <style>
                    .disappear-animation {
                        animation: hide-progress 1s forwards;
                    }
                </style>
                <script>
                    const progressBar = document.querySelector('.stProgress > div > div');
                    progressBar.addEventListener('animationend', () => {
                        progressBar.style.display = 'none';
                    });
                    progressBar.classList.add('disappear-animation');
                </script>
            """
        st.markdown(progress_bar_html, unsafe_allow_html=True)
        st.success('Seu agendamento foi enviado!')


        def enviar_email():
            corpo_email = f"""
            <html>
            <head>
                <style>
                    /* Estilos personalizados */
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f8f8f8;
                        color: #333333;
                        line-height: 1.6;
                        margin: 0;
                        padding: 0;
                    }}
                    #container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        border: 1px solid #dddddd;
                        background-color: #ffffff;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        font-size: 28px;
                        font-weight: bold;
                        color: #ff99cc; /* Troque para a cor rosa bebê (#ff99cc) */
                        margin-bottom: 20px;
                    }}
                    p {{
                        font-size: 16px;
                        margin-bottom: 15px;
                    }}
                    strong {{
                        font-weight: bold;
                        color: #ff99cc; /* Troque para a cor rosa bebê (#ff99cc) */
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        border-top: 1px solid #dddddd;
                        padding-top: 15px;
                    }}
                    .footer p {{
                        font-size: 14px;
                        color: #888888;
                    }}
                </style>
            </head>
            <body>
                <div id="container">
                    <h1>Solicitação de Agendamento</h1>
                    <p>Olá, <strong>{nome}</strong></p>
                    <p>Seu agendamento foi processado com sucesso. Entraremos em contato para confirmação com mais detalhes.</p>
                    <p>A especialidade escolhida é: <strong>{option}</strong>!</p>
                    <p>O agendamento foi solicitado para o dia <strong>{data_formatada}</strong> no horário <strong>{t}</strong>.</p>
                    <p>Aguarde a confirmação via WhatsApp!</p>
                    <p>Agradecemos por escolher nossos serviços e estamos ansiosos para vê-lo em breve.</p>
                </div>
                <div class="footer">
                    <p>Atenciosamente,<br>Equipe do Espaço Abrace<br> </p>
                </div>
            </body>
            </html>
            """

            msg = email.message.Message()
            msg['Subject'] = "Solicitação de Agendamento"
            msg['From'] = formataddr(("Espaço Abrace", "helionsc.work@gmail.com"))
            msg['To'] = f'{e}'
            msg['Title'] = "Agendamento de consulta"
            password = 'xyjpqhveoymisapx'
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email)

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login('helionsc.work@gmail.com', password)
            s.sendmail('helionsc.work@gmail.com', [msg['To']], msg.as_string().encode('utf-8'))

            dados = {
                'Nome': [nome],
                'Data': [data_formatada],
                'Hora': [t],
                'Profissional': [option],
                'Data da Marcação': [hoje]
            }
            df = pd.DataFrame(dados)
            df.to_excel("Dados2.xlsx")


        enviar_email()

        def enviar_email2():
            corpo_email2 = f"""
            <html>
            <head>
                <style>
                    /* Estilos personalizados */
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f8f8f8;
                        color: #333333;
                        line-height: 1.6;
                        margin: 0;
                        padding: 0;
                    }}
                    #container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        border: 1px solid #dddddd;
                        background-color: #ffffff;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        font-size: 28px;
                        font-weight: bold;
                        color: #ff99cc; /* Cor rosa bebê claro (#ff99cc) */
                        margin-bottom: 20px;
                    }}
                    p {{
                        font-size: 16px;
                        margin-bottom: 15px;
                    }}
                    strong {{
                        font-weight: bold;
                        color: #ff99cc; /* Cor rosa bebê claro (#ff99cc) */
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        border-top: 1px solid #dddddd;
                        padding-top: 15px;
                    }}
                    .footer p {{
                        font-size: 14px;
                        color: #888888;
                    }}
                </style>
            </head>
            <body>
                <div id="container">
                    <h1>Solicitação de Agendamento</h1>
                    <p>Olá, Erika o paciente(a) <strong>{nome}</strong> entrou em contato para marcar uma consulta.</p>
                    <p>A especialidade escolhida é: <strong>{option}</strong>!</p>
                    <p>O agendamento foi solicitado para a seguinte data: <strong>{data_formatada}</strong> e o seguinte horário: <strong>{t}</strong>.</p>
                    <p>Por favor, entre em contato com a paciente através do WhatsApp: <strong>{numero_formatado}</strong></p>
                </div>
                <div class="footer">
                    <p>Atenciosamente,<br>Equipe do Espaço Abrace</p>
                </div>
            </body>
            </html>
            """

            msg = email.message.Message()
            msg['Subject'] = "Confirmação de Agendamento"
            msg['From'] = formataddr(("Abrace / Solicitação Agendamento", "helionsc.work@gmail.com"))
            msg['To'] = f'erikaterapeuta@yahoo.com'
            msg['Title'] = "Agendamento de consulta"
            password = 'xyjpqhveoymisapx'
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email2)

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login('helionsc.work@gmail.com', password)
            s.sendmail('helionsc.work@gmail.com', [msg['To']], msg.as_string().encode('utf-8'))

        enviar_email2()




