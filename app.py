import os
import datetime
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel, Label, Entry, Button, ttk, simpledialog
import json
import subprocess # Importar para executar comandos Git

# --- Configurações ---
POSTS_DIR = "posts"
INDEX_FILE = "index.html"

# --- Funções Auxiliares ---
def slugify(text):
    """Converte texto para um slug URL-amigável."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.strip('-')
    return text

def format_categories_for_js(category_string):
    """Formata a string de categorias para ser usada no array JavaScript."""
    return ','.join([c.strip().lower() for c in category_string.split(',') if c.strip()])

# --- Templates HTML (Mantido o mesmo) ---
FULL_POST_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{post_description}" />
    <meta name="keywords" content="{post_keywords}" />
    <meta name="author" content="Hreff" />

    <title>{post_title_full} - Hreff</title>

    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet" />
    <link rel="stylesheet" href="/assets/css/root.css" />
    <link rel="stylesheet" href="/assets/css/reset.css" />
    <link rel="stylesheet" href="/assets/css/header.css" />
    <link rel="stylesheet" href="/assets/css/footer.css" />
    <link rel="stylesheet" href="/assets/css/responsive.css" />
    <link rel="stylesheet" href="/assets/css/table.css" />
    <link rel="stylesheet" href="/assets/css/post-content.css" />
</head>
<body>
    <header class="header">
        <a class="header-title" href="/">
            H<span>reff</span>.
        </a>
        <div class="header-container">
            <nav class="header-container-menu" aria-label="Menu Principal">
                <ul class="header-container-menu-list">
                    <li class="header-container-menu-list-item">
                        <a class="header-container-menu-list-item-link" href="/#about">Sobre</a>
                    </li>
                    <li class="header-container-menu-list-item">
                        <a class="header-container-menu-list-item-link" href="/#categories">Categorias</a>
                    </li>
                    <li class="header-container-menu-list-item">
                        <a class="header-container-menu-list-item-link" href="/#latest-posts">Últimos Posts</a>
                    </li>
                    <li class="header-container-menu-list-item">
                        <a class="header-container-menu-list-item-link" href="/#contact">Contato</a>
                    </li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <section class="post-section" aria-labelledby="post-main-title">
            <div class="post-container">
                <h1 id="post-main-title" class="post-title post-full-title">{post_title_full}</h1>
                <p class="post-date">Publicado em {post_date_formatted}</p>
                <p class="post-category">Categoria: {post_category}</p>

                <div class="post-content post-full-content">
                    {post_full_content}
                    </div>
            </div>
        </section>
    </main>

    <footer class="footer container" role="contentinfo">
        <p>&copy; <span id="current-year-post"></span> All Rights Reserved to Hreff.</p>
        <div class="social">
            <a href="https://br.linkedin.com/in/arissandro" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn de Arissandro">
                <i class="bx bxl-linkedin"></i>
            </a>
        </div>
    </footer>

    <script>
        document.getElementById('current-year-post').textContent = new Date().getFullYear();
    </script>
</body>
</html>
"""

