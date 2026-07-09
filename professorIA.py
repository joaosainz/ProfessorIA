##########MÓDULOS

import tkinter as tk
from tkinter import ttk
import random
import os
import sys
import time
import datetime
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
MODELO_GROQ = "llama-3.3-70b-versatile"
cliente_groq = Groq(api_key=GROQ_API_KEY)

##########LISTAS E VARIÁVEIS INICIAIS

nomes_alunos = ["Gabriel", "Sophia", "Lucas", "Beatriz", "Matheus", "Heloísa", "Rodrigo", "Alice", "Pedro", "Davi", "Felipe", "Caio", "Gustavo", "Henrique", "Rafael", "Thiago", "Bruno", "Leonardo", "Vinícius", "Arthur", "Isabella", "Valentina", "Júlia", "Manuela", "Larissa", "Camila", "Fernanda", "Mariana", "Letícia", "Amanda", "Carolina", "Giovanna", "Theo", "Bento", "Murilo", "Cauã", "Lívia", "Rebeca", "Yasmin", "Talita",]
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
historico_avaliacao = []
salas_de_aula = 0
interacoes_atuais = 0
max_interacoes = 4
input_fechado = True
aluno_atual = None
personalidade_atual = None
simulacao_ativa = False

##########DEFININDO FUNÇÕES ANTES DO INÍCIO
##########FUNÇÕES DE JANELA

