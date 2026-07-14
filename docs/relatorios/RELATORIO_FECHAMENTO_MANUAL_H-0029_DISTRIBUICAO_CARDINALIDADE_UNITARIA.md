# Relatório de fechamento manual — H-0029

## 1. Identificação

```yaml
ciclo: H-0029
titulo: Distribuição de containers com cardinalidade unitária
atividade: FECHAMENTO_MANUAL
data: 2026-07-13
estado: PRONTO_PARA_STAGE
commit: NAO_CONFIRMADO
```

## 2. Objetivo do ciclo

O H-0029 corrigiu a renderização de containers hierárquicos com distribuição explícita e cardinalidade unitária.

O ciclo passou a garantir que:

* `modo: igual` com um único filho atribua toda a área distribuível ao filho;
* `modo: fracao` com `valores: [1]` produza a mesma geometria;
* `modo: percentual` com `valores: [100]` produza a mesma geometria;
* um grupo estrutural que recebe uma cota do container pai complete corretamente essa cota;
* a ausência de distribuição continue preservando a altura natural dos filhos;
* a distribuição permaneça independente em cada nível da hierarquia;
* o comportamento já existente para dois ou mais filhos seja preservado.

## 3. Causa técnica confirmada

Em `_renderizar_container_vertical`, um filho do tipo `grupo` inserido em um container com distribuição explícita podia retornar apenas a altura natural de seu conteúdo interno.

O bloco do grupo era adicionado sem completar a cota atribuída pelo container pai.

Como o corpo já estava marcado como distribuído, o preenchimento externo histórico não era aplicado. O resultado podia possuir menos linhas que a altura solicitada.

A correção completa o bloco estrutural do grupo até a cota recebida, sem:

* criar distribuição implícita;
* alterar a semântica de ausência de distribuição;
* propagar distribuição entre níveis;
* alterar os JSONs de referência.

## 4. Telas permanentes adicionadas

Foram criadas sete telas permanentes para reprodução automatizada e validação humana:

```text
scripts/config/telas/h0029_dashboard_igual.json
scripts/config/telas/h0029_dashboard_fracao.json
scripts/config/telas/h0029_dashboard_percentual.json
scripts/config/telas/h0029_grupo_pai_distribuido.json
scripts/config/telas/h0029_grupo_igual.json
scripts/config/telas/h0029_grupo_fracao.json
scripts/config/telas/h0029_grupo_percentual.json
```

As telas não foram integradas ao lançador neste ciclo.

Os arquivos existentes usados como referência permaneceram preservados:

```text
scripts/config/telas/grupo_minimo.json
scripts/config/telas/destino_minimo.json
scripts/config/telas/stub_b.json
scripts/config/telas/orquestrador.json
```

## 5. Cobertura automatizada

A suíte de `teste_renderizador.py` passou a incluir:

* testes sintéticos de cardinalidade unitária;
* matriz de cenários para corpo e grupos;
* equivalência entre `igual`, `fracao [1]` e `percentual [100]`;
* testes em mais de uma altura;
* verificação de posições de bordas;
* posição da `barra_de_menus`;
* preservação da altura natural;
* ausência de sobreposição;
* integração nominal com os sete JSONs permanentes.

Foram adicionadas 256 verificações nominais para as telas permanentes, além dos testes focais anteriores do H-0029.

## 6. Resultado da suíte canônica

A suíte canônica foi executada diretamente pelos seis scripts de teste:

```text
teste_loader.py:                    172/172
teste_modelo.py:                     88/88
teste_renderizador.py:              820/820
teste_demo.py:                      303/303
teste_diagnostico.py:                28/28
teste_explorar_barra_de_menus.py:    38/38
```

Resultado consolidado:

```yaml
verificacoes: 1449/1449
falhas: 0
codigo_saida: 0
git_diff_check: limpo
```

A coleta automática por `pytest` não foi utilizada como substituta da suíte canônica.

## 7. Abertura das telas no demo