# --- Classe Principal da Aplicação GUI ---
class PostManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de Posts Hreff - MODO HACKER")
        
        # --- Configuração de Tamanho e Centralização da Janela ---
        window_width = 800
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # --- Habilitar Redimensionamento ---
        master.resizable(True, True) # Permite redimensionar em largura e altura

        # --- Tema Hacker (Cores Inalteradas para o fundo e texto geral) ---
        bg_color = "#0a0a0a"       # Preto muito escuro
        fg_color = "#39ff14"       # Verde neon (cor "second-color" do seu root.css)
        accent_color = "#00ffff"   # Ciano para detalhes
        input_bg = "#1c1c1c"       # Cinza escuro para inputs
        input_fg = fg_color        # Texto verde neon para inputs
        border_color = "#555555"   # Borda cinza escura para elementos

        # --- Cores dos Botões (Novas) ---
        button_bg_new = "white"
        button_fg_new = "black"
        button_active_bg_new = "#f0f0f0" # Levemente cinza ao clicar
        button_active_fg_new = "black"

        # Configurações de estilo para toda a aplicação
        master.config(bg=bg_color) # Fundo da janela principal
        master.option_add('*Font', 'Consolas 12 bold') # Fonte monospace, negrito, TAMANHO AUMENTADO
        master.option_add('*PadX', 10) 
        master.option_add('*PadY', 10) 
        
        # Estilo para Frames
        master.option_add('*Frame.background', bg_color)

        # Estilo para Labels
        master.option_add('*Label.background', bg_color)
        master.option_add('*Label.foreground', fg_color)

        # Estilo para Entradas (inputs)
        master.option_add('*Entry.borderWidth', 2)
        master.option_add('*Entry.relief', 'flat')
        master.option_add('*Entry.background', input_bg)
        master.option_add('*Entry.foreground', input_fg)
        master.option_add('*Entry.insertBackground', accent_color) # Cor do cursor
        master.option_add('*Entry.highlightbackground', border_color) # Borda quando não selecionado
        master.option_add('*Entry.highlightcolor', accent_color) # Borda quando selecionado
        master.option_add('*Entry.font', 'Consolas 12') # Define a fonte explicitamente para Entries para controle de altura
        
        # Estilo para Botões (NOVAS CORES!)
        master.option_add('*Button.background', button_bg_new)
        master.option_add('*Button.foreground', button_fg_new)
        master.option_add('*Button.activebackground', button_active_bg_new) 
        master.option_add('*Button.activeforeground', button_active_fg_new) 
        master.option_add('*Button.borderWidth', 2)
        master.option_add('*Button.relief', 'raised')
        master.option_add('*Button.font', 'Consolas 12 bold') 

        # Estilo para Listbox
        master.option_add('*Listbox.borderWidth', 2)
        master.option_add('*Listbox.relief', 'sunken')
        master.option_add('*Listbox.background', input_bg)
        master.option_add('*Listbox.foreground', fg_color)
        master.option_add('*Listbox.selectBackground', accent_color)
        master.option_add('*Listbox.selectForeground', bg_color)
        master.option_add('*Listbox.highlightbackground', border_color)
        master.option_add('*Listbox.highlightcolor', accent_color)
        master.option_add('*Listbox.font', 'Consolas 12') # Define a fonte explicitamente para Listbox

        # Estilo para ScrolledText (para a saída do Git)
        master.option_add('*Scrolledtext.background', input_bg)
        master.option_add('*Scrolledtext.foreground', fg_color)
        master.option_add('*Scrolledtext.insertBackground', accent_color)
        master.option_add('*Scrolledtext.highlightbackground', border_color)
        master.option_add('*Scrolledtext.highlightcolor', accent_color)
        master.option_add('*Scrolledtext.font', 'Consolas 10')

        # Estilo para Notebook (abas)
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure('TNotebook', background=bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background=bg_color, foreground=fg_color, 
                        font='Consolas 11 bold', padding=[12, 6]) # Aumenta padding da aba
        style.map('TNotebook.Tab', background=[('selected', accent_color)], 
                  foreground=[('selected', bg_color)])


        self.main_frame = tk.Frame(master, padx=15, pady=15) 
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_tab = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.create_tab, text="Criar Novo Post")
        self._setup_create_tab(self.create_tab)

        self.edit_tab = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.edit_tab, text="Editar Post")
        self._setup_edit_tab(self.edit_tab)

        self.delete_tab = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.delete_tab, text="Excluir Post")
        self._setup_delete_tab(self.delete_tab)

        # --- Nova Aba de Git ---
        self.git_tab = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.git_tab, text="Git")
        self._setup_git_tab(self.git_tab)


        self.status_label = tk.Label(self.main_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, pady=5,
                                     bg=bg_color, fg=fg_color, font='Consolas 10') # Status label ligeiramente maior
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Botão de Sair do App com as novas cores dos botões
        self.exit_button = tk.Button(self.main_frame, text="SAIR DO APP", command=master.quit, 
                                     bg=button_bg_new, fg=button_fg_new, font='Consolas 12 bold', 
                                     relief='raised', bd=2, activebackground=button_active_bg_new, activeforeground=button_active_fg_new) 
        self.exit_button.pack(side=tk.BOTTOM, pady=(5,0))


        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
        self._load_posts_to_listbox(self.edit_post_listbox) 


    def _on_tab_change(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab in ["Editar Post", "Excluir Post"]:
            self._load_posts_to_listbox(self.delete_post_listbox)
            self._load_posts_to_listbox(self.edit_post_listbox)
        elif selected_tab == "Git":
            # Limpa a saída do Git ao mudar para a aba
            self.git_output_text.delete(1.0, tk.END)
            self._set_status_message("Aba Git Ativada.", "info")


    def _set_status_message(self, message, message_type="info"):
        colors = {"info": "#00ffff", "success": "#00ff00", "warning": "#ffff00", "error": "#ff0000"} 
        self.status_label.config(text=message, fg=colors.get(message_type, "#00ffff"))
        self.master.after(7000, lambda: self.status_label.config(text="") if self.status_label.cget("text") == message else None)

    def _update_index_post_list(self, old_file_path=None, new_post_data=None):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                index_content = f.read()

            post_files_array_pattern = re.compile(r"const postFiles = \[([^\]]*)\];", re.DOTALL)
            match = post_files_array_pattern.search(index_content)

            if not match:
                self._set_status_message(f"ERRO: Não foi possível encontrar o array 'postFiles' em '{INDEX_FILE}'. Verifique a estrutura.", "error")
                return False

            current_array_str = match.group(1).strip()
            posts_list = []

            entry_pattern = re.compile(r"\{\s*file:\s*'(.*?)',\s*url:\s*'(.*?)',\s*categories:\s*'(.*?)'\s*\}")
            for entry_match in entry_pattern.finditer(current_array_str):
                posts_list.append({
                    'file': entry_match.group(1).strip(),
                    'url': entry_match.group(2).strip(),
                    'categories': entry_match.group(3).strip()
                })
            
            if old_file_path:
                old_js_file_path = old_file_path.lstrip('/')
                original_len = len(posts_list)
                posts_list = [p for p in posts_list if p['file'] != old_js_file_path]
                if len(posts_list) < original_len:
                    self._set_status_message(f"Entrada ANTIGA '{old_js_file_path}' REMOVIDA da lista 'postFiles'.", "success")
                else:
                    self._set_status_message(f"AVISO: Entrada ANTIGA '{old_js_file_path}' NÃO ENCONTRADA na lista 'postFiles'.", "warning")
                    if not new_post_data: 
                        return False

            if new_post_data:
                new_js_file_path = new_post_data['post_url'].lstrip('/')
                formatted_categories = format_categories_for_js(new_post_data['post_category'])
                
                new_entry = {
                    'file': new_js_file_path,
                    'url': new_js_file_path,
                    'categories': formatted_categories
                }

                if any(p['file'] == new_js_file_path for p in posts_list):
                     self._set_status_message(f"AVISO: O post '{new_js_file_path}' já existe na lista 'postFiles'. Nenhuma nova adição necessária.", "warning")
                else:
                    posts_list.append(new_entry)
                    self._set_status_message(f"Nova entrada para o post '{new_js_file_path}' ADICIONADA à lista 'postFiles'.", "success")

            new_js_entries = []
            posts_list_sorted = sorted(posts_list, key=lambda x: x['file'])

            for post in posts_list_sorted:
                ordered_post = {k: post[k] for k in ['file', 'url', 'categories']}
                new_js_entries.append(
                    f"            {{ file: '{ordered_post['file']}', url: '{ordered_post['url']}', categories: '{ordered_post['categories']}' }}"
                )
            
            new_array_content = ",\n".join(new_js_entries)
            
            updated_content = post_files_array_pattern.sub(f"const postFiles = [\n{new_array_content}\n];", index_content)

            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                f.write(updated_content)
            return True

        except FileNotFoundError:
            self._set_status_message(f"ERRO CRÍTICO: O arquivo '{INDEX_FILE}' NÃO FOI ENCONTRADO. Verifique o caminho.", "error")
            return False
        except Exception as e:
            self._set_status_message(f"ERRO INESPERADO ao atualizar o index.html: {e}", "error")
            return False

    def _setup_create_tab(self, tab_frame):
        tk.Label(tab_frame, text="TÍTULO DO POST:").grid(row=0, column=0, sticky="w")
        self.create_title_entry = tk.Entry(tab_frame, width=50) # Menos largo
        self.create_title_entry.grid(row=0, column=1, sticky="ew", pady=7) # Mais altura
        
        tk.Label(tab_frame, text="RESUMO:").grid(row=1, column=0, sticky="w")
        self.create_summary_entry = tk.Entry(tab_frame, width=50) 
        self.create_summary_entry.grid(row=1, column=1, sticky="ew", pady=7)

        tk.Label(tab_frame, text="CATEGORIAS (vírgula):").grid(row=2, column=0, sticky="w")
        self.create_category_entry = tk.Entry(tab_frame, width=50) 
        self.create_category_entry.grid(row=2, column=1, sticky="ew", pady=7)

        tk.Label(tab_frame, text="PALAVRAS-CHAVE (vírgula):").grid(row=3, column=0, sticky="w")
        self.create_keywords_entry = tk.Entry(tab_frame, width=50) 
        self.create_keywords_entry.grid(row=3, column=1, sticky="ew", pady=7)

        tk.Label(tab_frame, text="DESCRIÇÃO:").grid(row=4, column=0, sticky="w")
        self.create_description_entry = tk.Entry(tab_frame, width=50) 
        self.create_description_entry.grid(row=4, column=1, sticky="ew", pady=7)

        self.create_button = tk.Button(tab_frame, text="CRIAR NOVO POST", command=self._create_post_gui)
        self.create_button.grid(row=5, column=0, columnspan=2, pady=15)
        tab_frame.grid_columnconfigure(1, weight=1) 

    def _setup_edit_tab(self, tab_frame):
        tk.Label(tab_frame, text="SELECIONE UM POST PARA EDITAR:").grid(row=0, column=0, sticky="w", columnspan=2)
        
        self.edit_post_listbox = tk.Listbox(tab_frame, height=8, width=70) # Menos largo
        self.edit_post_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", pady=7)
        self.edit_post_listbox.bind('<<ListboxSelect>>', self._load_post_data_for_editing) 
        
        self.edit_scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=self.edit_post_listbox.yview)
        self.edit_scrollbar.grid(row=1, column=2, sticky="ns", pady=7)
        self.edit_post_listbox.config(yscrollcommand=self.edit_scrollbar.set)

        tk.Label(tab_frame, text="TÍTULO DO POST:").grid(row=2, column=0, sticky="w")
        self.edit_title_entry = tk.Entry(tab_frame, width=50) # Menos largo
        self.edit_title_entry.grid(row=2, column=1, sticky="ew", pady=7)

        tk.Label(tab_frame, text="RESUMO:").grid(row=3, column=0, sticky="w")
        self.edit_summary_entry = tk.Entry(tab_frame, width=50) 
        self.edit_summary_entry.grid(row=3, column=1, sticky="ew", pady=7)

        tk.Label(tab_frame, text="CATEGORIAS (vírgula):").grid(row=4, column=0, sticky="w")
        self.edit_category_entry = tk.Entry(tab_frame, width=50) 
        self.edit_category_entry.grid(row=4, column=1, sticky="ew", pady=7)

        tk.Label(tab_frame, text="PALAVRAS-CHAVE (vírgula):").grid(row=5, column=0, sticky="w")
        self.edit_keywords_entry = tk.Entry(tab_frame, width=50) 
        self.edit_keywords_entry.grid(row=5, column=1, sticky="ew", pady=7)

        tk.Label(tab_frame, text="DESCRIÇÃO:").grid(row=6, column=0, sticky="w")
        self.edit_description_entry = tk.Entry(tab_frame, width=50) 
        self.edit_description_entry.grid(row=6, column=1, sticky="ew", pady=7)
        
        self.edit_button = tk.Button(tab_frame, text="SALVAR ALTERAÇÕES", command=self._edit_post_gui)
        self.edit_button.grid(row=7, column=0, columnspan=2, pady=15)

        tab_frame.grid_columnconfigure(1, weight=1) 
        tab_frame.grid_columnconfigure(0, weight=1) 

    def _setup_delete_tab(self, tab_frame):
        tk.Label(tab_frame, text="SELECIONE UM POST PARA EXCLUIR:").grid(row=0, column=0, sticky="w", columnspan=2)
        
        self.delete_post_listbox = tk.Listbox(tab_frame, height=15, width=70) # Menos largo
        self.delete_post_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", pady=7)
        
        self.delete_scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=self.delete_post_listbox.yview)
        self.delete_scrollbar.grid(row=1, column=2, sticky="ns", pady=7)
        self.delete_post_listbox.config(yscrollcommand=self.delete_scrollbar.set)

        self.delete_button = tk.Button(tab_frame, text="EXCLUIR POST SELECIONADO", command=self._delete_post_gui)
        self.delete_button.grid(row=2, column=0, columnspan=2, pady=15)

        self.refresh_posts_button = tk.Button(tab_frame, text="ATUALIZAR LISTA DE POSTS", command=lambda: self._load_posts_to_listbox(self.delete_post_listbox))
        self.refresh_posts_button.grid(row=3, column=0, columnspan=2, pady=5)
        tab_frame.grid_columnconfigure(0, weight=1) 


    def _setup_git_tab(self, tab_frame):
        # Configuração da aba Git
        tk.Label(tab_frame, text="URL do Repositório Git:").grid(row=0, column=0, sticky="w")
        self.git_repo_url_entry = tk.Entry(tab_frame, width=70)
        self.git_repo_url_entry.grid(row=0, column=1, sticky="ew", pady=5)
        self.git_repo_url_entry.insert(0, "https://github.com/seu-usuario/seu-repositorio.git") # Exemplo
        
        tk.Label(tab_frame, text="Caminho Local (onde estará o projeto):").grid(row=1, column=0, sticky="w")
        self.git_local_path_entry = tk.Entry(tab_frame, width=70)
        self.git_local_path_entry.grid(row=1, column=1, sticky="ew", pady=5)
        self.git_local_path_entry.insert(0, os.getcwd()) # Padrão para o diretório atual do script

        tk.Label(tab_frame, text="Nome da Branch (Ex: main, master):").grid(row=2, column=0, sticky="w")
        self.git_branch_entry = tk.Entry(tab_frame, width=70)
        self.git_branch_entry.grid(row=2, column=1, sticky="ew", pady=5)
        self.git_branch_entry.insert(0, "main") # Branch padrão

        # Botões de Operação Git
        git_buttons_frame = tk.Frame(tab_frame)
        git_buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(git_buttons_frame, text="CONECTAR / CLONAR", command=self._connect_clone_gui).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(git_buttons_frame, text="BAIXAR ATUALIZAÇÕES", command=self._pull_gui).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(git_buttons_frame, text="ADICIONAR & COMMITAR", command=self._add_commit_gui).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(git_buttons_frame, text="ENVIAR ALTERAÇÕES", command=self._push_gui).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Label(tab_frame, text="Saída dos Comandos Git:").grid(row=4, column=0, sticky="w", columnspan=2, pady=(10,0))
        self.git_output_text = scrolledtext.ScrolledText(tab_frame, wrap=tk.WORD, height=15, width=70)
        self.git_output_text.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=5)

        tab_frame.grid_columnconfigure(1, weight=1)
        tab_frame.grid_rowconfigure(5, weight=1)


    def _run_git_command(self, command_list, cwd=None):
        """Executa um comando Git e exibe a saída no ScrolledText."""
        self.git_output_text.insert(tk.END, f"\n--- Executando: {' '.join(command_list)} ---\n")
        self.git_output_text.see(tk.END)
        self.master.update_idletasks() # Atualiza a GUI para mostrar a mensagem

        try:
            process = subprocess.run(command_list, cwd=cwd, capture_output=True, text=True, check=True, encoding='utf-8')
            self.git_output_text.insert(tk.END, process.stdout)
            self._set_status_message(f"COMANDO GIT EXECUTADO COM SUCESSO!", "success")
            return True
        except subprocess.CalledProcessError as e:
            self.git_output_text.insert(tk.END, f"\nERRO (Código {e.returncode}):\n{e.stderr}")
            self._set_status_message(f"ERRO AO EXECUTAR COMANDO GIT: {e.cmd}", "error")
            return False
        except FileNotFoundError:
            self.git_output_text.insert(tk.END, "\nERRO: Comando 'git' não encontrado. Certifique-se de que o Git está instalado e no seu PATH.\n")
            self._set_status_message("ERRO: GIT NÃO INSTALADO OU NÃO ENCONTRADO NO PATH.", "error")
            return False
        except Exception as e:
            self.git_output_text.insert(tk.END, f"\nERRO INESPERADO: {e}\n")
            self._set_status_message(f"ERRO INESPERADO AO EXECUTAR GIT: {e}", "error")
            return False
        finally:
            self.git_output_text.see(tk.END) # Garante que a saída mais recente seja visível

    def _connect_clone_gui(self):
        repo_url = self.git_repo_url_entry.get().strip()
        local_path = self.git_local_path_entry.get().strip()

        if not repo_url:
            self._set_status_message("A URL DO REPOSITÓRIO NÃO PODE ESTAR VAZIA.", "warning")
            return
        if not local_path:
            self._set_status_message("O CAMINHO LOCAL NÃO PODE ESTAR VAZIO.", "warning")
            return

        if os.path.exists(os.path.join(local_path, ".git")):
            self._set_status_message(f"O diretório '{local_path}' já parece ser um repositório Git. Tentando 'PULL' em vez de 'CLONE'.", "info")
            self._pull_gui() # Se já for um repo, tenta puxar
        elif os.path.exists(local_path) and len(os.listdir(local_path)) > 0:
             messagebox.showerror("Diretório Não Vazio", f"O diretório '{local_path}' existe e não está vazio. Por favor, especifique um diretório vazio para clonar, ou um diretório que não existe.")
             self._set_status_message(f"Diretório '{local_path}' não vazio.", "error")
        else:
            self._set_status_message(f"Clonando repositório de '{repo_url}' para '{local_path}'...", "info")
            if self._run_git_command(["git", "clone", repo_url, local_path], cwd=os.path.dirname(local_path) or None):
                self._set_status_message("CLONE CONCLUÍDO COM SUCESSO!", "success")
            else:
                self._set_status_message("FALHA AO CLONAR O REPOSITÓRIO.", "error")

    def _pull_gui(self):
        local_path = self.git_local_path_entry.get().strip()
        branch = self.git_branch_entry.get().strip()

        if not os.path.exists(os.path.join(local_path, ".git")):
            self._set_status_message("O CAMINHO LOCAL NÃO É UM REPOSITÓRIO GIT VÁLIDO. Tente CLONAR primeiro.", "warning")
            return
        if not branch:
            self._set_status_message("O NOME DA BRANCH NÃO PODE ESTAR VAZIO.", "warning")
            return

        self._set_status_message(f"Baixando atualizações da branch '{branch}' em '{local_path}'...", "info")
        if self._run_git_command(["git", "pull", "origin", branch], cwd=local_path):
            self._set_status_message("ATUALIZAÇÕES BAIXADAS COM SUCESSO!", "success")
        else:
            self._set_status_message("FALHA AO BAIXAR ATUALIZAÇÕES.", "error")

    def _add_commit_gui(self):
        local_path = self.git_local_path_entry.get().strip()

        if not os.path.exists(os.path.join(local_path, ".git")):
            self._set_status_message("O CAMINHO LOCAL NÃO É UM REPOSITÓRIO GIT VÁLIDO. Tente CLONAR primeiro.", "warning")
            return

        self._set_status_message(f"Adicionando arquivos para commit em '{local_path}'...", "info")
        if not self._run_git_command(["git", "add", "."], cwd=local_path):
            self._set_status_message("FALHA AO ADICIONAR ARQUIVOS.", "error")
            return

        commit_message = simpledialog.askstring("Mensagem de Commit", "Digite a mensagem para o commit:", parent=self.master)
        if not commit_message:
            commit_message = "Atualização automática via app" # Mensagem padrão se o usuário cancelar ou deixar vazio
            self._set_status_message("Mensagem de commit vazia ou cancelada. Usando mensagem padrão.", "info")

        self._set_status_message(f"Commitando alterações com a mensagem: '{commit_message}'...", "info")
        if self._run_git_command(["git", "commit", "-m", commit_message], cwd=local_path):
            self._set_status_message("COMMIT REALIZADO COM SUCESSO!", "success")
        else:
            self._set_status_message("FALHA AO REALIZAR O COMMIT.", "error")


    def _push_gui(self):
        local_path = self.git_local_path_entry.get().strip()
        branch = self.git_branch_entry.get().strip()

        if not os.path.exists(os.path.join(local_path, ".git")):
            self._set_status_message("O CAMINHO LOCAL NÃO É UM REPOSITÓRIO GIT VÁLIDO. Tente CLONAR primeiro.", "warning")
            return
        if not branch:
            self._set_status_message("O NOME DA BRANCH NÃO PODE ESTAR VAZIO.", "warning")
            return

        self._set_status_message(f"Enviando alterações da branch '{branch}' para o remoto em '{local_path}'...", "info")
        if self._run_git_command(["git", "push", "origin", branch], cwd=local_path):
            self._set_status_message("ALTERAÇÕES ENVIADAS COM SUCESSO!", "success")
        else:
            self._set_status_message("FALHA AO ENVIAR ALTERAÇÕES.", "error")


    def _load_posts_to_listbox(self, listbox_widget):
        listbox_widget.delete(0, tk.END) 
        if not os.path.exists(POSTS_DIR):
            self._set_status_message(f"DIRETÓRIO '{POSTS_DIR}' NÃO ENCONTRADO.", "error")
            return

        posts = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.html')])
        if not posts:
            self._set_status_message(f"NENHUM POST HTML ENCONTRADO EM '{POSTS_DIR}'.", "info")
            return

        for i, post_file in enumerate(posts):
            listbox_widget.insert(tk.END, f"{i + 1}. {post_file}")
        self._set_status_message(f"LISTA DE POSTS ATUALIZADA. {len(posts)} posts encontrados.", "info")

    def _create_post_gui(self):
        title = self.create_title_entry.get().strip()
        summary = self.create_summary_entry.get().strip()
        category = self.create_category_entry.get().strip()
        keywords = self.create_keywords_entry.get().strip()
        description = self.create_description_entry.get().strip()

        if not all([title, summary, category, keywords, description]):
            self._set_status_message("TODOS OS CAMPOS DE CRIAÇÃO DEVEM SER PREENCHIDOS!", "warning")
            return

        full_content_placeholder = "<p>Este é um post novo. Edite este arquivo HTML para adicionar o conteúdo real!</p>"

        file_slug = slugify(title)
        filename = f"{file_slug}.html"
        post_url = f"/{POSTS_DIR}/{filename}"

        current_date = datetime.date.today()
        month_translation = {
            "January": "Janeiro", "February": "Fevereiro", "March": "Março",
            "April": "Abril", "May": "Maio", "June": "Junho",
            "July": "Julho", "August": "Agosto", "September": "Setembro",
            "October": "Outubro", "November": "Novembro", "December": "Dezembro"
        }
        date_formatted = current_date.strftime("%d de %B de %Y")
        for en, pt in month_translation.items():
            date_formatted = date_formatted.replace(en, pt)

        post_data = {
            "post_title_full": title,
            "post_title_card": title, 
            "post_summary": summary,
            "post_category": category,
            "post_keywords": keywords,
            "post_description": description,
            "post_date_formatted": date_formatted,
            "post_full_content": full_content_placeholder,
            "post_url": post_url
        }

        if not os.path.exists(POSTS_DIR):
            os.makedirs(POSTS_DIR)
        
        full_post_path = os.path.join(POSTS_DIR, filename)
        
        if os.path.exists(full_post_path):
            self._set_status_message(f"AVISO: ARQUIVO '{full_post_path}' JÁ EXISTE. ATUALIZANDO ENTRADA NO INDEX.HTML.", "warning")
            if self._update_index_post_list(new_post_data=post_data):
                 self._set_status_message(f"ENTRADA DO POST '{filename}' ATUALIZADA NO INDEX.HTML (ARQUIVO HTML NÃO RECRIADO).", "success")
                 self._clear_create_fields()
                 self._load_posts_to_listbox(self.delete_post_listbox)
                 self._load_posts_to_listbox(self.edit_post_listbox)
            return

        try:
            with open(full_post_path, "w", encoding="utf-8") as f:
                f.write(FULL_POST_TEMPLATE.format(**post_data))
            self._set_status_message(f"ARQUIVO DE POST '{full_post_path}' CRIADO COM SUCESSO!", "success")

            if self._update_index_post_list(new_post_data=post_data):
                self._set_status_message(f"POST '{filename}' CRIADO E ADICIONADO AO INDEX.HTML. LEMBRE-SE DE EDITAR O CONTEÚDO DO HTML!", "success")
                self._clear_create_fields()
                self._load_posts_to_listbox(self.delete_post_listbox)
                self._load_posts_to_listbox(self.edit_post_listbox)

        except IOError as e:
            self._set_status_message(f"ERRO AO CRIAR O ARQUIVO DE POST: {e}", "error")
        except Exception as e:
            self._set_status_message(f"OCORREU UM ERRO INESPERADO: {e}", "error")

    def _clear_create_fields(self):
        self.create_title_entry.delete(0, tk.END)
        self.create_summary_entry.delete(0, tk.END)
        self.create_category_entry.delete(0, tk.END)
        self.create_keywords_entry.delete(0, tk.END)
        self.create_description_entry.delete(0, tk.END)

    def _load_post_data_for_editing(self, event):
        selected_indices = self.edit_post_listbox.curselection()
        if not selected_indices:
            self._clear_edit_fields()
            return

        index = selected_indices[0]
        selected_display_text = self.edit_post_listbox.get(index)
        self.current_editing_filename = selected_display_text.split(". ", 1)[1] 
        
        full_post_path = os.path.join(POSTS_DIR, self.current_editing_filename)

        try:
            with open(full_post_path, "r", encoding="utf-8") as f:
                content = f.read()

            title_match = re.search(r"<title>(.*?)\s*- Hreff</title>", content)
            summary_match = re.search(r"<meta name=\"description\" content=\"(.*?)\" />", content) 
            keywords_match = re.search(r"<meta name=\"keywords\" content=\"(.*?)\" />", content)
            description_match = re.search(r"<meta name=\"description\" content=\"(.*?)\" />", content)
            category_match = re.search(r"<p class=\"post-category\">Categoria: (.*?)</p>", content)

            self.edit_title_entry.delete(0, tk.END)
            self.edit_title_entry.insert(0, title_match.group(1).strip() if title_match else "")
            
            self.edit_summary_entry.delete(0, tk.END)
            self.edit_summary_entry.insert(0, summary_match.group(1).strip() if summary_match else "") 

            self.edit_category_entry.delete(0, tk.END)
            self.edit_category_entry.insert(0, category_match.group(1).strip() if category_match else "")

            self.edit_keywords_entry.delete(0, tk.END)
            self.edit_keywords_entry.insert(0, keywords_match.group(1).strip() if keywords_match else "")
            
            self.edit_description_entry.delete(0, tk.END)
            self.edit_description_entry.insert(0, description_match.group(1).strip() if description_match else "")

            self._set_status_message(f"DADOS DO POST '{self.current_editing_filename}' CARREGADOS PARA EDIÇÃO.", "info")

        except FileNotFoundError:
            self._set_status_message(f"ERRO: ARQUIVO '{full_post_path}' NÃO ENCONTRADO.", "error")
            self._clear_edit_fields()
        except Exception as e:
            self._set_status_message(f"ERRO AO CARREGAR DADOS DO POST PARA EDIÇÃO: {e}", "error")
            self._clear_edit_fields()

    def _clear_edit_fields(self):
        self.edit_title_entry.delete(0, tk.END)
        self.edit_summary_entry.delete(0, tk.END)
        self.edit_category_entry.delete(0, tk.END)
        self.edit_keywords_entry.delete(0, tk.END)
        self.edit_description_entry.delete(0, tk.END)
        self.current_editing_filename = None 

    def _edit_post_gui(self):
        if not hasattr(self, 'current_editing_filename') or not self.current_editing_filename:
            self._set_status_message("NENHUM POST SELECIONADO PARA EDIÇÃO.", "warning")
            return

        old_filename = self.current_editing_filename
        old_post_path = os.path.join(POSTS_DIR, old_filename)
        old_post_url = f"/{POSTS_DIR}/{old_filename}" 

        new_title = self.edit_title_entry.get().strip()
        new_summary = self.edit_summary_entry.get().strip()
        new_category = self.edit_category_entry.get().strip()
        new_keywords = self.edit_keywords_entry.get().strip()
        new_description = self.edit_description_entry.get().strip()

        if not all([new_title, new_summary, new_category, new_keywords, new_description]):
            self._set_status_message("TODOS OS CAMPOS DE EDIÇÃO DEVEM SER PREENCHIDOS!", "warning")
            return
        
        new_file_slug = slugify(new_title)
        new_filename = f"{new_file_slug}.html"
        new_post_path = os.path.join(POSTS_DIR, new_filename)
        new_post_url = f"/{POSTS_DIR}/{new_filename}"

        if old_filename != new_filename:
            if os.path.exists(new_post_path):
                self._set_status_message(f"ERRO: UM POST COM O NOVO TÍTULO ('{new_filename}') JÁ EXISTE. ESCOLHA UM TÍTULO DIFERENTE.", "error")
                return

            try:
                os.rename(old_post_path, new_post_path)
                self._set_status_message(f"ARQUIVO '{old_filename}' RENOMEADO PARA '{new_filename}'.", "success")
            except OSError as e:
                self._set_status_message(f"ERRO AO RENOMEAR O ARQUIVO DE POST: {e}", "error")
                return
        else:
            self._set_status_message("NOME DO ARQUIVO NÃO FOI ALTERADO.", "info")


        current_date = datetime.date.today()
        month_translation = {
            "January": "Janeiro", "February": "Fevereiro", "March": "Março",
            "April": "Abril", "May": "Maio", "June": "Junho",
            "July": "Julho", "August": "Agosto", "September": "Setembro",
            "October": "Outubro", "November": "Novembro", "December": "Dezembro"
        }
        date_formatted = current_date.strftime("%d de %B de %Y")
        for en, pt in month_translation.items():
            date_formatted = date_formatted.replace(en, pt)

        updated_post_data = {
            "post_title_full": new_title,
            "post_title_card": new_title,
            "post_summary": new_summary,
            "post_category": new_category,
            "post_keywords": new_keywords,
            "post_description": new_description,
            "post_date_formatted": date_formatted, 
            "post_full_content": "" 
        }

        try:
            with open(new_post_path, "r", encoding="utf-8") as f:
                current_html_content = f.read()
            
            content_match = re.search(r'(<div class="post-content post-full-content">.*?)(<div class="post-tags">|</section>)', current_html_content, re.DOTALL)
            if content_match:
                # Pegar o conteúdo entre a tag de abertura e a tag de fechamento ou a próxima seção
                raw_content = content_match.group(1)
                # Remover a tag de abertura para obter apenas o conteúdo interno
                updated_post_data["post_full_content"] = raw_content.replace('<div class="post-content post-full-content">', '').strip()
            else:
                updated_post_data["post_full_content"] = "<p>CONTEÚDO ORIGINAL NÃO ENCONTRADO. ADICIONE O CONTEÚDO DO POST AQUI.</p>"
            
            new_html_output = FULL_POST_TEMPLATE.format(**updated_post_data)

            with open(new_post_path, "w", encoding="utf-8") as f:
                f.write(new_html_output)
            
            self._set_status_message(f"ARQUIVO HTML '{new_filename}' ATUALIZADO COM NOVOS METADADOS.", "success")

        except IOError as e:
            self._set_status_message(f"ERRO AO REESCREVER O ARQUIVO HTML DO POST: {e}", "error")
            return
        except Exception as e:
            self._set_status_message(f"ERRO INESPERADO AO ATUALIZAR O ARQUIVO HTML: {e}", "error")
            return

        if self._update_index_post_list(old_file_path=old_post_url, new_post_data={'post_url': new_post_url, 'post_category': new_category}):
            self._set_status_message(f"POST '{new_filename}' EDITADO E INDEX.HTML ATUALIZADO COM SUCESSO!", "success")
            self._clear_edit_fields()
            self._load_posts_to_listbox(self.edit_post_listbox)
            self._load_posts_to_listbox(self.delete_post_listbox)
        else:
            self._set_status_message(f"ERRO AO ATUALIZAR O INDEX.HTML PARA O POST '{new_filename}'.", "error")


    def _delete_post_gui(self):
        selected_indices = self.delete_post_listbox.curselection()
        if not selected_indices:
            self._set_status_message("NENHUM POST SELECIONADO PARA EXCLUSÃO.", "warning")
            return

        index = selected_indices[0]
        selected_display_text = self.delete_post_listbox.get(index)
        
        selected_post_file = selected_display_text.split(". ", 1)[1] 

        selected_post_path = os.path.join(POSTS_DIR, selected_post_file)
        selected_post_url = f"/{POSTS_DIR}/{selected_post_file}"

        confirmation = messagebox.askyesno("CONFIRMAÇÃO DE EXCLUSÃO", 
                                           f"TEM CERTEZA QUE DESEJA EXCLUIR '{selected_post_file}' E REMOVÊ-LO DO INDEX.HTML?",
                                           icon='warning')
        if confirmation:
            if self._update_index_post_list(old_file_path=selected_post_url, new_post_data=None): 
                try:
                    if os.path.exists(selected_post_path):
                        os.remove(selected_post_path)
                        self._set_status_message(f"ARQUIVO '{selected_post_file}' EXCLUÍDO COM SUCESSO!", "success")
                    else:
                        self._set_status_message(f"ARQUIVO '{selected_post_file}' NÃO ENCONTRADO NO DIRETÓRIO '{POSTS_DIR}'.", "warning")
                    self._load_posts_to_listbox(self.delete_post_listbox)
                    self._load_posts_to_listbox(self.edit_post_listbox) # Atualiza a lista da aba de edição também
                except OSError as e:
                    self._set_status_message(f"ERRO AO EXCLUIR O ARQUIVO '{selected_post_file}': {e}", "error")
                except Exception as e:
                    self._set_status_message(f"OCORREU UM ERRO INESPERADO AO EXCLUIR O POST: {e}", "error")
            else:
                self._set_status_message("FALHA AO ATUALIZAR O INDEX.HTML. POST NÃO EXCLUÍDO.", "error")

if __name__ == "__main__":
    root = tk.Tk()
    app = PostManagerApp(root)
    root.mainloop()