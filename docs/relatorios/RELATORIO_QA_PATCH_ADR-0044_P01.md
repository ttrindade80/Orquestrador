# Relatório QA — Patch P01 da ADR-0044

```yaml
item: ITEM-0017
adr: docs/adr/ADR-0044-popup-modal-generico-de-decisao.md
patch: P01
status: ADR_PATCH_APPROVED_WITH_NOTES
```

## Resultado

A auditoria integral da ADR confirma que D-POP-25 foi transportada sem perda
material: `popups` é um mapa/objeto no nível geral, fora de `cabecalho`,
`corpo` e `barra_de_menus`, com cardinalidade `0..N`; a identidade está na
chave estável, sem `id` interno obrigatório redundante. Conteúdo concreto,
estado vivo, produtor, loader e origem permanecem fora da configuração.

O fluxo normativo exige ID, envelope pronto, resolução por `popups[ID]`,
validação conjunta e materialização da instância. A reutilização com envelopes
compatíveis diferentes e a distinção declaração × instância estão explícitas.

Também permanecem preservadas as decisões anteriores auditadas: pop-up modal
genérico, não-console, não-região permanente e não-elemento do corpo; ausência
de ação de negócio e paginação; separação entre configuração, conteúdo e
runtime; políticas de marcação; retornos `ABORTADO`/`CONFIRMADO`; resize,
terminal pequeno e a decomposição incremental em quatro etapas.

Não foi identificada decisão normativa nova além do escopo autorizado de
D-POP-25.

## Nota técnica

`git diff --check` padrão não inspeciona a ADR porque ela está não rastreada.
Na verificação direta (`git diff --no-index --check /dev/null <ADR>`), foram
acusados espaços finais nas linhas 3–5 do cabeçalho, usados como quebra de
linha Markdown. É uma ressalva não material ao conteúdo do patch; a ADR não
foi alterada por estar fora dos arquivos permitidos.
