# Matriz de rastreabilidade e revisão de qualidade

Escopo observado nos arquivos do repositório em 14/11/2026. Os requisitos abaixo são **hipóteses de estudo**, não especificações oficiais dos serviços.

| ID | Comportamento esperado | Teste automatizado | Verificações implementadas | Evidência / situação |
| --- | --- | --- | --- | --- |
| REQ-WEB-001 / CT-001 | Credenciais válidas permitem login | `tests/test_login.py::test_login_valido` | URL `/inventory.html` e título `Products` | Plano registra aprovação local em 13/11; não verificado no CI |
| REQ-WEB-002 / CT-002 | Senha inválida impede login | `tests/test_login.py::test_login_senha_invalida` | Mensagem de erro contém `Username and password do not match` | Plano registra aprovação local em 13/11; não verificado no CI |
| REQ-API-001 | GET de usuário existente retorna dados coerentes | `tests/test_users_api.py::test_consultar_usuario_existente` | IDs 1, 2, 3; HTTP 200, ID correspondente, nome não vazio e e-mail contendo @ | Workflow API tests #3 aprovado |
| REQ-API-002 | GET de usuário inexistente retorna 404 e objeto vazio | `tests/test_users_api.py::test_consultar_usuario_inexistente` | IDs 0 e 999999; HTTP 404 e JSON `{}` | Workflow API tests #3 aprovado |

## Evidências verificáveis

- [PR #5](https://github.com/jaquelineleite/qa-python-web-api/pull/5): relatórios Pytest e upload do JUnit XML, integrado à `main`.
- [GitHub Actions — API tests #3](https://github.com/jaquelineleite/qa-python-web-api/actions/runs/43538355446): job `Pytest API (Python 3.12)` concluído com sucesso; upload de `pytest-api-junit` confirmado.
- `docs/test-plan.md`: registro de aprovação local web em 13/11/2026, sem link de execução independente ou artefato web. Tratar como registro histórico, não prova de regressão atual.

## Revisão técnica: limites e próximos passos

1. **Separação de camadas:** o workflow atual roda apenas `tests/test_users_api.py`; não atribuir seu resultado aos testes web.
2. **Massa e dependências:** os dados da API vêm de um serviço externo; as credenciais web ficam em `data/login_data.py`. Não há banco local nem isolamento dos serviços.
3. **Asserções:** API valida campos essenciais, mas não todos os tipos, contratos ou propriedades; Web valida os dois comportamentos de login previstos.
4. **Evidências:** JUnit XML da API é temporário (retenção de sete dias); não há evidência automática de screenshot/vídeo web.
5. **Regressão completa:** executar `python -m pytest -v --browser chromium` em ambiente com navegador instalado e registrar o resultado antes de afirmar aprovação da suíte inteira.
6. **Escopo:** ampliar cenários apenas quando houver requisito ou risco concreto; evitar incorporar ferramentas não relacionadas ao objetivo.

**Status desta revisão:** documentação atualizada; nenhuma nova execução de testes foi produzida por esta alteração documental. A aprovação do workflow do PR #5 é evidência histórica, não valida automaticamente este PR.
