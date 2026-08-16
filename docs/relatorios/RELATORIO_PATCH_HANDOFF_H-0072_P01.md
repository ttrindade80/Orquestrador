# RELATORIO_PATCH_HANDOFF_H-0072_P01

## Rastreabilidade

```yaml
etapa: PATCH_HANDOFF
objeto: H-0072
patch: P01
causa: ADR-0047 P03 / aplicação P02
cadeia_raiz: docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0047_POS_P02.md
```

## Limitação original

H-0072, já implementado e com QA original aprovado, fechava

`formato.dois_niveis_por_foco.filho.designador`

somente como `tipo`. O loader rejeitava `prefixo`/`sufixo`. Isso não
preserva apresentações vigentes `A)` `B)` `C)` `D)`. A ADR-0047 P03 e a
aplicação documental P02 já fecharam os adornos; o handoff ainda não.

## Delta prefixo/sufixo

O handoff passa a exigir objeto fechado:

- `tipo` obrigatório: `decimal_composto` | `alfabetico_maiusculo` | `nenhum`;
- `prefixo`/`sufixo` opcionais string; ausência = vazio nos tipos visuais;
- visual = `prefixo + designador_base + sufixo`;
- `nenhum`: sem designador; `prefixo` e `sufixo` ausentes;
- chaves desconhecidas inválidas;
- sem herança, `fonte`, `herdar`, parsing de conteúdo ou nova navegação.

O caso 6 original (`alfabetico_maiusculo` → `A)`) foi corrigido: sem
adornos o resultado é `A`; `A)` exige `sufixo: ")"` estrutural.

Tabulação, texto/tabela, colunas, espaçamento, alinhamento, quebra,
resize, item lógico, seleção, navegação e a separação configuração ×
conteúdo × renderer permanecem.

## Arquivos nominais para o patch de implementação

Editar:

- `tela/carregamento/formato_dois_niveis_por_foco.py`
- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json`
- `tela/teste_formato_filho_dois_niveis_por_foco.py`
- `demo/teste_demo_h0072_formatacao_generica.py`

Não editar (leitura focal):

- `tela/modelo.py` — já transporta o dict `filho` inteiro;
- `tela/renderizacao/designadores.py` — `_texto_designador` já aplica
  prefixo/núcleo/sufixo;
- `tela/renderizacao/conteudo_externo.py` — já passa `designador_cfg`
  integral ao mecanismo canônico;
- `tela_json.py`, `navegacao.py`, `selecao.py`, `console.py`,
  `matriz_participantes.py`, `demo/demo.py`.

Somente leitura/teste: conteúdo H-0072, `teste_navegacao.py`,
`teste_loader.py`, `teste_demo_console.py`.

Preservados: H-0055, H-0063, H-0073, ADR, contratos, nomenclatura,
`RELATORIO_IMPLEMENTACAO_H-0072.md`.

## Validações adicionais

V-DNF-12 prefixo não string; V-DNF-13 sufixo não string; V-DNF-14 chave
desconhecida em `designador`; V-DNF-15 `nenhum`+prefixo; V-DNF-16
`nenhum`+sufixo. V-DNF-01..11 permanecem.

## Testes adicionais

Além da regressão dos 18 casos: alfabetico sem adornos (`A`); alfabetico
+ `sufixo: ")"` (`A)`); prefixo; prefixo+sufixo; decimal sem adornos
(`1.1`); decimal com adornos só envolvendo a base; rejeições 7–11;
`nenhum` sem designador; ausência compatível; navegação/seleção e
texto/tabela inalterados.

## Fixture genérica

Alterável: sim. Acrescentar `prefixo: "("` e `sufixo: ")"` em
`console_h0072_tabela` (já `alfabetico_maiusculo`) → `(A)` `(B)`.
Preservar texto (`decimal_composto`) e `nenhum` sem adornos. Conteúdo
externo inalterado. Não vira fixture de H-0055.

## H-0055 / H-0073

H-0055 só como caso de capacidade no teste dedicado. Não configurar
`h0055_dois_niveis_por_foco.json`.

H-0073 preservado integralmente; retomado só após QA deste handoff,
PATCH_IMPLEMENTACAO H-0072 P01 e QA dessa implementação.

## Relatório futuro de implementação

`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P01.md`

Não sobrescrever `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md`.

## Verificações

- Nenhuma decisão documental permanece aberta.
- Menor delta de implementação nominalmente fechado.
- H-0073 não alterado.
- H-0055 não configurado concretamente.
- Handoff e este relatório existem.
- `git diff --check` nos dois artefatos desta etapa.

## Bloqueios

nenhum
\n