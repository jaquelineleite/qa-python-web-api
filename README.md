# QA Python — Web & API Automation

Projeto de estudos em Quality Engineering com Python,
Pytest e Playwright, organizado em entregas incrementais.

## Objetivo
Automatizar cenários funcionais de aplicações web
e, futuramente, APIs REST, priorizando qualidade,
rastreabilidade e manutenção.

## Aplicação sob teste
SauceDemo: https://www.saucedemo.com/

## Tecnologias
- Python 3.12
- Pytest
- Playwright
- Page Object Model
- Git

## Arquitetura
- pages/: elementos e ações das páginas
- tests/: cenários automatizados
- docs/: planejamento e rastreabilidade
- pytest.ini: configuração da execução

## Cobertura implementada
- CT-001: login válido
- CT-002: login com senha inválida

## Execução local
Instalar dependências:

python -m pip install -r requirements.txt
python -m playwright install chromium

Executar testes:

python -m pytest -v

## Resultado confirmado
- 2 testes aprovados
- Chromium
- Execução local em 13/11/2026
- 1 aviso de compatibilidade do Pytest

## Próximas entregas
- Automação de API REST
- Fixtures e parametrização
- Validações de dados
- Pipeline CI/CD

## Observações
Projeto independente, sem vínculo com a Sauce Labs.
Os requisitos documentados são cenários de estudo.
