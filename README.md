<<<<<<< HEAD
# 📊 Sales Analytics Platform

Plataforma completa para análise de vendas, composta por uma API REST desenvolvida com FastAPI e um dashboard interativo construído com Streamlit. Toda a aplicação é containerizada com Docker, facilitando a implantação e escalabilidade.

![Dashboard Preview](link-para-uma-imagem-do-dashboard.png) <!-- Substitua pelo link real de uma imagem do dashboard -->

---

## ✨ Funcionalidades

- 📈 **Dashboard interativo** com métricas de vendas em tempo real
- 🔌 **API RESTful** para consulta e importação de dados
- 📤 **Importação de dados** via upload de arquivos CSV/Excel ou inserção manual
- 🗃️ **Banco de dados relacional** PostgreSQL para persistência
- ⚡ **Cache com Redis** para melhor performance
- 🐳 **Containerização com Docker** e orquestração com Docker Compose
- 🔄 **Recarregamento automático** da API durante o desenvolvimento
- 📊 **Visualizações gráficas** com Plotly
- 🧪 **Dados de exemplo** para testes e demonstração

---

## 🛠️ Tecnologias Utilizadas

| Categoria          | Tecnologias                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Backend            | Python, FastAPI, Uvicorn                                                    |
| Frontend (Dashboard)| Streamlit                                                                  |
| Banco de Dados     | PostgreSQL                                                                 |
| Cache              | Redis                                                                      |
| Containerização    | Docker, Docker Compose                                                     |
| Visualização       | Plotly, Pandas                                                             |
| Comunicação        | HTTP (requests), CORS habilitado                                           |
| Desenvolvimento    | Git, Ambiente virtual Python, Dotenv                                       |

---


---

## 🚀 Como Executar a Plataforma

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados
- Git (opcional, para clonar o repositório)

### Passo a passo

1. **Clone o repositório** (ou copie os arquivos para sua máquina):
   ```bash
   git clone https://github.com/seu-usuario/sales-analytics-platform.git
   cd sales-analytics-platform

---
## Ínicie o serviçocom Docker Compose

docker compose up -d

---

## Acesse os serviços:

Dashboard Streamlit: http://localhost:8501

API FastAPI: http://localhost:8000

Documentação automática da API: http://localhost:8000/docs

Banco PostgreSQL: localhost:5432 (usuário admin, senha admin123)

Redis: localhost:6379

---

## Parar os serviços:

docker compose down

---

## Uso da Plataforma
### Dashboard

* Visão Geral: Exibe KPIs principais (receita total, pedidos, ticket médio, clientes ativos) e gráfico de vendas diárias.

* Análise Detalhada: Lista todas as vendas em formato tabular e estatísticas básicas.

* Importar Dados: Permite fazer upload de arquivos CSV/Excel ou inserir vendas manualmente. Após a importação, o cache é limpo e os novos dados aparecem imediatamente nos gráficos.

Sobre: Informações do projeto.


---

## API Endpoints
Método	Endpoint	Descrição
GET	/	Boas-vindas e lista de endpoints
GET	/health	Status da API
GET	/api/v1/kpis	KPIs principais
GET	/api/v1/sales	Todas as vendas
GET	/api/v1/sales/daily	Vendas diárias (parâmetro days)
GET	/api/v1/sales/by-category	Vendas por categoria
POST	/api/v1/sales/batch	Importar múltiplas vendas (lote)


---

## Capturas de Tela



---

## Testes

Para executar os testes (quando implementados), utilize:
docker compose exec api pytest

---

## 🤝 Contribuição
Contribuições são bem-vindas! Siga os passos:

Faça um fork do projeto

Crie uma branch (git checkout -b feature/nova-funcionalidade)

Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')

Push para a branch (git push origin feature/nova-funcionalidade)

Abra um Pull Request

---

## Autor
Desenvolvido por Gedionir Amaral Paim como projeto educacional para demonstrar boas práticas com Python, FastAPI, Streamlit e Docker.

---

## ⭐️ Se este projeto foi útil, deixe uma estrela no GitHub!


---


## 🔧 Comandos úteis (lista para referência)

Crie também um arquivo `COMMANDS.md` separado com os comandos utilizados:

```markdown
# Comandos Úteis para o Projeto

## Docker Compose

| Comando                                      | Descrição                                      |
|----------------------------------------------|------------------------------------------------|
| `docker compose up -d`                       | Inicia todos os serviços em segundo plano      |
| `docker compose down`                         | Para e remove todos os containers              |
| `docker compose down -v`                      | Para e remove containers **e volumes**         |
| `docker compose ps`                           | Lista o status dos containers                  |
| `docker compose logs -f [serviço]`            | Acompanha logs em tempo real (ex: `api`)       |
| `docker compose restart [serviço]`             | Reinicia um serviço específico                 |
| `docker compose exec [serviço] [comando]`      | Executa um comando dentro do container         |

## Gerenciamento da API

| Comando                                      | Descrição                                      |
|----------------------------------------------|------------------------------------------------|
| `docker compose exec api bash`                | Acessa o terminal da API                       |
| `curl http://localhost:8000/health`           | Testa se a API está saudável                   |
| `curl http://localhost:8000/api/v1/sales`     | Lista todas as vendas via API                  |

## Gerenciamento do Dashboard

| Comando                                      | Descrição                                      |
|----------------------------------------------|------------------------------------------------|
| `docker compose exec dashboard bash`          | Acessa o terminal do dashboard                 |
| `docker compose logs dashboard`               | Ver logs do dashboard                           |

## Banco de Dados

| Comando                                      | Descrição                                      |
|----------------------------------------------|------------------------------------------------|
| `docker compose exec postgres psql -U admin -d sales_db` | Acessa o console PostgreSQL          |
| `docker compose exec postgres pg_dump -U admin sales_db > backup.sql` | Backup do banco de dados |

## Desenvolvimento

| Comando                                      | Descrição                                      |
|----------------------------------------------|------------------------------------------------|
| `python -m venv venv`                         | Cria ambiente virtual (local)                  |
| `source venv/Scripts/activate` (Git Bash)     | Ativa ambiente virtual                         |
| `pip install -r requirements.txt`              | Instala dependências localmente                |
| `uvicorn app.api.main:app --reload`            | Roda API localmente (fora do Docker)           |
| `streamlit run app/dashboard/app.py`           | Roda dashboard localmente                       |

## Manutenção

| Comando                                      | Descrição                                      |
|----------------------------------------------|------------------------------------------------|
| `docker system prune -a`                      | Remove containers, imagens e caches não usados |
| `docker volume prune`                          | Remove volumes não utilizados                  |

---

>>>>>>> 120b10826447558fb4f74a27505b718a9d984165
