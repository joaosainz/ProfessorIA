##########MÓDULOS
import tkinter as tk
from tkinter import ttk
import random
import os
import sys
import time
from datetime import datetime
import json
import requests
import urllib.request
import shutil
from dotenv import load_dotenv
from groq import Groq
import winsound

##########GROQ
if hasattr(sys, '_MEIPASS'):
    caminho_env = os.path.join(sys._MEIPASS, ".env")
else:
    caminho_env = os.path.join(os.path.abspath("."), ".env")
load_dotenv(dotenv_path=caminho_env)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODELO_GROQ = "groq/compound-mini"
cliente_groq = Groq(api_key=GROQ_API_KEY)

##########LISTAS E VARIÁVEIS INICIAIS
nomes_alunos = ["Gabriel", "Sophia", "Lucas", "Beatriz", "Matheus", "Heloísa", "Rodrigo", "Alice", "Pedro", "Davi", "Felipe", "Caio", "Gustavo", "Henrique", "Rafael", "Thiago", "Bruno", "Leonardo", "Vinícius", "Arthur", "Isabella", "Valentina", "Júlia", "Manuela", "Larissa", "Camila", "Fernanda", "Mariana", "Letícia", "Amanda", "Carolina", "Giovanna", "Theo", "Bento", "Murilo", "Cauã", "Lívia", "Rebeca", "Yasmin", "Talita"]

personalidades = [
    "Perfeccionista, trava em detalhes pequenos e não avança sem entender tudo a fundo antes de seguir adiante",
    "Disperso, começa a tarefa mas se distrai fácil e esquece o que já foi explicado minutos atrás",
    "Questiona tudo filosoficamente antes de aceitar qualquer conceito, perguntando 'mas por que isso é assim?'",
    "Apegado ao método que já conhece, trava quando o professor mostra outro caminho pra mesma coisa",
    "Só entende de verdade debatendo em voz alta, fica perdido em explicação silenciosa e pede pra repetir em forma de conversa",
    "Tem medo de parecer burro e prefere ficar quieto a arriscar uma resposta errada",
    "Concorda com tudo que o professor diz mesmo sem entender, só pra não parecer que está discordando",
    "Questiona e contesta a explicação do professor mesmo quando está errado, difícil de convencer",
    "Interpreta qualquer erro como sinal de que não é capaz, fica ansioso antes de tentar de novo",
    "Acha que já entendeu tudo certo e não sente necessidade de revisar nada, mesmo errando",
    "Erra, frustra-se rápido, mas insiste sozinho antes de pedir ajuda",
    "Desiste no primeiro erro e diz que não serve pra isso",
    "Só presta atenção quando o exemplo é prático e do dia a dia, se desliga com explicação abstrata",
    "Só consegue formular a própria dúvida depois de ouvir outro colega perguntar primeiro",
    "Só entende quando o professor compara o conteúdo com jogo, série ou meme",
    "Investe muito esforço mesmo em tarefa difícil, mas demora a perceber quando precisa mudar de estratégia e insiste no mesmo caminho que não funciona",
    "Muda de postura dependendo de quem está por perto: ativo e participativo em grupo, mas se fecha completamente quando fala sozinho com o professor",
    "Aprende melhor de um jeito específico (visual, prático ou auditivo) e trava quando o professor explica em outro formato, mesmo entendendo o conteúdo",
    "Diz que está tudo bem e que entendeu a matéria, mas demonstra pouco entusiasmo nas respostas, parecendo neutro o tempo todo",
    "Tem ideias criativas e foge do óbvio, mas se perde no meio do raciocínio e erra por falta de organização, não por falta de capacidade",
    "Evita perguntar por medo de incomodar o professor, mesmo quando está completamente perdido no conteúdo",
    "Tem uma habilidade ainda pouco desenvolvida na matéria, mas evolui rápido quando emparelhado com colega de perfil complementar",
    "Mais imaturo emocionalmente que a média da turma, reage com impaciência ou bagunça quando o conteúdo fica difícil",
    "Participa bastante e fala alto, mas perde o fio da meada no meio da própria pergunta",
    "Só rende bem quando o conteúdo é entregue do seu jeito específico de aprender; em explicação genérica, parece não entender nada",
]

historico_contexto = []
interacoes_atuais = 0
max_interacoes = 5
input_fechado = True
aluno_atual = None
personalidade_atual = None
simulacao_ativa = False
atualizacao_pendente = False
aluno_respondeu = False
verificacao_lista = True
versao = "1.3.3"
url_versao = "https://raw.githubusercontent.com/joaosainz/ProfessorIA/main/version.txt"
url_download = "https://github.com/joaosainz/ProfessorIA/releases/download/Windows/ProfessorIA.exe"

##########CRIANDO ARQUIVOS NA PASTA DOCUMENTOS DO USUÁRIO
pasta_destino = os.path.join(os.path.expanduser("~"), "Documents", "professoria")
caminho_historico = os.path.join(pasta_destino, "historico.json")
caminho_aulas = os.path.join(pasta_destino, "aulas.json")
caminho_nome = os.path.join(pasta_destino, "nome.json")

