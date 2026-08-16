# Relatório — QA Pós-Patch P02 da ADR-0047

## Metadata

- Etapa: `QA_POS_PATCH_ADR`
- Objeto: ADR-0047
- Patch auditado: P02
- Artefato criado: `docs/relatorios/RELATORIO_QA_ADR-0047_POS_P02.md` (este arquivo)

## Rastreabilidade

- `cadeia.raiz`: `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
- `cadeia.predecessor_imediato`: `docs/relatorios/RELATORIO_PATCH_ADR-0047_P02.md`

## Bloqueio de H-0073

`RESOLVIDO`. O bloqueio documental registrado em
`RELATORIO_CRIACAO_HANDOFF_H-0073.md` (§"Campos reais de H-0063
identificados"/§"Bloqueios") decorria de a ADR-0047 §4.11 pressupor dois
campos semânticos já separados em H-0063. O patch P02 corrige esse
pressuposto, fecha os nomes literais `preset`/`amostra` e autoriza
`campos["amostra"]` como extensão compatível da projeção, com proveniência
explícita e proibição de parsing de `titulo`. Nenhuma decisão de
nomenclatura necessária à especialização de H-0063 permanece aberta.

## Verificações factuais (leitura de código)

- `tela/estilo.py::ControladorTelaEstilo._construir_conteudo` (linhas
  146–197): para cada filho, popula exatamente `navegavel`, `selecionavel`,
  `titulo`, `categoria`, `preset`. Confirma o fato corrigido — não existe
  campo isolado de amostra. `campos["preset"] = nome` (linha 171) confirma
  que `preset` já é campo real e existente da projeção.
- `campos["titulo"]` é o retorno direto de
  `tela/renderizacao/estilo.py::compor_titulo_com_amostra` (linha 166),
  chamada com `nome`, `categoria`, `preset.dados`.
- `compor_titulo_com_amostra` (linhas 164–175) chama
  `amostra_de_preset(categoria, dados)` (linha 174) como etapa discreta
  *antes* da concatenação final em string única — confirma que a amostra já
  existe semanticamente no fluxo, como valor isolado, antes da composição de
  `titulo`.
- `amostra_de_preset` (linhas 151–161) é função pública, já exportada em
  `__all__`, que despacha por `categoria` e devolve diretamente a amostra —
  sem qualquer dependência de `titulo`. É tecnicamente possível chamá-la de
  `_construir_conteudo` com os mesmos argumentos (`categoria`,
  `preset.dados`) já disponíveis nesse escopo, produzindo
  `campos["amostra"]` sem parsing de `titulo`, com resultado idêntico ao
  hoje embutido em `titulo` (o preenchimento de `largura_nome` afeta somente
  a parte `nome`, nunca a amostra).

## Verificações normativas (ADR-0047 pós-P02)

1. Fato corrigido corresponde ao código real — confirmado.
2. `preset` é campo já existente da projeção — confirmado.
3. Amostra visual já existe semanticamente no fluxo antes da composição de
   `titulo` — confirmado (`amostra_de_preset` chamada isolada).
4. É tecnicamente possível expor esse valor como `campos["amostra"]` sem
   parsing de `titulo` — confirmado.
5. Preservar `titulo` mantém compatibilidade com consumidores existentes —
   confirmado; `compor_titulo_com_amostra` permanece intocada, `titulo`
   segue com mesmo valor/significado.
6. `amostra` é extensão compatível de dados, não mudança de conteúdo
   visível — confirmado; nenhum valor existente é alterado.
7. ADR fecha deterministicamente as duas colunas de H-0063 como
   `preset`/`amostra` — confirmado em §4.11 (YAML) e §4.11.1.
8. Exibição como tabela permanece exclusivamente no JSON estrutural da tela
   — confirmado; §4.11.1 remete a §4.13/§5, e P02 não move nada para o
   documento de conteúdo.
9. Nenhuma geometria/configuração visual foi transferida ao conteúdo —
   confirmado; `amostra` é valor semântico de texto (mesmo hoje embutido em
   `titulo`), não largura, posição ou geometria.
10. P02 não contradiz o schema já fechado da ADR-0047 (§4.13) — confirmado;
    `tabela.colunas[].campo` continua referência semântica genérica, apenas
    instanciada com os literais `preset`/`amostra`.
11. Nenhuma decisão material adicional permanece aberta para `APLICAR_ADR`
    ou para a futura correção de H-0073 — confirmado pela cláusula de
    fechamento no fim de §4.11.1.
12. D-DNF-01 a D-DNF-11 permanecem semanticamente preservadas — confirmado;
    §3 não foi tocada por P02, e o relatório do patch afirma explicitamente
    a preservação de substância de D-DNF-09.

## Achados materiais

Nenhum.

## Status final

`ADR_APPROVED`
\n