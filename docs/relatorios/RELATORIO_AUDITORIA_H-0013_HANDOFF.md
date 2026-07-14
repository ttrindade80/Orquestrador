# Relatorio de Reauditoria — H-0013 Demo de acesso a tela grupo minimo

## Status final

`QA_APPROVED`

## Natureza desta auditoria

Reauditoria pos-correcao do handoff:

`docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md`

Este relatorio substitui a auditoria anterior, mantendo rastreabilidade do
primeiro resultado:

- auditoria anterior: `QA_REJECTED`
- achados anteriores: 1 bloqueante, 2 nao bloqueantes
- motivo bloqueante anterior: contradicao entre permitir o chip `g` e proibir
  "novo chip declarativo"
- objetivo desta reauditoria: verificar se as correcoes resolveram o bloqueio
  e as notas sem abrir nova ambiguidade ou expansao de escopo

Nenhum codigo foi implementado. Nenhum arquivo de codigo foi editado. Nenhum
commit foi realizado. O unico arquivo atualizado nesta etapa foi este relatorio.

## Arquivos lidos

- `docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0013_HANDOFF.md`
- `docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/relatorios/RELATORIO_QA_H-0012_GRUPO_ESTRUTURAL_MINIMO_TELA_ISOLADA.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_json_lancador.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `config/telas/orquestrador.json`
- `config/telas/destino_minimo.json`
- `config/telas/grupo_minimo.json`
- `tela/demo.py`
- `tela/renderizador.py`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/teste_demo.py`
- `tela/teste_renderizador.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_diagnostico.py`

Todos os arquivos obrigatorios existem.

## Comandos executados

```bash
git status --short
git log --oneline -5
sed -n '1,260p' docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
sed -n '261,620p' docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
sed -n '621,980p' docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
sed -n '1,260p' docs/relatorios/RELATORIO_AUDITORIA_H-0013_HANDOFF.md
sed -n '1,260p' docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
sed -n '1,240p' docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
sed -n '1,260p' docs/relatorios/RELATORIO_QA_H-0012_GRUPO_ESTRUTURAL_MINIMO_TELA_ISOLADA.md
sed -n '1,260p' docs/contratos/contrato_processo_desenvolvimento.md
sed -n '1,240p' docs/contratos/contrato_lancador.md
sed -n '1,240p' docs/contratos/contrato_json_lancador.md
sed -n '1,260p' docs/contratos/contrato_tela_json.md
sed -n '1,260p' docs/contratos/contrato_composicao_corpo.md
sed -n '1,280p' docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
sed -n '1,220p' config/telas/orquestrador.json
sed -n '1,220p' config/telas/destino_minimo.json
sed -n '1,220p' config/telas/grupo_minimo.json
sed -n '1,280p' tela/demo.py
sed -n '1,320p' tela/loader.py
sed -n '1,320p' tela/modelo.py
sed -n '1,380p' tela/renderizador.py
sed -n '1,260p' tela/teste_demo.py
sed -n '261,620p' tela/teste_demo.py
sed -n '621,1040p' tela/teste_demo.py
sed -n '1,260p' tela/teste_diagnostico.py
sed -n '1,620p' tela/teste_loader.py
sed -n '1,520p' tela/teste_modelo.py
sed -n '1,1040p' tela/teste_renderizador.py
rg -n 'novo chip declarativo|novo tipo de chip|novo mecanismo de chip|novo binding de chip|O chip `g`|working tree|tipo `grupo` funcional|tipo `grupo` estrutural|IMP-0013|TTY|subprocess|Alterar obrigatório|Alterar condicional|Arquivos proibidos' docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
python -c "from copy import deepcopy; from tela.loader import carregar_tela; from tela.modelo import construir_modelo; from tela.demo import processar_comando; raw=deepcopy(carregar_tela(None,'orquestrador')); raw['corpo']['elementos'][2]['itens'].append({'id':'item_grupo_minimo','chip':'g','texto':'Grupo Min.','tela_destino':'grupo_minimo'}); modelo=construir_modelo(raw); estado={'tipo_borda':'curva','saindo':False,'tela_atual':'orquestrador','pilha_telas':[]}; e=processar_comando(estado,'g',modelo); v=processar_comando(e,'\x1b'); print(e['tela_atual'], e['pilha_telas'], e['saindo'], v['tela_atual'], v['pilha_telas'], v['saindo'])"
python -c "from tela.loader import carregar_tela; from tela.modelo import construir_modelo; from tela.renderizador import renderizar_tela; m=construir_modelo(carregar_tela(None,'grupo_minimo')); g=m.corpo.elementos[0]; s=renderizar_tela(m, largura=80); print(m.id, g.tipo, len(g.elementos), g.elementos[0].tipo, 'GRUPO MINIMO' in s, 'Dashboard dentro de grupo estrutural' in s, s.count('╭'))"
```

