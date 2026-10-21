🟢 OFFTEC DEV

Seu ambiente de desenvolvimento com IA, direto no Android.

Crie aplicações, desenvolva sites e programe scripts com assistência de inteligência artificial usando o Termux. Sem precisar de um computador para começar.

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.1.1-39FF14?style=for-the-badge" alt="Versão 0.1.1">
  <img src="https://img.shields.io/badge/Platform-Android-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android">
  <img src="https://img.shields.io/badge/Environment-Termux-111111?style=for-the-badge" alt="Termux">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="Licença MIT">
</p>---

🚀 Sobre o projeto

O OFFTEC DEV é um ambiente de desenvolvimento baseado em terminal (TUI), criado para facilitar a criação e o gerenciamento de projetos de software diretamente no Android.

Integrando recursos de inteligência artificial com ferramentas do ecossistema de desenvolvimento, o projeto busca tornar a programação mais acessível, prática e produtiva — inclusive para quem não possui um computador.

Em vez de depender de vários comandos executados manualmente, o usuário pode utilizar uma interface organizada para acessar as funções disponíveis no ambiente e trabalhar em seus projetos.

A proposta é simples: transformar o celular em um espaço de desenvolvimento assistido por IA.

✨ Principais recursos

- 🤖 Desenvolvimento assistido por IA: integração com o ecossistema OpenCode e provedores de modelos compatíveis, conforme a configuração.
- 📱 Criado para Android: pensado para funcionar no Termux.
- 🧩 Criação de projetos: fluxo de criação de aplicativos, projetos web e scripts.
- 💻 Interface TUI: navegação por menus diretamente no terminal.
- 🧪 Execução e testes: recursos para executar projetos e identificar testes reconhecidos pelo ambiente.
- 📂 Organização de projetos: diretório de trabalho dedicado para manter os projetos em um local apropriado.
- 🔐 Configuração local: suporte à configuração de credenciais de API sem precisar incorporá-las ao código-fonte.
- 🛠️ Ambiente extensível: desenvolvido para evoluir com novas ferramentas e funcionalidades.

«Os recursos efetivamente disponíveis dependem da versão instalada, das ferramentas presentes no Termux e da configuração do provedor de IA.»

📦 Versão atual — v0.1.1

Correções específicas para Termux

Esta versão concentra-se na confiabilidade da criação e execução de projetos no Android.

O que foi corrigido:

- Diretório de trabalho dedicado: criação de projetos e scripts direcionada para "~/offtec_workspace".
- Permissões de execução: tratamento das permissões necessárias para scripts executáveis, incluindo "chmod +x" quando aplicável.
- Compatibilidade com o armazenamento interno do Termux: evita depender de diretórios compartilhados do Android que podem apresentar restrições de execução, como "noexec".
- Organização do ambiente: separação dos projetos do restante dos arquivos pessoais.

Essas alterações ajudam a reduzir erros relacionados a diretórios inexistentes, permissões e execução de arquivos. O comportamento também depende das permissões do Android, da instalação do Termux e das ferramentas utilizadas por cada projeto.

---

📋 Requisitos

Antes de começar, você precisará de:

