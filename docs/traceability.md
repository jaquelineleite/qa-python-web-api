# Matriz de rastreabilidade e revisão de qualidade

Revisão estática em 17/11/2026 da branch `main`. Requisitos são hipóteses didáticas, não contratos oficiais dos serviços externos. **Presença de teste no código não equivale a execução aprovada.**

| ID | Comportamento esperado | Teste / cobertura | Evidência e limite |
| --- | --- | --- | --- |
| REQ-WEB-001 | Login válido permite acesso | `tests/test_login.py::test_login_valido`; URL e título | Registro local em 13/11; CI Web atual não confirmado nesta revisão |
| REQ-WEB-002 | Senha inválida impede acesso | `tests/test_login.py::test_login_senha_invalida`; mensagem de erro | Registro local em 13/11; CI Web atual não confirmado nesta revisão |
| REQ-API-001 | GET usuários existentes | `test_users_api.py`; IDs 1, 2, 3, status 200 e campos selecionados | Evidência histórica de API no PR #5; nova execução não confirmada |
| REQ-API-002 | GET usuários inexistentes | `test_users_api.py`; IDs 0 e 999999, status 404 e objeto vazio | Evidência histórica de API no PR #5 |
| REQ-API-003 | Contrato estrutural parcial | `test_users_contract.py`; IDs 1 e 10, tipos e campos selecionados | PR #8; não é validação de schema completo |
| REQ-API-004 | Borda do dataset demonstrativo | `test_users_contract.py`; ID 11 retorna 404 | PR #8; depende do dataset externo |
| REQ-API-005 | Propagação de falhas de transporte | `test_users_resilience.py`; ConnectTimeout, ReadTimeout e ConnectionError simulados | PR #9; mocks não comprovam timeout real, retry automático ou latência |
| REQ-API-006 | Nova chamada após falha | `test_users_resilience.py`; duas chamadas explícitas | PR #9; não existe política automática de retry |
| REQ-API-007 | Repetição da mesma chave/payload não duplica pedido | `test_orders_idempotency.py`; 201, depois 200; um registro | PR #10; API local em memória, teste sequencial |
| REQ-API-008 | Mesma chave com payload diferente é rejeitada | `test_orders_idempotency.py`; 409 e um registro | PR #10; contrato didático |
| REQ-API-009 | Chaves distintas geram pedidos distintos | `test_orders_idempotency.py`; dois IDs e dois registros | PR #10; sem banco |
| REQ-API-010 | Chave ausente é rejeitada | `test_orders_idempotency.py`; 400, zero registros | PR #10; sem banco |

## CI e evidências

- [API tests #3](https://github.com/jaquelineleite/qa-python-web-api/actions/runs/43538355446): aprovação histórica documentada em 14/11/2026 para escopo anterior. Não valida automaticamente PRs #8–#10.
- [Workflow API](../.github/workflows/api-tests.yml): executa `test_users_api.py`, `test_users_contract.py`, `test_users_resilience.py` e `test_orders_idempotency.py`; gera `reports/api-results.xml` e publica artefato JUnit com retenção de 7 dias.
- [Workflow Web](../.github/workflows/web-smoke.yml): executa `test_login.py` no Chromium; gera `reports/web-results.xml` e publica artefato JUnit com retenção de 7 dias.
- A consulta ao conector não retornou execuções associadas ao último commit mergeado; isso **não comprova** que não houve execução. Conferir [Actions](https://github.com/jaquelineleite/qa-python-web-api/actions) e os checks do PR antes do merge.
- Relatório JUnit é evidência de execução quando produzido por um job verificável, não de cobertura total, persistência ou comportamento de produção.

## Riscos e decisões técnicas

1. **Concorrência:** `ThreadingHTTPServer` aceita requisições simultâneas, mas o teste duplo mantém `saved` e `created` sem sincronização explícita. Os quatro cenários do PR #10 são sequenciais e não comprovam ausência de corrida. Criar teste determinístico e revisar a seção crítica em PR separado.
2. **Dependências externas:** SauceDemo e JSONPlaceholder podem mudar ou ficar indisponíveis; distinguir falha do produto, ambiente e teste.
3. **Escopo:** sem PostgreSQL, Kafka, persistência, carga ou E2E financeiro; não atribuir essas capacidades ao repositório atual.
4. **Qualidade:** antes de aprovar o PR, conferir diff, checks de API e Web, artefatos e rastreabilidade; não inferir sucesso pelo código.
5. **Separação de mudanças:** este PR é somente documental; nenhuma alteração de comportamento ou nova execução foi produzida por sua criação.

## Checklist de revisão do PR #11

- [x] Inventariar cenários presentes no código até o PR #10.
- [x] Atualizar a matriz com limites e dependências.
- [x] Corrigir a descrição dos workflows.
- [x] Registrar o risco de concorrência.
- [ ] Conferir resultados atuais dos jobs API e Web no GitHub Actions.
- [ ] Validar diff e aprovar merge após revisão humana.
