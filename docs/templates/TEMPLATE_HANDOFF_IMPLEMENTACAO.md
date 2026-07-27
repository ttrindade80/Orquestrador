---
name: H-NNNN-descricao
description: "[preencher] Objetivo verificável da implementação"
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-NNNN
  data_criacao: YYYY-MM-DD
rastreabilidade:
  contrato_alvo: null
  adr_relacionadas: []
  issues_relacionadas: []
  handoffs_anteriores: []
---

# H-NNNN — [Verbo + objeto + capacidade]

## 1. Etapa única

Este handoff autoriza exclusivamente:

`IMPLEMENTAR`

Ele não autoriza QA, aprovação, commit ou início de outro ciclo.

## 2. Ordem de autoridade

1. decisão explícita do usuário;
2. ADRs aprovadas e aplicadas;
3. contratos ativos;
4. este handoff.

Se houver falta, divergência ou decisão nova necessária, bloquear.

## 3. Estado comprovado

[Registre somente fatos comprovados. Use `NAO_CONFIRMADO` quando necessário.]

## 4. Objetivo

[Uma capacidade coesa e verificável.]

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - [arquivo indispensável]
leitura_focal:
  - arquivo: [arquivo]
    comando_busca: [comando exato]
    objetivo: [informação necessária]
buscas_autorizadas:
  - [caminho, termo e limite exatos]
nao_ler:
  - docs/relatorios/**, salvo item nominalmente autorizado acima
  - [outros caminhos fora do contexto]
```

Para leitura focal, execute o comando indicado e leia somente sua saída. Não abra o arquivo inteiro por conveniência. Se a saída for insuficiente, pare e solicite expansão focal; não amplie autonomamente o contexto.

## 6. Escopo da implementação

### 6.1 Arquivos e diretórios autorizados

- `[arquivo ou diretório relativo diretamente à raiz]`

Diretórios ainda inexistentes podem ser criados somente quando aparecerem nominalmente nesta lista.

### 6.2 Arquivos e diretórios preservados ou proibidos

- `[caminho relativo diretamente à raiz]`

### 6.3 Escopo positivo

- [Comportamento obrigatório]

### 6.4 Escopo negativo

- [Comportamento ou decisão fora deste ciclo]

## 7. Entradas, fixtures, temporários e saídas

```yaml
entradas_reais:
fixtures:
configuracoes:
temporarios_operacionais:
saidas_geradas:
politica_de_sobrescrita:
politica_de_limpeza:
```

Não misture entrada real com fixture. Não sobrescreva entrada real sem decisão explícita. Nenhuma evidência material pode permanecer somente em `/tmp`.

## 8. Tarefas

1. [Tarefa objetiva]
2. [Tarefa objetiva]
3. Executar as verificações locais previstas.
4. Criar o relatório próprio desta execução usando o template canônico.

## 9. Critérios de aceite

| ID | Critério | Evidência independente esperada |
|---|---|---|
| CA-01 | [Comportamento] | [Teste, inspeção, saída ou demonstração] |

O valor esperado não pode ser derivado da própria saída observada.

## 10. Testes obrigatórios

Execute a partir da raiz:

```bash
<comando>
```

Declare somente os casos, invariantes e regressões materialmente necessários. A suíte canônica do Orquestrador é `PYTHONDONTWRITEBYTECODE=1 python -m pytest`, salvo `NAO_APLICAVEL` justificado.

## 11. Demonstração operacional

```yaml
cwd: "."
comando:
entrada_ou_fixture:
configuracao:
saida_esperada:
prova_semantica:
arquivos_persistentes:
temporarios_operacionais:
limpeza_ou_restauracao:
validacao_manual:
  executor_exclusivo: USUARIO_EM_TTY_REAL
```

Código de saída zero, isoladamente, não comprova a entrega.

## 12. Relatório da execução

Criar um novo relatório em:

```text
docs/relatorios/IMP-NNNN-descricao.md
```

Usar obrigatoriamente:

```text
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

Regras:

- cada execução material produz seu próprio relatório;
- não sobrescrever relatório anterior;
- registrar somente fatos materiais, alterações, verificações, evidências, achados e bloqueios;
- não copiar código, diff completo, handoff, logs extensos ou metodologia narrativa;
- omitir campos e seções vazios;
- teto normal de 600 palavras; até 900 somente quando houver conteúdo material que não possa ser reduzido;
- evidência separada somente quando indispensável por formato, tamanho ou reutilização direta, sempre em `docs/relatorios/` e referenciada no relatório;
- o relatório não aprova formalmente a implementação.

## 13. Resposta terminal

Retorne somente:

```yaml
status: <STATUS_LITERAL>
relatorio: docs/relatorios/<arquivo>.md
artefatos:
  - <somente arquivos criados ou alterados>
bloqueios:
  - <somente quando houver>
proxima_acao: <somente quando objetivamente determinada>
```

Omitir campos vazios. Não copiar o relatório nem acrescentar conclusão narrativa.

## 14. Exceção operacional

Arquivo ou diretório fora da lista nominal não pode ser alterado silenciosamente.

Se um item externo for estritamente necessário para cumprir o handoff, preservar testes obrigatórios ou evitar aborto desproporcional:

1. pare antes da alteração;
2. informe item, motivo, escopo exato e mudança esperada;
3. peça autorização explícita ao usuário.

A autorização não permite criar semântica, arquitetura, schema, formato ou política nova.

## 15. Condições de bloqueio

Bloquear quando:

- faltar decisão;
- houver contradição documental;
- for necessário inventar formato ou schema;
- diretório novo necessário não estiver autorizado;
- houver risco de sobrescrever entrada real;
- o handoff for inexequível;
- a leitura focal autorizada for insuficiente.

Se o bloqueio ocorrer antes de qualquer resultado material, não crie relatório. Se já houver leitura, verificação, alteração ou evidência que precise sobreviver ao contexto, crie relatório factual do bloqueio.

## 16. Limite de encerramento

Ao concluir implementação, testes locais, demonstração e relatório, pare.

Não faça QA formal.
Não aprove a própria entrega.
Não prepare nem execute commit.
Não inicie outro ciclo.
