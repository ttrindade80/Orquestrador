# QA pós-patch — marcação de substituição do H-0024

## 1. Objeto

Auditoria independente da correção documental localizada aplicada ao handoff
**H-0024** (`docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`),
cujo objetivo exclusivo era registrar, de forma curta, a substituição
operacional do H-0024 pelo **H-0025**.

Alterações autorizadas pelo escopo do patch:

1. No frontmatter, `status: proposto` passou para `status: substituido`.
2. Após o frontmatter foi incluída a nota curta de substituição pelo H-0025.

Nenhuma causa da substituição deveria ser registrada.

Este QA não corrige achados, não altera o H-0024, o H-0025, a ADR-0018, nem o
relatório de levantamento, e não executa stage ou commit.

## 2. Autoridades

| Autoridade | Caminho | Uso neste QA |
|---|---|---|
| Handoff auditado | `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md` | objeto do diff e do exame do frontmatter/nota |
| Handoff substituto | `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md` | consulta à §2.3, que declara a substituição operacional |
| Relatório de levantamento | `docs/relatorios/RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025.md` | evidência secundária; tratado como somente leitura |

Declaração chave em **H-0025 §2.3** ("Papel deste handoff"):

> "Este handoff **substitui operacionalmente** o H-0024 para a implementação."
>
> "O H-0024 **permanece preservado** como evidência histórica e **não deve ser
> alterado, renomeado ou removido**."

A nota incluída pelo patch não contradiz essa declaração.

## 3. Estado Git inicial

Raiz Git detectada:

```text
git rev-parse --show-toplevel
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1
```

Estado registrado antes da criação deste relatório:

```text
$ git branch --show-current
master

$ git log -1 --oneline
c003f3e feat: implementa composicao hierarquica do corpo com tres niveis de grupos

$ git status --short
 M scripts/docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025.md
```

Diferenciação das entradas:

| Entrada | Classificação |
|---|---|
| `M scripts/docs/handoff/H-0024-...md` | alteração do patch (objeto do QA) |
| `?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025.md` | relatório de levantamento preexistente, não rastreado |
| `RELATORIO_QA_POS_PATCH_H-0024_SUBSTITUICAO.md` (este) | relatório criado por este QA |

Confirmações:

- O **H-0024 é o único arquivo rastreado modificado** pelo patch.
- O relatório de levantamento é um arquivo **não rastreado preexistente**.
- **Não há arquivo inesperado** relacionado ao patch.
- O **stage está vazio** (`git diff --staged --stat` sem saída).

Observação de base de caminhos: o diretório de trabalho é
`scripts/`. A partir da raiz Git, os caminhos aparecem com o prefixo
`scripts/`. Durante todo este QA foi usada uma única base (`scripts/docs/...`),
portanto `docs/handoff/...` e `scripts/docs/handoff/...` não foram tratados
como arquivos diferentes.

## 4. Diff examinado

Comando executado (a partir da raiz Git):

```bash
git --no-pager diff -- \
  scripts/docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
```

Resultado completo:

```diff
diff --git a/scripts/docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md b/scripts/docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
index df80374..bd8ace2 100644
--- a/scripts/docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
+++ b/scripts/docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
@@ -3,7 +3,7 @@ name: H-0024-distribuicao-vertical-percentual-fracao-corpo
 description: Handoff de implementação — distribuição da altura útil do corpo entre seus elementos quando corpo.arranjo é vertical, aplicando os modos percentual e por fração de corpo.distribuicao e executando a divisão igual normativa (modo igual e ausência de distribuicao) conforme ADR-0015 (arranjo/distribuição por container, modos, arredondamento por maiores restos, preenchimento de área alocada), preservando o arranjo horizontal e o redimensionamento reativo H-0023
 metadata:
   type: handoff
-  status: proposto
+  status: substituido
   data: 2026-07-11
 rastreabilidade:
   adr_base: docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
@@ -27,6 +27,8 @@ rastreabilidade:
   relatorio_implementacao_esperado: docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
 ---

+> **Situação:** este handoff foi substituído operacionalmente pelo H-0025.
+
 # H-0024 — Distribuição vertical da altura do corpo: modos percentual e por fração
```

Estatística: `1 file changed, 3 insertions(+), 1 deletion(-)`.

O diff contém exatamente:

- substituição de `status: proposto` por `status: substituido`;
- inclusão da nota curta de substituição pelo H-0025.

