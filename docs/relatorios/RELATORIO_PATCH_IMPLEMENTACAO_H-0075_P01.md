# RELATORIO_PATCH_IMPLEMENTACAO_H-0075_P01

```yaml
cadeia:
  raiz: H-0075
  predecessor_imediato: RELATORIO_QA_IMPLEMENTACAO_H-0075.md
  item: ITEM-0026
  adr: ADR-0048
  handoff: H-0075
  patch_implementacao: P01
achados_tratados:
  - QA-IMPL-H0075-001
status: IMPLEMENTATION_PATCHED
```

## Causa

`_origem_satisfaz_predicado` aceitava a origem por política, `ConteudoExterno` e `pai.id`, sem exigir pertencimento real ao `modelo`. `_transferir_escolha_dois_niveis` gravava a seleção da origem antes da sincronização, indexando `estado["selecoes"]` por `console.id`.

Um clone estrangeiro com o mesmo ID, o mesmo `ConteudoExterno` (`is`) e a mesma política passava no predicado antigo: a escrita contaminava o console real e a enumeração dos destinos ainda podia propagar o candidato.

## Correção

Quando `modelo is not None`, a transferência compartilhada só começa se a origem for um dos consoles enumerados por `_enumerar_consoles_modelo` (mesmo descenso já usado para delimitar participantes).

Critério de pertencimento: identidade de objeto (`membro is console`). Igualdade de `console.id`, `pai.id`, política ou `ConteudoExterno` não autoriza.

Se a origem não pertencer:

- devolve o `estado` recebido;
- não chama `_escrever_selecao`;
- não propaga candidato;
- não cria vencedor nem efeito lateral.

`_origem_satisfaz_predicado` passou a receber `modelo` e recusa origem não pertencente antes do predicado restante. Chamada legítima com origem do modelo permanece inalterada. `modelo=None` (H-0074) não passa por essa guarda.

## Testes

Regressivo: `teste_origem_estrangeira_mesmo_id_nao_contamina_modelo`.

Modelo H-0072 real; origem clonada fora do modelo, mesmo `console.id`, mesmo `ConteudoExterno` e política `dois_niveis_por_foco`. `alternar(..., modelo=modelo)` não altera seleção do console real, candidato nem demais consoles.

Positivo adjacente: `teste_origem_real_do_modelo_sincroniza_legitimamente` — origem enumerada no modelo continua sincronizando o pai alvo nos três consoles, preservando o outro pai.

## Resultados

Coleta pytest de `tela/teste_filho_default_h0075.py` bloqueada pelo resíduo EOF histórico em `tela/carregamento/tela_json.py` (`SyntaxError` na linha 528). Não corrigido.

Evidência complementar em memória (stub de `tela.navegacao` só para evitar a cadeia loader/`tela_json`):

- adversarial mesmo ID: PASS;
- sincronização legítima / H-0072-like (três consoles): PASS;
- H-0074 `modelo=None` sem propagação: PASS;
- política diferente sem propagação: PASS;
- mapa candidato inconsistente → `TelaEstruturaInvalida`; Aplicar/solicitação recusam: PASS.

Suíte canônica `PYTHONDONTWRITEBYTECODE=1 python -m pytest`: 118 coletados / 44 erros de coleta (EOF em `tela_json.py`, `estilo.py`, `texto_ansi.py` e equivalentes). Nenhuma falha nova atribuída a este patch.

`git diff --check` nos três arquivos do manifesto: limpo.

Busca no delta P01: nenhuma autorização `origem.id in ids_do_modelo`. Pertencimento usa `is`.

## Arquivos alterados

- `tela/selecao.py`
- `tela/teste_filho_default_h0075.py`
- `docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0075_P01.md`

## Desvios e bloqueios

Nenhum arquivo fora do manifesto foi alterado nesta execução. Handoff, ADR, contratos, nomenclatura, backlog, demo, loaders, JSON e persistência intocados. Resíduos EOF históricos não corrigidos. QA pós-patch e validação TTY fora desta etapa.
