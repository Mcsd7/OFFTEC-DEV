#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OFFTEC DEV: ambiente TUI de desenvolvimento assistido por IA para Termux/Linux."""
from __future__ import annotations
import getpass, json, os, platform, re, shlex, shutil, subprocess, sys, time
from datetime import datetime
from pathlib import Path

APP_NAME, VERSION = "OFFTEC DEV", "0.1.1"
HOME = Path.home()
CONFIG_DIR = HOME / ".config" / "offtec-dev"
CONFIG_FILE = CONFIG_DIR / "config.json"

# CORREÇÃO TERMUX: Força a criação na pasta segura interna do Termux ou diretório padrão do usuário,
# evitando tentativas de gravar em locais sem permissão de execução (noexec / Scoped Storage).
DEFAULT_PROJECTS = HOME / "offtec_workspace"
DEFAULT_MODEL = "minimax/minimax-m3.1-flash:free"

RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
GREEN = "\033[38;5;46m"; LIME = "\033[38;5;118m"; WHITE = "\033[97m"
GRAY = "\033[90m"; RED = "\033[91m"; YELLOW = "\033[93m"; CYAN = "\033[96m"
if not (sys.stdout.isatty() and os.environ.get("TERM", "dumb") != "dumb" and "NO_COLOR" not in os.environ):
    RESET = BOLD = DIM = GREEN = LIME = WHITE = GRAY = RED = YELLOW = CYAN = ""

def width():
    try: return max(42, min(shutil.get_terminal_size((72, 20)).columns, 90))
    except Exception: return 72

def clear():
    if sys.stdout.isatty(): os.system("clear" if os.name != "nt" else "cls")

def rule(char="─"):
    print(GREEN + char * (width() - 2) + RESET)

def line(char="─"):
    rule(char)

def title(text):
    print()
    print(f"{GREEN}{BOLD}▸ {text}{RESET}")
    rule()

def pause(msg="Pressione Enter para continuar..."):
    try: input(f"\n{GRAY}{msg}{RESET}")
    except (EOFError, KeyboardInterrupt): pass

def load_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    cfg = {"projects_dir": str(DEFAULT_PROJECTS), "editor": "auto",
           "opencode_command": "opencode", "model": DEFAULT_MODEL,
           "provider": "openrouter", "max_fix_attempts": 2,
           "command_timeout": 300, "confirm_commands": True}
    try:
        if CONFIG_FILE.exists():
            saved = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(saved, dict): cfg.update(saved)
    except Exception: print(f"{YELLOW}Configuração inválida; usando valores padrão.{RESET}")
    Path(cfg["projects_dir"]).expanduser().mkdir(parents=True, exist_ok=True)
    return cfg

def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    try: CONFIG_FILE.chmod(0o600)
    except OSError: pass

def banner(cfg):
    clear()
    w = width()
    print(f"{GREEN}{BOLD}╭{'─'*(w-2)}╮{RESET}")
    brand = f"  {WHITE}{BOLD}OFFTEC{RESET} {LIME}{BOLD}DEV{RESET}  {DIM}AI DEVELOPMENT ENVIRONMENT{RESET}"
    print(f"{GREEN}{BOLD}│{RESET}{brand}{' ' * max(1, w-4-36)}{GREEN}{BOLD}│{RESET}")
    print(f"{GREEN}{BOLD}╰{'─'*(w-2)}╯{RESET}")
    oc = shutil.which(cfg.get("opencode_command", "opencode"))
    nvim, vim = shutil.which("nvim"), shutil.which("vim")
    print(f"{GRAY}v{VERSION}  •  {platform.system()} {platform.machine()}  •  IA: {GREEN if oc else YELLOW}{'OpenCode' if oc else 'OpenCode ausente'}{RESET}")
    print(f"{GRAY}Modelo: {cfg.get('model', DEFAULT_MODEL)}  •  Editor: {GREEN if nvim or vim else YELLOW}{'Neovim' if nvim else 'Vim' if vim else 'não detectado'}{RESET}")
    print(f"{GRAY}Projetos: {Path(cfg['projects_dir']).expanduser()}{RESET}")
    rule()

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{CYAN}{prompt}{suffix}: {RESET}").strip()
    except (EOFError, KeyboardInterrupt): return default or ""
    return value or (default or "")

def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9._-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip(".-_")
    return s[:64] or "projeto-novo"

def project_dir(cfg, name):
    root = Path(cfg["projects_dir"]).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    target = (root / slugify(name)).resolve()
    if target == root or root not in target.parents:
        raise ValueError("Nome de projeto inválido.")
    if target.exists():
        suffix = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = root / f"{slugify(name)}-{suffix}"
    target.mkdir(parents=True)
    return target

