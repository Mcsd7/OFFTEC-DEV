#!/data/data/com.termux/files/usr/bin/bash
set -eu
ROOT="$(cd "$(dirname "$0")" && pwd)"
BIN="$HOME/.local/bin"
mkdir -p "$BIN"
mkdir -p "$HOME/offtec_workspace"
cp "$ROOT/offtec_dev.py" "$BIN/offtec-dev"
chmod 755 "$BIN/offtec-dev"
chmod +x "$ROOT/install.sh"
case ":$PATH:" in
  *":$BIN:"*) ;;
  *) export PATH="$BIN:$PATH"
     echo "Adicione ao PATH do seu shell: export PATH=\"$BIN:\$PATH\"" ;;
esac
echo "Instalação concluída com sucesso em $BIN/offtec-dev"
echo "Pasta de workspace segura criada em: ~/offtec_workspace"
echo "Execute: offtec-dev"
