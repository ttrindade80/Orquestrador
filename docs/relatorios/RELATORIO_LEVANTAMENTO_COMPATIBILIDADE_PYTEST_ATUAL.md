# RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL

## 1. Identificacao

```yaml
etapa: LEVANTAMENTO_DOCUMENTAL_OU_ARQUITETURAL
papel: investigador tecnico-documental
data: 2026-07-21
raiz_git: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch: master
HEAD: 23f49d0 docs: aplica nomenclatura modular e leitura seletiva
relatorio_de_saida: docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
```

## 2. Objetivo e limites

Objetivo: determinar o estado atual e reproduzivel da compatibilidade da suite
do Orquestrador com `pytest`.

Limites observados:

- nao houve correcao de testes, nomes, fixtures, configuracao ou codigo;
- nao houve criacao de `pytest.ini`, `conftest.py` ou qualquer configuracao;
- nao houve ADR, handoff, QA, stage, commit ou push;
- o unico arquivo criado por esta etapa foi este relatorio.

## 3. Estado Git inicial observado

Comandos executados a partir da raiz real do repositorio:

```bash
git status --short --untracked-files=all
git branch --show-current
git log -1 --oneline
git diff --cached --name-only
```

Resultado observado:

```yaml
branch: master
HEAD: 23f49d0 docs: aplica nomenclatura modular e leitura seletiva
stage: VAZIO
workspace: COM_ARQUIVO_NAO_RASTREADO
arquivos_nao_rastreados:
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
divergencia_do_estado_inicial_esperado: nao
```

Evidencia material:

```text
?? docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
```

## 4. Arquivos criados ou alterados pela etapa

```yaml
arquivos_criados:
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
arquivos_alterados: []
arquivos_removidos: []
arquivos_movidos: []
stage_alterado: nao
```

## 5. Inventario atual dos testes

Foram localizados 10 arquivos relevantes por `rg --files -g 'teste_*.py'`.

| caminho | forma_de_execucao_direta | participa_da_suite_historica | participa_da_suite_atual | coletado_pelo_pytest | quantidade_de_testes_ou_verificacoes | observacoes |
| --- | --- | --- | --- | --- | ---: | --- |
| `tela/teste_loader.py` | `PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py` | sim, no grupo historico de scripts diretos | sim | padrao: nao; explicito: sim, 19 itens | 512 verificacoes diretas; 19 itens pytest explicito | Seis funcoes historicas agora usam fixture `tmp_path`; ha tambem `teste_config_lancador_h0034(tmp_path)`. |
| `tela/teste_modelo.py` | `PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py` | sim | sim | padrao: nao; explicito: sim, 15 itens | 186 verificacoes diretas; 15 itens pytest explicito | Coleta explicita passa. |
| `tela/teste_renderizador.py` | `PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py` | sim | sim | padrao: nao; explicito: sim, 292 itens | 1290 verificacoes diretas; 292 itens pytest explicito | Coleta explicita passa, mas produz avisos de retorno nao-None em tres funcoes. |
| `tela/teste_distribuicao_matricial.py` | `PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py` | nao, posterior ao relatorio historico | sim | padrao: nao; explicito: sim, 25 itens | 36 verificacoes diretas; 25 itens pytest explicito | Novo script da suite atual, compativel na coleta explicita. |
| `demo/teste_diagnostico.py` | `PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py` | sim | sim | padrao: nao; explicito: sim, 6 itens | 48 verificacoes diretas; 6 itens pytest explicito | `teste_modo_executavel(resultado_esperado)` ainda exige argumento posicional nao definido como fixture. |
| `demo/teste_demo.py` | `PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo.py` | sim | sim | padrao: nao; explicito: sim, 15 itens | 363 verificacoes diretas; 15 itens pytest explicito | Importa `pytest` e define fixture `modelo`; quatro funcoes usam `modelo` e passam na coleta explicita. |
| `demo/teste_demo_console.py` | `PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console.py` | nao, posterior ao relatorio historico | sim | padrao: nao; explicito: sim, 6 itens | 116 verificacoes diretas; 6 itens pytest explicito | Novo script da suite atual, compativel na coleta explicita. |
| `demo/teste_demo_console_modos.py` | `PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console_modos.py` | nao, posterior ao relatorio historico | sim | padrao: nao; explicito: sim, 11 itens | 80 verificacoes diretas; 11 itens pytest explicito | Adicionado pelo H-0037; compativel na coleta explicita. |
| `demo/teste_demo_distribuicao.py` | `PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py` | nao, posterior ao relatorio historico | sim | padrao: nao; explicito: sim, 14 itens | 109 verificacoes diretas; 14 itens pytest explicito | Novo script da suite atual, compativel na coleta explicita. |
| `demo/teste_explorar_barra_de_menus.py` | `PYTHONDONTWRITEBYTECODE=1 python demo/teste_explorar_barra_de_menus.py` | sim | sim | padrao: nao; explicito: sim, 19 itens | 38 verificacoes diretas; 19 itens pytest explicito | Coleta explicita passa. |

