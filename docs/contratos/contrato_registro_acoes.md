---
name: contrato-registro-acoes
description: Contrato semântico do registro autoritativo de ações e da elegibilidade para o controle universal de execução
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  adrs_aplicadas:
    - docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md
  dependencias_nomenclatura:
    - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    - docs/nomenclatura/32_CONSOLE.md
---

# Contrato — registro autoritativo de ações

## 1. Objetivo e natureza

Este contrato define a semântica do registro autoritativo que acompanha a
implementação das ações. Ele é independente da arquitetura física do registro:
não escolhe localização, classe, dataclass, dicionário, módulo, centralização
ou distribuição.

A identidade de uma ação registrada é resolvida pelos mecanismos vigentes. O
registro mantém, junto à implementação, os metadados que são autoridade sobre
a categoria e a compatibilidade com modos de execução. O `tela.json` apenas
referencia a ação pelos mecanismos existentes; não recebe campo novo para
declarar ou duplicar esses metadados.

## 2. Registro da ação

Uma entrada que participe do registro autoritativo possui identidade já
resolvida e, obrigatoriamente, uma `categoria`. A ausência da entrada, da
identidade resolvida ou da categoria não é completada por inferência.

Forma semântica mínima:

```yaml
acao_registrada:
  identidade: resolvida_por_mecanismos_vigentes
  implementacao: autoridade_da_acao
  categoria: processo | navegacao | visualizacao
  modos_execucao_aceitos:
    - executar
    - dry_run
  # obrigatório para processo; a ação pode registrar somente um subconjunto real
```

O bloco é uma representação normativa, não uma exigência de formato ou de
estrutura física.

## 3. Categoria da ação

`categoria` é obrigatória para toda entrada que participe do registro e aceita
exatamente:

```yaml
categoria:
  enum:
    - processo
    - navegacao
    - visualizacao
```

Categoria ausente, desconhecida ou inferida é inválida. A configuração do JSON,
o identificador, o nome, o rótulo, o texto, o script, uma flag, um adaptador ou
o comportamento observado não substituem essa declaração autoritativa.

## 4. Modos de execução aceitos

Para uma ação de `processo`, `modos_execucao_aceitos` é obrigatório e seus
valores pertencem exatamente ao conjunto:

```yaml
modos_execucao_aceitos:
  valores_permitidos:
    - executar
    - dry_run
```

A ação declara somente os modos que realmente implementa. Portanto, uma ação
de processo que aceite apenas um modo continua registrada, mas não é elegível
para uma tela que declare `controle_execucao`, pois essa tela exige os dois
modos explicitamente.

Para `navegacao` e `visualizacao`, o campo não participa da elegibilidade do
controle universal. Este contrato não decide se ele deve estar ausente ou ser
tolerado nessas categorias e não cria semântica adicional para seus valores.

## 5. Resolução e elegibilidade da tela

Quando uma tela declara o objeto raiz `controle_execucao`:

1. suas ações relevantes são identificadas pelos mecanismos vigentes;
2. cada ação é resolvida no registro autoritativo;
3. cada entrada deve possuir categoria válida;
4. toda ação de `processo` deve declarar `modos_execucao_aceitos`;
5. toda ação de `processo` relevante deve aceitar explicitamente `executar` e
   `dry_run`;
6. a validação falha antes da execução quando qualquer requisito não é atendido.

Ações de navegação e visualização ficam fora da exigência do item 5, mas ainda
precisam resolver para entradas registradas com categoria válida. Uma ação
legada sem classificação não pode ser usada como ação de processo em tela
adotante. A tela não declara `categoria` nem `modos_execucao_aceitos` e não
pode contradizer, falsificar ou ignorar o registro.

Registro ausente, identidade não resolvida, categoria ausente ou desconhecida,
processo sem declaração de modos ou processo sem ambos os modos exigidos
produzem falha fechada de resolução. Não há fallback, compatibilidade implícita
ou elegibilidade parcial.

## 6. Autoridade e fronteiras

O registro da implementação é a fonte de verdade. A implementação consumidora
não pode ignorar sua classificação ou compatibilidade. Uma associação focal de
uma demonstração não representa autoridade universal.

Este contrato não exige migração global das ações legadas. Ações existentes sem
classificação podem permanecer fora da capacidade universal e são inelegíveis
para telas adotantes. Também não cria dispatcher, catálogo, registry físico
obrigatório ou protocolo público de execução.

## 7. Requisição e modo capturado

Este contrato preserva a transmissão semântica do modo: a tela captura
explicitamente `executar` ou `dry_run`, transmite-o na requisição e o faz
acompanhar o lote reconciliado quando aplicável. O modo não integra a identidade
do lote; o executor não consulta o runtime da interface; e uma requisição
iniciada permanece imutável.

Nenhuma representação interna concreta, como `{ids, modo}`, é transformada por
este contrato em protocolo público universal. A escolha dessa representação
permanece reversível quando já existente contrato público aplicável.