- Um dispositivo Android compatível.
- "Termux" (https://github.com/termux/termux-app) instalado.
- Python 3.
- Git.
- Conexão com a internet para baixar dependências e utilizar serviços de IA online.
- Uma chave de API de um provedor compatível, caso a função de IA utilizada exija autenticação.
- OpenCode e demais dependências instalados ou configurados conforme os requisitos do projeto.

Recomendação: prefira uma versão atualizada do Termux obtida por uma fonte oficial, evitando misturar instalações de fontes diferentes.

⚙️ Instalação

1. Atualize os pacotes do Termux

Abra o Termux e execute:

pkg update && pkg upgrade -y

2. Instale os requisitos básicos

pkg install git python -y

3. Baixe o OFFTEC DEV

git clone https://github.com/Mcsd7/OFFTEC-DEV.git

4. Entre no diretório

cd OFFTEC-DEV

5. Execute o instalador

bash install.sh

O instalador deve ser utilizado conforme os recursos e as dependências implementados nesta versão. Se alguma dependência não for instalada automaticamente, consulte "requirements.txt" e as instruções do próprio instalador.

6. Inicie o ambiente

Se o instalador não fornecer um comando de inicialização próprio, o ponto de entrada Python do projeto é:

python offtec_dev.py

Se ocorrer algum erro, confira a mensagem apresentada no terminal antes de reinstalar ou remover arquivos.

---

🧭 Como utilizar

Após iniciar o OFFTEC DEV, navegue pelos menus da interface e escolha a operação desejada.

O fluxo de trabalho geral é:

1. Abra o OFFTEC DEV no Termux.
2. Escolha o tipo de projeto que deseja desenvolver.
3. Configure o provedor de IA, caso ainda não tenha feito isso.
4. Informe os detalhes e os requisitos do projeto.
5. Revise o código e os arquivos gerados.
6. Execute os testes e corrija os problemas encontrados.
7. Continue desenvolvendo dentro do diretório de trabalho.

O comportamento de cada etapa depende da opção selecionada e das ferramentas disponíveis no dispositivo.

📂 Diretório de trabalho

Na versão 0.1.1, o diretório padrão de projetos é:

~/offtec_workspace

No Termux, esse caminho fica dentro do diretório privado do aplicativo, onde os arquivos podem receber permissões de execução compatíveis com o ambiente.

Exemplo de estrutura de projetos:

~/offtec_workspace/
├── meu_app/
├── meu_site/
└── meu_script/

A estrutura acima é apenas ilustrativa: os diretórios serão criados conforme os projetos que você desenvolver.

Por que não usar o armazenamento compartilhado?

Pastas como "~/storage/shared" podem apresentar limitações de permissão e execução. Manter projetos executáveis no diretório privado do Termux evita depender dessas permissões específicas do armazenamento compartilhado.

Se precisar transferir um projeto para outra pasta, verifique as permissões e os requisitos de execução antes de utilizá-lo.

---

🤖 Inteligência artificial e OpenCode

O OFFTEC DEV foi desenvolvido para trabalhar com ferramentas de desenvolvimento assistido por IA, incluindo a integração com o ecossistema OpenCode.

A disponibilidade dos modelos depende do provedor configurado, das credenciais, da conectividade e das compatibilidades existentes na instalação.

Configuração da API

Quando a interface solicitar a configuração da IA:

1. Obtenha uma chave de API diretamente no site oficial do provedor escolhido.
2. Informe a chave no campo apropriado do OFFTEC DEV.
3. Confirme a configuração.
4. Faça um teste de funcionamento antes de iniciar um projeto maior.

Nunca publique chaves de API no GitHub, em capturas de tela, vídeos ou arquivos de configuração compartilhados.

Importante: a utilização de serviços externos pode gerar custos, conforme o provedor e o modelo escolhido. Confira os preços e limites de uso antes de fazer solicitações.

🔐 Segurança e boas práticas

O OFFTEC DEV é uma ferramenta de desenvolvimento. O código produzido por IA pode conter falhas, dependências inseguras ou comportamentos inesperados.

Para utilizar o ambiente com responsabilidade:

- Revise o código antes de executá-lo.
- Não execute comandos gerados por IA sem entender seus efeitos.
- Não compartilhe chaves de API, senhas ou tokens.
- Evite conceder permissões desnecessárias aos scripts.
- Utilize ambientes de teste para projetos desconhecidos.
- Confira as dependências antes de instalá-las.
- Mantenha cópias de segurança dos projetos importantes.
- Teste aplicações antes de utilizá-las com dados reais.

A execução de código no Termux pode afetar os arquivos acessíveis ao aplicativo e, conforme as permissões concedidas, outros recursos do dispositivo.

🛠️ Solução de problemas

Erro de pasta segura não encontrada

Confira se o diretório existe:

mkdir -p ~/offtec_workspace

Depois, verifique se o usuário tem permissão para gravar nele:

touch ~/offtec_workspace/.teste
rm ~/offtec_workspace/.teste

Erro de permissão ao executar scripts

Para um script próprio e confiável, utilize:

chmod +x meu_script.sh

Execute-o a partir do diretório correto:

cd ~/offtec_workspace
./meu_script.sh

Se continuar apresentando erro, verifique o interpretador declarado no script, as dependências e o caminho em que o arquivo está armazenado.

Erro ao executar o OFFTEC DEV

Confirme se está no diretório correto:

cd ~/OFFTEC-DEV

Confira a versão do Python:

python --version

E tente iniciar novamente:

python offtec_dev.py

A IA não responde

Confira:

- Se a conexão com a internet está funcionando.
- Se a chave de API foi configurada corretamente.
- Se o provedor e o modelo selecionados continuam disponíveis.
- Se sua conta possui créditos ou limite de utilização.
- Se o OpenCode e as dependências necessárias estão instalados.

---

🔄 Atualização

Para atualizar o código a partir do GitHub, entre no diretório do repositório:

cd ~/OFFTEC-DEV
git pull --ff-only

Se você instalou o projeto em outro local, utilize o caminho correspondente.

Antes de atualizar, faça backup de eventuais modificações locais. A atualização do código não substitui automaticamente as configurações locais nem garante que dependências adicionais sejam instaladas.

🗺️ Roadmap

O OFFTEC DEV é um projeto em evolução. Entre as áreas que podem receber melhorias estão:

- [ ] Aprimoramento da interface TUI.
- [ ] Melhorias na criação e organização de projetos.
- [ ] Ampliação da detecção de linguagens e ferramentas.
- [ ] Aprimoramento dos fluxos de execução e testes.
- [ ] Diagnóstico mais claro de erros e dependências.
- [ ] Melhorias na integração com provedores de IA.
- [ ] Documentação mais completa para novos usuários.
- [ ] Novos recursos para desenvolvimento diretamente no Android.

Os itens acima representam possibilidades de evolução, não funcionalidades garantidas para a versão atual.

🤝 Contribuições

Contribuições são bem-vindas!

Se você encontrou um problema ou deseja sugerir uma melhoria:

1. Confira se já existe uma issue relacionada.
2. Abra uma issue descrevendo o problema ou a sugestão.
3. Inclua a versão do Termux, do Python e do OFFTEC DEV.
4. Se possível, forneça os passos para reproduzir o problema, removendo dados pessoais e credenciais.
5. Para contribuir com código, crie um fork, prepare suas alterações e envie um pull request.

Mantenha as alterações objetivas e evite incluir tokens, arquivos de configuração privados ou dados pessoais nos commits.

📄 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo ""LICENSE"" (LICENSE) para conhecer os termos de utilização, modificação e redistribuição.

👨‍💻 Desenvolvido por

Mcsd7 — OFFTEC

Projeto open source dedicado a tornar ferramentas de desenvolvimento e tecnologias de IA mais acessíveis no Android.

🔗 Repositório oficial: "github.com/Mcsd7/OFFTEC-DEV" (https://github.com/Mcsd7/OFFTEC-DEV)

---

<p align="center">
  <b>OFFTEC DEV</b><br>
  <i>Seu Android. Suas ideias. Seu ambiente de desenvolvimento.</i>
</p>