Observacao: `python -m pytest` sem argumentos nao coleta nenhum dos 10 arquivos,
pois nao ha configuracao local que inclua o padrao `teste_*.py` na descoberta
padrao do pytest. Quando os arquivos sao fornecidos explicitamente ao pytest,
as funcoes e classes internas sao coletadas.

## 6. Definicao documental da suite

Documento atual mais direto localizado: `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md`.

Evidencias:

- secao 23.1 lista 9 scripts de baseline direta;
- secao 23.2 adiciona `demo/teste_demo_console_modos.py`;
- secao 23.2 afirma que a suite prevista passa a possuir dez scripts;
- secao 23.4 define que o comando canonico e `PYTHONDONTWRITEBYTECODE=1 python <script>`, a partir da raiz, e que os scripts sao executados diretamente, nao via `pytest`;
- a matriz da secao 31 confirma: "Comando canonico e execucao direta (nao pytest)".

Classificacao:

```text
SUITE_CANONICA_ATUAL_FORMALIZADA_EM_HANDOFF_H-0037
```

Restricao documental ainda relevante: a definicao esta em handoff com status
`AGUARDANDO_QA`, nao em contrato, ADR ou arquivo de configuracao executavel da
suite. Portanto, antes de criar handoff corretivo, ainda ha decisao de processo
sobre onde formalizar a politica de pytest.

## 7. Configuracao atual do pytest

Verificacoes executadas:

```bash
find . -name pytest.ini -o -name pyproject.toml -o -name setup.cfg -o -name tox.ini -o -name conftest.py
find . -maxdepth 3 -name requirements.txt -o -name requirements-dev.txt -o -name setup.py -o -name Pipfile -o -name poetry.lock -o -name environment.yml -o -name environment.yaml
env
python -m pytest --version
```

Resultado:

| item | classificacao | evidencia |
| --- | --- | --- |
| `pytest.ini` | AUSENTE | `find` sem saida |
| `pyproject.toml` | AUSENTE | `find` sem saida |
| `setup.cfg` | AUSENTE | `find` sem saida |
| `tox.ini` | AUSENTE | `find` sem saida |
| `conftest.py` | AUSENTE | `find` sem saida |
| regras de ignore do pytest | AUSENTE | nenhum arquivo de configuracao pytest localizado |
| padroes personalizados de coleta | AUSENTE | nenhum `python_files`, `python_classes` ou `python_functions` localizado |
| opcoes padrao do pytest | AUSENTE | nenhum `addopts` localizado |
| plugins obrigatorios declarados | AUSENTE | nao ha dependencias/config declaradas; ambiente carregou `anyio-4.14.2` e `typeguard-4.5.2` |
| variaveis de ambiente pytest | AUSENTE | `env` nao mostrou `PYTEST_*` |
| dependencias declaradas | AUSENTE | nenhum `requirements`, `setup.py`, `Pipfile`, `poetry.lock` ou `environment.yml` localizado |
| `.pytest_cache/` | PRESENTE | existe no filesystem, mas nao e configuracao nem prova compatibilidade |

Versao observada:

```text
pytest 9.0.3
platform linux -- Python 3.14.6, pytest-9.0.3, pluggy-1.6.0
plugins: anyio-4.14.2, typeguard-4.5.2
```

