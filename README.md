# QA Python — Web & API Automation

Projeto independente de estudos em Quality Engineering, com testes automatizados em Python. As aplicações sob teste são serviços públicos de demonstração; os cenários são definidos para estudo e não representam requisitos oficiais.

## Aplicações e escopo

| Camada | Aplicação | Ferramentas | Cobertura implementada |
| --- | --- | --- | --- |
| Web | [SauceDemo](https://www.saucedemo.com/) | Playwright + Pytest | Login válido e senha inválida (2 testes) |
| API REST | [JSONPlaceholder](https://jsonplaceholder.typicode.com/) | Requests + Pytest | GET de usuários existentes (IDs 1, 2, 3) e inexistentes (0, 999999): 5 casos; contrato estrutural selecionado (IDs 1 e 10) e borda do dataset (ID 11): 3 casos adicionais |

A suíte não implementa testes de banco de dados, carga, segurança, contratos completos de API ou fluxos de compra.

## Organização

- `pages/login_page.py`: Page Object de login web (seletores e ações).
- `data/login_data.py`: massas de autenticação usadas nos testes.
- `tests/test_login.py`: dois cenários de autenticação com Playwright.
- `tests/test_users_api.py`: consultas HTTP e verificações de status e campos JSON.
- `tests/test_users_contract.py`: contrato estrutural selecionado e limite do dataset de demonstração.
- `tests/test_users_resilience.py`: falhas simuladas de transporte, sem HTTP externo.
- `api_client.py`: função pequena para GET com timeout configurável e propagação de erros.
- `tests/conftest.py`: fixture com URL-base da API.
- `docs/test-plan.md`: plano de testes web e registros históricos de execução.
- `docs/traceability.md`: matriz de rastreabilidade e limites da evidência.
- `docs/test-reports.md`: geração e consulta do JUnit XML de API.
- `.github/workflows/api-tests.yml`: CI de API com artefato JUnit XML.
- `.github/workflows/web-smoke.yml`: CI de smoke Web com Chromium e relatório JUnit XML (validação do novo workflow pendente).

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
python -m pytest tests/test_users_api.py tests/test_users_contract.py tests/test_users_resilience.py -v
```

Executar somente Web:

```bash
python -m pytest tests/test_login.py -v --browser chromium
```

Gerar relatório JUnit XML da API:

```bash
python -m pytest tests/test_users_api.py tests/test_users_contract.py tests/test_users_resilience.py -v --junitxml=reports/api-results.xml
```

## Evidências e status

- **Web:** o plano de testes registra aprovação local dos dois cenários em 13/11/2026; isso **não** equivale a uma execução web recente no CI.
- **API:** o workflow [API tests #3](https://github.com/jaquelineleite/qa-python-web-api/actions/runs/43538355446), associado ao PR #5, concluiu com sucesso em 14/11/2026 (UTC). A etapa de geração de relatório e o upload do artefato `pytest-api-junit` foram concluídos; o artefato foi confirmado disponível. O arquivo expira após 7 dias.
- O PR #7 propõe um workflow separado de smoke Web com Chromium para os dois testes de login. A execução no GitHub Actions deve ser conferida antes de afirmar que o CI Web está aprovado. Um job aprovado de API não comprova regressão Web.
- Para casos, verificações e limitações, consulte [a matriz de rastreabilidade](docs/traceability.md).

## Limitações e decisões

- Os testes dependem de SauceDemo e JSONPlaceholder, sujeitos a mudanças ou indisponibilidade.
- A validação de API verifica status HTTP e campos selecionados; não cobre esquema completo nem persistência.
- Os relatórios JUnit XML registram resultados de testes, não screenshots, vídeos ou cobertura de código. O novo relatório Web depende da execução bem-sucedida do respectivo workflow.
- O projeto mantém uma única stack Python/Pytest para Web e API e não adiciona dashboards ou frameworks extras sem necessidade.

Este repositório não é afiliado às aplicações utilizadas.

## PR #8 — contrato e borda da API

- Verificações de `Content-Type`, tipos e presença de campos essenciais e estruturas aninhadas (`address.geo` e `company`) para usuários 1 e 10.
- Consulta ao ID 11 como borda do dataset público de demonstração de dez usuários, com expectativa HTTP 404 e objeto vazio.
- Não é validação de esquema OpenAPI completo, persistência, idempotência, timeout ou segurança; o serviço externo pode mudar.
- O CI de API executa ambos os arquivos de teste. **Aprovação do PR #8 depende de execução real no GitHub Actions**; não inferir resultados pelo código.

## PR #9 — timeout e resiliência de transporte

- O cliente `get_user` utiliza `requests.get(..., timeout=10)` por padrão; timeout configurado **não** significa timeout provocado.
- Quatro casos determinísticos verificam `ConnectTimeout`, `ReadTimeout`, `ConnectionError` e uma nova tentativa **explícita** bem-sucedida após falha anterior. Usam `monkeypatch` e `unittest.mock`, sem rede externa ou dependências adicionais.
- A biblioteca Requests não executa retry automático neste cliente. O cenário de recuperação faz duas chamadas separadas, sem afirmar política de retry, backoff, circuit breaker ou recuperação do servidor.
- Os testes simulam exceções e verificam sua propagação; não medem latência, tempo real de espera, paralelismo ou disponibilidade do JSONPlaceholder.
- O workflow de API executa os três módulos e publica JUnit. Resultados somente devem ser declarados aprovados após consultar a execução real no GitHub Actions.

## PR #10 — idempotência de operações de escrita (API local de teste)

- `tests/test_orders_idempotency.py` inicia um servidor HTTP local isolado em porta dinâmica, com endpoint demonstrativo `POST /orders` e cabeçalho `Idempotency-Key`.
- Quatro cenários: repetição da mesma chave e payload sem duplicação; chave repetida com payload diferente retorna 409; chaves distintas criam pedidos distintos; ausência de chave retorna 400.
- O servidor é uma **implementação de teste controlada**, não a API JSONPlaceholder nem um serviço de produção. As regras 201/200/409/400 são um contrato didático definido neste projeto, não um padrão universal.
- O teste verifica respostas HTTP reais sobre loopback e estado em memória; não comprova persistência em banco, concorrência, recuperação após reinício ou idempotência distribuída.
- Executar: `python -m pytest tests/test_orders_idempotency.py -v`. O workflow API inclui esses quatro cenários e publica JUnit.
