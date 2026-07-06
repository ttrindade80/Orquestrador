---
name: prompts-build-docs
description: Prompts operacionais para as sessoes de construcao de documentacao no Claude Code
metadata:
  type: prompts
  scope: build_docs
  criado_em: 2026-07-05
---

# Prompts — Construção de Documentação

Três prompts, cada um com um papel fixo. Usar como estão, ajustando só o
que estiver entre `[colchetes]`.

---

## Prompt 1 — Adicionar item ao `to_do.md`

Usar quando uma nova pendência surgir durante a conversa (decisão adiada,
mudança que contradiz contrato ativo, ou fato ainda sem descrição do
usuário) e precisar ser registrada sem se perder.

```
Leia scripts/docs/build_docs/instruction.md antes de qualquer coisa.

Adicione ao scripts/docs/build_docs/to_do.md um novo item com o formato já
usado no arquivo (mesmo template dos itens existentes: tipo, status,
arquivo(s) envolvido(s), origem, descrição, próxima ação).

Contexto do item a adicionar:
[descrever a decisão pendente, ou colar o trecho da conversa que originou]

Classifique como `pronto_para_execucao` só se a decisão já estiver
completamente fechada em docs/NOMENCLATURA.md e não sobrar nenhuma
pergunta em aberto. Caso contrário, classifique como `bloqueado_decisao` e
descreva exatamente o que falta decidir.

Não toque em nenhum outro arquivo além de to_do.md.
```

---

## Prompt 2 — Início de sessão de trabalho

Usar no começo de cada sessão de execução, pra pegar a próxima tarefa
pronta e restringir o escopo de escrita só aos arquivos daquela tarefa.

```
Leia scripts/docs/build_docs/instruction.md e
scripts/docs/build_docs/to_do.md antes de qualquer coisa.

Liste os itens com status pronto_para_execucao. Se houver mais de um,
pergunte qual eu quero executar antes de começar — não escolha sozinho.

Depois que eu escolher, releia a origem indicada no item (seção do
docs/NOMENCLATURA.md) pra confirmar que a decisão está mesmo fechada e sem
ambiguidade. Se encontrar algo que precisa de confirmação minha antes de
prosseguir, pergunte — não assuma.

A partir daí, você só pode escrever nos arquivos listados em
"Arquivo(s) envolvido(s)" desse item específico (e, se for criar um ADR
novo, no arquivo novo dele em docs/adr/). Nenhum outro arquivo do projeto
deve ser alterado nesta sessão.

Ao terminar, marque o item como concluído no to_do.md (não apague — deixe
o histórico) e me avise que terminou, sem rodar verificação de
consistência ainda (isso é outro prompt, só no fim de vários itens).
```

---

## Prompt 3 — Verificação final de consistência

Usar só ao final, depois de vários itens concluídos — não a cada alteração
individual (custo alto, sem necessidade de rodar toda hora).

```
Leia scripts/docs/build_docs/instruction.md antes de qualquer coisa.

Verifique a consistência entre os artefatos que definem [a tarefa X / o
conjunto de itens concluídos desde a última verificação]:
- docs/NOMENCLATURA.md (seções relevantes)
- Contrato(s) afetado(s) em docs/contratos/
- ADR(s) criada(s) em docs/adr/
- Arquivo(s) de config afetado(s) em config/

Cheque especificamente:
1. Nenhuma contradição entre o que o NOMENCLATURA.md diz e o que o
   contrato/ADR/JSON efetivamente registram.
2. Nenhum campo citado num arquivo sem existir nos outros (ex.: contrato
   referencia campo que não está no JSON, ou vice-versa).
3. Nenhuma pendência do to_do.md foi silenciosamente fechada sem estar de
   fato resolvida em todos os arquivos.
4. Nomenclatura de arquivo e campo segue a política da seção 0 do
   NOMENCLATURA.md (sem abreviação que misture termos distintos).

Relate cada inconsistência encontrada com a localização exata (arquivo +
trecho) — não corrija sozinho, só reporte. Se tudo estiver consistente,
diga isso explicitamente.
```
