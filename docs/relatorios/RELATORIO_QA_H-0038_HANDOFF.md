# RELATORIO_QA_H-0038_HANDOFF

## 1. Identificacao

```yaml
etapa: QA_HANDOFF
papel: auditor independente
data: 2026-07-21
raiz_operacional: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
relatorio_criado: docs/relatorios/RELATORIO_QA_H-0038_HANDOFF.md
```

## 2. Artefato auditado

```yaml
artefato:
  - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
encerramento_do_artefato: HANDOFF_CORRIGIDO_AGUARDANDO_QA
```

## 3. Autoridades

```yaml
autoridades_consultadas:
  - decisao explicita do usuario de adotar pytest como padrao unico
  - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  - docs/relatorios/RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md
  - docs/contratos/contrato_processo_desenvolvimento.md
  - docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  - arquivos de teste citados nominalmente pelo handoff
```

## 4. Estado Git inicial

Comandos executados:

```bash
git status --short --untracked-files=all
git branch --show-current
git log -1 --oneline
git diff --cached --name-only
```

Resultado:

```yaml
branch: master
HEAD: 23f49d0 docs: aplica nomenclatura modular e leitura seletiva
stage: VAZIO
workspace: COM_TRES_ARQUIVOS_NAO_RASTREADOS
arquivos_nao_rastreados:
  - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
divergencia_do_estado_inicial_esperado_pelo_QA: nao
```

## 5. Fidelidade a decisao

```yaml
padrao_unico: pytest
comando_canonico: python -m pytest
forma_recomendada: PYTHONDONTWRITEBYTECODE=1 python -m pytest
execucao_direta_anterior: deixa_de_ser_gate_canonico
objetivos_preservados:
  - descoberta automatica
  - execucao unificada
  - preservacao_da_cobertura
resultado_da_auditoria: CONFORME_COM_RESSALVA_TECNICA
```

O H-0038 atribui a decisao central ao usuario, nao reabre a escolha entre execucao direta e pytest e proibe dois padroes oficiais paralelos. A ressalva tecnica esta nos achados: a especificacao ainda nao fecha como o pytest transformara falhas registradas por `_registrar()` em falhas reais do gate canonico.

## 6. Origem semantica

```yaml
decisao_central_atribuida_ao_usuario: sim
numeros_iniciais_conferem_com_levantamento:
  verificacoes_diretas: 2778
  itens_pytest_explicito: 422
  execucao_pytest_explicita: 421 passed, 1 error, 7 warnings
erro_resultado_esperado:
  confirmado: sim
  origem: LEGADA_COMPROVADA
  commit: 54e85090
warnings_retorno_nao_none:
  quantidade: 7
  objetos: confirmados por relatorio e por codigo atual
H-0037:
  commit_relacionado: c90349c feat: implementa apresentacoes multinivel com modos por tela
  comando_canonico_historico: execucao direta, nao pytest
HEAD_atual:
  commit: 23f49d0 docs: aplica nomenclatura modular e leitura seletiva
  relacao: posterior a c90349c
ADR-0029:
  historicamente_separada_de_H-0037_e_HEAD: confirmado por historico documental
contrato_como_autoridade_permanente:
  confirmado: sim
  evidencia: contrato_processo_desenvolvimento.md secao 3 coloca contrato de processo acima de ADRs, contratos de modulo, handoffs, relatorios de implementacao e relatorios de QA
fatos_nao_confirmados: []
```

## 7. Escopo e arquivos

Lista auditada:

```yaml
criar:
  - pytest.ini
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0038_PYTEST_PADRAO_UNICO.md
modificar:
  - demo/teste_diagnostico.py
  - tela/teste_loader.py
  - tela/teste_modelo.py
  - tela/teste_renderizador.py
  - docs/contratos/contrato_processo_desenvolvimento.md
preservar_sem_alteracao:
  - tela/teste_distribuicao_matricial.py
  - demo/teste_demo.py
  - demo/teste_demo_console.py
  - demo/teste_demo_console_modos.py
  - demo/teste_demo_distribuicao.py
  - demo/teste_explorar_barra_de_menus.py
  - docs/INDICE.md
  - docs/NOMENCLATURA.md
  - docs/nomenclatura/00_INDICE.md
```

