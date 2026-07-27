# Relatório de Validação Manual H-0040

## 1. Identificação

```yaml
etapa: VALIDACAO_MANUAL
handoff: H-0040
adr: ADR-0031
responsavel_execucao: usuario
ambiente: terminal_TTY_real
resultado_global: FALHOU_PATCH_NECESSARIO
```

## 2. Objeto

Registrar os resultados da validação manual da navegação simples e seleção única em consoles de nível único implementadas pelo H-0040.

A validação manual foi executada exclusivamente pelo usuário em terminal real.

Os resultados de QA automatizado anteriores permanecem preservados como histórico, mas não substituem a evidência manual.

## 3. Histórico da validação

A primeira rodada manual identificou problemas no roteiro, nos cenários de demonstração e na implementação.

Foram realizados:

1. levantamento pós-validação manual;
2. primeiro patch pós-validação;
3. QA rejeitado do primeiro patch;
4. segundo patch pós-validação;
5. QA aprovado do segundo patch;
6. repetição focal dos testes manuais afetados.

Os resultados finais consolidados são registrados neste relatório.

## 4. Resultado consolidado

```yaml
resultados_finais:
  VM-01: APROVADO
  VM-02: APROVADO
  VM-03: APROVADO
  VM-04: APROVADO
  VM-05: APROVADO
  VM-06: APROVADO
  VM-07: APROVADO
  VM-08: APROVADO
  VM-09: APROVADO
  VM-10: APROVADO
  VM-11: FALHOU
```

## 5. VM-01 — Avanço entre consoles

```yaml
resultado: APROVADO
comportamento_observado:
  - Tab moveu o foco para o próximo console
  - a navegação foi circular
  - a seta apareceu somente no console focado
```

## 6. VM-02 — Tab e Shift+Tab

O teste final utilizou o cenário com três consoles, permitindo distinguir o sentido direto do inverso.

```yaml
resultado: APROVADO
Tab:
  circularidade_correta: sim
Shift_Tab:
  circularidade_correta: sim
entrada_no_primeiro_item: sim
```

A ordem direta, inversa e circular foi observada corretamente.

## 7. VM-03 — Seta para a esquerda

```yaml
resultado: APROVADO
```

A navegação permaneceu na mesma linha, realizou retorno toroidal e não apontou células vazias.

## 8. VM-04 — Seta para a direita

```yaml
resultado: APROVADO
```

A navegação permaneceu na mesma linha, realizou retorno toroidal e não apontou células vazias.

## 9. VM-05 — Seta para cima

```yaml
resultado: APROVADO
```

A navegação permaneceu na mesma coluna, realizou retorno toroidal e não executou salto diagonal.

## 10. VM-06 — Seta para baixo

```yaml
resultado: APROVADO
```

A navegação permaneceu na mesma coluna, realizou retorno toroidal e não executou salto diagonal.

## 11. VM-07 — Item multilinha e modo verboso

O teste foi repetido após a correção do roteiro e da preservação do modo verboso.

```yaml
resultado: APROVADO
item_multilinha_visivel: sim
indicador_somente_na_primeira_linha: sim
modo_verboso_preservado_apos_navegacao: sim
sobreposicao_entre_itens: nao
```

Foi necessário reduzir a largura da janela para que o texto ocupasse múltiplas linhas.

A seta permaneceu somente no início do item selecionado e não foi repetida nas linhas seguintes.

### Observação de terminologia

“Linhas de continuação” são as linhas físicas adicionais pertencentes ao mesmo item quando seu texto não cabe em uma única linha.

No teste, a seta apareceu somente na primeira linha do item, conforme esperado.

## 12. VM-08 — Maximização da janela

```yaml
resultado: APROVADO
```

O mesmo item lógico permaneceu apontado após maximizar a janela.

## 13. VM-09 — Restauração da janela

```yaml
resultado: APROVADO
```

O mesmo item lógico permaneceu apontado após restaurar a janela.

## 14. VM-10 — Redistribuição de 2×3 para 3×2

```yaml
resultado: APROVADO
formacao_inicial: 2x3
formacao_apos_reducao: 3x2
mesmo_item_preservado: sim
indicador_acompanhou_item: sim
indicador_em_celula_vazia: nao
sobreposicao: nao
```

A distribuição visual foi recalculada e o item selecionado foi reposicionado corretamente.

## 15. VM-11 — Recálculo da navegação após redimensionamento

```yaml
resultado: FALHOU
formacoes_observadas:
  - 2x3
  - 3x2
identidade_do_item_preservada: sim
item_reposicionado: sim
indicador_permaneceu_no_item_correto: sim
sobreposicao: nao
navegacao_recalculada: nao
```

### Evidência material

Após a mudança da formação visual entre `2×3` e `3×2`:

* o item lógico permaneceu selecionado;
* o item foi reposicionado corretamente;
* a seta acompanhou o item;
* os vizinhos usados pelas teclas de direção não foram recalculados.

A navegação continuou refletindo a geometria anterior à mudança de tamanho.

### Classificação

```yaml
falha:
  tipo: DEFEITO_DE_IMPLEMENTACAO
  componente: recalculo_da_navegacao_apos_redimensionamento
  decisao_afetada: D10
  nova_ADR_necessaria: nao
  patch_necessario: sim
```

O defeito deve ser corrigido no ciclo existente.

## 16. Chips e encerramento

```yaml
chips:
  alternar_console_visivel_com_dois_ou_mais_consoles: sim
  navegar_itens_visivel_quando_aplicavel: sim

encerramento_normal:
  resultado: sim
```

## 17. Observações adicionais sobre distribuição espacial

Durante VM-07 foi observado que a distribuição reserva altura uniforme para os elementos de uma mesma formação.

Quando um item possui várias linhas e os demais possuem apenas uma linha, podem surgir áreas vazias associadas à altura do maior item.

O comportamento desejado levantado pelo usuário é:

```yaml
distribuicao_vertical_desejada:
  altura_de_cada_item: baseada_no_proprio_conteudo
  separacao_entre_itens:
    respeitar_configuracao_existente: true
    exemplos:
      - nenhuma_linha_em_branco
      - uma_linha_em_branco
      - duas_ou_mais_linhas_em_branco
  item_multilinha:
    nao_deve_criar_espaco_vazio_artificial_nos_demais_itens: true
```

Esse ponto ainda precisa de investigação separada para determinar se representa:

* defeito da distribuição atual;
* comportamento já contratado e não cumprido;
* ou nova forma de distribuição com alturas independentes.

Não foi classificado como causa da falha do H-0040 nesta execução.

## 18. Observações sobre cenários futuros de validação

Para validações mais fortes de navegação e distribuição, foram sugeridos cenários com:

```yaml
cenario_futuro:
  quantidade_minima_de_itens: 26

```
