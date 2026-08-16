# RELATORIO QA HANDOFF H-0073 POS P01

## Rastreabilidade

- etapa: `QA_HANDOFF`
- objeto: `H-0073`
- patch_auditado: `P01`
- cadeia_raiz: `docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md`
- predecessor_imediato: `docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0073_P01.md`

## Status

`H2_HANDOFF_PATCH_REQUIRED`

O bloqueio documental de H-0063 está resolvido. O pacote, porém, não fecha
integralmente H-0055.

## Auditoria

O escopo nominal está fechado: os JSONs estruturais de H-0055 e H-0063,
`tela/estilo.py`, os dois arquivos de teste H-0055 e os três testes novos
estão explicitamente autorizados; os arquivos preservados, incluindo o
conteúdo externo de H-0055 e as duas fixtures H-0072, estão identificados.
Não há descoberta de arquivo transferida para IMPLEMENTAR nem autorização
ampla estranha à atividade.

H-0063 está documentalmente fechada com tabulação 5..10, designador
`nenhum`, apresentação `tabela`, exatamente as colunas `preset` e `amostra`
e espaçamento 3..8. O handoff preserva literalmente `preset` e `titulo`,
determina `amostra` por `amostra_de_preset` sem parsing de `titulo`, autoriza
somente a extensão de `tela/estilo.py` e mantém `tela/renderizacao/estilo.py`
como leitura/preservação. Seleção, navegação, candidato, baseline, aplicação,
persistência e publicação permanecem protegidos.

H-0062 está fora da reconciliação como precedente histórico sem produtor
ativo. H-0072 permanece preservado, com regressão obrigatória e proibição de
alteração das fixtures. A regressão H-0070 está corretamente exigida sem
alteração antecipada da assertiva; o resultado futuro deve ser tratado por
causalidade. H-0055 e H-0063 têm demonstrações nominais pelo ponto de entrada
real `demo/demo.py`, incluindo a demonstração dinâmica de H-0063.

## Achado material

`ACH-001 — H-0055: designador vigente não preservado.`

O conteúdo externo autorizado como byte-a-byte preservado declara, em
`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`, o designador
filho `alfabetico_maiusculo` com sufixo `)`. Contudo, H-0073 §8.1 autoriza
somente `designador.tipo` e declara expressamente a mudança visual de `A)` a
`D)` para `A` a `D`, sem sufixo; §11.1 transforma essa mudança em critério de
aceite. Isso contradiz a exigência transportada de preservar o designador e a
apresentação vigentes, além da preservação de símbolos/conteúdo visual.

A justificativa de que o schema estrutural não aceita `sufixo` não resolve a
contradição: deixa aberta uma decisão material entre a autoridade de
preservação e a configuração proposta. H-0055, portanto, não está
integralmente fechada para IMPLEMENTAR. P01 requer patch documental antes da
implementação; nenhuma correção foi feita nesta auditoria.

\n