Resultado: a lista cobre as alteracoes nominais de configuracao, erro legado `resultado_esperado`, sete warnings de retorno nao-`None` e atualizacao contratual. Contudo, ela nao cobre a conversao geral da semantica de falha dos testes baseados em `_registrar()`. Essa lacuna e material para o objetivo de preservar a cobertura sob o novo gate pytest.

## 8. Exequibilidade

Verificacao material das alteracoes prescritas:

```yaml
demo/teste_diagnostico.py:
  teste_invariantes_anteriores_retorna_bool: confirmado
  teste_gerar_diagnostico_retorna_resultado_str: confirmado
  teste_modo_executavel_parametro_resultado_esperado: confirmado
  main_captura_resultado_e_chama_teste_modo_executavel: confirmado
  calculo_interno_por_gerar_diagnostico_tela: tecnicamente_exequivel
tela/teste_loader.py:
  teste_caminho_feliz_retorna_tela: confirmado
  main_usa_tela_real_para_impressao_diagnostica: confirmado
  remocao_do_retorno_com_ajuste_do_main: tecnicamente_exequivel
tela/teste_modelo.py:
  teste_modelo_orquestrador_retorna_modelo: confirmado
  main_captura_modelo_sem_uso_posterior_material: confirmado
tela/teste_renderizador.py:
  tres_funcoes_retornam_modelo: confirmado
  main_nao_captura_esses_retornos: confirmado
```

As alteracoes prescritas removem o erro e os warnings nominais. Elas nao sao suficientes, isoladamente, para tornar o pytest um gate equivalente de falha para as verificacoes internas registradas pelos scripts.

## 9. Configuracao do pytest

Proposta auditada:

```ini
[pytest]
python_files = teste_*.py
testpaths = tela demo
```

Comando de simulacao executado sem criar arquivo de configuracao e com cache desativado:

```bash
env PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -p no:cacheprovider -o 'python_files=teste_*.py' -o 'testpaths=tela demo'
```

Resultado:

```yaml
codigo_de_saida: 0
itens_coletados: 422
arquivos_teste_localizados_em_tela_demo: 10
configuracoes_concorrentes_localizadas:
  pytest.ini: ausente
  pyproject.toml: ausente
  setup.cfg: ausente
  tox.ini: ausente
  conftest.py: ausente
suficiencia_para_descoberta_dos_10_arquivos: confirmada
```

A configuracao e suficiente para descoberta automatica dos dez arquivos. A ressalva e que a coleta real tambem inclui metodos `test_*` dentro de classes `Test*`; portanto o CA-10 precisa ser corrigido para refletir o inventario real.

## 10. Preservacao da cobertura

O handoff reconhece corretamente que `2778` verificacoes diretas e `422` itens pytest nao sao grandezas equivalentes. Tambem exige uma matriz de rastreabilidade por script.

Resultado da auditoria:

```yaml
criterio_de_preservacao:
  distingue_2778_de_422: sim
  exige_matriz: sim
  demonstra_automaticamente_equivalencia_de_falha_no_pytest: nao
  exige_conversao_de__registrar_false_para_falha_pytest: nao
  suficiente_para_preservar_materialmente_cobertura: nao
```

Evidencia: em arquivos como `demo/teste_diagnostico.py`, `tela/teste_loader.py`, `tela/teste_modelo.py` e `tela/teste_renderizador.py`, `_registrar()` apenas adiciona `(nome, passou)` em `_RESULTADOS`. O codigo de saida 1 e produzido pelo `main()` apos somar `falharam`; o pytest coleta funcoes diretamente e nao executa `main()`. Assim, uma verificacao interna registrada como falsa pode nao se converter em falha de item pytest.

