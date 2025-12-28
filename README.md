# Projeto de Dublagem de Vídeos com IA

Este projeto é um **programa de dublagem de vídeos utilizando inteligência artificial**. Ele automatiza o processo de obtenção de vídeos, processamento de áudio e geração de dublagem, concentrando toda a lógica principal em um único ponto de execução.

## Visão geral

* O projeto realiza **dublagem automática de vídeos** usando IA.
* Atualmente **não possui interface gráfica**, mas **necessita de uma GUI no futuro** para facilitar o uso por usuários não técnicos.
* Todo o fluxo do sistema é executado a partir do arquivo **`pipeline.py`**, que orquestra as etapas do processo.

## Execução do projeto

Para rodar o projeto corretamente, siga os passos abaixo.

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

### 3. Executar o pipeline

O projeto é executado via terminal, utilizando o módulo principal do pipeline.

Para baixar um vídeo do YouTube e iniciar o processo de dublagem, execute:

```bash
python -m pipeline.run_pipeline --url "url_do_video"
```

Substitua `url_do_video` pela URL do vídeo desejado.

---

Este README descreve apenas o funcionamento básico do projeto. Detalhes internos de implementação e estrutura são intencionalmente omitidos.

