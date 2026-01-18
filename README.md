# Projeto de Dublagem de Vídeos com IA

Este projeto é um **programa de dublagem de vídeos utilizando inteligência artificial**. Ele automatiza o processo de obtenção de vídeos, processamento de áudio e geração de dublagem, concentrando toda a lógica principal em um único ponto de execução.
Pela complexidade do projeto e a falta de conteúdo online sobre o assunto fiz o uso de inteligência artificial para gerar alguns trechos de código, bem como para aprender mais sobre a área de dublagem de vídeos.

## Visão geral

* O projeto realiza **dublagem automática de vídeos** usando IA.


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

Recomendo que se use a versão 3.11 do python
Use um ambiente virtual para evitar conflitos de dependências.

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

### 4. Instalar downloader de vídeos e ffmpeg
Execute os seguintes comando no seu terminal
```bash
sudo apt update
sudo apt upgrade
sudo apt install yt-dlp
sudo apt install ffmpeg

``

### 5. Executar o pipeline

O projeto é executado via Flask. Para acessar a interface deve inserir no terminal o seguinte comando: 

```bash
python app.py
```
Logo em seguida você deve inserir uma url de video no input. 

Ainda não testei o limite do pipeline mas acredito que se o vídeo passar de 10 ou 15 minutos a IA pode começar a alucinar.

 Recomendo que o vídeo seja de uma das seguintes plataformas e que não seja muito longo. 

YouTube

Vimeo

Dailymotion

Twitch (VODs e clips)

TikTok

Instagram

Facebook

Twitter / X

Kwai

Bilibili

---

Este README descreve apenas o funcionamento básico do projeto. Detalhes internos de implementação e estrutura são intencionalmente omitidos.