## 11. Criterios de aceite

```yaml
CA-01:
  resultado: insuficiente
  motivo: codigo 0 do pytest nao prova que todas as verificacoes _registrar passaram
CA-02:
  resultado: conforme
  motivo: descoberta automatica dos 10 arquivos e verificavel por collect-only
CA-03:
  resultado: insuficiente
  motivo: 0 failed nao cobre falhas internas apenas registradas
CA-04:
  resultado: conforme_para_erros_pytest
  motivo: 0 errors e observavel
CA-05:
  resultado: conforme
  motivo: separa warnings do projeto e do ambiente
CA-06:
  resultado: conforme
  motivo: ausencia do erro resultado_esperado e observavel
CA-07:
  resultado: conforme
  motivo: criterio documental objetivo
CA-08:
  resultado: insuficiente
  motivo: matriz sem regra de falha pytest nao comprova ausencia de regressao material
CA-09:
  resultado: conforme
  motivo: stage vazio e verificavel sem preparar stage
CA-10:
  resultado: contraditorio_ou_subespecificado
  motivo: coleta real inclui metodos test_* em classes Test*, enquanto o criterio fala somente em funcoes com prefixo teste_; tambem nao define inventario objetivo de auxiliares
```

## 12. Testes

Os testes focais e a suite completa sao executaveis para os quatro arquivos modificados e para o conjunto da suite, desde que o erro `resultado_esperado` e os warnings sejam corrigidos.

A prova negativa esta subespecificada:

```yaml
usa_arquivo_temporario_ou_mecanismo_isolado: parcial
confirma_codigo_diferente_de_zero: sim
remove_integralmente_artefato_temporario: exigido_mas_sem_procedimento_preciso
nao_modifica_permanentemente_teste_ou_configuracao: nao_garantido
nao_deixa_cache_ou_arquivo_nao_rastreado_relevante: nao_garantido
reproduzivel_por_QA_posterior: parcial
```

Com `testpaths = tela demo`, um arquivo temporario fora de `tela/` e `demo/` nao sera coletado pelo comando canonico sem argumentos. Um arquivo temporario dentro de `tela/` ou `demo/` precisa de nome, conteudo, local, remocao e verificacao Git final explicitamente definidos.

## 13. Documentacao

O handoff define corretamente a atualizacao prevista de `docs/contratos/contrato_processo_desenvolvimento.md`:

```yaml
comando_canonico: PYTHONDONTWRITEBYTECODE=1 python -m pytest
papel_da_execucao_direta: nao_canonico_mas_permitido
dois_padroes_oficiais: proibidos
limite_da_alteracao_documental: restrito_a_politica_de_testes
relacao_com_H-0037: contrato_supera_handoff_por_hierarquia
```

Nao ha necessidade material demonstrada de alterar `docs/INDICE.md`, `docs/NOMENCLATURA.md` ou `docs/nomenclatura/00_INDICE.md`.

## 14. Achados