Não há terceira alteração. Nada foi reescrito, removido, reescalonado, e não há
qualquer registro de causa, alucinação, erro de chat ou perda de contexto. IDs,
títulos, testes e critérios não foram alterados.

## 5. Verificação do frontmatter

| Verificação | Resultado |
|---|---|
| Existe exatamente um campo `status` no frontmatter | OK (linha 6: `status: substituido`) |
| Valor atual é exatamente `substituido` | OK |
| `status: proposto` não permanece no frontmatter | OK (removido pelo patch) |
| Nenhum outro campo do frontmatter foi modificado pelo patch | OK |

Frontmatter final (linhas 4–7 do arquivo):

```yaml
metadata:
  type: handoff
  status: substituido
  data: 2026-07-11
```

## 6. Verificação da nota de substituição

Nota incluída (linha 30 do arquivo):

```markdown
> **Situação:** este handoff foi substituído operacionalmente pelo H-0025.
```

| Verificação | Resultado |
|---|---|
| Aparece uma única vez | OK (1 ocorrência exata) |
| Posição visível logo após o frontmatter | OK (linha 30, imediatamente após o `---` de fechamento) |
| Identifica o H-0025 como substituto operacional | OK |
| Não registra a causa | OK |
| Não afirma que o H-0024 foi implementado | OK |
| Não transforma o H-0024 em autoridade ativa | OK |
| Não contradiz a seção 2.3 do H-0025 | OK (a nota é coerente com "substitui operacionalmente") |

## 7. Preservação do conteúdo histórico

Ocorrências de `ARCHITECTURE_REVIEW_REQUIRED` no corpo do H-0024:

| Verificação | Resultado |
|---|---|
| Quantidade de ocorrências no arquivo | 5 (no corpo histórico preexistente) |
| Adicionadas pelo patch (via diff) | nenhuma (`grep` no diff sem correspondência) |
| Modificadas pelo patch (via diff) | nenhuma |

Essas ocorrências são conteúdo histórico preexistente e não foram tocadas pelo
patch. A verificação foi feita pelo diff (e não apenas por busca textual).
Nenhuma remoção foi exigida ou executada.

## 8. Arquivos fora do escopo

Confirmação, por `git diff --quiet -- <arquivo>`, de que nenhum arquivo fora do
escopo foi modificado pelo patch:

| Arquivo | Estado |
|---|---|
| `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md` | inalterado (tracked clean) |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | inalterado (tracked clean) |
| `docs/adr/INDICE_ADR.md` | inalterado (tracked clean) |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025.md` | inalterado (não rastreado preexistente) |

A criação deste próprio relatório de QA não é tratada como alteração indevida.

## 9. Verificações mecânicas

```text
$ git diff --check
(sem saída; EXIT=0)
```

`git diff --check` escopado ao H-0024 e em toda a worktree: **limpo** (exit 0).

Não foram executados testes de código, pois o patch é exclusivamente documental.

## 10. Achados

| ID | Severidade | Descrição | Resolução |
|---|---|---|---|
| — | — | nenhum | — |

Nenhum achado bloqueante, alto, médio ou baixo. As duas alterações autorizadas
estão corretas, não há terceira alteração, nenhum arquivo fora do escopo foi
modificado, o conteúdo histórico foi preservado e `git diff --check` está limpo.

## 11. Conclusão

```text
classificacao: QA_POS_PATCH_APPROVED
```

O patch aplicado ao H-0024 é uma correção documental localizada, contida e
fiel ao escopo autorizado. A marcação de substituição pelo H-0025 está
presente exatamente nas duas formas previstas (status do frontmatter e nota
curta pós-frontmatter), sem registro de causa, sem reescrita da especificação
histórica e sem afetar arquivos fora do escopo. A nota é coerente com a
declaração de substituição em H-0025 §2.3.

## 12. Estado Git final

Após a criação deste relatório, o estado do repositório é:

```text
$ git branch --show-current
master

$ git log -1 --oneline
c003f3e feat: implementa composicao hierarquica do corpo com tres niveis de grupos

$ git status --short
 M scripts/docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025.md
?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_SUBSTITUICAO.md
```

| Entrada | Classificação |
|---|---|
| `M scripts/docs/handoff/H-0024-...md` | alteração do patch |
| `?? .../RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025.md` | relatório de levantamento preexistente |
| `?? .../RELATORIO_QA_POS_PATCH_H-0024_SUBSTITUICAO.md` | relatório criado por este QA |

Stage: **vazio**. Nenhum commit foi preparado ou executado por este QA.