Como `demo.py` não possui argumento direto de linha de comando para selecionar a tela inicial, foi documentado um mecanismo que:

1. preserva a função original `criar_estado_inicial`;
2. cria o estado uma única vez;
3. altera `tela_atual` no mesmo dicionário;
4. retorna o mesmo estado modificado;
5. chama o loop real de `demo.py`.

O primeiro mecanismo documentado chamava a função original duas vezes e abria incorretamente a tela `orquestrador`.

O achado `QA-POS-H0029-001` corrigiu esse mecanismo.

Após a correção:

```yaml
telas_confirmadas: 7/7
orquestrador_aberto_indevidamente: nao
smoke_tests: 7/7
teste_demo: 303/303
codigo_saida: 0
```

## 8. QA do ciclo

### QA do handoff inicial

```yaml
status: H1_HANDOFF_APPROVED
```

### QA da implementação inicial

```yaml
status: I2_IMPLEMENTATION_PATCH_REQUIRED
motivo: estado final continha alteracao experimental em destino_minimo.json
```

A alteração havia sido realizada pelo usuário para teste visual e já estava restaurada antes do patch. Nenhum JSON de referência permanece alterado.

### QA do handoff após inclusão das telas

O handoff foi corrigido para autorizar nominalmente as sete telas permanentes.

Um achado alto identificou permissão residual para alterar `grupo_minimo.json`. A permissão foi removida e o arquivo passou a ser explicitamente classificado como referência preservada.

Resultado posterior:

```yaml
status: H1_HANDOFF_APPROVED
achados_pendentes: nenhum
```

### QA das telas permanentes

```yaml
sete_jsons: aprovados
testes_nominais: 256/256
suite_canonica: 1449/1449
achado: comandos do demo abriam orquestrador
status: I2_IMPLEMENTATION_PATCH_REQUIRED
```

### QA dos comandos corrigidos

```yaml
status: I5_MANUAL_VALIDATION_REQUIRED
telas_alvo_confirmadas: 7/7
smoke_tests: 7/7
achados_funcionais_pendentes: nenhum
```

## 9. Validação manual em TTY real

A validação foi executada exclusivamente pelo usuário nas sete telas permanentes.

### Dashboard direto

```yaml
- tela: h0029_dashboard_igual
  carregou: sim
  altura_total_correta: sim
  barra_de_menus_na_posicao_correta: sim
  borda_inferior_do_dashboard: imediatamente_antes_da_barra
  lacuna_indevida: nao
  sobreposicao: nao
  resultado: APROVADO

- tela: h0029_dashboard_fracao
  carregou: sim
  altura_total_correta: sim
  barra_de_menus_na_posicao_correta: sim
  borda_inferior_do_dashboard: imediatamente_antes_da_barra
  lacuna_indevida: nao
  sobreposicao: nao
  resultado: APROVADO

- tela: h0029_dashboard_percentual
  carregou: sim
  altura_total_correta: sim
  barra_de_menus_na_posicao_correta: sim
  borda_inferior_do_dashboard: imediatamente_antes_da_barra
  lacuna_indevida: nao
  sobreposicao: nao
  resultado: APROVADO
```

### Grupo pai distribuído sem distribuição interna

```yaml
- tela: h0029_grupo_pai_distribuido
  carregou: sim
  altura_total_correta: sim
  barra_de_menus_na_posicao_correta: sim
  borda_inferior_do_dashboard: altura_natural
  lacuna_indevida: nao
  sobreposicao: nao
  resultado: APROVADO
  observacao: executado duas vezes
```

A área estrutural abaixo do dashboard é esperada nesse cenário, pois o grupo não possui distribuição interna.

### Corpo e grupo distribuídos

