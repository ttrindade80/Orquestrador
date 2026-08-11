# Relatório de fechamento — H-0057 / ADR-0044

## 1. Identificação

```yaml
item: ITEM-0017
adr: ADR-0044
handoff: H-0057
baseline_commit: 1211a70
status_validacao_manual: MANUAL_VALIDATION_APPROVED
```

## 2. Estado final

H-0057 está concluído. A ADR-0044 permanece aplicada. A implementação, os
patches P01/P02, a QA pós-patch e a validação manual final foram transportados
como encerrados, sem reabrir QA ou criar P03.

## 3. Resultado funcional

Foram aceitos largura intrínseca dinâmica limitada pela largura do corpo,
wrapping sem perda de conteúdo ou whitespace, alinhamento à esquerda,
centralizado e justificado com residual determinístico, altura derivada,
chips multilinha, resize reativo, mesma instância lógica, últimas dimensões
válidas, quadro geral de terminal pequeno, restauração automática e regressão
H-0056 preservada.

## 4. Patches P01/P02

P01 corrigiu a perda de separadores durante o wrapping e estabeleceu a
reconstrução integral da entrada. P02 tornou determinística a distribuição
residual da justificação, sem declarar eliminação da limitação visual global.

## 5. QA

Os relatórios existentes registram H1_HANDOFF_APPROVED, o achado
QA-H0057-IMP-001 corrigido por P01 e QA pós-P02 em
I5_MANUAL_VALIDATION_REQUIRED. Não há achado técnico aberto para este
fechamento.

## 6. Validação manual

O usuário aprovou a validação em TTY_REAL com status
MANUAL_VALIDATION_APPROVED, incluindo wrapping, resize, centralização,
terminal pequeno, restauração, modalidade, tecla inerte, Esc e retorno.

## 7. Limitação conhecida

```yaml
id: MV-H0057-001
area: texto_justificado
descricao: Em determinadas larguras, a composição visual do parágrafo justificado ainda pode apresentar diferença de uma coluna ou distribuição desigual entre linhas.
impacto: nao compromete wrapping, resize, centralizacao do popup, modalidade ou retorno
decisao_usuario: ACEITA_PARA_FECHAMENTO
```

O defeito não é declarado eliminado.

## 8. Deferimento

```yaml
tema: composicao_e_justificacao_global_de_texto
estado: DEFERIDO_PARA_ITEM_FUTURO
escopo_futuro: Adotar algoritmo canônico/global de composição de parágrafo e justificação para todas as ocorrências de texto justificado da TUI, evitando soluções locais por componente.
momento_registro_backlog: fechamento final do ITEM-0017, depois de H-0058 e H-0059
```

Nenhum item futuro foi criado em `docs/backlog.md`.

## 9. Estado do ITEM-0017

```yaml
status: em_andamento
adr: ADR-0044 aplicada
H-0056: concluido
H-0057: concluido
proxima_entrega: H-0058
```

## 10. Testes finais

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py -q
48 passed

PYTHONDONTWRITEBYTECODE=1 python -m pytest
1145 passed
```

Ambos os comandos terminaram sem falhas.

## 11. Higiene

O cache de pytest, diretórios `__pycache__` e arquivos `*.pyc` gerados nos
caminhos relevantes foram removidos. Os arquivos materiais do ciclo foram
normalizados quanto a trailing whitespace e EOF. `git diff --check` foi
executado sem apontamentos.

## 12. Stage

O stage final contém somente os arquivos reais do ciclo H-0057: handoff,
relatórios nominais, implementação, testes, fixture, configuração, backlog
com a reconciliação do ITEM-0017 e este relatório. Não contém caches, arquivos
do H-0056 já commitados ou item futuro de justificação.

```yaml
manifesto_staged: 19
```

## 13. Próxima entrega

H-0058 — lista navegável e marcação exclusiva/múltipla; status não iniciada.

## 14. Bloqueios

Nenhum bloqueio para o fechamento. H-0058 não foi iniciado.

## 15. Mensagem de commit proposta

```text
feat: implementa popup com geometria dinamica
```