def carregar_intro():
    intro = tk.Tk()
    intro.title("Carregando...")
    #
    ########
    #CÓDIGO RESPONSÁVEL POR AJUSTAR O TAMANHO DA JANELA
    #ESSE CÓDIGO FOI FEITO COM AUXÍLIO DA DOCUMENTAÇÃO OFICIAL DO MÓDULO.
    largura, altura = 500, 300
    tela_largura = intro.winfo_screenwidth()
    tela_altura = intro.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    intro.geometry(f"{largura}x{altura}+{x}+{y}")
    #
    intro.configure(bg="#121214")
    intro.overrideredirect(True)
    #
    tk.Label(intro, text="👨‍🏫", font=("Consolas", 50), bg="#121214", fg="white").pack(pady=(40, 5))
    tk.Label(intro, text="ProfessorIA", font=("Consolas", 28, "bold"), bg="#121214", fg="white").pack()
    tk.Label(intro, text="Simulador Docente Baseado em IA", font=("Consolas", 12), bg="#121214", fg="#a8a8b3").pack(pady=(5, 20))
    #
    lbl_status = tk.Label(intro, text="Iniciando módulos pedagógicos...", font=("Consolas", 9, "italic"), bg="#121214", fg="#8f8f98")
    lbl_status.pack()
    #
    estilo = ttk.Style()
    estilo.theme_use('default')
    estilo.configure("Intro.Horizontal.TProgressbar", thickness=6, background="#2b7a4b", troughcolor="#202024", borderwidth=0)
    #
    barra_progresso = ttk.Progressbar(intro, style="Intro.Horizontal.TProgressbar", orient="horizontal", length=350, mode="determinate")
    barra_progresso.pack(pady=10)
    #
    lbl_pct = tk.Label(intro, text="  0%", font=("Consolas", 9, "bold"), bg="#121214", fg="#2b7a4b", width=5)
    lbl_pct.pack()
    #
    ########
    #CÓDIGO RESPONSÁVEL POR INICIAR UM ÁUDIO NO WINDOWS USANDO O MÓDULO WINSOUND
    #ESSE CÓDIGO FOI FEITO COM AUXÍLIO DE IA GENERATIVA E DOCUMENTAÇÃO OFICIAL DO MÓDULO.
    winsound.PlaySound(obter_caminho("intro.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    #
    for i in range(1, 101):
        barra_progresso['value'] = i
        lbl_pct.config(text=f"  {i}%")
        if i == 33: lbl_status.config(text="Conectando ao cérebro dos alunos...")
        if i == 66: lbl_status.config(text="Preparando diário de classe...")
        intro.update()
        time.sleep(0.025)
    #
    intro.destroy()

def sobre_app():
    winsound.PlaySound(obter_caminho("clique.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    sobre = tk.Tk()
    sobre.title("Sobre o App")
    sobre.configure(bg="#121214")
    #
    largura, altura = 500, 300
    tela_largura = sobre.winfo_screenwidth()
    tela_altura = sobre.winfo_screenheight()
    x = ((tela_largura // 2) - (largura // 2))
    y = (tela_altura // 2) - (altura // 2)
    sobre.geometry(f"{largura}x{altura}+{x}+{y}")
    #
    sobre.iconbitmap(obter_caminho("professorIA.ico"))
    sobre.resizable(False, False)
    #
    sobre.update()
    #
    sobre_titulo = tk.Label(sobre, text="👨‍🏫 ProfessorIA", font=("Consolas", 24, "bold"), bg="#121214", fg="white", pady=20)
    sobre_titulo.pack()
    #
    sobre_corpo = tk.Label(sobre, wraplength=500, text="O ProfessorIA© é um aplicativo simulador onde o professor pratica explicar um conteúdo e recebe crítica real sobre como foi. A IA não ensina o professor, ela faz papel de aluno. O professor digita a explicação, o aluno reage, faz perguntas, fica confuso, aprofunda.", font=("Consolas", 12, "bold"), bg="#121214", fg="white")
    sobre_corpo.pack(pady=(5, 50))

def historico():
    global historico_avaliacao
    winsound.PlaySound(obter_caminho("clique.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    #
    janela_historico = tk.Tk()
    janela_historico.title("Histórico de Aulas")
    janela_historico.configure(bg="#121214")
    janela_historico.resizable(False, False)
    #
    largura, altura = 800, 400
    tela_largura = janela_historico.winfo_screenwidth()
    tela_altura = janela_historico.winfo_screenheight()
    x = ((tela_largura // 2) - (largura // 2))
    y = (tela_altura // 2) - (altura // 2)
    janela_historico.geometry(f"{largura}x{altura}+{x}+{y}")
    #
    janela_historico.iconbitmap(obter_caminho("professorIA.ico"))
    janela_historico.update()
    #
    tk.Label(janela_historico, text="📜 Histórico", font=("Consolas", 24, "bold"), bg="#121214", fg="white", pady=20).pack()
    #
    text_area = tk.Text(janela_historico, height=10, width=60, bg="#121214", fg="white", font=("Consolas", 12, "bold"), highlightthickness=0, borderwidth=0, padx=10)
    scrollbar_hist = tk.Scrollbar(janela_historico, orient="vertical", command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar_hist.set)
    #
    texto_formatado = ""
    if not historico_avaliacao:
        texto_formatado = "Nenhum histórico registrado ainda."
    else:
        for item in historico_avaliacao:
            texto_formatado += f"AULA: {item['Aula']}\n\n"
            texto_formatado += f"PROFESSOR: {item['Nome']}\n\n"
            texto_formatado += f"TEMA: {item['Tema']}\n\n"
            texto_formatado += f"PERSONALIDADE: {item['Personalidade']}.\n\n"
            texto_formatado += f"AVALIAÇÃO: {item['Avaliação']}\n\n"
            texto_formatado += "-" * 30 + "\n\n"
    
    text_area.insert("1.0", texto_formatado)
    text_area.configure(state="disabled")
    #
    scrollbar_hist.pack(side="right", fill="y")
    text_area.pack(side="left", fill="both", expand=True)
##########FUNÇÕES DE FUNCIONALIDADE

def configurar_scroll_largura(event):
    canvas_chat.itemconfig(canvas_chat.find_withtag("all")[0], width=event.width)
    canvas_chat.configure(scrollregion=canvas_chat.bbox("all"))

def executar_chamada_groq(mensagens, temp=0.8, max_t=120):
    completion = cliente_groq.chat.completions.create(model=MODELO_GROQ, messages=mensagens, temperature=temp, max_tokens=max_t)
    return completion.choices[0].message.content

########
#FUNÇÃO RESPONSÁVEL PARA IMPEDIR COM QUE AO COMPILAR O APP USANDO python -m PyInstaller --noconsole --onefile --icon=professorIA.ico --add-data "mensagemrecebida.wav;." --add-data "clique.wav;." --add-data "conectar.wav;." --add-data "desconectar.wav;." --add-data "iniciar.wav;." --add-data "encerrar.wav;." --add-data "mensagemenviada.wav;." --add-data "intro.wav;." --add-data "professorIA.ico;." --add-data ".env;." professorIA.py
#O APLICATIVO PASSE A PROCURAR PELOS ARQUIVOS COMPILADOS DENTRO DA ESTRUTURA DE DADOS DO .EXE, NÃO MAIS NA ESTRUTURA DE PASTAS DO ARQUIVO PYTHON.
#ESSA FUNÇÃO FOI FEITA COM AUXÍLIO DE IA GENERATIVA E DOCUMENTAÇÃO OFICIAL DO COMANDO.
def obter_caminho(arquivo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, arquivo)
    return os.path.join(os.path.abspath("."), arquivo)

##########FUNÇÕES DE EVENTOS

def gerar_perfil():
    global aluno_atual, personalidade_atual, historico_contexto, interacoes_atuais, salas_de_aula
    #
    if not nome_professor.get().strip():
        reiniciar_aula()
        adicionar_balao_chat("Entrada inválida na sala de aula", f"Digite um nome válido para começar a aula!", "erro")
        return
    #
    winsound.PlaySound(obter_caminho("conectar.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    #
    aluno_atual = random.choice(nomes_alunos)
    personalidade_atual = random.choice(personalidades)
    historico_contexto = []
    interacoes_atuais = 0
    salas_de_aula = salas_de_aula + 1
    #
    for child in frame_conversa.winfo_children():
        child.destroy()
    #
    canvas_chat.configure(scrollregion=canvas_chat.bbox("all"))
    #
    progresso.config(text=f"Progresso: 0 de {max_interacoes} interações — Sala de Aula {salas_de_aula}")
    #
    adicionar_balao_chat(None, f"📢 O(A) aluno(a) {aluno_atual} entrou na sala.\n\nSeu coordenador te disse que a personalidade do aluno é: \n{personalidade_atual}", "sistema")
    adicionar_balao_chat(None, f"📢 {nome_professor.get()} entrou na sala.", "sistema")
    #
    comecar.config(state="normal", bg="#2b7a4b", fg="white")
    btn_sair_aula.config(state="normal", bg="#aa3a3a", fg="white")
    tema.config(state="normal", fg="white", bg="#18181c")
    nome_professor.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    btn_sobre.config(state="normal", bg="#1E96FC", fg="white")
    btn_historico.config(state="normal", bg="#1E96FC", fg="white")
    #
    btn_entrar_aula.config(state="disabled", bg="#444449", fg="#8f8f98")
    #
    overlay.destroy()

def iniciar_simulacao():
    global simulacao_ativa
    if not aluno_atual: return
    #
    simulacao_ativa = True
    comecar.config(state="disabled", bg="#444449", fg="#8f8f98")
    btn_entrar_aula.config(state="disabled", bg="#444449")
    tema.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    #
    if not tema.get().strip():
        reiniciar_aula()
        adicionar_balao_chat("Sala de aula encerrada", f"Digite um tema válido para começar a aula!", "erro")
        return
    #
    winsound.PlaySound(obter_caminho("iniciar.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    prompt_sistema = (
        f"Você é um estudante real chamado {aluno_atual}. Sua personalidade é: {personalidade_atual}. "
        f"Você está em uma aula com seu professor {nome_professor.get()} sobre o tema: '{tema.get()}'. "
        "Responda estritamente em português brasileiro, agindo como o aluno de verdade. "
        "Gere respostas curtas (máximo de 2 frases), simulando mensagens instantâneas de chat. "
        "Mantenha sempre suas dúvidas focadas no tema e de acordo com as falhas da sua personalidade. "
        "Nunca saia do personagem e não dê respostas prontas de IA."
    )
    historico_contexto.append({"role": "system", "content": prompt_sistema})
    adicionar_balao_chat(None, f"💭 {aluno_atual} está pensando em uma dúvida para iniciar a aula...", "sistema")
    root.update()
    #
    prompt_gatilho = [{"role": "user", "content": f"Inicie a aula fazendo uma pergunta ou expondo uma dúvida inicial bem específica sobre o tema '{tema.get()}'. Lembre-se de seguir seu perfil: {personalidade_atual}. Seja breve."}]
    duvida_inicial = executar_chamada_groq(historico_contexto + prompt_gatilho)
    #
    historico_contexto.append({"role": "assistant", "content": duvida_inicial})
    root.after(7000, lambda: adicionar_fala_aluno_e_liberar_interface(duvida_inicial))

def enviar_mensagem_professor():
    global interacoes_atuais, input_fechado
    #
    texto_professor = input_mensagem.get("1.0", "end-1c").strip()
    if not texto_professor or not simulacao_ativa or input_fechado == True: return
    winsound.PlaySound(obter_caminho("mensagemenviada.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    input_fechado = True
    #
    adicionar_balao_chat(nome_professor.get(), texto_professor, "professor")
    historico_contexto.append({"role": "user", "content": texto_professor})
    #
    input_mensagem.config(state="normal")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.insert("1.0", "Aguarde...")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    #
    interacoes_atuais += 1
    progresso.config(text=f"Progresso: {interacoes_atuais} de {max_interacoes} interações")
    root.update()
    #
    if interacoes_atuais >= max_interacoes:
        finalizar_aula()
        return
    #
    adicionar_balao_chat(None, f"💭 {aluno_atual} está pensando...", "sistema")
    root.update()
    #
    resposta_ia = executar_chamada_groq(historico_contexto)
    historico_contexto.append({"role": "assistant", "content": resposta_ia})
    ########
    #NESSA PARTE ESTAVA DANDO ERRO SEM O USO DO LAMBDA, COM AUXÍLIO DE PESQUISAS, O LAMBDA FOI IMPLEMENTADO MESMO COM DIFICULDADE DE INTERPRETAÇÃO DO QUE REALMENTE ELE FAZ
    #ESSA PARTE FOI FEITA COM AUXÍLIO DE IA GENERATIVA E DA DOCUMENTAÇÃO OFICIAL.
    root.after(4000, lambda: adicionar_fala_aluno_e_liberar_interface(resposta_ia))

def adicionar_balao_chat(remetente, texto, tipo):
    largura_balao = int(canvas_chat.winfo_width() * 0.55)
    linha_frame = tk.Frame(frame_conversa, bg="#121214")
    linha_frame.pack(fill="x", padx=10, pady=5)
    #
    agora = datetime.datetime.now()
    #
    if tipo == "professor":
        balao = tk.Label(linha_frame, text=f"{remetente} - {agora.strftime('%H:%M:%S')}\n\n{texto}", font=("Consolas", 11), bg="#005c4b", fg="white", justify="left", wraplength=largura_balao, padx=12, pady=8, bd=0)
        balao.pack(side="right", anchor="e")
    #
    elif tipo == "aluno":
        winsound.PlaySound(obter_caminho("mensagemrecebida.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
        balao = tk.Label(linha_frame, text=f"{remetente} - {agora.strftime('%H:%M:%S')}\n\n{texto}", font=("Consolas", 11), bg="#202c33", fg="white", justify="left", wraplength=largura_balao, padx=12, pady=8, bd=0)
        balao.pack(side="left", anchor="w")
    #
    elif tipo == "sistema":
        balao = tk.Label(linha_frame, text=texto, font=("Consolas", 10, "italic"), bg="#18181c", fg="#a8a8b3", justify="center", wraplength=int(canvas_chat.winfo_width() * 0.80), padx=10, pady=5)
        balao.pack(side="top", anchor="center")
    #
    elif tipo == "avaliacao":
        balao = tk.Label(linha_frame, text=f"📝 {remetente}\n{texto}", font=("Consolas", 11, "bold"), bg="#2c2401", fg="#e1b12c", justify="left", wraplength=int(canvas_chat.winfo_width() * 0.80), padx=12, pady=8, bd=1, relief="solid")
        balao.pack(side="top", anchor="center", pady=5)
    #
    elif tipo == "ambiental":
        balao = tk.Label(linha_frame, text=f"🌿 {remetente}\n{texto}", font=("Consolas", 11, "bold"), bg="#0d2b1a", fg="#4caf7d", justify="left", wraplength=int(canvas_chat.winfo_width() * 0.80), padx=12, pady=8, bd=1, relief="solid")
        balao.pack(side="top", anchor="center", pady=5)
    #
    elif tipo == "erro":
        balao = tk.Label(linha_frame, text=f"❌ {remetente}\n{texto}", font=("Consolas", 10, "italic"), bg="#c03434", fg="#f3f3f3", justify="left", wraplength=int(canvas_chat.winfo_width() * 0.80), padx=10, pady=5, bd=1, relief="solid")
        balao.pack(side="top", anchor="center", pady=5)
    canvas_chat.update_idletasks()
    canvas_chat.configure(scrollregion=canvas_chat.bbox("all"))
    canvas_chat.yview_moveto(1.0)

def adicionar_fala_aluno_e_liberar(texto):
    adicionar_fala_aluno_e_liberar_interface(texto)

def adicionar_fala_aluno_e_liberar_interface(texto):
    global input_fechado, simulacao_ativa
    #
    if simulacao_ativa == False:
        return
    #
    adicionar_balao_chat(aluno_atual, texto, "aluno")
    #
    input_fechado = False
    input_mensagem.config(state="normal", fg="white", bg="#18181c")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.focus_set()

def reiniciar_aula():
    winsound.PlaySound(obter_caminho("desconectar.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    global aluno_atual, personalidade_atual, historico_contexto, interacoes_atuais, simulacao_ativa
    #
    aluno_atual = None
    personalidade_atual = None
    historico_contexto = []
    interacoes_atuais = 0
    simulacao_ativa = False
    #
    for child in frame_conversa.winfo_children():
        child.destroy()
    canvas_chat.configure(scrollregion=canvas_chat.bbox("all"))
    #
    progresso.config(text="Sala de Aula Vazia...")
    #
    input_mensagem.config(state="normal", fg="white", bg="#18181c")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.insert("1.0", "Inicie uma aula para digitar...")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    #
    btn_entrar_aula.config(state="normal", bg="#2b7a4b", fg="white")
    nome_professor.config(state="normal", fg="white", bg="#18181c")
    comecar.config(state="disabled", bg="#444449", fg="#8f8f98")
    btn_sair_aula.config(state="disabled", bg="#444449", fg="#8f8f98")
    tema.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    btn_sobre.config(state="disabled", bg="#444449", fg="#8f8f98")
    btn_historico.config(state="disabled", bg="#444449", fg="#8f8f98")

def finalizar_aula():
    global personalidade_atual, simulacao_ativa, historico_avaliacao, historico_contexto, salas_de_aula
    #
    simulacao_ativa = False
    progresso.config(text="Aula Concluída! Veja a avaliação final.")
    adicionar_balao_chat(None, "🏁 Limite de interações atingido. A simulação foi encerrada com sucesso! Veja sua avaliação final abaixo:", "sistema")
    prompt_aval = [{
        "role": "user",
        "content": (
            f"Você é um pedagogo especialista em ensino. Avalie a seguinte sequência de respostas que o professor {nome_professor.get()} deu "
            f"para o aluno {aluno_atual} ({personalidade_atual}) sobre o tema '{tema.get()}'.\n"
            f"Histórico da aula: \"{historico_contexto}\"\n\n."
            f"Escreva uma crítica curta avaliando o desempenho do professor na aula."
            f"E, para finalizar, finalize o texto obrigatoriamente com uma nota geral de 0 a 10. Exemplo: '[Nota: X/10] ...'"
        )
    }]
    critica = executar_chamada_groq(prompt_aval, temp=0.6, max_t=400)
    #
    adicionar_balao_chat("Avaliação", critica, "avaliacao")
    winsound.PlaySound(obter_caminho("encerrar.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    #
    historico_avaliacao.append({
    "Aula": salas_de_aula,
    "Nome": nome_professor.get(),
    "Personalidade": personalidade_atual,
    "Avaliação": critica,
    "Tema": tema.get()})
    root.update()
    #
    prompt_ambiental = [{
        "role": "user",
        "content": (
            f"O tema da aula foi '{tema.get()}'. "
            f"Escreva uma curiosidade curta e surpreendente que conecte esse tema ao meio ambiente. "
            f"Seja direto, use no máximo 3 frases.'. "
            f"Não use listas, não use títulos extras, só o texto corrido."
        )
    }]
    curiosidade = executar_chamada_groq(prompt_ambiental, temp=0.7, max_t=150)
    adicionar_balao_chat("Meio ambiente", curiosidade, "ambiental")
    root.update()
    #
    input_mensagem.config(state="normal")
    input_mensagem.delete("1.0", tk.END)
    input_mensagem.insert("1.0", "Aula encerrada.")
    input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
    #
    btn_entrar_aula.config(state="normal", bg="#2b7a4b", fg="white")
    nome_professor.config(state="normal", fg="white", bg="#18181c")
    comecar.config(state="disabled", bg="#444449", fg="#8f8f98")
    btn_sair_aula.config(state="disabled", bg="#444449", fg="#8f8f98")
    tema.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
    btn_sobre.config(state="disabled", bg="#444449", fg="#8f8f98")
    btn_historico.config(state="disabled", bg="#444449", fg="#8f8f98")

##########LIGANDO O APP
carregar_intro()

##########INICIANDO A JANELA PRINCIPAL
root = tk.Tk()
root.title("ProfessorIA - Simulador Docente")
root.iconbitmap(obter_caminho("professorIA.ico"))
root.configure(bg="#121214")
largura, altura = 1172, 710
root.minsize(1172, 710)
tela_largura = root.winfo_screenwidth()
tela_altura = root.winfo_screenheight()
x = (tela_largura // 2) - (largura // 2)
y = (tela_altura // 2) - (altura // 2)
root.geometry(f"{largura}x{altura}+{x}+{y}")

##########CONFIGURANDO APARÊNCIA NO TKINTER
root.columnconfigure(0, weight=0); root.columnconfigure(1, weight=1); root.rowconfigure(0, weight=1)

##########PAINEL ESQUERDO
painel_esquerdo = tk.Frame(root, bg="#202024", width=300, height=620)
painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
painel_esquerdo.grid_propagate(False)
tk.Label(painel_esquerdo, text="👨‍🏫 ProfessorIA", font=("Consolas", 24, "bold"), bg="#202024", fg="white").grid(row=0, column=0, sticky="w", padx=20, pady=(30, 10))
#
tk.Label(painel_esquerdo, text="Qual o nome do professor?", font=("Consolas", 11), bg="#202024", fg="#e1e1e6").grid(row=1, column=0, sticky="w", padx=20, pady=(5, 5))
#
nome_professor = tk.Entry(painel_esquerdo, font=("Consolas", 12), bg="#121214", fg="black", insertbackground="black", bd=1, relief="solid")
nome_professor.insert(0, " ")
nome_professor.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew", ipady=8)
nome_professor.config(state="normal", fg="white", bg="#18181c")
#
btn_entrar_aula = tk.Button(painel_esquerdo, text="🚪 Entrar na Sala de Aula", font=("Consolas", 12, "bold"), bg="#2b7a4b", fg="white", bd=0, relief="flat", height=2, width=26, command=gerar_perfil)
btn_entrar_aula.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")
#
tk.Frame(painel_esquerdo, bg="#29292e", height=1).grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
tk.Label(painel_esquerdo, text="Configuração da Aula", font=("Consolas", 16, "bold"), bg="#202024", fg="#e1e1e6").grid(row=5, column=0, sticky="w", padx=20, pady=(10, 20))
tk.Label(painel_esquerdo, text="Qual o tema/conceito da aula?", font=("Consolas", 11), bg="#202024", fg="#e1e1e6").grid(row=6, column=0, sticky="w", padx=20, pady=(5, 5))
#
tema = tk.Entry(painel_esquerdo, font=("Consolas", 12), bg="#121214", fg="black", insertbackground="black", bd=1, relief="solid")
tema.insert(0, " ")
tema.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew", ipady=8)
tema.config(state="disabled", disabledbackground="#202024", disabledforeground="#8f8f98")
#
comecar = tk.Button(painel_esquerdo, text="🚀 Iniciar Simulação", font=("Consolas", 12, "bold"), bg="#444449", fg="#8f8f98", bd=0, relief="flat", height=2, command=iniciar_simulacao)
comecar.grid(row=8, column=0, padx=20, pady=(0, 15), sticky="ew")
comecar.config(state="disabled", bg="#444449", fg="#8f8f98")
#
btn_sair_aula = tk.Button(painel_esquerdo, text="🏃 Sair da Sala de Aula", font=("Consolas", 12, "bold"), bg="#444449", fg="#8f8f98", bd=0, relief="flat", height=2, command=reiniciar_aula)
btn_sair_aula.grid(row=9, column=0, padx=20, pady=(0, 15), sticky="ew")
btn_sair_aula.config(state="disabled", bg="#444449", fg="#8f8f98")
#
btn_historico = tk.Button(painel_esquerdo, text="📜 Histórico", font=("Consolas", 12, "bold"), bg="#1E96FC", fg="white", bd=0, relief="flat", height=2, command=historico)
btn_historico.grid(row=10, column=0, padx=20, pady=(0, 15), sticky="ew")
btn_historico.config(state="disabled", bg="#444449", fg="#8f8f98")
#
btn_sobre = tk.Button(painel_esquerdo, text="📌 Sobre o App", font=("Consolas", 12, "bold"), bg="#1E96FC", fg="white", bd=0, relief="flat", height=2, command=sobre_app)
btn_sobre.grid(row=11, column=0, padx=20, pady=(0, 15), sticky="ew")
btn_sobre.config(state="disabled", bg="#444449", fg="#8f8f98")
#
overlay = tk.Frame(painel_esquerdo, bg="#202024", width=300, height=700)
overlay.place(x=0, y=250, relwidth=1, relheight=0.75)
tk.Label(overlay, text="🔒\nDesbloqueia após entrar \nna sala de aula pela primeira vez", font=("Consolas", 11, "italic"), bg="#202024", fg="#555560", justify="center").place(relx=0.5, rely=0.3, anchor="center")
#
direitos = tk.Label(painel_esquerdo, text="UnB - Computação - APC 06\nGarotos de Programa", bg="#202024", fg="gray")
direitos.place(relx=0.5, rely=1.0, anchor="s", y=-10)

##########PAINEL DIREITO
painel_direito = tk.Frame(root, bg="#121214")
painel_direito.grid(row=0, column=1, sticky="nsew", padx=40, pady=30)
painel_direito.columnconfigure(0, weight=1); painel_direito.rowconfigure(1, weight=1)
#
tk.Label(painel_direito, text="Sala de Aula Virtual", font=("Consolas", 28, "bold"), bg="#121214", fg="white").grid(row=0, column=0, sticky="w", pady=(0, 15))
#
area_chat = tk.Frame(painel_direito, bg="#202024", bd=1, relief="solid")
area_chat.grid(row=1, column=0, sticky="nsew")
area_chat.columnconfigure(0, weight=1); area_chat.rowconfigure(1, weight=1)
#
progresso = tk.Label(area_chat, text="Sala de aula vazia...", font=("Consolas", 11), bg="#202024", fg="#a8a8b3")
progresso.grid(row=0, column=0, sticky="w", padx=20, pady=15)
#
########
#CONFIGURAÇÕES RESPONSÁVEIS POR CONFIGURAR A ÁREA DE CHAT DO PROGRAMA, O TKINTER NÃO POSSUI SCROLLBAR NATIVA PARA A NECESSIDADE, SENDO MUITO DIFÍCIL IMPLEMENTAR
#ESSA SEÇÃO FOI FEITA COM AUXÍLIO DE IA GENERATIVA E DOCUMENTAÇÃO OFICIAL DO MÓDULO.
canvas_chat = tk.Canvas(area_chat, bg="#121214", bd=0, highlightthickness=0)
canvas_chat.grid(row=1, column=0, sticky="nsew", padx=(20, 5), pady=(0, 20))
#
scrollbar = ttk.Scrollbar(area_chat, orient="vertical", command=canvas_chat.yview)
scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 20), padx=(0, 5))
#
canvas_chat.configure(yscrollcommand=scrollbar.set)
frame_conversa = tk.Frame(canvas_chat, bg="#121214")
canvas_chat.create_window((0, 0), window=frame_conversa, anchor="nw", width=1)
frame_conversa.bind("<Configure>", lambda e: canvas_chat.configure(scrollregion=canvas_chat.bbox("all")))
canvas_chat.bind("<Configure>", configurar_scroll_largura)
#
frame_input = tk.Frame(painel_direito, bg="#202024")
frame_input.grid(row=2, column=0, sticky="ew", pady=(15, 0))
frame_input.columnconfigure(0, weight=1)
#
input_mensagem = tk.Text(frame_input, font=("Consolas", 12), bg="#202024", fg="#8f8f98", bd=0, insertbackground="white", height=3, wrap="word", padx=10, pady=10)
input_mensagem.insert("1.0", "Inicie uma aula para digitar...")
input_mensagem.config(state="disabled", bg="#202024", fg="#8f8f98")
input_mensagem.grid(row=0, column=0, sticky="ew")
#
scrollbar_input = ttk.Scrollbar(frame_input, orient="vertical", command=input_mensagem.yview)
scrollbar_input.grid(row=0, column=1, sticky="ns")
input_mensagem.configure(yscrollcommand=scrollbar_input.set)
#
input_mensagem.bind("<Return>", lambda event: (enviar_mensagem_professor(), "break")[1])
input_mensagem.bind("<Shift-Return>", lambda event: None)

##########LOOP DO ROOT
root.mainloop()

##########FIM DO CÓDIGO