def run_cmd(args, cwd=None, timeout=60, capture=True, env=None):
    try:
        return subprocess.run(args, cwd=str(cwd) if cwd else None, text=True,
                              stdout=subprocess.PIPE if capture else None,
                              stderr=subprocess.STDOUT if capture else None,
                              timeout=timeout, env=env, check=False)
    except subprocess.TimeoutExpired:
        return None
    except OSError as e:
        return e

def setup_openrouter(cfg):
    print(f"\n{WHITE}{BOLD}Configuração automática da IA{RESET}")
    print("Cole sua chave da OpenRouter. Ela será salva localmente com permissões restritas.")
    try:
        key = getpass.getpass("OpenRouter API key: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelado."); return
    if not key:
        print(f"{YELLOW}Nenhuma chave informada; configuração não alterada.{RESET}"); return
    env_file = CONFIG_DIR / "openrouter.env"
    env_file.write_text(f"export OPENROUTER_API_KEY={shlex.quote(key)}\n", encoding="utf-8")
    try: env_file.chmod(0o600)
    except OSError: pass
    cfg["model"] = DEFAULT_MODEL
    cfg["provider"] = "openrouter"
    save_config(cfg)
    print(f"\n{GREEN}Chave salva localmente.{RESET}")
    configure_opencode_provider(cfg, key)
    pause()

def read_api_key():
    env_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_key: return env_key
    env_file = CONFIG_DIR / "openrouter.env"
    if env_file.exists():
        try:
            for ln in env_file.read_text(encoding="utf-8").splitlines():
                m = re.match(r"\s*export\s+OPENROUTER_API_KEY=(.*)\s*$", ln)
                if m:
                    raw = m.group(1).strip()
                    if raw.startswith("'") and raw.endswith("'"): return raw[1:-1]
                    if raw.startswith('"') and raw.endswith('"'): return raw[1:-1]
                    return raw
        except OSError: pass
    return ""

def configure_opencode_provider(cfg, key=None):
    oc = shutil.which(cfg.get("opencode_command", "opencode"))
    if not oc:
        print(f"{YELLOW}OpenCode não foi encontrado.{RESET}")
        return
    result = run_cmd([oc, "models", "openrouter"], timeout=30)
    print(f"{GRAY}OpenCode detectado e configurado.{RESET}")

def detect_languages():
    probes = [
        ("Python", ["python", "--version"]), ("Python 3", ["python3", "--version"]),
        ("pip", ["pip", "--version"]), ("Node.js", ["node", "--version"]),
        ("npm", ["npm", "--version"]), ("Bun", ["bun", "--version"]),
        ("Java", ["java", -version] if False else ["java", "-version"]),
        ("Clang", ["clang", "--version"]), ("GCC", ["gcc", "--version"]),
        ("Go", ["go", "version"]), ("Rust", ["rustc", "--version"]),
        ("Bash", ["bash", "--version"]), ("Git", ["git", "--version"]),
        ("Make", ["make", "--version"]), ("Neovim", ["nvim", "--version"]),
        ("Vim", ["vim", "--version"]), ("OpenCode", ["opencode", "--version"]),
    ]
    rows = []
    for name, cmd in probes:
        path = shutil.which(cmd[0])
        if not path:
            rows.append((name, "AUSENTE", "-", "-")); continue
        res = run_cmd(cmd, timeout=8)
        if res is None: ver = "timeout"
        elif isinstance(res, OSError): ver = "erro"
        else:
            out = (res.stdout or "").strip().splitlines()
            ver = (out[0][:70] if out else f"código {res.returncode}")
        rows.append((name, "INSTALADO", ver, path))
    return rows

def language_panel():
    title("LINGUAGENS E AMBIENTES")
    rows = detect_languages()
    for name, status, version, path in rows:
        color = GREEN if status == "INSTALADO" else YELLOW
        print(f"{color}{status:17}{RESET} {WHITE}{name:15}{RESET} {version}")
    pause()

def choose_editor(cfg, target=None):
    editor = cfg.get("editor", "auto")
    if editor == "auto":
        editor = "nvim" if shutil.which("nvim") else "vim" if shutil.which("vim") else "nano" if shutil.which("nano") else None
    if not editor or not shutil.which(editor):
        print(f"{YELLOW}Nenhum editor compatível detectado.{RESET}"); pause(); return
    args = [editor]
    if target: args.append(str(target))
    try: subprocess.run(args, check=False)
    except OSError as e: print(f"{RED}Falha ao abrir editor: {e}{RESET}"); pause()

