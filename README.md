# QA Python — Web & API Automation

Projeto independente de estudos em Quality Engineering, com testes automatizados em Python. As aplicações sob teste são serviços públicos de demonstração; os cenários são definidos para estudo e não representam requisitos oficiais.

## Aplicações e escopo

| Camada | Aplicação | Ferramentas | Cobertura implementada |
| --- | --- | --- | --- |
| Web | [SauceDemo](https://www.saucedemo.com/) | Playwright + Pytest | Login válido e senha inválida (2 testes) |
| API REST | [JSONPlaceholder](https://jsonplaceholder.typicode.com/) | Requests + Pytest | GET de usuários existentes (IDs 1, 2, 3) e inexistentes (0, 999999): 5 casos parametrizados |

A suíte não implementa testes de banco de dados, carga, segurança, contratos completos de API ou fluxos de compra.

## Organização

- `pages/login_page.py`: Page Object de login web (seletores e ações).
- `data/login_data.py`: massas de autenticação usadas nos testes.
- `tests/test_login.py`: dois cenários de autenticação com Playwright.
- `tests/test_users_api.py`: consultas HTTP e verificações de status e campos JSON.
- `tests/conftest.py`: fixture com URL-base da API.
- `docs/test-plan.md`: plano de testes web e registros históricos de execução.
- `docs/traceability.md`: matriz de rastreabilidade e limites da evidência.
- `docs/test-reports.md`: geração e consulta do JUnit XML de API.
- `.github/workflows/api-tests.yml`: CI **somente de API**, com artefato JUnit XML.

## Pré-requisitos e execução local

Python 3.12 e acesso à internet para as aplicações de demonstração.

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Executar a suíte completa (Web + API, exige Chromium):

```bash
python -m pytest -v --browser chromium
```

Executar somente API, sem navegador:

```bash
python -m pytest tests/test_users_api.py -v
```

Executar somente Web:

```bash
python -m pytest tests/test_login.py -v --browser chromium
```

Gerar relatório JUnit XML da API:

```bash
python -m pytest tests/test_users_api.py -v --junitxml=reports/api-results.xml
```

## Evidências e status

- **Web:** o plano de testes registra aprovação local dos dois cenários em 13/11/2026; isso **não** equivale a uma execução web recente no CI.
- **API:** o workflow [API tests #3](https://github.com/jaquelineleite/qa-python-web-api/actions/runs/43538355446), associado ao PR #5, concluiu com sucesso em 14/11/2026 (UTC). A etapa de geração de relatório e o upload do artefato `pytest-api-junit` foram concluídos; o artefato foi confirmado disponível. O arquivo expira após 7 dias.
- O CI atual **não executa os testes web**. Um job aprovado de API não comprova regressão web.
- Para casos, verificações e limitações, consulte [a matriz de rastreabilidade](docs/traceability.md).

## Limitações e decisões

- Os testes dependem de SauceDemo e JSONPlaceholder, sujeitos a mudanças ou indisponibilidade.
- A validação de API verifica status HTTP e campos selecionados; não cobre esquema completo nem persistência.
- O relatório JUnit XML registra resultados de API, não screenshots, vídeos ou cobertura de código.
- O projeto mantém uma única stack Python/Pytest para Web e API e não adiciona dashboards ou frameworks extras sem necessidade.

Este repositório não é afiliado às aplicações utilizadas.
