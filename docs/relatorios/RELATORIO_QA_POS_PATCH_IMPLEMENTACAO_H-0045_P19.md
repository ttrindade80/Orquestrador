---
name: RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0045_P19
descricao: "QA técnico final do PATCH_IMPLEMENTACAO P19 e da correção focal de largura horizontal"
metadata:
  tipo: relatorio_qa_pos_patch_implementacao
  status: I5_MANUAL_VALIDATION_REQUIRED
  handoff: H-0045
  data: "2026-08-02"
rastreabilidade:
  etapa: QA_POS_PATCH
  tipo_execucao: PATCH_IMPLEMENTACAO
  cadeia_raiz: VM-H0045-R07-001
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P19.md
  achados_retestados:
    - QA-H0045-P18-001
    - QA-H0045-P18-002
    - QA-H0045-P18-003
---

# RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0045_P19

## 1. Identificação e resultado

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: I5_MANUAL_VALIDATION_REQUIRED
resultado: APROVADO_TECNICAMENTE
```

O QA técnico do P19 foi aprovado. A validação manual focal do usuário não foi
executada, conforme o escopo desta etapa; portanto `VM-H0045-R07-001` permanece
pendente dessa validação para encerramento integral.

## 2. Provas semânticas retestadas

- `QA-H0045-P18-001`: o texto alongado é aplicado antes das duas renderizações
  locais sobre o mesmo modelo; ambas recebem o mesmo foco, lista e cursor 2.
  A prova preserva `len(linhas_com_gamma) >= 2`. Na prova CLI, as duas
  invocações usam a mesma cópia temporária e diferem apenas por `--verboso`;
  `TemporaryDirectory` garante limpeza e a fixture original não é escrita.
- `QA-H0045-P18-002`: a página de continuação é selecionada no plano, mas
  também é alcançada e renderizada pelo caminho real. O quadro é comparado
  linha a linha com a continuação esperada; indicador, ausência de cursor,
  ausência de início de item, ordem, ausência de perda/repetição e retorno
  `,`/`.` permanecem comprovados.
- `QA-H0045-P18-003`: os dois testes P10 usam comparação ordenada direta
  (`produzidas == esperadas`). Não há `sorted`; `set` aparece somente como
  verificação adicional de duplicação, não como substituto da prova de ordem.

## 3. Largura horizontal

Medição da fixture fixa de célula única, em modo verboso, com a geometria do
renderer e do mapa físico. “Texto” é a largura da célula atribuída; as duas
colunas do indicador ficam dentro dela. A maior linha pode ser menor por causa
do limite natural de palavras.

| terminal | útil | texto | maior linha física | resíduo estrutural | renderer/mapa |
|---:|---:|---:|---:|---:|---:|
| 80  | 77  | 75  | 72  | 2 | 75/75 |
| 120 | 117 | 115 | 112 | 2 | 115/115 |
| 160 | 157 | 155 | 152 | 2 | 155/155 |
| 200 | 197 | 195 | 192 | 2 | 195/195 |

Não reaparece o teto próximo da metade. O ramo de célula única usa a largura
atribuída; distribuições com múltiplas células mantêm o cálculo próprio. A
suíte completa confirma indicador, resize, ausência de overflow/truncamento
indevido, ausência de perda/repetição, regressão do caminho externo H-0037 e
coerência de navegação.

## 4. Verificações executadas

```yaml
testes_nominais_corrigidos: "5 passed"
suite_focal: "417 passed"
suite_focal_ampliada: "430 passed"
suite_completa: "856 passed"
git_diff_check: "exit 0"
```

Comandos executados sem TTY interativo e com `PYTHONDONTWRITEBYTECODE=1` nas
suítes. A inspeção adicional não encontrou whitespace final nos quatro
arquivos do delta.

## 5. Escopo e pendências

O delta acumulado dos patches autorizados restringe-se a
`tela/renderizador.py`, `tela/teste_renderizador.py`,
`demo/teste_demo_paginacao.py` e `demo/teste_demo_navegacao.py`. O worktree
contém alterações anteriores do H-0045; elas não são atribuídas ao P19. O
relatório QA não foi tratado como achado por estar não rastreado no momento.
Nenhum arquivo de código, teste, configuração ou outra documentação foi
alterado por esta auditoria.

As validações anteriores permanecem aprovadas e não foram reabertas. Permanecem
fora deste delta, sem resolução declarada: `VM-H0045-R06-001` e
`QA-H0045-P08-001`.

```yaml
proxima_acao: validacao_manual_focal_pelo_usuario
```