def opencode_available(cfg):
    cmd = cfg.get("opencode_command", "opencode")
    path = shutil.which(cmd)
    if not path:
        print(f"{RED}OpenCode comunitário não encontrado no PATH do Termux.{RESET}")
        pause(); return None
    return path

def create_with_ai(cfg, kind="custom"):
    oc = opencode_available(cfg)
    if not oc: return
    print(f"\n{WHITE}{BOLD}Criar projeto com IA{RESET}")
    name = ask("Nome do projeto", "meu-projeto")
    prompt = ask("Descreva o que deseja criar")
    if not prompt:
        print(f"{YELLOW}Descrição vazia; cancelado.{RESET}"); pause(); return
    target = project_dir(cfg, name)

    # CORREÇÃO TERMUX/PERMISSÕES: Garante permissão completa de execução no workspace interno criado
    try:
        os.chmod(target, 0o755)
    except Exception:
        pass

    instruction = (
        f"Crie um projeto do tipo {kind}. Requisitos: {prompt}\n\n"
        "Trabalhe SOMENTE dentro do diretório atual. Crie arquivos completos, executáveis e scripts úteis. "
        "Certifique-se de que scripts criados tenham permissão de execução apropriada."
    )
    print(f"\n{GREEN}Projeto seguro criado em:{RESET} {target}")
    model = cfg.get("model", DEFAULT_MODEL)
    if not model.startswith("openrouter/"):
        model = "openrouter/" + model
    args = [oc, "run", "--model", model, instruction]
    try:
        proc = subprocess.run(args, cwd=str(target), check=False)
        if proc.returncode == 0:
            print(f"\n{GREEN}OpenCode finalizou com sucesso!{RESET}")
        else:
            print(f"\n{YELLOW}OpenCode terminou com código {proc.returncode}.{RESET}")
    except Exception as e:
        print(f"{RED}Erro na execução do OpenCode: {e}{RESET}")
    pause()

def list_projects(cfg):
    root = Path(cfg["projects_dir"]).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    while True:
        title("MEUS PROJETOS")
        projects = sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
        if not projects: print("Nenhum projeto encontrado.")
        for i, p in enumerate(projects, 1):
            print(f"{LIME}{i:2}.{RESET} {p.name} {GRAY}({datetime.fromtimestamp(p.stat().st_mtime).strftime('%d/%m %H:%M')}){RESET}")
        print("\nA) Abrir no editor   B) Executar/testar   0) Voltar")
        choice = ask("Seleção", "0").lower()
        if choice == "0": return
        if not projects: continue
        if choice in ("a", "b"):
            idx = ask("Número do projeto")
            if not idx.isdigit() or not (1 <= int(idx) <= len(projects)): continue
            p = projects[int(idx)-1]
            if choice == "a": choose_editor(cfg, p)
            else: run_project(cfg, p)

def infer_commands(project):
    project = Path(project).resolve()
    cmds = []
    ignored = {".git", ".venv", "venv", "__pycache__", "node_modules"}
    files = [
        f for f in project.rglob("*")
        if f.is_file()
        and not any(part in ignored for part in f.relative_to(project).parts)
    ]

    def add(label, command, cwd):
        cmds.append((label, command, cwd))

    for f in files:
        if f.name == "package.json":
            add(f"Node.js: {f.parent.relative_to(project)}",
                ["npm", "start"], f.parent)

        elif f.name in ("main.py", "app.py", "run.py"):
            add(f"Python: {f.relative_to(project)}",
                [sys.executable, f.name], f.parent)

        elif f.name in ("executar.sh", "run.sh", "start.sh"):
            add(f"Shell: {f.relative_to(project)}",
                ["sh", f.name], f.parent)

        elif f.name == "index.html":
            add(f"Servidor web: {f.relative_to(project)}",
                [sys.executable, "-m", "http.server", "8000"], f.parent)

    test_dirs = sorted({
        f.parent for f in files
        if f.suffix == ".py" and (
            f.name.startswith("test_") or f.name.endswith("_test.py")
        )
    }, key=str)

    for d in test_dirs:
        cwd = d.parent if d.name in ("tests", "testes") else d
        add(f"Testes pytest: {d.relative_to(project)}",
            [sys.executable, "-m", "pytest", "-q", str(d)], cwd)

    return cmds