```yaml
- id: QA-H0038-001
  severidade: ALTA
  local: H-0038 secoes 4, 8, 9 e 10; arquivos de teste com _registrar()
  evidencia: "_registrar() em arquivos como demo/teste_diagnostico.py, tela/teste_loader.py, tela/teste_modelo.py e tela/teste_renderizador.py apenas adiciona resultados em _RESULTADOS; main() converte falharam em codigo 1, mas pytest coleta funcoes diretamente e nao executa main()."
  regra_ou_decisao: "pytest deve ser padrao unico, com execucao unificada e preservacao material da cobertura."
  impacto: "python -m pytest pode retornar codigo 0 mesmo que uma verificacao interna registrada por _registrar(False) tenha falhado; CA-01, CA-03 e CA-08 nao provam cobertura material."
  correcao_necessaria: "Definir como cada verificacao registrada se converte em falha pytest, ajustar a lista de arquivos autorizados se necessario e prescrever evidencia objetiva de equivalencia de falha."

- id: QA-H0038-002
  severidade: MEDIA
  local: H-0038 secao 9, CA-10
  evidencia: "A coleta simulada com python_files=teste_*.py e testpaths=tela demo coletou 422 itens, incluindo funcoes teste_* e tambem metodos test_* em classes Test*. Exemplo material: TestHelperHorizontalH0033Patch2 aparece na coleta."
  regra_ou_decisao: "criterios de aceite devem ter resultado observavel, limite objetivo e ausencia de contradicao."
  impacto: "CA-10 nao permite diferenciar de forma objetiva teste real, metodo pytest real e auxiliar coletado acidentalmente; tambem descreve a coleta como se apenas funcoes teste_* aparecessem."
  correcao_necessaria: "Substituir CA-10 por inventario objetivo de node IDs, contagens por arquivo/classe ou regra explicita que inclua metodos test_* reais e defina como identificar auxiliares."

- id: QA-H0038-003
  severidade: MEDIA
  local: H-0038 secao 10, prova negativa
  evidencia: "A prova negativa exige introduzir falha em arquivo temporario, mas nao define local, nome, conteudo, comando, isolamento ou verificacao de limpeza. Com testpaths=tela demo, arquivo temporario fora desses diretorios nao e coletado pelo comando canonico."
  regra_ou_decisao: "testes prescritos devem ser reproduziveis, nao deixar artefatos e confirmar codigo diferente de zero."
  impacto: "QA posterior pode executar uma prova negativa que nao testa o gate canonico ou que deixa arquivo nao rastreado/cache relevante."
  correcao_necessaria: "Definir procedimento isolado completo, incluindo local coletavel ou invocacao justificada, conteudo minimo, comando, codigo esperado, remocao e verificacao Git final."

- id: QA-H0038-004
  severidade: BAIXA
  local: H-0038 secoes 3 e 15
  evidencia: "A secao 3 registra workspace COM_DOIS_ARQUIVOS_NAO_RASTREADOS, enquanto o estado inicial operacional para implementacao apos a criacao do H-0038 e COM_TRES_ARQUIVOS_NAO_RASTREADOS, tambem descrito na secao 15.3 e confirmado pelo QA."
  regra_ou_decisao: "estado inicial e final devem ser concretos e nao ambiguos."
  impacto: "Pode gerar divergencia desnecessaria no relatorio de implementacao sobre o estado inicial."
  correcao_necessaria: "Rotular a secao 3 como estado antes da criacao do handoff ou alinhar o estado de partida da futura implementacao a COM_TRES_ARQUIVOS_NAO_RASTREADOS."
```

## 15. Bloqueios

```yaml
bloqueios:
  - id: BLOQ-H0038-001
    tipo: especificacao_incompleta
    descricao: "Sem regra para converter falhas registradas por _registrar() em falhas pytest, o handoff nao garante preservacao material da cobertura sob o novo gate canonico."
```

## 16. Conclusao

O H-0038 e fiel a decisao do usuario e e materialmente correto quanto a descoberta dos dez arquivos, ao erro legado `resultado_esperado`, aos sete warnings de retorno nao-`None`, a escolha de `pytest.ini` e a autoridade do contrato de processo.

Mesmo assim, o handoff ainda requer patch antes da implementacao. A lacuna principal e que a nova suite canonica pode executar funcoes que apenas registram resultados em `_RESULTADOS`, sem transformar falhas internas em falhas pytest. Isso impede concluir que `python -m pytest` preservara materialmente a cobertura atual.

## 17. Estado Git final

Comandos finais executados apos a criacao deste relatorio:

```bash
git status --short --untracked-files=all
git diff --cached --name-only
```

Resultado observado:

```yaml
stage: VAZIO
workspace: COM_QUATRO_ARQUIVOS_NAO_RASTREADOS
arquivos_nao_rastreados:
  - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
  - docs/relatorios/RELATORIO_QA_H-0038_HANDOFF.md
```

H2_HANDOFF_PATCH_REQUIRED