## 8. Resultado da execucao direta

Comandos executados separadamente, sem alterar arquivos do projeto:

| comando | codigo_de_saida | verificacoes_aprovadas | verificacoes_falhas | erros | duracao_aproximada |
| --- | ---: | ---: | ---: | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py` | 0 | 48 | 0 | nenhum | < 1s |
| `PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py` | 0 | 1290 | 0 | nenhum | < 1s observado pela chamada |
| `PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console.py` | 0 | 116 | 0 | nenhum | < 1s |
| `PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py` | 0 | 186 | 0 | nenhum | < 1s |
| `PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console_modos.py` | 0 | 80 | 0 | nenhum | < 1s |
| `PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo.py` | 0 | 363 | 0 | nenhum | ~2s |
| `PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py` | 0 | 36 | 0 | nenhum | < 1s |
| `PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py` | 0 | 512 | 0 | nenhum | < 1s observado pela chamada |
| `PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py` | 0 | 109 | 0 | nenhum | ~12s |
| `PYTHONDONTWRITEBYTECODE=1 python demo/teste_explorar_barra_de_menus.py` | 0 | 38 | 0 | nenhum | < 1s |

Consolidado:

```yaml
total_de_scripts: 10
total_de_verificacoes: 2778
total_de_falhas: 0
total_de_erros: 0
todos_com_saida_zero: true
```

## 9. Resultado da coleta

### 9.1 Coleta pytest padrao

```yaml
comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only
codigo_de_saida: 5
itens_coletados: 0
testes_aprovados: 0
testes_falhos: 0
erros_de_coleta: 0
erros_de_execucao: 0
avisos: 0
mensagem_material: no tests collected in 0.02s
```

Interpretacao: a coleta padrao atual nao encontra os arquivos `teste_*.py`.
O codigo 5 decorre de ausencia de testes coletados, nao de falha material dos
testes.

### 9.2 Coleta pytest explicita dos 10 arquivos

Comando complementar executado para comparar com o relatorio historico:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only tela/teste_loader.py tela/teste_modelo.py tela/teste_renderizador.py tela/teste_distribuicao_matricial.py demo/teste_diagnostico.py demo/teste_demo.py demo/teste_demo_console.py demo/teste_demo_console_modos.py demo/teste_demo_distribuicao.py demo/teste_explorar_barra_de_menus.py
```

Resultado:

```yaml
codigo_de_saida: 0
itens_coletados: 422
testes_aprovados: 0
testes_falhos: 0
erros_de_coleta: 0
erros_de_execucao: 0
avisos: 0
```

Contagem por arquivo:

```yaml
tela/teste_loader.py: 19
tela/teste_modelo.py: 15
tela/teste_renderizador.py: 292
tela/teste_distribuicao_matricial.py: 25
demo/teste_diagnostico.py: 6
demo/teste_demo.py: 15
demo/teste_demo_console.py: 6
demo/teste_demo_console_modos.py: 11
demo/teste_demo_distribuicao.py: 14
demo/teste_explorar_barra_de_menus.py: 19
total: 422
```

## 10. Resultado da execucao com pytest

### 10.1 Execucao pytest padrao

```yaml
comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
codigo_de_saida: 5
itens_coletados: 0
testes_aprovados: 0
testes_falhos: 0
erros_de_coleta: 0
erros_de_execucao: 0
avisos: 0
mensagem_material: no tests ran in 0.03s
```

### 10.2 Execucao pytest explicita dos 10 arquivos

```yaml
comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py tela/teste_modelo.py tela/teste_renderizador.py tela/teste_distribuicao_matricial.py demo/teste_diagnostico.py demo/teste_demo.py demo/teste_demo_console.py demo/teste_demo_console_modos.py demo/teste_demo_distribuicao.py demo/teste_explorar_barra_de_menus.py
codigo_de_saida: 1
itens_coletados: 422
testes_aprovados: 421
testes_falhos: 0
erros_de_coleta: 0
erros_de_execucao: 1
avisos: 7
duracao_observada: 16.66s
```

Erro nominal:

