# Relatório de patch do handoff H-0075 — P01

```yaml
cadeia:
  raiz: H-0075
  predecessor_imediato: RELATORIO_QA_HANDOFF_H-0075.md
achados_tratados:
  - QA-H0075-001
```

## Decisão do usuário

A autoridade sobre concorrência entre consoles foi fechada: a escolha
candidata é única por par documento externo + pai, não por console. Se o
mesmo pai é apresentado por vários consoles, todos representam a mesma
escolha; alterar essa escolha em qualquer console atualiza a escolha
compartilhada observada pelos demais. `lista_foco` não tem papel na
persistência — governa apenas travessia/navegação, como já fechado em
`contrato_console.md` §22.2 e `nomenclatura/32` §4.5.

## Remoção da precedência por `lista_foco`

QA-H0075-001 apontava que o §4.8 original mandava persistir "a escolha do
primeiro console da `lista_foco` que divergir", fixando
`console_h0072_texto` como primeiro — autoridade nova, não amparada por
ADR-0048, pelo contrato ou pela nomenclatura. O §4.8 foi reescrito por
completo: a regra foi removida integralmente, com qualquer variante
("primeiro console vence", precedência por ordem de foco). A verificação
textual sobre o arquivo final não retornou nenhuma ocorrência.

## Chave e representação runtime para compartilhamento por pai

Levantamento focal confirmou que `_propagar_conteudo_externo`
(`tela/modelo.py`) já atribui o **mesmo objeto** `ConteudoExterno` a todos
os consoles de um documento — logo os nós-pai e
`pai.campos["filho_default"]` (baseline) já são, por identidade de
objeto, uma única fonte por pai. O problema estava isolado no candidato:
`estado["selecoes"]` (H-0074) é indexado por `console.id`, então o mesmo
pai podia ter entradas independentes em consoles distintos.

Correção mínima, compatível com H-0074, sem novo armazenamento: parâmetro
opcional `modelo=None` em `alternar` e `_transferir_escolha_dois_niveis`
(`tela/selecao.py`), retrocompatível com toda chamada de H-0074 que não o
informa. Quando informado, após reconciliar a escolha do console de
origem, a mesma lista reconciliada é propagada, no mesmo evento de
Espaço, para `estado["selecoes"]` de todo console em
`navegacao.lista_foco(modelo)` cujo `conteudo_externo` seja o mesmo
objeto (identidade `is`). `demo/demo.py` passa `modelo=modelo` no ramo de
Espaço de `dois_niveis_por_foco`. Nenhum schema público novo, nenhum
segundo armazenamento persistido.

`mapa_candidato_filho_default` deixa de "mesclar" valores de consoles:
como a propagação garante entrada idêntica por pai entre todos os
consoles aplicáveis, a leitura é determinística, independente de qual
console ou de qual ordem de `lista_foco` é usada.

## Comportamento H-0072

O §4.8 fecha que os três consoles observam a mesma baseline e o mesmo
candidato por pai; uma alteração em qualquer um atualiza a escolha
compartilhada visível nos demais, inclusive antes de qualquer Aplicar;
trocar foco ou mover cursor não altera o candidato; Aplicar calcula
divergência uma única vez por `pai.id` (nunca por par console-pai); o
snapshot contém uma única entrada por pai; a persistência escreve o
`filho_default` uma única vez por pai.

## Alterações na lista futura de arquivos

Sem arquivo novo. Ajustadas apenas as descrições de delta de
`tela/selecao.py` (parâmetro `modelo` e propagação) e `demo/demo.py`
(passar `modelo=modelo` no ramo de Espaço) na tabela §10.1. Os arquivos já
autorizados (`tela/teste_filho_default_h0075.py`,
`demo/teste_demo_filho_default_h0075.py`) absorvem os testes novos.

## Testes adicionais

Dez testes explícitos de H-0072 inseridos em §12 (itens 26–35): baseline
compartilhada inicial; propagação A→B e B→A sem candidato concorrente;
imunidade a troca de foco/cursor; `aplicar_disponivel` sem dependência de
ordem; snapshot com valor único por pai; persistência e restauração desse
valor; inversão de `lista_foco` sem efeito; ausência de código de
resolução entre consoles. O item de regressão H-0074 foi renumerado para
36, cobrindo as chamadas existentes sem `modelo`.

## Verificações

As duas buscas obrigatórias foram executadas sobre o arquivo final: a
primeira (precedência entre consoles) não retornou ocorrência; a segunda
(compartilhamento por documento/pai) retornou múltiplas ocorrências no
§4.8 e nas demais seções já fechadas, confirmando o fechamento semântico
por pai.

## Bloqueios

Nenhum. A extensão aditiva de `alternar`/`_transferir_escolha_dois_niveis`
é compatível com a assinatura e o comportamento já fechados por H-0074;
nenhuma reabertura de schema externo, de ADR, de contrato ou de
nomenclatura foi necessária.
