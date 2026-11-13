# Plano de Testes — Autenticação Web

## Objetivo
Validar o comportamento de autenticação da aplicação
SauceDemo utilizando Python, Pytest e Playwright.

## Escopo
- Login com credenciais válidas
- Login com senha inválida

## Requisitos de teste
REQ-001: Credenciais válidas devem permitir acesso.
REQ-002: Senha inválida deve impedir a autenticação
e apresentar uma mensagem de erro.

Observação: requisitos derivados dos cenários de estudo,
não de uma especificação oficial da aplicação.

## Cenários

### CT-001 — Login válido
Dado que o usuário está na página de login
Quando informa credenciais válidas
Então deve acessar a página de produtos.

Status: APROVADO
Evidência: execução Pytest — 13/11/2026.

### CT-002 — Senha inválida
Dado que o usuário está na página de login
Quando informa uma senha incorreta
Então deve visualizar a mensagem de erro.

Status: APROVADO
Evidência: execução Pytest — 13/11/2026.

## Riscos
- Mudança de seletores da aplicação
- Indisponibilidade do ambiente externo
- Alteração das mensagens de erro

## Pendências
- Investigar aviso de compatibilidade do Pytest
- Configurar evidências automáticas
- Revisar dependências antes do PR