```yaml
- arquivo: demo/teste_diagnostico.py
  objeto: demo/teste_diagnostico.py::teste_modo_executavel
  categoria: erro_de_setup_pytest_fixture_ausente
  mensagem_material: "fixture 'resultado_esperado' not found"
  origem_provavel: LEGADA_COMPROVADA
  evidencia:
    - relatorio_historico: erro 10, fixture ausente resultado_esperado
    - git_blame: 54e85090, 2026-07-07, assinatura def teste_modo_executavel(resultado_esperado)
```

Avisos nominais da execucao explicita:

```yaml
- categoria: PytestReturnNotNoneWarning
  quantidade: 7
  objetos:
    - tela/teste_loader.py::teste_caminho_feliz
    - tela/teste_modelo.py::teste_modelo_orquestrador
    - tela/teste_renderizador.py::teste_renderizador_orquestrador
    - tela/teste_renderizador.py::teste_renderizador_destino_minimo
    - tela/teste_renderizador.py::teste_renderizador_grupo_minimo
    - demo/teste_diagnostico.py::teste_invariantes_anteriores
    - demo/teste_diagnostico.py::teste_gerar_diagnostico
  mensagem_material: funcoes coletadas como testes retornam objeto diferente de None
  origem_provavel: NAO_CONFIRMADA
```

## 11. Comparacao com o relatorio historico

Relatorio comparado:
`docs/relatorios/RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md`.

Matriz:

| Incompatibilidade historica | Ainda existe | Quantidade anterior | Quantidade atual | Mudanca comprovada | Evidencia |
| --------------------------- | -----------: | ------------------: | ---------------: | ------------------ | --------- |
| `tmp_base` ausente em `tela/teste_loader.py` | nao | 6 | 0 | sim | `git blame` mostra `be9612ac` alterando as assinaturas para `tmp_path`; pytest explicito executou `tela/teste_loader.py` sem erro. |
| `modelo` ausente em `demo/teste_demo.py` | nao | 3 | 0 | sim | `demo/teste_demo.py` define `@pytest.fixture(name="modelo")` em `c90349cd`; pytest explicito executou as funcoes com `modelo` sem erro. |
| `resultado_esperado` ausente em `demo/teste_diagnostico.py` | sim | 1 | 1 | nao, permanece | pytest explicito falhou em `demo/teste_diagnostico.py::teste_modo_executavel`; `git blame` aponta origem `54e85090`. |
| ausencia historica de configuracao pytest | sim | 5 arquivos ausentes | 5 arquivos ausentes | nao, permanece | `pytest.ini`, `pyproject.toml`, `setup.cfg`, `tox.ini` e `conftest.py` ausentes. |
| comando pytest como gate sem suporte integral | parcialmente | 10 erros na coleta/execucao explicita | 1 erro na execucao explicita; 0 itens no pytest padrao | sim, melhorou parcialmente | coleta explicita: 422 itens; execucao explicita: 421 passed, 1 error; execucao padrao: 0 itens, codigo 5. |

Separacao requerida:

```yaml
incompatibilidades_ja_existentes_na_origem:
  - demo/teste_diagnostico.py::teste_modo_executavel exige resultado_esperado posicional sem fixture pytest.
incompatibilidades_introduzidas_posteriormente:
  - nenhuma incompatibilidade nova comprovada nesta etapa.
incompatibilidades_historicas_corrigidas_ou_superadas:
  - seis erros de tmp_base em tela/teste_loader.py foram superados pela troca para tmp_path em be9612ac.
  - tres erros de modelo em demo/teste_demo.py foram superados por fixture pytest em c90349cd.
novos_testes_compativeis:
  - tela/teste_distribuicao_matricial.py: 25 itens pytest explicitos passam.
  - demo/teste_demo_console.py: 6 itens pytest explicitos passam.
  - demo/teste_demo_console_modos.py: 11 itens pytest explicitos passam.
  - demo/teste_demo_distribuicao.py: 14 itens pytest explicitos passam.
fatos_nao_confirmados:
  - origem historica completa dos 7 PytestReturnNotNoneWarning atuais.
  - se a politica futura deve tratar warning pytest como incompatibilidade bloqueante.
```