if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

##########CARREGANDO OU CRIANDO HISTÓRICO
if os.path.exists(caminho_historico):
    with open(caminho_historico, "r", encoding="utf-8") as f:
        try:
            historico_avaliacao = json.load(f)
        except json.JSONDecodeError:
            historico_avaliacao = []
else:
    historico_avaliacao = []

##########CARREGANDO OU CRIANDO AULAS
if os.path.exists(caminho_aulas):
    with open(caminho_aulas, "r", encoding="utf-8") as f:
        try:
            salas_de_aula = json.load(f)
        except json.JSONDecodeError:
            salas_de_aula = 0
else:
    salas_de_aula = 0

##########CARREGANDO OU CRIANDO NOME USUÁRIO
if os.path.exists(caminho_nome):
    with open(caminho_nome, "r", encoding="utf-8") as f:
        try:
            nome_professor_i = json.load(f)
        except json.JSONDecodeError:
            nome_professor_i = " "
else:
    nome_professor_i = " "

##########FUNÇÕES DE JANELA
def carregar_intro():
    global versao, versao_recente, url_versao, atualizacao_pendente
    intro = tk.Tk()
    intro.title("Carregando...")
    
    largura, altura = 500, 300
    tela_largura = intro.winfo_screenwidth()
    tela_altura = intro.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    intro.geometry(f"{largura}x{altura}+{x}+{y}")
    
    intro.configure(bg="#121214")
    intro.overrideredirect(True)
    
    logo_base = tk.PhotoImage(file=obter_caminho("professorIA.gif"))
    logo_img = logo_base.subsample(2, 2)
    label_logo = tk.Label(intro, image=logo_img, bg="#121214")
    label_logo.image = logo_img
    label_logo.pack(pady=(40, 5))
    tk.Label(intro, text="Simulador Docente Baseado em IA", font=("Consolas", 12), bg="#121214", fg="#a8a8b3").pack(pady=(5, 20))
    
    lbl_status = tk.Label(intro, text="Iniciando módulos pedagógicos...", font=("Consolas", 9, "italic"), bg="#121214", fg="#8f8f98")
    lbl_status.pack()
    
    estilo = ttk.Style()
    estilo.theme_use('default')
    estilo.configure("Intro.Horizontal.TProgressbar", thickness=6, background="#2b7a4b", troughcolor="#202024", borderwidth=0)
    
    barra_progresso = ttk.Progressbar(intro, style="Intro.Horizontal.TProgressbar", orient="horizontal", length=350, mode="determinate")
    barra_progresso.pack(pady=10)
    
    lbl_pct = tk.Label(intro, text=" 0%", font=("Consolas", 9, "bold"), bg="#121214", fg="#2b7a4b", width=5)
    lbl_pct.pack()
    
    if getattr(sys, 'frozen', False):
        pasta_atual = os.path.dirname(sys.executable)
    else:
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    time.sleep(1.5)
    caminho_do_arquivo = os.path.join(pasta_atual, "DeletarProfessorIA.exe")
    pasta_usuario = os.path.expanduser("~")
    pasta_destino = os.path.join(pasta_usuario, "Documents", "professoria", "versoesantigas")
    
    if os.path.exists(caminho_do_arquivo):
        agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        novo_nome = f"SUBSTITUIDO EM {agora}.exe"
        caminho_destino = os.path.join(pasta_destino, novo_nome)
        os.makedirs(pasta_destino, exist_ok=True)
        shutil.move(caminho_do_arquivo, caminho_destino)
    
    winsound.PlaySound(obter_caminho("intro.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    try:
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        resposta = requests.get(url_versao, headers=headers, timeout=2)
        resposta.raise_for_status()
        versao_recente = resposta.text.strip()
        
        if versao_recente != versao:
            atualizacao_pendente = True
        else:
            atualizacao_pendente = False
    except:
        atualizacao_pendente = False
        versao_recente = versao
    
    for i in range(1, 101):
        barra_progresso['value'] = i
        lbl_pct.config(text=f" {i}%")
        if i == 33: lbl_status.config(text="Conectando ao cérebro dos alunos...")
        if i == 66: lbl_status.config(text="Preparando diário de classe...")
        intro.update()
        time.sleep(0.02)
    
    if atualizacao_pendente:
        lbl_status.config(text="Baixando nova versão...", bg="#121214", fg="#8f8f98")
        intro.update()
        time.sleep(1)
        urllib.request.urlretrieve(url_download, f"ProfessorIA_{versao_recente}.exe")
            
        for i in range(1, 101):
            barra_progresso['value'] = i
            lbl_pct.config(text=f" {i}%")
            intro.update()
            time.sleep(0.08)
            
        if getattr(sys, 'frozen', False):
            caminho_atual = sys.executable
            pasta_atual = os.path.dirname(caminho_atual)
            caminho_temporario = os.path.join(pasta_atual, "DeletarProfessorIA.exe")
            os.rename(caminho_atual, caminho_temporario)
            time.sleep(1.5)
                
            pasta_usuario = os.path.expanduser("~")
            pasta_destino = os.path.join(pasta_usuario, "Documents", "professoria", "versoesantigas")
            os.makedirs(pasta_destino, exist_ok=True)
                
            if os.path.exists(caminho_temporario):
                agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                novo_nome = f"SUBSTITUIDO EM {agora}.exe"
                caminho_destino = os.path.join(pasta_destino, novo_nome)
                shutil.move(caminho_temporario, caminho_destino)
    
    intro.destroy()

def sobre_app():
    winsound.PlaySound(obter_caminho("clique.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    sobre = tk.Tk()
    sobre.title("Sobre o App")
    sobre.configure(bg="#121214")
    
    largura, altura = 500, 300
    tela_largura = sobre.winfo_screenwidth()
    tela_altura = sobre.winfo_screenheight()
    x = ((tela_largura // 2) - (largura // 2))
    y = (tela_altura // 2) - (altura // 2)
    sobre.geometry(f"{largura}x{altura}+{x}+{y}")
    
    sobre.iconbitmap(obter_caminho("professorIA.ico"))
    sobre.resizable(False, False)
    sobre.update()
    
    sobre_corpo = tk.Label(
        sobre, 
        wraplength=460, 
        text="O ProfessorIA© é um aplicativo simulador onde o professor pratica explicar um conteúdo e recebe crítica real sobre como foi. A IA não ensina o professor, ela faz papel de aluno. O professor digita a explicação, o aluno reage, faz perguntas, fica confuso, aprofunda.", 
        font=("Consolas", 12, "bold"), 
        bg="#121214", 
        fg="white"
    )
    sobre_corpo.pack(pady=(80, 50))

def historico():
    global historico_avaliacao, caminho_historico, pasta_destino, verificacao_lista
    winsound.PlaySound(obter_caminho("clique.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    janela_historico = tk.Tk()
    janela_historico.title("Histórico de Aulas")
    janela_historico.configure(bg="#121214")
    janela_historico.resizable(False, False)
    
    largura, altura = 800, 400
    tela_largura = janela_historico.winfo_screenwidth()
    tela_altura = janela_historico.winfo_screenheight()
    x = ((tela_largura // 2) - (largura // 2))
    y = (tela_altura // 2) - (altura // 2)
    janela_historico.geometry(f"{largura}x{altura}+{x}+{y}")
    
    janela_historico.iconbitmap(obter_caminho("professorIA.ico"))
    janela_historico.update()
    
    tk.Label(janela_historico, text="📜 Histórico", font=("Consolas", 24, "bold"), bg="#121214", fg="white", pady=20).pack()
    
    text_area = tk.Text(janela_historico, height=12, width=70, bg="#121214", fg="white", font=("Consolas", 11), highlightthickness=0, borderwidth=0, padx=15)
    scrollbar_hist = tk.Scrollbar(janela_historico, orient="vertical", command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar_hist.set)
    
    texto_formatado = ""
    verificacao_lista = True
    
    if historico_avaliacao:
        for dicionarios in historico_avaliacao:
            campos = ['Aula', 'Nome', 'Interações', 'Tema', 'Personalidade', 'Avaliação']
            if not all(campo in dicionarios for campo in campos):
                verificacao_lista = False
                break
        
        if not verificacao_lista:
            historico_avaliacao = []
            with open(caminho_historico, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)
            texto_formatado = "Seu histórico foi apagado devido a uma atualização."
        else:
            for item in historico_avaliacao:
                texto_formatado += f"AULA: {item['Aula']}\n\n"
                texto_formatado += f"PROFESSOR: {item['Nome']}\n\n"
                texto_formatado += f"INTERAÇÕES: {item['Interações']}\n\n"
                texto_formatado += f"TEMA: {item['Tema']}\n\n"
                texto_formatado += f"PERSONALIDADE: {item['Personalidade']}.\n\n"
                texto_formatado += f"AVALIAÇÃO: {item['Avaliação']}\n\n"
                texto_formatado += "-" * 40 + "\n\n"
    else:
        texto_formatado = "Nenhum histórico registrado ainda."
    
    text_area.insert("1.0", texto_formatado)
    text_area.configure(state="disabled")
    
    scrollbar_hist.pack(side="right", fill="y")
    text_area.pack(side="left", fill="both", expand=True)

##########FUNÇÕES DE FUNCIONALIDADE
def configurar_scroll_largura(event):
    canvas_chat.itemconfig(canvas_chat.find_withtag("all")[0], width=event.width)
    canvas_chat.configure(scrollregion=canvas_chat.bbox("all"))

def truncar_resposta(texto, max_palavras=120):
    palavras = texto.strip().split()
    if len(palavras) <= max_palavras:
        return texto.strip()
    
    texto_truncado = " ".join(palavras[:max_palavras])
    
    for pontuacao in [".", "!", "?"]:
        if pontuacao in texto_truncado:
            ultimo = texto_truncado.rfind(pontuacao)
            return texto_truncado[:ultimo + 1]
    
    return texto_truncado + "..."

def executar_chamada_groq(mensagens, temp=0.75, max_t=90):
    try:
        completion = cliente_groq.chat.completions.create(
            model=MODELO_GROQ,
            messages=mensagens,
            temperature=temp,
            max_tokens=max_t,
            top_p=0.9,
        )
        texto = completion.choices[0].message.content.strip()
        return truncar_resposta(texto, max_palavras=int(max_t * 1.1))
    except Exception as e:
        raise e

def obter_caminho(arquivo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, arquivo)
    return os.path.join(os.path.abspath("."), arquivo)

##########FUNÇÕES DE EVENTOS
def gerar_perfil():
    global aluno_atual, personalidade_atual, historico_contexto, interacoes_atuais, salas_de_aula, aluno_respondeu
    
    if not nome_professor.get().strip():
        reiniciar_aula()
        adicionar_balao_chat("Entrada inválida", "Digite um nome válido para começar a aula!", "erro")
        return
    
    winsound.PlaySound(obter_caminho("conectar.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    aluno_atual = random.choice(nomes_alunos)
    personalidade_atual = random.choice(personalidades)
    historico_contexto = []
    interacoes_atuais = 0
    aluno_respondeu = False
    salas_de_aula += 1
    
    with open(caminho_aulas, "w", encoding="utf-8") as f:
        json.dump(salas_de_aula, f, indent=4, ensure_ascii=False)
    with open(caminho_nome, "w", encoding="utf-8") as f:
        json.dump(nome_professor.get(), f, indent=4, ensure_ascii=False)
    
    for child in frame_conversa.winfo_children():
        child.destroy()
    
    canvas_chat.configure(scrollregion=canvas_chat.bbox("all"))
    progresso.config(text=f"Sala criada — Sala de Aula {salas_de_aula}")
    
    adicionar_balao_chat(None, f"📢 O(A) aluno(a) {aluno_atual} entrou na sala.\n\nSeu coordenador te disse que a personalidade do aluno é:\n{personalidade_atual}", "sistema")
    adicionar_balao_chat(None, f"📢 {nome_professor.get()} entrou na sala.", "sistema")
    
    input_mensagem.config(state="normal")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.insert("1.0", "Digite um tema e comece a aula...")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    comecar.config(state="normal", text="🚀 Iniciar Simulação", bg="#202024", fg="#2b7a4b", relief="solid", borderwidth=1)
    btn_sair_aula.config(state="normal", bg="#202024", fg="#aa3a3a", relief="solid", borderwidth=1)
    tema.config(state="normal", fg="white", bg="#18181c")
    nome_professor.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    btn_sobre.config(state="normal", bg="#202024", fg="#1E96FC", relief="solid", borderwidth=1)
    btn_historico.config(state="normal", bg="#202024", fg="#1E96FC", relief="solid", borderwidth=1)
    btn_entrar_aula.config(state="disabled", bg="#202024", fg="#8f8f98")

def iniciar_simulacao():
    global simulacao_ativa, input_fechado, historico_contexto
    
    if not aluno_atual:
        return
    
    if simulacao_ativa:
        input_mensagem.config(state="normal")
        input_mensagem.delete("1.0", tk.END)
        input_mensagem.insert("1.0", "Gerando relatório...")
        input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
        comecar.config(state="disabled", bg="#202024", fg="#8f8f98", text="🚀 Iniciar Simulação")
        finalizar_aula()
        return
    
    if not tema.get().strip():
        reiniciar_aula()
        adicionar_balao_chat("Sala encerrada", "Digite um tema válido para começar a aula!", "erro")
        return
    
    input_mensagem.config(state="normal")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.insert("1.0", "Aguarde...")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    comecar.config(state="disabled", bg="#202024", fg="#8f8f98", text="❌ Encerrar Simulação")
    simulacao_ativa = True
    btn_entrar_aula.config(state="disabled", bg="#202024", fg="#8f8f98")
    tema.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    
    winsound.PlaySound(obter_caminho("iniciar.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    prompt_sistema = (
        f"Você é {aluno_atual}, um estudante real com a seguinte personalidade: {personalidade_atual}.\n\n"
        f"Tema da aula de hoje: {tema.get()}.\n\n"
        "REGRAS OBRIGATÓRIAS:\n"
        "- Responda SEMPRE como esse aluno, respeitando a personalidade acima.\n"
        "- Máximo 4 frases curtas e naturais.\n"
        "- Suas perguntas e comentários DEVEM ser sobre o tema da aula.\n"
        "- Fale de forma espontânea, como adolescente/jovem adulto.\n"
        "- Mantenha a lógica e coerência do diálogo, mesmo que o professor mude de assunto.\n"
        "- Nunca diga que é uma IA ou que está seguindo regras.\n"
        "- Não use markdown, listas ou formatação."
    )
    
    historico_contexto = [{"role": "system", "content": prompt_sistema}]
    
    adicionar_balao_chat(None, f"💭 {aluno_atual} está pensando em uma dúvida para iniciar a aula...", "sistema")
    root.update()
    
    mensagens = [
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": f"Faça UMA pergunta curta e natural sobre '{tema.get()}'. Máximo 4 frases. Fale como aluno real."}
    ]
    
    try:
        duvida_inicial = executar_chamada_groq(mensagens, temp=0.8, max_t=70)
        historico_contexto.append({"role": "assistant", "content": duvida_inicial})
    except Exception as e:
        comecar.config(state="normal", bg="#202024", fg="#aa3a3a", text="❌ Encerrar Simulação")
        input_fechado = False
        input_mensagem.config(state="normal", fg="white", bg="#18181c")
        input_mensagem.delete("1.0", tk.END)
        input_mensagem.focus_set()
        adicionar_balao_chat("Erro de IA", f"Não foi possível gerar a dúvida inicial.\nErro: {str(e)}", "erro")
        return
    
    root.after(4000, lambda: adicionar_fala_aluno_e_liberar_interface(duvida_inicial))

def enviar_mensagem_professor():
    global interacoes_atuais, input_fechado, historico_contexto
    
    texto_professor = input_mensagem.get("1.0", "end-1c").strip()
    if not texto_professor or not simulacao_ativa or input_fechado:
        return
    
    winsound.PlaySound(obter_caminho("mensagemenviada.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    input_fechado = True
    
    adicionar_balao_chat(nome_professor.get(), texto_professor, "professor")
    historico_contexto.append({"role": "user", "content": texto_professor})
    
    comecar.config(state="disabled", bg="#202024", fg="#8f8f98", text="❌ Encerrar Simulação")
    input_mensagem.config(state="normal")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.insert("1.0", "Aguarde...")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    interacoes_atuais += 1
    progresso.config(text=f"Progresso: {interacoes_atuais}/{max_interacoes} — Aluno: {aluno_atual} — Professor: {nome_professor.get()} — Sala {salas_de_aula}")
    root.update()
    
    adicionar_balao_chat(None, f"💭 {aluno_atual} está pensando...", "sistema")
    root.update()
    
    mensagens = [historico_contexto[0]]
    
    historico_recente = [m for m in historico_contexto if m["role"] != "system"][-6:]
    mensagens.extend(historico_recente)
    
    try:
        resposta_ia = executar_chamada_groq(mensagens, temp=0.75, max_t=80)
        historico_contexto.append({"role": "assistant", "content": resposta_ia})
    except Exception as e:
        comecar.config(state="normal", bg="#202024", fg="#aa3a3a", text="❌ Encerrar Simulação")
        input_fechado = False
        input_mensagem.config(state="normal", fg="white", bg="#18181c")
        input_mensagem.delete("1.0", tk.END)
        input_mensagem.focus_set()
        interacoes_atuais -= 1
        progresso.config(text=f"Progresso: {interacoes_atuais}/{max_interacoes} — Aluno: {aluno_atual} — Professor: {nome_professor.get()} — Sala {salas_de_aula}")
        adicionar_balao_chat("Erro de IA", f"Não foi possível gerar a resposta do aluno.\nErro: {str(e)}", "erro")
        return
    
    root.after(2800, lambda: adicionar_fala_aluno_e_liberar_interface(resposta_ia))

def adicionar_balao_chat(remetente, texto, tipo):
    global aluno_respondeu
    largura_balao = int(canvas_chat.winfo_width() * 0.55) if canvas_chat.winfo_width() > 100 else 400
    
    linha_frame = tk.Frame(frame_conversa, bg="#121214")
    linha_frame.pack(fill="x", padx=10, pady=5)
    
    agora = datetime.now()
    
    if tipo == "professor":
        balao = tk.Label(
            linha_frame, 
            text=f"{remetente} • {agora.strftime('%H:%M:%S')}\n\n{texto}", 
            font=("Consolas", 11), 
            bg="#005c4b", fg="white", 
            justify="left", wraplength=largura_balao, 
            padx=12, pady=8, bd=0
        )
        balao.pack(side="right", anchor="e")
    
    elif tipo == "aluno":
        winsound.PlaySound(obter_caminho("mensagemrecebida.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
        balao = tk.Label(
            linha_frame, 
            text=f"{remetente} • {agora.strftime('%H:%M:%S')}\n\n{texto}", 
            font=("Consolas", 11), 
            bg="#1E4C66", fg="white", 
            justify="left", wraplength=largura_balao, 
            padx=12, pady=8, bd=0
        )
        balao.pack(side="left", anchor="w")
        aluno_respondeu = True
    
    elif tipo == "sistema":
        balao = tk.Label(
            linha_frame, 
            text=texto, 
            font=("Consolas", 10, "italic"), 
            bg="#18181c", fg="#a8a8b3", 
            justify="center", 
            wraplength=int(canvas_chat.winfo_width() * 0.80) if canvas_chat.winfo_width() > 100 else 600, 
            padx=10, pady=5
        )
        balao.pack(side="top", anchor="center")
    
    elif tipo == "avaliacao":
        balao = tk.Label(
            linha_frame, 
            text=f"📝 {remetente}\n{texto}", 
            font=("Consolas", 11, "bold"), 
            bg="#ad8822", fg="white", 
            justify="left", 
            wraplength=int(canvas_chat.winfo_width() * 0.80) if canvas_chat.winfo_width() > 100 else 600, 
            padx=12, pady=8, bd=1, relief="solid"
        )
        balao.pack(side="top", anchor="center", pady=5)
    
    elif tipo == "ambiental":
        balao = tk.Label(
            linha_frame, 
            text=f"🌿 {remetente}\n{texto}", 
            font=("Consolas", 11, "bold"), 
            bg="#357a58", fg="white", 
            justify="left", 
            wraplength=int(canvas_chat.winfo_width() * 0.80) if canvas_chat.winfo_width() > 100 else 600, 
            padx=12, pady=8, bd=1, relief="solid"
        )
        balao.pack(side="top", anchor="center", pady=5)
    
    elif tipo == "erro":
        balao = tk.Label(
            linha_frame, 
            text=f"❌ {remetente}\n{texto}", 
            font=("Consolas", 11, "italic"), 
            bg="#c03434", fg="#f3f3f3", 
            justify="left", 
            wraplength=int(canvas_chat.winfo_width() * 0.80) if canvas_chat.winfo_width() > 100 else 600, 
            padx=12, pady=8, bd=1, relief="solid"
        )
        balao.pack(side="top", anchor="center", pady=5)
    
    canvas_chat.update_idletasks()
    canvas_chat.configure(scrollregion=canvas_chat.bbox("all"))
    canvas_chat.yview_moveto(1.0)

def adicionar_fala_aluno_e_liberar_interface(texto):
    global input_fechado, simulacao_ativa
    
    if not simulacao_ativa:
        return
    
    adicionar_balao_chat(aluno_atual, texto, "aluno")
    
    comecar.config(state="normal", bg="#202024", fg="#aa3a3a", text="❌ Encerrar Simulação")
    input_fechado = False
    input_mensagem.config(state="normal", fg="white", bg="#18181c")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.focus_set()
    
    if interacoes_atuais >= max_interacoes:
        finalizar_aula()

def reiniciar_aula():
    winsound.PlaySound(obter_caminho("desconectar.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    global aluno_atual, personalidade_atual, historico_contexto, interacoes_atuais, simulacao_ativa, input_fechado, aluno_respondeu
    
    aluno_atual = None
    personalidade_atual = None
    historico_contexto = []
    interacoes_atuais = 0
    simulacao_ativa = False
    input_fechado = True
    aluno_respondeu = False
    
    for child in frame_conversa.winfo_children():
        child.destroy()
    canvas_chat.configure(scrollregion=canvas_chat.bbox("all"))
    
    progresso.config(text="Sala de Aula Vazia...")
    
    input_mensagem.config(state="normal", fg="white", bg="#18181c")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.insert("1.0", "Inicie uma aula para digitar...")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    btn_entrar_aula.config(state="normal", bg="#202024", fg="#2b7a4b")
    nome_professor.config(state="normal", fg="white", bg="#18181c")
    comecar.config(state="disabled", text="🚀 Iniciar Simulação", bg="#202024", fg="#8f8f98")
    btn_sair_aula.config(state="disabled", bg="#202024", fg="#8f8f98")
    tema.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    btn_sobre.config(state="disabled", bg="#202024", fg="#8f8f98")
    btn_historico.config(state="disabled", bg="#202024", fg="#8f8f98")

def finalizar_aula():
    global simulacao_ativa, historico_avaliacao, historico_contexto, interacoes_atuais, aluno_respondeu
    
    winsound.PlaySound(obter_caminho("encerrar.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    if not aluno_respondeu:
        return
    
    adicionar_balao_chat(None, "🏁 A simulação foi encerrada com sucesso! Veja sua avaliação final abaixo:", "sistema")
    
    historico_formatado = ""
    for mensagem in historico_contexto:
        if mensagem.get("role") == "system":
            continue
        elif mensagem.get("role") == "user":
            historico_formatado += f"PROFESSOR ({nome_professor.get()}): {mensagem.get('content')}\n\n"
        elif mensagem.get("role") == "assistant":
            historico_formatado += f"ALUNO ({aluno_atual}): {mensagem.get('content')}\n\n"
    
    prompt_aval = [{
    "role": "user",
    "content": (
        f"Você é um pedagogo especialista em ensino. Avalie a atuação do professor {nome_professor.get()} "
        f"com o aluno {aluno_atual} (personalidade: {personalidade_atual}) sobre o tema '{tema.get()}'.\n\n"
        f"Histórico da aula:\n{historico_formatado}\n\n"
        "Escreva uma crítica construtiva em um único parágrafo contínuo, de forma direta e natural. "
        "Não use markdown, negrito, itálico, listas, tópicos, títulos ou qualquer formatação. "
        "Escreva apenas texto corrido. "
        "Finalize obrigatoriamente com a nota no formato: [Nota: X/10]"
    )
    }]
    
    try:
        critica = executar_chamada_groq(prompt_aval, temp=0.55, max_t=175)
    except Exception as e:
        adicionar_balao_chat("Erro de IA", f"Não foi possível gerar a avaliação final.\nErro: {str(e)}", "erro")
        return
    
    adicionar_balao_chat("Avaliação", critica, "avaliacao")
    
    historico_avaliacao.append({
        "Aula": salas_de_aula,
        "Nome": nome_professor.get(),
        "Personalidade": personalidade_atual,
        "Interações": interacoes_atuais,
        "Avaliação": critica,
        "Tema": tema.get()
    })
    
    with open(caminho_historico, "w", encoding="utf-8") as f:
        json.dump(historico_avaliacao, f, indent=4, ensure_ascii=False)
    
    root.update()
    
    prompt_ambiental = [{
        "role": "user",
        "content": (
            f"O tema da aula foi '{tema.get()}'. "
            "Escreva uma curiosidade curta e interessante que conecte esse tema ao meio ambiente. "
            "Máximo 4 frases. Texto corrido, sem listas ou títulos."
        )
    }]
    
    try:
        curiosidade = executar_chamada_groq(prompt_ambiental, temp=0.7, max_t=140)
        adicionar_balao_chat("Meio ambiente", curiosidade, "ambiental")
    except:
        pass
    
    root.update()
    
    simulacao_ativa = False
    progresso.config(text="Aula Concluída! Veja a avaliação final.")
    
    input_mensagem.config(state="normal")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.insert("1.0", "Aula encerrada.")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    btn_entrar_aula.config(state="normal", bg="#202024", fg="#2b7a4b")
    nome_professor.config(state="normal", fg="white", bg="#18181c")
    comecar.config(state="disabled", bg="#202024", fg="#8f8f98", text="🚀 Iniciar Simulação")
    btn_sair_aula.config(state="disabled", bg="#202024", fg="#8f8f98")
    tema.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    btn_sobre.config(state="disabled", bg="#202024", fg="#8f8f98")
    btn_historico.config(state="disabled", bg="#202024", fg="#8f8f98")

##########LIGANDO O APP
carregar_intro()

if not atualizacao_pendente:
    root = tk.Tk()
    root.title("ProfessorIA - Simulador Docente")
    root.iconbitmap(obter_caminho("professorIA.ico"))
    root.configure(bg="#121214")
    
    largura, altura = 1172, 755
    root.minsize(1172, 755)
    tela_largura = root.winfo_screenwidth()
    tela_altura = root.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    
    ##########PAINEL ESQUERDO
    painel_esquerdo = tk.Frame(root, bg="#202024", width=300, height=620)
    painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
    painel_esquerdo.grid_propagate(False)
    
    logo_base = tk.PhotoImage(file=obter_caminho("professorIA.gif"))
    logo_img = logo_base.subsample(3, 3)
    label = tk.Label(painel_esquerdo, image=logo_img, bg="#202024")
    label.image = logo_img
    label.grid(row=0, column=0, sticky="w", padx=20, pady=(30, 10))
    
    tk.Label(painel_esquerdo, text="Qual o nome do professor?", font=("Consolas", 11), bg="#202024", fg="#e1e1e6").grid(row=1, column=0, sticky="w", padx=20, pady=(5, 5))
    
    nome_professor = tk.Entry(painel_esquerdo, font=("Consolas", 12), bg="#121214", fg="black", insertbackground="black", bd=1, relief="solid")
    nome_professor.insert(0, nome_professor_i)
    nome_professor.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew", ipady=8)
    nome_professor.config(state="normal", fg="white", bg="#18181c")
    
    btn_entrar_aula = tk.Button(painel_esquerdo, text="🚪 Entrar na Sala de Aula", font=("Consolas", 12, "bold"), bg="#202024", fg="#2b7a4b", bd=0, relief="solid", borderwidth=1, height=2, width=26, command=gerar_perfil)
    btn_entrar_aula.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")
    
    tk.Frame(painel_esquerdo, bg="#29292e", height=1).grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
    tk.Label(painel_esquerdo, text="Configuração da Aula", font=("Consolas", 16, "bold"), bg="#202024", fg="#e1e1e6").grid(row=5, column=0, sticky="w", padx=20, pady=(10, 20))
    tk.Label(painel_esquerdo, text="Qual o tema/conceito da aula?", font=("Consolas", 11), bg="#202024", fg="#e1e1e6").grid(row=6, column=0, sticky="w", padx=20, pady=(5, 5))
    
    tema = tk.Entry(painel_esquerdo, font=("Consolas", 12), bg="#121214", fg="black", insertbackground="black", bd=1, relief="solid")
    tema.insert(0, " ")
    tema.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew", ipady=8)
    tema.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    
    comecar = tk.Button(painel_esquerdo, text="🚀 Iniciar Simulação", font=("Consolas", 12, "bold"), bg="#202024", fg="#8f8f98", bd=0, relief="solid", borderwidth=1, height=2, command=iniciar_simulacao)
    comecar.grid(row=8, column=0, padx=20, pady=(0, 15), sticky="ew")
    comecar.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    btn_sair_aula = tk.Button(painel_esquerdo, text="🏃 Sair da Sala de Aula", font=("Consolas", 12, "bold"), bg="#444449", fg="#8f8f98", bd=0, relief="solid", borderwidth=1, height=2, command=reiniciar_aula)
    btn_sair_aula.grid(row=9, column=0, padx=20, pady=(0, 15), sticky="ew")
    btn_sair_aula.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    btn_historico = tk.Button(painel_esquerdo, text="📜 Histórico", font=("Consolas", 12, "bold"), bg="#1E96FC", fg="white", bd=0, relief="solid", borderwidth=1, height=2, command=historico)
    btn_historico.grid(row=10, column=0, padx=20, pady=(0, 15), sticky="ew")
    btn_historico.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    btn_sobre = tk.Button(painel_esquerdo, text="📌 Sobre o App", font=("Consolas", 12, "bold"), bg="#1E96FC", fg="white", bd=0, relief="solid", borderwidth=1, height=2, command=sobre_app)
    btn_sobre.grid(row=11, column=0, padx=20, pady=(0, 15), sticky="ew")
    btn_sobre.config(state="disabled", bg="#202024", fg="#8f8f98")
    
    direitos = tk.Label(painel_esquerdo, text="UnB - Computação - APC 06\nGarotos de Programa", bg="#202024", fg="gray")
    direitos.place(relx=0.5, rely=1.0, anchor="s", y=-10)
    
    ##########PAINEL DIREITO
    painel_direito = tk.Frame(root, bg="#121214")
    painel_direito.grid(row=0, column=1, sticky="nsew", padx=40, pady=15)
    painel_direito.columnconfigure(0, weight=1)
    painel_direito.rowconfigure(1, weight=1)
    
    tk.Label(painel_direito, text="Sala de Aula Virtual", font=("Consolas", 28, "bold"), bg="#121214", fg="white").grid(row=0, column=0, sticky="w", pady=(0, 15))
    
    area_chat = tk.Frame(painel_direito, bg="#202024", bd=1, relief="solid")
    area_chat.grid(row=1, column=0, sticky="nsew")
    area_chat.columnconfigure(0, weight=1)
    area_chat.rowconfigure(1, weight=1)
    
    progresso = tk.Label(area_chat, text="Sala de aula vazia...", font=("Consolas", 11), bg="#202024", fg="#a8a8b3")
    progresso.grid(row=0, column=0, sticky="w", padx=20, pady=15)
    
    canvas_chat = tk.Canvas(area_chat, bg="#121214", bd=0, highlightthickness=0)
    canvas_chat.grid(row=1, column=0, sticky="nsew", padx=(20, 5), pady=(0, 20))
    
    scrollbar = ttk.Scrollbar(area_chat, orient="vertical", command=canvas_chat.yview)
    scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 20), padx=(0, 5))
    
    canvas_chat.configure(yscrollcommand=scrollbar.set)
    frame_conversa = tk.Frame(canvas_chat, bg="#121214")
    canvas_chat.create_window((0, 0), window=frame_conversa, anchor="nw", width=1)
    frame_conversa.bind("<Configure>", lambda e: canvas_chat.configure(scrollregion=canvas_chat.bbox("all")))
    canvas_chat.bind("<Configure>", configurar_scroll_largura)
    
    frame_input = tk.Frame(painel_direito, bg="#202024")
    frame_input.grid(row=2, column=0, sticky="ew", pady=(15, 0))
    frame_input.columnconfigure(0, weight=1)
    
    input_mensagem = tk.Text(frame_input, font=("Consolas", 12), bg="#202024", fg="#8f8f98", bd=0, insertbackground="white", height=3, wrap="word", padx=10, pady=10)
    input_mensagem.insert("1.0", "Inicie uma aula para digitar...")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    input_mensagem.grid(row=0, column=0, sticky="ew")
    
    txt_aviso = tk.Label(painel_direito, text="ProfessorIA é uma IA e pode cometer erros.", font=("Consolas", 9), bg="#121214", fg="#8f8f98")
    txt_aviso.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 0))
    
    scrollbar_input = ttk.Scrollbar(frame_input, orient="vertical", command=input_mensagem.yview)
    scrollbar_input.grid(row=0, column=1, sticky="ns")
    input_mensagem.configure(yscrollcommand=scrollbar_input.set)
    
    input_mensagem.bind("<Return>", lambda event: (enviar_mensagem_professor(), "break")[1])
    input_mensagem.bind("<Shift-Return>", lambda event: None)
    
    root.mainloop()