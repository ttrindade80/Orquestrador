# RELATORIO PATCH HANDOFF H-0073 P02

## Rastreabilidade

```yaml
etapa: PATCH_HANDOFF
objeto: H-0073
patch: P02
achado: ACH-001
cadeia_raiz: docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0073_POS_P01.md
```

## Status

`BLOCKED_DOCUMENTATION`

Caminho B constatado. O handoff **não** foi alterado: P02 recusou
materializar `A` como substituto de `A)`, inventar campo, omitir
`designador` contra o schema fechado ou reabrir H-0072.

## Mecanismo real do designador

Fonte canônica vigente de H-0055 (conteúdo externo, byte-a-byte
preservado): `niveis[1].designador` =
`{"tipo": "alfabetico_maiusculo", "sufixo": ")"}`.
`_texto_designador` aplica `prefixo`/`sufixo` quando presentes no dict
(`tela/renderizacao/designadores.py`); isso produz `A)`, `B)`, `C)`, `D)`.

Quando `formato.dois_niveis_por_foco.filho` existe, esse caminho deixa de
governar o filho:

1. O loader exige `filho.designador` junto com `tabulacao` e
   `apresentacao` (`formato_dois_niveis_por_foco.py`, campos obrigatórios).
2. `_validar_designador_filho` aceita somente `tipo`; `sufixo` é campo
   desconhecido e falha fechada.
3. `_linhas_dois_niveis_formatado_com_mapa` lê
   `config_filho["designador"]` e chama `_texto_designador(designador_cfg,
   ...)` (`conteudo_externo.py`). Não mescla
   `niveis[1].designador` do conteúdo. O pai continua no designador do
   envelope; o filho não.
4. Dict estrutural `{"tipo": "alfabetico_maiusculo"}` cai no default
   `sufixo=""` → `A`, `B`, `C`, `D`.

`contrato_tela_json.md` §36.2/§36.4 fecha o bloco estrutural com
`designador.tipo` apenas. `contrato_json_console.md` §12.3 permite
`sufixo` no envelope de conteúdo; §15 proíbe declarar o bloco de
formatação nesse envelope, mas não define herança do `sufixo` externo
quando o bloco estrutural existe.

H-0072 §21 caso 6 documenta `alfabetico_maiusculo` como `A)`. Isso não
altera o runtime vigente: com schema só-`tipo`, a forma emitida é `A`.

## Caminho A rejeitado

Não é possível aplicar a formatação nova a H-0055 sem substituir o
designador externo, sem mudar schema ou runtime:

- omitir `designador` no JSON estrutural viola o loader;
- declarar só `tipo` empobrece `A)` em `A`;
- copiar `sufixo` no estrutural é campo desconhecido;
- alterar o conteúdo é proibido.

## Preservação de A)

Não preservada neste patch. `A` não é equivalente. ADR-0047 exige
`alfabetico_maiusculo` com sufixo (`A)`). ACH-001 permanece material.

## Handoff / critérios / testes

Nenhum trecho de H-0073 foi corrigido. Critérios e testes futuros que
aceitam `A`/`B`/`C`/`D` sem `)` **não** foram reescritos aqui: isso seria
solução inválida. Continuam como evidência do achado, não como aceite.

## H-0063

Não reaberto. Estado pós-P01 permanece no handoff intocado: preset;
amostra; titulo preservado; designador `nenhum`; tabela 2 colunas;
tabulação 5..10; espaçamento 3..8.

## Bloqueio

- **Regra/schema:** `filho.designador` obrigatório; somente `tipo`;
  renderer formatado ignora `sufixo` do conteúdo.
- **Arquivos da limitação:**
  `tela/carregamento/formato_dois_niveis_por_foco.py` (schema);
  `tela/renderizacao/conteudo_externo.py`
  (`_linhas_dois_niveis_formatado_com_mapa`, runtime).
- **Por que H-0073 sozinho não preserva `A)`:** é só aplicação da
  capacidade já fechada. Sem herança do envelope, sem `sufixo`
  estrutural e sem omissão de `designador`, qualquer JSON autorizado
  perde `)`.
- **Camada a corrigir:** autoridade/capacidade anterior —
  ADR-0047 / H-0072 / `contrato_tela_json.md` §36 (designador estrutural
  só-`tipo`, sem herança de `prefixo`/`sufixo` do conteúdo), apesar de
  H-0072 §21.6 já exigir a forma `A)`.

## Verificações

- Handoff não editado (sem solução falsa).
- Nenhum arquivo de implementação, ADR, contrato, nomenclatura,
  configuração, código ou teste alterado.
- `h0055_dois_niveis_por_foco_conteudo.json` não tocado.
- `git diff --check` somente sobre este relatório.

## Fora de escopo

H-0062, H-0072, testes H-0070, projeção amostra, navegação, seleção,
resize, alinhamento de colunas, QA pós-P02, implementação.
\n