## 12. Incompatibilidades atuais

```yaml
- id: PYTEST-PADRAO-SEM-COLETA
  escopo: python -m pytest
  severidade_processual: alta se pytest for canonico; baixa se pytest continuar auxiliar
  estado: atual
  fato: pytest padrao coleta 0 itens e retorna codigo 5.
  origem_provavel: configuracao ausente e padrao pytest nao inclui teste_*.py

- id: PYTEST-EXPLICITO-RESULTADO_ESPERADO
  escopo: python -m pytest <10 arquivos>
  severidade_processual: alta se coleta explicita dos scripts for gate obrigatorio
  estado: atual
  fato: demo/teste_diagnostico.py::teste_modo_executavel falha no setup por fixture ausente resultado_esperado.
  origem_provavel: LEGADA_COMPROVADA

- id: PYTEST-EXPLICITO-WARNINGS-RETORNO
  escopo: python -m pytest <10 arquivos>
  severidade_processual: media/baixa enquanto forem avisos
  estado: atual
  fato: 7 PytestReturnNotNoneWarning em funcoes que retornam objetos/bool/string.
  origem_provavel: NAO_CONFIRMADA
```

## 13. Alternativas sem decisao

```yaml
- alternativa: manter execucao direta como canonica e registrar pytest como nao-canonico
  arquivos_provavelmente_afetados:
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/handoff futuros
  vantagens_objetivas:
    - preserva a suite atual de 10 scripts com 2778/2778 verificacoes passando
    - evita alterar harness legado
  riscos_objetivos:
    - pytest padrao continuara retornando codigo 5
    - ferramentas externas que esperem pytest podem interpretar ausencia de coleta como falha
  preserva_execucao_direta: sim
  altera_coleta_do_pytest: nao
  exige_decisao_do_usuario: sim

- alternativa: configurar pytest para coletar explicitamente teste_*.py
  arquivos_provavelmente_afetados:
    - pytest.ini ou pyproject.toml
    - possivelmente demo/teste_diagnostico.py
  vantagens_objetivas:
    - `python -m pytest` deixaria de coletar zero itens
    - torna a politica de coleta material e reproduzivel
  riscos_objetivos:
    - exporia o erro remanescente de resultado_esperado
    - pode transformar warnings atuais em ruido processual permanente
  preserva_execucao_direta: sim, se nenhum teste for alterado
  altera_coleta_do_pytest: sim
  exige_decisao_do_usuario: sim

- alternativa: converter helpers parametrizados restantes para testes nativos pytest
  arquivos_provavelmente_afetados:
    - demo/teste_diagnostico.py
    - possivelmente outros scripts com retornos nao-None
  vantagens_objetivas:
    - permite equivalencia maior entre suite direta e pytest
    - remove erro remanescente de fixture ausente
  riscos_objetivos:
    - pode alterar fluxo direto atual se nao for feito com cuidado
    - exige criterio de equivalencia entre verificacoes diretas e itens pytest
  preserva_execucao_direta: a decidir
  altera_coleta_do_pytest: sim
  exige_decisao_do_usuario: sim

- alternativa: configurar pytest para ignorar `teste_*.py` e manter somente testes `test_*.py`
  arquivos_provavelmente_afetados:
    - pytest.ini ou pyproject.toml
  vantagens_objetivas:
    - evita coleta acidental dos scripts diretos
    - deixa claro que os scripts `teste_*.py` nao sao suite pytest
  riscos_objetivos:
    - `python -m pytest` pode continuar coletando zero itens ate haver testes pytest nativos
    - nao mede a suite direta
  preserva_execucao_direta: sim
  altera_coleta_do_pytest: sim
  exige_decisao_do_usuario: sim

- alternativa: criar suite pytest nativa separada e manter scripts diretos
  arquivos_provavelmente_afetados:
    - novo diretorio ou novos arquivos `test_*.py`
    - possivel configuracao pytest
  vantagens_objetivas:
    - separa harness legado de testes pytest
    - permite adoção incremental de pytest sem quebrar execucao direta
  riscos_objetivos:
    - duplica cobertura se nao houver criterio claro
    - aumenta custo de manutencao
  preserva_execucao_direta: sim
  altera_coleta_do_pytest: sim
  exige_decisao_do_usuario: sim
```

