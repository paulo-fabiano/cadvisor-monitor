# Monitoramento de Containers

## Sobre o projeto

O projeto foi desenvolvido com o objetivo de facilitar o monitoramento do desempenho dos containers e do host, utilizando ferramentas que coletam, armazenam e exibem métricas de forma eficiente.

## Ferramentas utilizadas

Nesse projeto utilizei
- cAdvisor - Framework que coleta métricas dos containers Docker.
- Node Exporter - Ferramenta para coletar métricas do host.
- Prometheus - Sistema de monitoramento e armazenamento de métricas.
- Script Python - Responsável por coletar métricas dos containers que estão parados a muito tempo.

## Configuração

### Requisitos

- Docker

Caso não possua o Docker instalado pode instalá-lo via script oficial com o comando

    curl -fsSL https://get.docker.com | bash

### Passo a passo

1. Primeiro crie uma rede no Docker com o comando.

        docker network create --driver bridge --subnet=192.168.1.0/24 monitoramento

2. Acesse o diretório `docker` e dentro dele execute o arquivo `compose.yml`.

        docker compose up -d

3. Verifique se os containers foram criados e estão funcionando da forma correta.

        docker ps 

    A saída deverá mostrar cinco containers Docker em execução em background.

4. Com tudo funcionando normal, podemos configurar o Grafana para utilizar o Prometheus e mostrar as métricas no Dashboard.

    4.1 Acesse a url do Grafana.

        http://localhost:3000

    4.2 Configure o Data Source

    1. Faça login no Grafana (usuário e senha padrão: `admin`/`admin`, caso não tenha alterado).
    2. No menu lateral, clique em **Configuration** > **Data Sources**.
    3. Clique em **Add data source** e selecione **Prometheus**.
    4. Insira a URL do Prometheus (geralmente `http://localhost:9090`).
    5. Clique em **Save & Test** para validar a conexão.


    4.3 Importe o Dashboard

    1. No menu lateral, clique em **Dashboards**.
    2. Clique em **New Dashboard** e, em seguida, em **Import**.
    3. Copie o conteúdo do arquivo `template.json`, localizado no diretório `grafana` deste repositório.
    4. Cole o conteúdo no campo de importação ou use o botão de upload para carregar o arquivo.
    5. Clique em **Import** para adicionar o dashboard.

    4.4 Carregando o Dashboard

    Caso o dashboard não seja carregado corretamente na primeira tentativa:  
    1. Acesse o painel problemático clicando nele.
    2. No menu de opções, clique em **Edit**.
    3. Faça qualquer alteração simples (exemplo: altere uma métrica temporariamente).
    4. Clique em **Run queries** para recarregar os dados.
    5. Desfaça as alterações realizadas e clique em **Save**.

    Após esse procedimento, o painel deverá estar funcionando normalmente.

## Funcionamento