```yaml
- tela: h0029_grupo_igual
  carregou: sim
  altura_total_correta: sim
  barra_de_menus_na_posicao_correta: sim
  borda_inferior_do_dashboard: imediatamente_antes_da_barra
  lacuna_indevida: nao
  sobreposicao: nao
  resultado: APROVADO

- tela: h0029_grupo_fracao
  carregou: sim
  altura_total_correta: sim
  barra_de_menus_na_posicao_correta: sim
  borda_inferior_do_dashboard: imediatamente_antes_da_barra
  lacuna_indevida: nao
  sobreposicao: nao
  resultado: APROVADO

- tela: h0029_grupo_percentual
  carregou: sim
  altura_total_correta: sim
  barra_de_menus_na_posicao_correta: sim
  borda_inferior_do_dashboard: imediatamente_antes_da_barra
  lacuna_indevida: nao
  sobreposicao: nao
  resultado: APROVADO
```

Resultado consolidado:

```yaml
status: MANUAL_VALIDATION_APPROVED
telas_aprovadas: 7/7
telas_reprovadas: 0
telas_nao_executadas: 0
```

## 10. Arquivos acumulados do ciclo

### Código e testes

```text
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
```

### Configurações de tela

```text
scripts/config/telas/h0029_dashboard_fracao.json
scripts/config/telas/h0029_dashboard_igual.json
scripts/config/telas/h0029_dashboard_percentual.json
scripts/config/telas/h0029_grupo_fracao.json
scripts/config/telas/h0029_grupo_igual.json
scripts/config/telas/h0029_grupo_pai_distribuido.json
scripts/config/telas/h0029_grupo_percentual.json
```

### Handoff

```text
scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
```

### Relatórios

```text
scripts/docs/relatorios/RELATORIO_FECHAMENTO_MANUAL_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_CORRECAO_GRUPO_MINIMO.md
scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_PATCH_TELAS_PERMANENTES.md
scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_COMANDOS_DEMO.md
scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_TELAS_PERMANENTES.md
```

Total esperado para o fechamento:

```yaml
arquivos: 19
codigo_e_testes: 2
jsons: 7
handoff: 1
relatorios: 9
```

## 11. Estado anterior ao stage

A última conferência apresentada pelo usuário continha:

```yaml
arquivos_modificados:
  - scripts/tela/renderizador.py
  - scripts/tela/teste_renderizador.py

arquivos_nao_rastreados:
  - sete JSONs h0029_*
  - handoff H-0029
  - oito relatórios já existentes do ciclo
```

O presente relatório de fechamento ainda deverá ser criado antes do stage.

Não foram observados:

* arquivos JSON de referência modificados;
* `__pycache__`;
* arquivos `.pyc`;
* stage;
* commit.

## 12. Classificação final anterior ao commit

```yaml
handoff: H1_HANDOFF_APPROVED
implementacao: APROVADA_TECNICAMENTE
qa_final: I5_MANUAL_VALIDATION_REQUIRED
validacao_manual: MANUAL_VALIDATION_APPROVED
suite_canonica: 1449/1449
git_diff_check: limpo
bloqueios: nenhum
estado_normalizado: PRONTO_PARA_STAGE
commit: NAO_CONFIRMADO
```

## 13. Próximas ações manuais

Depois de criar este relatório no caminho nominal:

1. executar `git status --short` na raiz Git;
2. confirmar os 19 arquivos acumulados do ciclo;
3. adicionar nominalmente somente os arquivos do H-0029;
4. verificar `git diff --cached --name-only`;
5. executar `git diff --cached --check`;
6. realizar o commit;
7. confirmar `git status --short`;
8. confirmar `git log -1 --oneline`.

O hash e a mensagem efetiva do commit deverão ser registrados somente após a saída real dos comandos.

## 14. Conclusão

O H-0029 corrigiu a distribuição vertical de containers hierárquicos com cardinalidade unitária, acrescentou sete telas permanentes de reprodução, ampliou a suíte para `1449/1449` verificações e recebeu aprovação manual em TTY real para todos os cenários previstos.

Não há bloqueio funcional, documental ou de validação manual pendente.

O ciclo está pronto para stage e commit manuais.
