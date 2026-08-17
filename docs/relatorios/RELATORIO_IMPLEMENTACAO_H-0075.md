# RELATORIO_IMPLEMENTACAO_H-0075

```yaml
item: ITEM-0026
adr: ADR-0048
handoff: H-0075
patch_handoff: P02
etapa: IMPLEMENTAR
status: IMPLEMENTATION_COMPLETED
```

## Arquivos efetivamente alterados

- `tela/selecao.py` — snapshot, mapas, Aplicar, sync por pai, persistência
- `tela/carregamento/conteudo_externo.py` — resolver, `caminho_arquivo`, patch, escrita atômica
- `tela/modelo.py` — `caminho_origem` runtime
- `demo/demo.py` — Enter/Aplicar, popup, override de caminho, `modelo=` no Espaço
- `config/telas/demo/h0055_dois_niveis_por_foco.json` — `chip_aplicar` + popup
- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json` — idem
- `tela/teste_filho_default_h0075.py` — criado
- `demo/teste_demo_filho_default_h0075.py` — criado
- `tela/teste_loader.py` — testes focais de resolver/persistir
- este relatório

Nenhum ADR, contrato, nomenclatura, backlog, `popup.py`, renderer, `estilo.py` ou JSON de conteúdo versionado foi alterado nesta execução.

## Compartilhamento documento+pai

A escolha é única por documento externo + `pai.id`. `alternar(..., modelo=)` sincroniza só aquele pai nos destinos que cumulativamente: pertencem ao modelo; compartilham o mesmo objeto `ConteudoExterno` (`is`); `tipo_navegacao_efetivo == "dois_niveis_por_foco"`; apresentam o pai; semântica ITEM-0026. Sem `modelo`, H-0074 permanece idêntico.

## Aplicar

`aplicar_disponivel_filho_default` é derivado: mapa candidato coerente ≠ baseline. Cursor e `lista_foco` não entram no cálculo. Inativo sem divergência; ativo com um ou vários pais.

## Inconsistência fail-closed

Representações distintas do mesmo pai levantam `TelaEstruturaInvalida` em `mapa_candidato_filho_default`. Aplicar fica inativo; solicitação `None`; sem snapshot, popup, escrita ou promoção. Não há eleição por primeiro/último/foco.

## Snapshot

`SolicitacaoAplicacaoFilhoDefault` frozen copia baseline, candidato (todos os pais) e `str(caminho_origem)`. Mutar `selecoes` depois não altera a instância. `CONFIRMADO` consome só o snapshot.

## Popup

Declaração `popup_confirmacao_aplicacao_filho_default` (`tipo: texto`, Voltar/Confirmar). Envelope genérico sem IDs. `popup.py` intocado.

## ABORTADO

Descarta a tentativa; arquivo, baseline, candidato e cursor preservados; Aplicar permanece ativo.

## CONFIRMADO

Persiste o snapshot; só `filho_default` pertinente muda; um `os.replace`; valida; promove baseline; equaliza `selecoes` dos destinos elegíveis; Aplicar inativo se não restar divergência.

## Caminho de destino

`ConteudoExterno.caminho_origem` (metadado runtime). Override `estado["caminhos_conteudo_externo"][id_tela]`. Persistência usa o caminho congelado no snapshot.

## Persistência atômica

Cópia profunda de `_raw`; tempfile no mesmo diretório; flush/fsync; `os.replace`; remove temporário em falha. Falha: arquivo anterior, baseline anterior, candidato divergente, Aplicar ativo; sem sucesso parcial nem retry.

## H-0072

Três consoles, mesmo `ConteudoExterno`: baseline comum; A altera → B observa e o inverso; foco irrelevante; mapa com uma entrada por pai; snapshot e write únicos; recarga restaura. Política diferente não recebe propagação.

## Testes focais

Comando (evidência complementar em memória, hook que ignora linha literal `\n` histórica em `.py` não autorizados):

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  tela/teste_filho_default_h0075.py \
  demo/teste_demo_filho_default_h0075.py \
  tela/teste_loader.py::teste_h0075_* \
  tela/teste_loader.py::teste_h0074_* \
  tela/teste_navegacao.py::teste_h0055_escolha_inicial_transferencia_idempotencia_e_isolamento
```

Resultado complementar: **33 passed**.

A suíte focada sem hook não coleta: `SyntaxError` em `tela/carregamento/tela_json.py:528` (`\n` literal pré-existente, arquivo fora da lista).

## Suíte canônica

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Resultado: **44 errors during collection** (resíduo EOF `\n` em `tela_json.py` e outros `.py` históricos). Causalidade pré-existente, não do H-0075. Complementar com o mesmo hook ainda interrompe em arquivos de teste históricos com o mesmo EOF (`teste_demo_console.py`, etc.).

## Prova com cópia temporária

`teste_prova_hash_abortado_confirmado_reabertura`: hash antes → divergência → ABORTADO (hash igual) → nova tentativa → CONFIRMADO (`filho_default` só nos pais esperados) → recarga restaura. Fixture versionada não foi escrita. Hashes finais das fixtures de conteúdo e de `config/estilo.json` inalterados nesta execução.

## Validação manual

`VALIDACAO_MANUAL_NECESSARIA` — `demo.py` ainda termina com `\n` literal histórico (não corrigido neste handoff). Procedimento TTY sobre cópia:

1. Copiar `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json` para arquivo temporário; anotar `sha256sum`.
2. Abrir a tela com `estado["caminhos_conteudo_externo"]["h0055_dois_niveis_por_foco"]` apontando para a cópia.
3. Espaço no nível filhos transfere a escolha; chip Aplicar ativo.
4. Enter → popup Voltar/Confirmar. Esc: hash inalterado; Aplicar ativo.
5. Enter + Confirmar: só `filho_default` muda na cópia; Aplicar inativo; reabrir restaura o novo valor.

Não declarar validação humana aprovada.

## Desvios

Removida a linha literal `\n` residual apenas dos dois JSON estruturais editados, para o documento permanecer JSON válido após `chip_aplicar`/`popups`. Sem reformatar `politica_paginacao`.

## Bloqueios

Nenhum bloqueio de implementação. Coleta da suíte canônica bloqueada por resíduo EOF histórico fora da lista autorizada.

`git diff --check` nos arquivos H-0075: limpo. ITEM-0023/0024 não tocados. H-0074 (`alternar` sem `modelo`) permanece.
