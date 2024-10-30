#!/bin/bash

# Verifica se um comando foi fornecido
if [ -z "$1" ]; then
  echo "Uso: $0 <ação>"
  echo "Ações disponíveis:"
  echo "  enviar    - Faz commit e push das mudanças. Exemplo: $0 enviar"
  echo "  remover    - Remove arquivos do repositório. Exemplo: $0 remover <arquivo>"
  echo "  status     - Mostra o status do repositório. Exemplo: $0 status"
  echo "  adicionar   - Adiciona arquivos ao staging. Exemplo: $0 adicionar <arquivo>"
  echo "  branch     - Lista branches ou cria uma nova. Exemplo: $0 branch <nova-branch>"
  echo "  trocar     - Troca para uma branch especificada. Exemplo: $0 trocar <branch>"
  echo "  mesclar    - Mescla a branch especificada. Exemplo: $0 mesclar <branch>"
  echo "  log        - Mostra o histórico de commits. Exemplo: $0 log"
  echo "  pegar      - Puxa mudanças do repositório remoto. Exemplo: $0 pegar"
  echo "  reset      - Restaura alterações no diretório de trabalho. Exemplo: $0 reset"
  echo "  verificar   - Verifica as configurações de conta e repositório remoto. Exemplo: $0 verificar"
  echo "  sair       - Sai do script. Exemplo: $0 sair"
  exit 1
fi

# Captura a ação
action="$1"
shift # Remove o primeiro argumento, agora restam as opções

case $action in
  enviar)
    # Faz commit e push
    commit_message="atualização: $(date '+%Y-%m-%d %H:%M:%S')"
    if git add . && git commit -m "$commit_message" && git push; then
      echo "Mudanças enviadas com sucesso!"
    else
      echo "Erro ao enviar as mudanças."
      exit 1
    fi
    ;;

  remover)
    # Remove arquivos
    if [ -z "$1" ]; then
      echo "Uso: $0 remover <arquivos>"
      exit 1
    fi
    if git rm "$@"; then
      git commit -m "Removendo arquivos: $*"
      git push
      echo "Arquivos removidos com sucesso!"
    else
      echo "Erro ao remover arquivos."
      exit 1
    fi
    ;;

  status)
    git status
    ;;

  adicionar)
    # Adiciona arquivos ao staging
    if [ -z "$1" ]; then
      echo "Uso: $0 adicionar <arquivos>"
      exit 1
    fi
    if git add "$@"; then
      echo "Arquivos adicionados ao staging!"
    else
      echo "Erro ao adicionar arquivos."
      exit 1
    fi
    ;;

  branch)
    # Lista ou cria uma nova branch
    if [ -z "$1" ]; then
      git branch
    else
      if git branch "$1"; then
        echo "Branch '$1' criada com sucesso!"
      else
        echo "Erro ao criar a branch."
        exit 1
      fi
    fi
    ;;

  trocar)
    # Troca para uma branch especificada
    if [ -z "$1" ]; then
      echo "Uso: $0 trocar <branch>"
      exit 1
    fi
    if git checkout "$1"; then
      echo "Mudado para a branch '$1'!"
    else
      echo "Erro ao trocar para a branch '$1'."
      exit 1
    fi
    ;;

  mesclar)
    # Mescla a branch especificada
    if [ -z "$1" ]; then
      echo "Uso: $0 mesclar <branch>"
      exit 1
    fi
    if git merge "$1"; then
      echo "Branch '$1' mesclada com sucesso!"
    else
      echo "Erro ao mesclar a branch '$1'."
      exit 1
    fi
    ;;

  log)
    git log
    ;;

  pegar)
    # Puxa as mudanças do repositório remoto
    if git pull; then
      echo "Mudanças puxadas com sucesso!"
    else
      echo "Erro ao puxar as mudanças."
      exit 1
    fi
    ;;

  reset)
    # Restaura alterações no diretório de trabalho
    if git reset; then
      echo "Mudanças restauradas com sucesso!"
    else
      echo "Erro ao restaurar mudanças."
      exit 1
    fi
    ;;

  verificar)
    # Verifica as configurações de conta e repositório remoto
    if [ ! -d ".git" ]; then
      echo "Não está em um repositório Git."
      read -p "Deseja iniciar um novo repositório? (sim/não): " resposta
      if [[ "$resposta" == "sim" ]]; then
        echo "Inicializando repositório..."
        git init
        git add .
        git commit -m "Commit inicial"
        read -p "Deseja adicionar um repositório remoto? (sim/não): " adicionar_remoto
        if [[ "$adicionar_remoto" == "sim" ]]; then
          read -p "Digite a URL do repositório remoto: " url_remoto
          git remote add origin "$url_remoto"
          echo "Repositório remoto adicionado com sucesso!"
        fi
        echo "Repositório inicializado com sucesso!"
      else
        echo "Saindo..."
        exit 0
      fi
      exit 1
    fi

    echo "Verificando configurações de conta e repositório remoto..."
    
    echo "Usuário configurado:"
    git config --global user.name || echo "Nenhum usuário configurado."
    
    echo "Email configurado:"
    git config --global user.email || echo "Nenhum email configurado."
    
    echo "Repositórios remotos:"
    git remote -v || echo "Nenhum repositório remoto configurado."
    
    echo "Se precisar alterar as configurações, use:"
    echo "  git config --global user.name 'Seu Nome'"
    echo "  git config --global user.email 'seuemail@example.com'"
    ;;

  sair)
    echo "Saindo..."
    exit 0
    ;;

  *)
    echo "Ação desconhecida: $action"
    echo "Ações disponíveis:"
    echo "  enviar    - Faz commit e push das mudanças. Exemplo: $0 enviar"
    echo "  remover    - Remove arquivos do repositório. Exemplo: $0 remover <arquivo>"
    echo "  status     - Mostra o status do repositório. Exemplo: $0 status"
    echo "  adicionar   - Adiciona arquivos ao staging. Exemplo: $0 adicionar <arquivo>"
    echo "  branch     - Lista branches ou cria uma nova. Exemplo: $0 branch <nova-branch>"
    echo "  trocar     - Troca para uma branch especificada. Exemplo: $0 trocar <branch>"
    echo "  mesclar    - Mescla a branch especificada. Exemplo: $0 mesclar <branch>"
    echo "  log        - Mostra o histórico de commits. Exemplo: $0 log"
    echo "  pegar      - Puxa mudanças do repositório remoto. Exemplo: $0 pegar"
    echo "  reset      - Restaura alterações no diretório de trabalho. Exemplo: $0 reset"
    echo "  verificar   - Verifica as configurações de conta e repositório remoto. Exemplo: $0 verificar"
    echo "  sair       - Sai do script. Exemplo: $0 sair"
    exit 1
    ;;
esac