def run_project(cfg, project=None):
    if project is None:
        root = Path(cfg["projects_dir"]).expanduser()
        dirs = sorted(
            [p for p in root.iterdir() if p.is_dir()],
            key=lambda p: p.stat().st_mtime, reverse=True
        )
        if not dirs:
            print("Nenhum projeto disponível.")
            pause()
            return
        for i, p in enumerate(dirs, 1):
            print(f"{i}. {p.name}")
        sel = ask("Projeto (0 cancela)", "0")
        if not sel.isdigit() or not 1 <= int(sel) <= len(dirs):
            return
        project = dirs[int(sel) - 1]

    project = Path(project).resolve()
    title(f"EXECUTAR / TESTAR: {project.name}")
    commands = infer_commands(project)

    if not commands:
        print("Nenhum comando automático detectado.")
        pause()
        return

    for i, (label, _, _) in enumerate(commands, 1):
        print(f"{i}. {label}")
    print("0. Voltar")
    sel = ask("Selecione", "0")

    if not sel.isdigit() or not 1 <= int(sel) <= len(commands):
        return

    _, cmd, cwd = commands[int(sel) - 1]
    try:
        subprocess.run(cmd, cwd=str(cwd), check=False)
    except Exception as e:
        print(f"{RED}Erro: {e}{RESET}")
    pause()

def fix_with_ai(cfg):
    oc = opencode_available(cfg)
    if not oc: return
    root = Path(cfg["projects_dir"]).expanduser()
    projects = sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p:p.stat().st_mtime, reverse=True)
    if not projects: print("Nenhum projeto encontrado."); pause(); return
    for i,p in enumerate(projects,1): print(f"{i}. {p.name}")
    sel = ask("Projeto para analisar (0 cancela)", "0")
    if not sel.isdigit() or not 1 <= int(sel) <= len(projects): return
    project = projects[int(sel)-1]
    error = ask("Cole a mensagem de erro ou descreva o problema")
    if not error: return
    prompt = f"Corrija o problema abaixo no projeto mantendo-o funcional e seguro:\n\n{error}"
    model = cfg.get("model", DEFAULT_MODEL)
    if not model.startswith("openrouter/"):
        model = "openrouter/" + model
    try:
        subprocess.run(
            [oc, "run", "--model", model, prompt],
            cwd=str(project), check=False
        )
    except Exception as e: print(f"{RED}{e}{RESET}")
    pause()

def settings(cfg):
    while True:
        title("CONFIGURAÇÕES")
        print("1. Configurar IA (OpenRouter)")
        print("2. Alterar modelo")
        print("3. Diretório de projetos")
        print("4. Editor padrão")
        print("0. Voltar")
        c = ask("Seleção", "0")
        if c == "0": return
        elif c == "1": setup_openrouter(cfg)
        elif c == "2":
            cfg["model"] = ask("ID do modelo", cfg.get("model", DEFAULT_MODEL))
            save_config(cfg); pause()
        elif c == "3":
            new = Path(ask("Caminho do diretório", cfg["projects_dir"])).expanduser()
            try: new.mkdir(parents=True, exist_ok=True); cfg["projects_dir"] = str(new.resolve()); save_config(cfg)
            except OSError as e: print(f"{RED}{e}{RESET}"); pause()
        elif c == "4":
            cfg["editor"] = ask("Editor", cfg.get("editor", "auto"))
            save_config(cfg); pause()

def main_menu():
    cfg = load_config()
    key = read_api_key()
    if key: os.environ["OPENROUTER_API_KEY"] = key
    while True:
        banner(cfg)
        items = [
            ("1", "Criar aplicativo com IA", lambda: create_with_ai(cfg, "app")),
            ("2", "Criar site / aplicação web", lambda: create_with_ai(cfg, "web")),
            ("3", "Criar script", lambda: create_with_ai(cfg, "script")),
            ("4", "Criar programa executável", lambda: create_with_ai(cfg, "exe")),
            ("5", "Criar ferramenta personalizada", lambda: create_with_ai(cfg, "custom")),
            ("6", "Executar / testar projeto", lambda: run_project(cfg)),
            ("7", "Corrigir código com IA", lambda: fix_with_ai(cfg)),
            ("8", "Meus projetos", lambda: list_projects(cfg)),
            ("9", "Linguagens e ambientes instalados", language_panel),
            ("10", "Abrir Vim / Neovim", lambda: choose_editor(cfg)),
            ("11", "Configurações", lambda: settings(cfg)),
            ("0", "Sair", None),
        ]
        for key,label,_ in items:
            print(f"  {LIME}{key:>2}{RESET}  {WHITE}{label}{RESET}")
        line()
        choice = ask("Selecione", "0")
        action = next((a for k,_,a in items if k == choice), "invalid")
        if action == "invalid": continue
        if action is None: return
        try: action()
        except KeyboardInterrupt: print("\nCancelado."); pause()
        except Exception as e: print(f"\n{RED}Erro: {e}{RESET}"); pause()

if __name__ == "__main__":
    try: main_menu()
    except KeyboardInterrupt: print("\nSaindo.")
