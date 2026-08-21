# Relatório de QA — ADR-0049

## Verificações executadas

Foi feita a leitura integral de `docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md` e dos módulos de nomenclatura `01_NUCLEO_COMUM.md`, `20_TELA_CORPO_E_COMPOSICAO.md` e `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`. O conteúdo foi confrontado com D-0027-01 a D-0027-09 e com os critérios de QA, especialmente as fronteiras entre conteúdo semântico e representação física, composição declarativa, largura dinâmica, medição/renderização, truncamento e padding/alinhamento.

## Achados materiais

### QA-ADR-0049-01 — Prescrição de implementação fora das decisões

Local: §5, linhas 171–176; contraste com §8, linhas 201–204.

A tabela de artefatos afetados prescreve reconciliação de helpers específicos (`_quebrar_texto`, `_justificar_linha`, `_formatar_linha` e `_truncar_com_marcador`), lista módulos Python concretos e determina que `tela/renderizador.py` reexporte a partir do mecanismo canônico. As decisões fechadas definem autoridade, comportamento e fronteiras, mas não escolhem módulo, API, fachada, reexportação ou assinatura. A própria ADR declara esses detalhes fora de escopo. Isso introduz arquitetura e detalhes executivos não decididos, restringindo indevidamente a aplicação futura.

### QA-ADR-0049-02 — Preservação nominal de helper histórico

Local: §5, linha 172.

A exigência de “preservar `_truncar_com_marcador`” transforma a identidade de um helper histórico em requisito. D-0027-03 autoriza preservar somente diferença que represente semântica necessária do consumidor; D-0027-09 preserva a distinção comportamental entre truncamento de linha única e wrap, não o nome nem a implementação de um helper. A fronteira deve permanecer semântica e local ao consumidor, sem exigir essa implementação histórica.

## Status

`ADR_REJECTED`
