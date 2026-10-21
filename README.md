# OFFTEC DEV v0.1.1 (Corrigido para Termux)

Ambiente TUI de desenvolvimento assistido por IA integrado ao **OpenCode** comunitário.

## Correção de Pasta Segura e Execução no Termux
Esta versão corrige o erro de **"pasta segura não encontrada"** ou **"falha de permissão / noexec"** direcionando nativamente a criação de projetos e scripts para o espaço interno seguro do Termux (`~/offtec_workspace`), garantindo as permissões corretas de execução (`chmod +x`).

## Instalação
No Termux, dentro da pasta do projeto:
```bash
chmod +x install.sh
./install.sh
offtec-dev
```
