---
name: instruction-build-docs
description: Como conduzir sessoes interativas de construcao de documentacao e como extrair fatos do sistema antigo via Codex
metadata:
  type: instrucao
  scope: build_docs
  criado_em: 2026-07-05
---

# Instruções — Construção de Documentação

## Papel nesta pasta

Aqui só se constrói documentação (`docs/NOMENCLATURA.md`, ADRs, contratos,
`config/*.json`). Nenhum código fora de `docs/build_docs/` é
tocado. Nenhuma implementação começa antes da documentação relevante
estar fechada — o objetivo é reduzir risco de ter que mudar código porque
foi necessário mudar a documentação depois.

## Regras herdadas do processo (não repetir, só lembrar)

- Nunca inventar valor que o usuário não disse. Ambiguidade é motivo pra
  perguntar, não pra assumir.
- Toda decisão nova é registrada **imediatamente** no lugar certo (ver
  "Onde registrar o quê" abaixo), não deixada solta na conversa.
- Mudança em contrato já `ativo` nunca é feita direto — sempre vira ADR
  primeiro (ver `docs/contratos/contrato_processo_desenvolvimento.md`,
  regra 6).
- Nomenclatura de arquivo nunca abrevia de forma que misture dois termos
  já distinguidos no glossário (ex.: `menu` vs `barra_de_menus` — ver
  `docs/NOMENCLATURA.md` seção 0).

## Como conduzir a sessão interativa

1. **Uma pergunta objetiva por vez.** Não empilhar três decisões
   diferentes numa pergunta só. Se surgir mais de uma pendência ao mesmo
   tempo, perguntar qual delas tratar primeiro.
2. **Oferecer opções concretas quando possível**, mas aceitar resposta
   livre — o usuário prefere digitar a escolher botão. Nunca assumir a
   opção mais provável e seguir sem confirmação.
3. **Distinguir "decidido" de "pendente" o tempo todo.** Se uma resposta
   fecha só parte de uma pergunta, registrar a parte fechada e continuar
   perguntando só o que falta — não fechar o item inteiro por engano.
4. **Verificar consequência cruzada antes de registrar.** Toda decisão
   nova pode contradizer algo já `ativo` — antes de escrever, checar se
   bate de frente com um contrato existente. Se bater, avisar que aquilo
   vai precisar de ADR antes de virar regra vigente (não é motivo pra não
   registrar a decisão em si no glossário, só pra marcar que ela ainda não
   é lei).
5. **Registrar assim que fechar**, não no fim da sessão inteira. Se a
   sessão for interrompida, nada se perde.
6. **Quando o usuário disser "fechado"/"terminamos X"**, resumir em texto
   corrido o que foi decidido antes de seguir pro próximo assunto — não
   silenciosamente assumir que está tudo registrado igual ao que foi dito.

## Onde registrar o quê

| Tipo de informação | Vai para |
|---|---|
| Nome, significado, tipo e regra de interpretação de um campo | `docs/NOMENCLATURA.md` |
| Valor concreto/default que o renderer vai ler | `config/<dominio>.json` |
| Mudança que contradiz um contrato já `ativo` | Nova entrada em `to_do.md` como `pronto_para_execucao`, tipo `adr` — nunca editar o contrato ativo direto |
| Decisão ainda não fechada, ou que o usuário decidiu adiar | `to_do.md`, seção "pendências"/"bloqueados" do glossário (seção 11) |
| Fato levantado do sistema antigo (não é decisão) | Seção 11 do `NOMENCLATURA.md`, marcado explicitamente como "levantamento, não decisão" |

## Como extrair fatos do sistema antigo via Codex

Usar sempre que uma decisão de design depender de saber o que o sistema
antigo realmente faz (não de como ele deveria funcionar).

**Regras do prompt de extração:**

- Papel do Codex: levantamento neutro. Nunca decidir arquitetura, nunca
  sugerir solução, nunca avaliar se o comportamento atual é bom ou ruim.
- Toda resposta precisa de evidência: arquivo + linha ou trecho de código.
  Sem evidência, a resposta é "não encontrado" — nunca preencher lacuna
  com suposição.
- Perguntas objetivas, numeradas, uma por comportamento específico (não
  "descreva como funciona X" solto).
- O Codex **nunca lê** `docs/NOMENCLATURA.md`, `docs/contratos/` nem
  qualquer artefato do sistema novo — a extração é só sobre o legado, pra
  não contaminar o levantamento com decisão já tomada.
- Resultado da extração entra na seção 11 do `NOMENCLATURA.md` como
  "levantamento — referência, não decisão" — só vira regra depois que o
  usuário decidir o que fazer com ela (pode confirmar, adaptar, ou
  descartar o comportamento do legado).

**Modelo de prompt** (adaptar escopo e perguntas pra cada caso — ver
exemplo real usado nesta sessão sobre `teste_classe_c.py`/`teste_combo.py`
no histórico, seção 11 do `NOMENCLATURA.md`):

```
# Prompt de extração — Codex

## Papel
Levantamento neutro de fatos do sistema antigo. Não decidir arquitetura,
não sugerir solução, não avaliar se o comportamento é bom ou ruim. Só
descrever o que o código faz, com evidência.

## Escopo
[arquivo(s) alvo, o que procurar]

## Perguntas a responder com evidência de código
1. [pergunta objetiva]
2. [pergunta objetiva]
...

## Formato de saída
Por pergunta: resposta objetiva + citação (arquivo:linha) + nota se não
encontrado ou ambíguo. Não preencher lacuna com suposição.

Não ler nem citar docs/NOMENCLATURA.md, docs/contratos/ ou qualquer
artefato do sistema novo.
```