## Evidencias

### Estado Git e base

`git log --oneline -5` confirmou HEAD base:

```text
0bcb477 feat: implementa grupo estrutural minimo em tela isolada
6c91279 docs: cancela H-0011 e remove H-0011A
a940fbc docs: fecha base documental de composicao hierarquica
f41bd2f docs: registra validacao declarativa com stub b
36c55d2 feat: implementa fluxo minimo do lancador com tela destino
```

`git status --short` antes da atualizacao deste relatorio indicava apenas os
documentos H-0013 nao rastreados:

```text
?? docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0013_HANDOFF.md
```

### Correcao do bloqueante anterior

O handoff corrigido removeu a ambiguidade anterior. A proibicao agora esta
redigida como:

```text
NAO criar novo tipo de chip, novo mecanismo de chip, nova semantica de chip,
novo registry de chip nem novo binding de chip.
O chip `g` do item declarativo previsto em F-1 e um valor de campo JSON em
`lancador.itens[]` ja suportado pelo codigo existente -- nao e um novo tipo de
chip nem um novo mecanismo. Adicionar esse item ao JSON do Orquestrador e o
escopo central deste handoff e esta explicitamente autorizado.
```

Interpretacao de QA: B-01 esta resolvido. O texto distingue adequadamente:

- permitido: adicionar o valor declarativo `chip: "g"` em item existente do
  tipo `lancador`;
- proibido: criar novo tipo, mecanismo, semantica, registry ou binding de chip.

Nao ha mais contradicao entre o escopo positivo e o escopo negativo.

### Confirmacao tecnica do fluxo

`tela/demo.py` ja percorre `lancador.itens[]` declarados no modelo:

- `processar_comando` percorre `modelo.corpo.elementos`;
- filtra `elemento.tipo == "lancador"`;
- percorre `_campos_inertes["itens"]`;
- compara `item.get("chip")` com o comando;
- ao encontrar coincidencia, empilha a tela atual e troca para
  `item.get("tela_destino")`.

Simulacao em memoria do item `g`, sem alterar arquivo:

```text
grupo_minimo ['orquestrador'] False orquestrador [] False
```

Interpretacao: o chip `g` navega para `grupo_minimo`, empilha
`orquestrador`; Esc volta para `orquestrador` sem definir `saindo=True`.
Portanto `demo.py` permanece corretamente proibido.

### Confirmacao tecnica de `grupo_minimo`

Carregamento, modelo e renderizacao:

```text
grupo_minimo grupo 1 dashboard True True 3
```

Interpretacao: `grupo_minimo` carrega como grupo estrutural com exatamente
1 dashboard interno; a renderizacao contem `GRUPO MINIMO`, contem o valor
literal do dashboard e produz 3 caixas visuais, coerente com cabecalho,
dashboard interno e menus, sem caixa propria do grupo. Portanto
`loader.py`, `modelo.py`, `renderizador.py` e `grupo_minimo.json` permanecem
corretamente proibidos neste ciclo.

