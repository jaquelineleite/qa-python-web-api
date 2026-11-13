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
