# Relatório de patch do handoff H-0075 — P02

```yaml
cadeia:
  raiz: H-0075
  predecessor_imediato: RELATORIO_QA_HANDOFF_H-0075_POS_P01.md
achados_tratados:
  - QA-H0075-001
  - QA-H0075-002
```

## QA-H0075-001 — eliminação da escolha silenciosa

O P01 removeu a precedência textual por primeiro da `lista_foco`, mas
ainda autorizava `mapa_candidato_filho_default` a ler o valor de um
console aplicável, sob o invariante de que a Espaço já teria equalizado
as listas. Chamadas de `alternar` sem `modelo` (compatibilidade H-0074)
podem deixar representações independentes do mesmo pai. Adotar uma
delas recria a precedência proibida.

O §4.8 passa a agrupar por documento externo + `pai.id`. Zero ou mais
representações equivalentes produzem uma entrada. Dois valores distintos
para o mesmo par falham fechados. Não há eleição por primeiro, último,
foco, console avulso ou ordem de `lista_foco`.

## Fail-closed

Sinalização interna: `mapa_candidato_filho_default` levanta
`TelaEstruturaInvalida` (`tela.carregamento.erros`) — família já usada
na persistência deste handoff. `aplicar_disponivel_filho_default`
captura e devolve `False` (inconsistência não é divergência aplicável).
`solicitar_aplicacao_filho_default` captura e devolve `None`. Sem
snapshot, sem pop-up, sem escrita, sem alteração de baseline, sem
vencedor; o documento persistido anterior permanece. Nenhum resultado
público de pop-up nem schema novo. Chamada sem `modelo` permanece
válida para os usos H-0074; não resolve concorrência. H-0074 não foi
reaberto.

`SolicitacaoAplicacaoFilhoDefault` só nasce de mapa coerente, único por
pai e independente da ordem dos consoles; depois permanece frozen.

## QA-H0075-002 — predicado de destino e sincronização por pai

O predicado “mesmo `ConteudoExterno` em `lista_foco`” era insuficiente:
contaminaria console de outra política que apenas compartilhasse o
documento. Destino agora exige, cumulativamente: mesmo `modelo`; mesmo
objeto `ConteudoExterno` (`is`); `tipo_navegacao_efetivo ==
"dois_niveis_por_foco"` (discriminador já existente, sem marcador novo);
mesmo `pai.id` em `conteudo_externo.nos`; semântica ITEM-0026. Enumeração
pelo descenso de elementos de H-0074, não por `lista_foco`.

A Espaço não copia mais a lista reconciliada inteira. Atualiza só a
escolha do `pai_alvo` nos destinos elegíveis; preserva demais entradas;
não copia pais inexistentes no destino; não escreve `selecoes` fora do
predicado. H-0072 permanece caso positivo.

## Testes

Itens 37–46 em §12, nos arquivos já autorizados:

1. dois consoles aplicáveis, mesmo candidato → uma entrada;
2. candidatos divergentes → fail-closed;
3. rejeição independente da ordem de `lista_foco`;
4. sem snapshot;
5. sem persistência válida;
6. sem escrita;
7. política distinta, mesmo documento → sem propagação (sintético em
   memória);
8. console que não apresenta o pai → intocado quanto a esse pai;
9. sync de um pai preserva os outros;
10. H-0072 continua compartilhando entre consoles aplicáveis.

Item 35 deixou de tratar a propagação como único mecanismo de
convergência: Espaço sincroniza o pai transferido; residual divergente
é rejeitado no mapa.

## Arquivos futuros

Reavaliados. As duas correções cabem em `tela/selecao.py` e
`demo/demo.py` já listados em §10.1, com testes nos arquivos já
autorizados. Nenhum arquivo novo.

## Verificações

```text
rg -n 'qualquer console|primeiro console|console.*vence|vence.*console|lista_foco.*preval|preval.*lista_foco'
→ nenhuma ocorrência; não resta regra que eleja valor por ordem ou console.

rg -n 'diverg|inconsist|fail.closed|mesma política|mesma politica|dois_niveis_por_foco|mesmo pai|propaga'
→ divergência de representações do mesmo pai é rejeitada; destino exige
  a mesma política `dois_niveis_por_foco`; sincronização é por pai.
```

## Bloqueios

nenhum.