### Correcao das notas anteriores

NB-01 foi corrigida. O handoff agora afirma que a working tree estava limpa
no commit base, exceto pelo proprio arquivo do handoff nao rastreado ate o
commit documental. Isso e coerente com a situacao observada.

NB-02 foi corrigida. A formulacao relevante usa `tipo "grupo" estrutural`; a
busca por `tipo "grupo" funcional` nao encontrou ocorrencia remanescente.

## Verificacoes obrigatorias

| Item | Resultado |
|---|---|
| 1. B-01 resolvido | Sim. |
| 2. Chip `g` permitido como valor declarativo de item de `lancador` | Sim. |
| 3. Novo tipo/mecanismo/semantica de chip proibidos | Sim. |
| 4. Handoff nao proibe a alteracao declarativa central | Sim. |
| 5. NB-01 e NB-02 corrigidas | Sim. |
| 6. Lista de arquivos permitidos suficiente e minima | Sim. Inclui JSON do Orquestrador, testes obrigatorios, condicionais adequados e IMP-0013. |
| 7. Lista de arquivos proibidos nao contradiz escopo positivo | Sim. |
| 8. `demo.py` corretamente proibido | Sim. Binding declarativo ja existe. |
| 9. `loader.py`, `modelo.py`, `renderizador.py` corretamente proibidos | Sim. Suporte de H-0012 basta. |
| 10. Nao autoriza segundo elemento em `grupo_minimo.json` | Sim. Proibido e coberto por CA-14/CA-15. |
| 11. Preserva `destino_minimo` | Sim. Item `d` deve permanecer inalterado e funcionando. |
| 12. Exige relatorio de implementacao | Sim. `IMP-0013-demo-acesso-tela-grupo-minimo.md`. |
| 13. Criterios de aceite testaveis | Sim. |
| 14. Diferencia TTY manual e testes automatizados | Sim. Ha secao especifica para subprocess e TTY real. |
| 15. Nao ha nova lacuna arquitetural | Sim. |

## Observacoes de escopo

A lista de arquivos permitidos esta adequada. A leitura dos testes confirmou
que, alem dos arquivos obrigatorios, os condicionais sao reais:

- `tela/teste_renderizador.py` possui constantes `_EXPECTED_ORQUESTRADOR` e
  `_EXPECTED_ORQUESTRADOR_RETA` com `[d] Destino`;
- `tela/teste_loader.py` verifica `lancador_principal.itens` com 1 item;
- `tela/teste_modelo.py` verifica a lista inerte do lancador com 1 item.

Isso nao e falha do handoff: a propria secao "Alterar condicional" permite
esses tres arquivos se a verificacao demonstrar dependencia de contagem ou
saida do Orquestrador.

O handoff tambem preserva corretamente os limites gerenciais:

- nao adiciona segundo elemento ao grupo;
- nao implementa `lado_a_lado`;
- nao implementa grupo aninhado;
- nao implementa distribuicao por percentual ou fracao;
- nao migra o Orquestrador inteiro para grupo;
- nao altera semantica de `grupo`;
- nao altera contratos nem ADRs;
- nao reabre H-0011;
- nao recria H-0011A;
- nao usa letras na sequencia;
- nao remove nem quebra `destino_minimo`;
- nao transforma `grupo` em caixa visual propria.

## Achados bloqueantes

Nenhum.

## Achados nao bloqueantes

Nenhum.

## Decisao final

`QA_APPROVED`

O handoff H-0013 corrigido esta implementavel sem ressalvas. A contradicao
anterior foi resolvida integralmente, as duas notas foram corrigidas, os
arquivos permitidos/proibidos estao coerentes com o escopo e os criterios de
aceite sao verificaveis. Nao foi identificada nova lacuna arquitetural nem
expansao indevida de escopo.

## Proxima etapa recomendada

Implementar o H-0013 exatamente conforme o handoff corrigido, criando o
relatorio `docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md` e sem
alterar codigo de modulo.
