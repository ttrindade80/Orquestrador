# Relatório — patch da aplicação documental da ADR-0044 P01

```yaml
status: ADR_APPLICATION_PATCHED
patch: P01
item: ITEM-0017
adr: ADR-0044
raiz_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0044.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_ADR-0044_P01.md
```

## Motivo

A aplicação original havia mantido em aberto a localização, a forma e a
identidade do schema estrutural de pop-ups. O patch aprovado D-POP-25 fechou
essas decisões e exigiu sua propagação documental.

## Arquivos alterados

- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_popup.md`
- `docs/nomenclatura/35_POPUP.md`
- `docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0044_P01.md`

`docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` não foi alterado:
sua remissão transversal já distinguia JSON estrutural, conteúdo recebido e
runtime, preservando a propriedade terminológica do módulo 35.

## Propagação de D-POP-25

O contrato de `tela.json` agora registra `popups` como campo literal opcional
de nível geral, mapa/objeto `0..N`, com ausência e mapa vazio válidos, chave
como ID estável e sem `id` interno obrigatório. Também fecha a separação entre
declaração, envelope e instância, mantendo pop-ups fora das três regiões e da
árvore do corpo, sem origem, produtor ou loader.

O contrato especializado registra resolução por `popups[ID]`, falha anterior à
materialização para ID inexistente, envelope pronto, reutilização e não
mutação da declaração. O módulo 35 recebeu o vocabulário proprietário e as
distinções correspondentes.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_criados: []
  modulos_alterados:
    - docs/nomenclatura/35_POPUP.md
  termos_adicionados:
    - declaração de pop-up
    - ID de declaração de pop-up
    - mapa `popups`
    - resolução da declaração
  termos_alterados:
    - instância de pop-up
  distincoes_adicionadas:
    - mapa popups ≠ instância aberta
    - chave de popups ≠ conteúdo
    - declaração ≠ envelope de entrada
    - declaração ≠ estado vivo
    - declaração ≠ instância
    - ID estrutural ≠ posição física
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
```

## Verificações

Confirmadas nos arquivos alterados: campo literal `popups` no nível geral;
mapa/objeto `0..N`; ausência e mapa vazio válidos; chave como ID sem `id`
redundante; conteúdo concreto externo; ID inexistente bloqueia abertura;
envelope pronto; reutilização; distinção declaração/instância; exclusão das
regiões e do corpo; ausência de origem, produtor e loader; e ausência de novas
regras para H-0057 a H-0059. Também foram executados `git diff --check` e
inspeção focal somente dos arquivos autorizados.

## Bloqueios

```yaml
bloqueios: []
```