## 14. Decisoes pendentes

```yaml
- decisao: se a execucao direta continuara canonica
  estado: pendente
  evidencia: H-0037 define execucao direta como canonica, mas nao ha contrato/config executavel consolidando isso.

- decisao: se pytest sera canonico ou auxiliar
  estado: pendente
  evidencia: pytest padrao coleta 0 itens; pytest explicito tem 1 erro.

- decisao: se funcoes auxiliares com prefixo teste_ serao renomeadas
  estado: pendente
  evidencia: historico mostra que prefixo teste_ causou coleta quando arquivos sao passados explicitamente ao pytest.

- decisao: se a coleta sera configurada para ignorar funcoes/scripts legados
  estado: pendente
  evidencia: nao ha configuracao pytest atual.

- decisao: se os scripts serao convertidos para testes nativos do pytest
  estado: pendente
  evidencia: 421 itens explicitos passam; 1 ainda falha por fixture ausente; 7 avisam retorno nao-None.

- decisao: se todos os dez arquivos atuais integram a suite obrigatoria
  estado: pendente_formalmente
  evidencia: H-0037 indica dez scripts; falta consolidacao normativa fora do handoff.

- decisao: se compatibilidade significa apenas coleta sem erros ou equivalencia completa de resultados
  estado: pendente
  evidencia: coleta explicita tem 422 itens; execucao direta tem 2778 verificacoes internas, grandezas nao equivalentes.
```

## 15. Conclusao

```yaml
execucao_direta:
  estado: compativel
  resultado: 10 scripts, 2778 verificacoes, 0 falhas, 0 erros, todos com codigo 0
pytest:
  versao: pytest 9.0.3
  padrao:
    estado: nao_coleta_suite_atual
    resultado: 0 itens, codigo 5
  explicito_10_arquivos:
    estado: quase_compativel_com_erro_remanescente
    resultado: 422 itens, 421 passed, 1 error, 7 warnings
incompatibilidades_legadas:
  atuais:
    - demo/teste_diagnostico.py::teste_modo_executavel exige resultado_esperado sem fixture
  historicas_superadas:
    - 6 erros tmp_base em tela/teste_loader.py
    - 3 erros modelo em demo/teste_demo.py
incompatibilidades_novas:
  comprovadas: []
suite_canonica_formalizada:
  estado: parcialmente
  detalhe: H-0037 formaliza 10 scripts diretos, mas nao ha configuracao executavel nem contrato final sobre pytest.
decisoes_pendentes:
  - papel futuro do pytest
  - criterio de compatibilidade
  - tratamento de teste_*.py
  - tratamento do erro resultado_esperado
  - tratamento dos avisos de retorno nao-None
handoff_pode_ser_criado: sim, se o usuario decidir a politica desejada para pytest antes
proxima_etapa_permitida: decisao_do_usuario_sobre_politica_de_testes_antes_de_handoff
```

Estado de encerramento da investigacao:

```text
LEVANTAMENTO_CONCLUIDO
```

## 16. Estado Git final observado

Comandos executados apos a criacao deste arquivo:

```bash
git status --short --untracked-files=all
git diff --cached --name-only
```

Estado esperado pelo levantamento:

```yaml
estado_inicial_observado:
  stage: VAZIO
  workspace: COM_ARQUIVO_NAO_RASTREADO
  arquivos_nao_rastreados:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
efeito_real_da_etapa:
  arquivos_criados:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  arquivos_alterados: []
  arquivos_removidos: []
  arquivos_movidos: []
estado_final_observado:
  stage: VAZIO
  workspace: COM_DOIS_ARQUIVOS_NAO_RASTREADOS
  arquivos_nao_rastreados:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
  arquivos_rastreados_modificados: []
  relatorio_anterior_preservado: sim
  relatorio_novo_listado_como_nao_rastreado: sim
  arquivos_adicionais_criados_no_status_git_padrao: nao
```

Evidencia final:

```text
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
```

`git diff --cached --name-only` nao produziu saida.
