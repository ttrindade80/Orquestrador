---

id: RELATORIO_VALIDACAO_MANUAL_H-0035
tipo: validacao_manual
handoff: H-0035
data: 2026-07-17
resultado_literal: MANUAL_VALIDATION_APPROVED
resultado_normalizado: VALIDACAO_MANUAL_APROVADA
------------------------------------------------

# RELATÓRIO DE VALIDAÇÃO MANUAL H-0035

## 1. Identificação

```yaml
etapa_executada: VALIDACAO_MANUAL
rodada: POS_QUARTO_PATCH
handoff: H-0035
ambiente: terminal_real
resultado_literal: MANUAL_VALIDATION_APPROVED
resultado_normalizado: VALIDACAO_MANUAL_APROVADA
```

## 2. Objetivo

Registrar permanentemente o resultado da validação manual do H-0035 — distribuição matricial configurável de nível único do conteúdo dos elementos.

A validação foi realizada diretamente pelo usuário em uma janela real de terminal.

Os testes automatizados já haviam sido concluídos em etapa anterior. Esta etapa teve como objetivo observar o comportamento real das telas durante navegação, seleção, redimensionamento, redução da janela e recuperação da exibição.

## 3. Comando utilizado

O demo foi executado a partir da raiz do repositório com:

```bash
PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py
```

## 4. Explicações dos principais termos

Para tornar este relatório compreensível fora do contexto de desenvolvimento, os termos usados têm os seguintes significados:

* **Participante:** texto, campo ou item exibido dentro da tela.
* **Formação:** maneira como os participantes são organizados em linhas e colunas.
* **Distribuição horizontal:** maneira como a largura disponível é dividida.
* **Distribuição vertical:** maneira como a altura disponível é dividida.
* **Matriz fixa:** formação que mantém uma quantidade determinada de linhas e colunas.
* **Quadro mínimo:** mensagem que substitui a tela quando a janela fica pequena demais para mostrar a formação corretamente.
* **Recuperação:** retorno da tela normal depois que a janela volta a ter espaço suficiente.
* **Resto:** uma ou mais unidades de espaço que sobram quando a largura ou a altura não pode ser dividida igualmente.
* **Mínimo fixo:** tamanho externo que não deve crescer automaticamente apenas porque o conteúdo interno é maior.
* **Com distribuição matricial:** tela que usa a nova configuração implementada no H-0035.
* **Sem distribuição matricial:** tela que preserva o comportamento anterior do sistema.

## 5. Catálogo e navegação

O catálogo inicial foi exibido corretamente.

Foram confirmados:

```yaml
catalogo:
  identidade_inicial: CORRETA
  teclas_numericas: "1 a 9"
  teclas_alfabeticas: "A a P"
  comandos_com_dois_digitos: AUSENTES
  quantidade_de_telas: 25
  todas_as_telas_alcancaveis: SIM
  selecao_sem_enter: SIM
  letras_maiusculas: FUNCIONANDO
  letras_minusculas: FUNCIONANDO
  retorno_ao_catalogo: FUNCIONANDO
  saida_do_demo: FUNCIONANDO
  resultado: APROVADO
```

As opções de dois dígitos anteriormente usadas para as telas 10 a 25 não estavam mais presentes.

Cada tela pôde ser aberta com uma única tecla.

## 6. Resultado das 25 telas

| Tecla | Tela                              | Resultado |
| ----- | --------------------------------- | --------- |
| `1`   | `h0035_pref_linhas`               | APROVADO  |
| `2`   | `h0035_pref_colunas`              | APROVADO  |
| `3`   | `h0035_matriz_fixa_cabe`          | APROVADO  |
| `4`   | `h0035_matriz_fixa_quadro_minimo` | APROVADO  |
| `5`   | `h0035_centralizado_h_colunas`    | APROVADO  |
| `6`   | `h0035_esquerda_margens_min_max`  | APROVADO  |
| `7`   | `h0035_h_uniforme`                | APROVADO  |
| `8`   | `h0035_h_margens_limitadas`       | APROVADO  |
| `9`   | `h0035_v_margens_min`             | APROVADO  |
| `A`   | `h0035_v_margens_min_max`         | APROVADO  |
| `B`   | `h0035_v_uniforme`                | APROVADO  |
| `C`   | `h0035_um_centralizado`           | APROVADO  |
| `D`   | `h0035_tres_centralizados`        | APROVADO  |
| `E`   | `h0035_quatro_centralizados`      | APROVADO  |
| `F`   | `h0035_minimo_fixo_excedido`      | APROVADO  |
| `G`   | `h0035_uma_linha`                 | APROVADO  |
| `H`   | `h0035_uma_coluna`                | APROVADO  |
| `I`   | `h0035_resto_horizontal`          | APROVADO  |
| `J`   | `h0035_resto_vertical`            | APROVADO  |
| `K`   | `h0035_console_com`               | APROVADO  |
| `L`   | `h0035_console_sem`               | APROVADO  |
| `M`   | `h0035_lancador_com`              | APROVADO  |
| `N`   | `h0035_lancador_sem`              | APROVADO  |
| `O`   | `h0035_dashboard_com`             | APROVADO  |
| `P`   | `h0035_dashboard_sem`             | APROVADO  |

