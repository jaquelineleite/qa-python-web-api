# Relatórios e evidências de execução — API

## Objetivo

Disponibilizar um relatório JUnit XML dos testes de API executados pelo GitHub Actions. O relatório permite consultar casos executados, duração e falhas sem adicionar bibliotecas de relatórios ao projeto.

## Como gerar localmente

Na raiz do repositório, com as dependências de `requirements.txt` instaladas:

```bash
python -m pytest tests/test_users_api.py -v --junitxml=reports/api-results.xml
```

O arquivo gerado fica em `reports/api-results.xml`. A pasta `reports/` está no `.gitignore`, pois contém saídas de execução, não código-fonte.

## Como consultar no GitHub Actions

1. Acesse a aba **Actions** do repositório.
2. Abra uma execução do workflow **API tests**.
3. Confira o resultado da etapa **Run API tests and generate JUnit report**.
4. Na seção **Artifacts**, baixe **pytest-api-junit**.
5. Extraia o ZIP e consulte `api-results.xml`.

O artefato é configurado com retenção de **7 dias**. A etapa de upload usa `if: always()` para tentar preservar o relatório mesmo quando o Pytest falha. Se o processo terminar antes de gerar o XML, o upload apenas emitirá um aviso; isso não deve ser interpretado como evidência disponível.

## Critérios de verificação

- O job executa os cinco casos parametrizados de `tests/test_users_api.py`.
- A saída do Pytest apresenta o resultado dos casos.
- O XML é gerado e aparece como artefato para download na execução.
- Se houver falhas nos testes, o job continua com resultado de falha; o upload do relatório não mascara esse resultado.

## Limites

- Este workflow **não executa os dois testes web com Playwright**.
- O XML JUnit registra resultados de testes, não screenshots, vídeos ou cobertura de código.
- A API JSONPlaceholder é um serviço público; indisponibilidade ou alterações externas podem afetar os resultados.
- A configuração de publicação do artefato deve ser considerada **não verificada** até existir uma execução do GitHub Actions com o artefato disponível.
