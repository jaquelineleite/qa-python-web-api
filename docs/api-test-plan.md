# Plano de Testes — API REST

## Objetivo
Validar consultas de usuários por meio de requisições
HTTP GET utilizando Python, Requests e Pytest.

## Aplicação sob teste
JSONPlaceholder
https://jsonplaceholder.typicode.com

## Escopo
- Consulta de usuário existente
- Consulta de usuário inexistente
- Validação de status HTTP
- Validação de campos JSON

## Requisitos de estudo
REQ-API-001: A consulta de um usuário existente
deve retornar HTTP 200 e dados do usuário.

REQ-API-002: A consulta de um usuário inexistente
deve retornar HTTP 404 e um objeto JSON vazio.

Os requisitos representam expectativas verificadas
neste ambiente de estudo.

## Cenários

### CT-API-001 — Usuário existente
Endpoint: GET /users/1
Esperado: HTTP 200, ID 1, nome e e-mail válidos.
Resultado: APROVADO

### CT-API-002 — Usuário inexistente
Endpoint: GET /users/999999
Esperado: HTTP 404 e JSON vazio.
Resultado: APROVADO

## Evidência
Execução local do Pytest em 13/11/2026.
Resultado: 2 testes aprovados em 0,92 segundo.

## Riscos
- Indisponibilidade da API pública
- Mudanças no comportamento dos endpoints
- Dependência de conexão com a internet

## Fora do escopo
- Autenticação
- Escrita e persistência de dados
- Testes de carga
- Validação completa de contrato OpenAPI

## Evolução — Fixtures e parametrização

### Objetivo
Reutilizar a configuração da API e ampliar os dados
de entrada sem duplicar funções de teste.

### Implementação
- Fixture api_base_url em tests/conftest.py
- Parametrização com pytest.mark.parametrize
- Reutilização da lógica de validação dos usuários

### Matriz de execução

| Caso | Entrada | HTTP esperado | Resultado |
|---|---|---|---|
| CT-API-001 | ID 1 | 200 | Aprovado |
| CT-API-003 | ID 2 | 200 | Aprovado |
| CT-API-004 | ID 3 | 200 | Aprovado |
| CT-API-005 | ID 0 | 404 | Aprovado |
| CT-API-002 | ID 999999 | 404 | Aprovado |

### Evidência de regressão
Data: 13/11/2026
Comando: python -m pytest -v
Resultado: 7 testes aprovados em 5,93 segundos.
Abrangência: 2 testes web e 5 testes de API.

### Pendência conhecida
PytestRemovedIn10Warning na execução dos testes web.
Investigar compatibilidade entre Pytest e pytest-playwright.

### Observação sobre cobertura
Os cinco casos de API são executados por duas funções
parametrizadas. A quantidade de execuções não representa
cinco funcionalidades distintas.

As validações de nome e e-mail são verificações básicas
de estrutura e conteúdo, não uma validação completa
de contrato da API.