## 7. Formação dos participantes

Foram observados e aprovados:

```yaml
formacao:
  preferencia_por_linhas: APROVADO
  preferencia_por_colunas: APROVADO
  matriz_fixa_3x4: APROVADO
  matriz_fixa_4x4: APROVADO
  um_participante: APROVADO
  tres_participantes: APROVADO
  quatro_participantes: APROVADO
  formacao_em_uma_linha: APROVADO
  formacao_em_uma_coluna: APROVADO
```

A preferência por linhas e a preferência por colunas produziram comportamentos distintos durante o redimensionamento.

As matrizes fixas mantiveram a quantidade declarada de linhas e colunas enquanto havia espaço disponível.

Não foi observada reorganização indevida das matrizes fixas.

## 8. Distribuição horizontal e vertical

Foram observados e aprovados:

```yaml
distribuicao:
  centralizacao_horizontal: APROVADO
  alinhamento_a_esquerda: APROVADO
  distribuicao_horizontal_uniforme: APROVADO
  distribuicao_vertical_uniforme: APROVADO
  distribuicao_nos_dois_eixos: APROVADO
  margens_horizontais: APROVADO
  margens_verticais: APROVADO
  espacos_entre_participantes: APROVADO
```

As telas responderam às mudanças de largura e altura.

As células foram reduzidas ou ampliadas de acordo com o espaço disponível, preservando a formação correspondente.

As margens e os espaços entre participantes permaneceram coerentes durante o redimensionamento.

## 9. Distribuição do espaço restante

As telas destinadas à observação das sobras horizontal e vertical foram aprovadas.

```yaml
restos:
  horizontal: APROVADO
  vertical: APROVADO
  repeticao_do_mesmo_tamanho: DETERMINISTICA
```

Ao retornar a janela para um tamanho anteriormente observado, a mesma organização foi recuperada.

Não foram observadas mudanças aleatórias na posição dos participantes.

## 10. Mínimo fixo

A tela `h0035_minimo_fixo_excedido` foi validada.

```yaml
minimo_fixo:
  dimensao_externa_estavel: SIM
  formacao_preservada: SIM
  crescimento_automatico_indevido: NAO
  invasao_de_outra_celula: NAO
  quadro_minimo_acionado_apenas_pelo_conteudo: NAO
  bordas_preservadas: SIM
  espacos_preservados: SIM
  resultado: APROVADO
```

A área externa não cresceu automaticamente para acomodar o conteúdo interno.

Não foi observada invasão do espaço pertencente a outro participante.

## 11. Console

Foram comparadas as telas de console com e sem a nova configuração.

```yaml
console:
  com_distribuicao_matricial: APROVADO
  sem_distribuicao_matricial: APROVADO
  diferenca_visual: CONFIRMADA
  comportamento_anterior_preservado_na_tela_sem_configuracao: SIM
```

A tela com distribuição matricial apresentou os participantes organizados em grade.

A tela sem distribuição matricial preservou o comportamento anterior, exibindo o conteúdo histórico do console.

## 12. Lançador

Foram comparadas as telas de lançador com e sem a nova configuração.

```yaml
lancador:
  com_distribuicao_matricial: APROVADO
  sem_distribuicao_matricial: APROVADO
  diferenca_visual: CONFIRMADA
  comportamento_anterior_preservado_na_tela_sem_configuracao: SIM
  H0034_permanece_separado: SIM
```

A tela com distribuição matricial manteve sua formação declarada.

A tela sem distribuição matricial preservou o comportamento anterior, inclusive a reorganização histórica durante a redução da largura.

Nenhuma correção do H-0034 foi atribuída ao H-0035.

## 13. Dashboard

Foram comparadas as telas de dashboard com e sem a nova configuração.

```yaml
dashboard:
  com_distribuicao_matricial: APROVADO
  sem_distribuicao_matricial: APROVADO
  diferenca_visual: CONFIRMADA
  comportamento_anterior_preservado_na_tela_sem_configuracao: SIM
```

A tela com distribuição matricial alterou sua formação conforme a largura disponível.

