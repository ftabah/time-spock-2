# Time Spock

Time Spock é uma ferramenta desktop para planejar histórias visualmente. O usuário cria cartões com títulos, descrições e cores, organiza-os livremente em uma ou mais timelines e conecta eventos para representar relações, ramificações e acontecimentos paralelos.

## Recursos

- Criar, editar, mover e excluir cartões.
- Personalizar a cor e o tamanho de cada cartão.
- Criar conexões direcionais entre cartões.
- Inverter ou remover conexões pelo menu contextual da linha.
- Criar e visualizar múltiplas timelines.
- Usar o mesmo cartão em mais de uma timeline.
- Mover a área de trabalho arrastando o fundo.
- Aproximar ou afastar a visualização segurando `Ctrl` e usando a roda do mouse.
- Salvar e abrir projetos em arquivos JSON locais.
- Executar como um único arquivo `.exe` no Windows.

## Executar Durante o Desenvolvimento

Requisitos:

- Windows
- Python 3.11 ou superior

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale a aplicação e as dependências de teste:

```powershell
python -m pip install -e ".[test]"
```

Execute:

```powershell
python -m time_spock
```

Se o pacote ainda não estiver instalado, execute a partir da raiz do projeto com:

```powershell
$env:PYTHONPATH = "src"
python -m time_spock
```

## Executar o Windows

O executável standalone fica em:

```text
dist\TimeSpock.exe
```

Ele já contém Python, PySide6 e o código da aplicação. O usuário final não precisa instalar essas dependências.

## Gerar o Executável

Instale o PyInstaller no ambiente de desenvolvimento:

```powershell
python -m pip install pyinstaller
```

Gere uma nova versão:

```powershell
.\scripts\build_windows.ps1
```

O resultado será escrito em `dist\TimeSpock.exe`.

## Controles Principais

- **Botão esquerdo em um cartão:** selecionar e mover.
- **Botão esquerdo no fundo:** mover a área de trabalho.
- **`Ctrl` + roda do mouse:** aproximar ou afastar a visualização.
- **Botão direito em um cartão:** alterar título, descrição ou cor.
- **Botão direito no fundo:** criar um cartão.
- **Selecionar dois cartões:** usar `Edit > Connect Selected Cards` para criar uma conexão.
- **Botão direito em uma conexão:** inverter sua direção ou removê-la.
- **Alça no canto inferior direito:** redimensionar um cartão.

## Testes

```powershell
python -m pytest
```

Os testes cobrem o modelo de dados, conexões, exclusões, timelines e persistência JSON.

## Documentação Adicional

- [Aceitação manual do MVP](docs/manual-acceptance.md)
- [Especificação](.specs/features/timeline-editor/spec.md)
- [Design técnico](.specs/features/timeline-editor/design.md)