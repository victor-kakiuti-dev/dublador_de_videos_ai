# Projeto de Dublagem de Vídeos com IA

Este projeto é um **programa de dublagem de vídeos utilizando inteligência artificial**. Ele automatiza o processo de obtenção de vídeos, processamento de áudio e geração de dublagem, concentrando toda a lógica principal em um único ponto de execução.
Pela complexidade do projeto e a falta de conteúdo online sobre o assunto fiz o uso de inteligência artificial para gerar alguns trechos de código, bem como para aprender mais sobre a área de dublagem de vídeos.

## Visão geral

* O projeto realiza **dublagem automática de vídeos** usando IA.
* Atualmente **não possui interface gráfica**, mas **necessita de uma GUI no futuro** para facilitar o uso por usuários não técnicos.
* Todo o fluxo do sistema é executado a partir do arquivo **`pipeline.py`**, que orquestra as etapas do processo.

## Execução do projeto

Para rodar o projeto corretamente, siga os passos abaixo.

### 0. Clonar o repositório

Clone o repositório para sua máquina local:

```bash
git clone https://github.com/victor-kakiuti-dev/dublador_de_videos_ai.git
```

Entre na pasta do projeto 

```bash
cd dublador_de_videos_ai
```


### 1. Criar e ativar um ambiente virtual com Conda

É recomendado usar um ambiente virtual para evitar conflitos de dependências.

Crie o ambiente:

```bash
conda create -n dub_venv python=3.11
```

Ative o ambiente:

```bash
conda activate dub_venv
```

### 2. Instalar as dependências

Com o ambiente ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```
### 3. Criar .env
Crie um arquivo .env na raiz no projeto e insira a chave api da OpenAi

```
OPENAI_API_KEY= sua_chave_api_aqui
```

### 4. Instalar downloader de vídeos
Execute os seguintes comando no seu terminal
```bash
sudo apt update
sudo apt install yt-dlp
``

### 4. Executar o pipeline

O projeto é executado via terminal, utilizando o módulo principal do pipeline.

Para baixar um vídeo do YouTube e iniciar o processo de dublagem, execute:

```bash
python -m pipeline.run_pipeline --url "url_do_video"
```

Substitua `url_do_video` pela URL do vídeo desejado.

---

Este README descreve apenas o funcionamento básico do projeto. Detalhes internos de implementação e estrutura são intencionalmente omitidos.