A tela sem distribuição matricial preservou a apresentação histórica em coluna.

Não foi observada aplicação automática da nova configuração à tela que não a declarou.

## 14. Redimensionamento da janela

A validação foi realizada modificando o tamanho real da janela do terminal.

Foram executados:

```yaml
redimensionamento:
  maximizar: APROVADO
  restaurar: APROVADO
  reduzir_horizontalmente: APROVADO
  reduzir_verticalmente: APROVADO
  reduzir_nos_dois_eixos: APROVADO
  redimensionar_livremente: APROVADO
  entrar_no_quadro_minimo: APROVADO
  recuperar_a_tela_normal: APROVADO
  segunda_reducao: APROVADO
  segunda_recuperacao: APROVADO
  necessidade_de_reiniciar_o_demo: NAO
```

O quadro mínimo apareceu quando a janela ficou pequena demais para mostrar a formação.

Ao aumentar novamente a janela, a tela normal foi recuperada.

O processo pôde ser repetido sem deixar elementos ou estados da exibição anterior.

## 15. Integridade visual

Durante a validação das 25 telas, não foram observados:

```yaml
integridade_visual:
  participantes_perdidos: NAO
  participantes_duplicados: NAO
  sobreposicao_invalida: NAO
  desenho_fora_da_area: NAO
  mistura_com_tela_anterior: NAO
  estado_residual: NAO
  traceback: NAO
  erro_fatal: NAO
```

## 16. Resultado consolidado

```yaml
catalogo: APROVADO
formacao: APROVADO
distribuicao_horizontal: APROVADO
distribuicao_vertical: APROVADO
distribuicao_nos_dois_eixos: APROVADO
matrizes_fixas: APROVADO
cardinalidades: APROVADO
restos: APROVADO
minimo_fixo: APROVADO
console: APROVADO
lancador: APROVADO
dashboard: APROVADO
redimensionamento: APROVADO
quadro_minimo: APROVADO
recuperacao: APROVADO
integridade_visual: APROVADO
```

## 17. Observação sobre o formulário utilizado

O formulário original usado durante a validação apresentou problemas de linguagem e organização.

```yaml
formulario_de_validacao:
  resultado: INADEQUADO
  problemas:
    - perguntas repetidas;
    - termos técnicos sem explicação;
    - campos formulados por negação;
    - critérios cujo significado não estava claro;
    - repetição da mesma observação em partes diferentes;
    - respostas aparentemente contraditórias causadas pela redação;
  responsabilidade_do_usuario: NENHUMA
  impacto_na_validacao:
    - não invalida a aprovação declarada pelo usuário;
    - não constitui defeito da implementação;
    - não deve ser convertido em reprovação técnica;
```

A aprovação deste relatório considera a declaração final e inequívoca do usuário após a execução de todas as 25 telas.

## 18. Regra para futuras validações manuais

Os próximos roteiros de validação manual devem:

1. indicar claramente a tecla e a tela;
2. dizer em linguagem comum o que deve aparecer;
3. explicar todo termo técnico antes de utilizá-lo;
4. evitar perguntas repetidas;
5. evitar perguntas formuladas pela negativa;
6. não exigir que o usuário conheça terminologia de desenvolvimento;
7. solicitar apenas informações que possam ser observadas diretamente;
8. não tratar ambiguidades do formulário como erro do usuário;
9. registrar o resultado no projeto imediatamente após a validação.

## 19. Assunto futuro fora do H-0035

O fornecimento externo de dados aos elementos da tela não faz parte do H-0035.

```yaml
fornecimento_externo_de_dados:
  pertence_ao_H0035: false
  tratamento: ADR_FUTURA
  adr_criada_nesta_etapa: false
  handoff_criado_nesta_etapa: false
  numero_de_handoff_reservado: false
  implementado_nesta_etapa: false
```

Nenhum número de handoff foi criado ou reservado.

## 20. Conclusão

A validação manual do H-0035 foi concluída em terminal real.

As 25 telas do catálogo foram abertas e avaliadas.

A navegação, as formações, as distribuições horizontal e vertical, as matrizes fixas, as margens, os espaços, os restos, o mínimo fixo, os consumidores, o quadro mínimo e a recuperação foram aprovados.

Não foram observados erros fatais, perda de participantes, duplicação, sobreposição inválida ou estado residual.

O H-0035 está manualmente aprovado.

## 21. Resultado literal

```text
MANUAL_VALIDATION_APPROVED
```

## 22. Resultado normalizado

```text
VALIDACAO_MANUAL_APROVADA
```

## 23. Próxima categoria

```text
FECHAMENTO_MANUAL
```
