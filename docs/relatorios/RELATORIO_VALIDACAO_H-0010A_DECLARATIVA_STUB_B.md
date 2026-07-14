# Relatório complementar — Validação declarativa pós-H-0010A com `stub_b`

## Status

VALIDACAO_EXPLORATORIA_APROVADA

## Contexto

Após a implementação e o QA do H-0010A — Fluxo mínimo de lançador com tela destino, foi realizado um teste complementar para verificar se o sistema já permite incluir novas telas e novos itens de lançador apenas por edição de JSON, sem alteração de código.

O objetivo não foi implementar nova funcionalidade no renderer, mas validar empiricamente a arquitetura declarativa recém-entregue pelo H-0010A.

O teste ocorreu antes do commit do ciclo, usando como base o estado implementado pelo handoff H-0010A.

## Objetivo da validação

Verificar se é possível:

```text
1. Criar uma nova tela JSON baseada em uma tela existente.
2. Registrar essa nova tela como destino de um item do lançador.
3. Exibir o novo item no lançador sem alterar código.
4. Acionar o novo chip do lançador.
5. Abrir a nova tela.
6. Retornar ao Orquestrador com Esc.
```

A hipótese validada era:

```text
Para criar uma nova tela do mesmo padrão estrutural já suportado, basta criar o JSON da nova tela e adicionar o item correspondente no lançador do JSON da tela chamadora.
```

## Arquivos envolvidos

### Criado experimentalmente

```text
config/telas/stub_b.json
```

### Alterado experimentalmente

```text
config/telas/orquestrador.json
```

### Referência de comparação

```text
config/telas/orquestrador.json_original
```

## Alterações declarativas testadas

### 1. Criação de nova tela `stub_b`

Foi criado o arquivo:

```text
config/telas/stub_b.json
```

A tela declara:

```text
schema = tela.v1
id = stub_b
cabecalho.titulo = STUB B - TESTE
cabecalho.descricao = Tela de destino para teste do lancador com múltiplas telas
corpo.arranjo = sobreposto
corpo.elementos[0].tipo = dashboard
corpo.elementos[0].titulo = STUB B
barra_de_menus.chips = Esc Voltar + Ajuda
```

O dashboard da tela `stub_b` contém valor literal:

```text
Tela stub B criada somente por JSON
```

### 2. Inclusão da tela no lançador do Orquestrador

No `config/telas/orquestrador.json`, o elemento `lancador_principal` passou a declarar dois itens:

```text
[d] Destino -> destino_minimo
[e] Stub B  -> stub_b
```

O novo item possui:

```text
id = item_stub_b
chip = e
texto = Stub B
tela_destino = stub_b
```

O texto `Stub B` respeita o limite contratual de 15 caracteres para itens do `lancador`.

### 3. Ajuste declarativo do dashboard da tela raiz

O título do dashboard da tela raiz foi alterado de:

```text
Info
```

para:

```text
Estado
```

A renderização refletiu a alteração sem mudança de código.

### 4. Redução declarativa dos chips da barra de menus

A barra de menus da tela raiz foi reduzida para:

```text
[Esc] Sair
[?] Ajuda
```

A renderização refletiu a remoção dos chips condicionais/excedentes sem mudança de código.

## Comandos executados

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/telas/stub_b.json >/dev/null && echo "stub_b.json OK"
python tela/demo.py
```

## Resultado observado

### Validação de JSON

Os dois JSONs foram validados com sucesso:

```text
orquestrador.json OK
stub_b.json OK
```

### Renderização do Orquestrador

A tela raiz passou a exibir:

```text
╭ ESTADO ...
╭ NAVEGAR ...
│ [d] Destino
│ [e] Stub B
╭ Menus ...
│ [Esc] Sair
│ [?] Ajuda
```

Isso confirma que:

```text
1. O título do dashboard veio do JSON.
2. A lista de itens do lançador veio do JSON.
3. A lista de chips da barra_de_menus veio do JSON.
```

### Abertura da tela `stub_b`

Ao acionar o chip `e`, a demo abriu a tela:

```text
STUB B - TESTE
```

E exibiu o dashboard:

```text
STUB B
Tela stub B criada somente por JSON
```

A barra da tela `stub_b` exibiu:

```text
[Esc] Voltar
[?] Ajuda
```

### Retorno ao Orquestrador

Após `Esc`, a demo retornou à tela `ORQUESTRADOR`, preservando o lançador com os dois itens:

```text
[d] Destino
[e] Stub B
```

### Validação cruzada com `destino_minimo`

Após o retorno, o item `[d] Destino` também continuou funcionando e abriu a tela `destino_minimo`, confirmando que a inclusão de `stub_b` não quebrou o fluxo entregue no H-0010A.

## Achados

### ACHADO-1 — Nova tela declarativa funcional

A criação de `config/telas/stub_b.json` foi suficiente para disponibilizar uma nova tela do mesmo padrão estrutural já suportado.

Não foi necessário alterar:

```text
tela/renderizador.py
tela/demo.py
tela/loader.py
tela/modelo.py
```

### ACHADO-2 — Lançador passou a aceitar múltiplos destinos declarados

O `lancador_principal.itens[]` passou a conter dois destinos e ambos foram exibidos na demo:

```text
[d] Destino
[e] Stub B
```

O acionamento do novo chip abriu corretamente a nova tela.

### ACHADO-3 — Barra de menus refletiu remoção declarativa de chips

A remoção dos chips condicionais/excedentes no JSON fez a barra renderizar apenas:

```text
[Esc] Sair
[?] Ajuda
```

Isso confirma que a barra não está presa a uma lista hardcoded de chips no renderer.

### ACHADO-4 — Dashboard refletiu alteração declarativa de título

A troca do título do dashboard de `Info` para `Estado` foi refletida diretamente na tela.

Isso confirma que o título da instância de `dashboard` vem do JSON/modelo.

### ACHADO-5 — `lado_a_lado` é preservado, mas ainda não executado visualmente

O `orquestrador.json` experimental passou a declarar:

```text
corpo.arranjo = lado_a_lado
```

O loader/modelo preservaram o valor, mas a saída visual continuou empilhada.

Portanto, a execução visual de `lado_a_lado` não pertence ao H-0010A e deve ser tratada no próximo ciclo.

Próximo trabalho definido:

```text
H-0011 — Renderização de arranjo lado_a_lado
```

## Limites da validação

Esta validação foi exploratória e ocorreu após o QA formal do H-0010A.

Como o `orquestrador.json` foi alterado manualmente depois do QA, testes com esperados literais do H-0010A podem falhar enquanto os arquivos de teste ainda esperarem o estado anterior:

```text
INFO
lista completa de chips condicionais
arranjo = sobreposto
```

Essas falhas não indicam necessariamente regressão do comportamento declarativo; indicam divergência entre o JSON experimental e os expected literals dos testes existentes.

Para commit com essas alterações incorporadas, é necessário reconciliar os testes ou registrar explicitamente que este relatório documenta uma validação exploratória separada do pacote originalmente aprovado.

## Conclusão

A validação foi bem-sucedida.

O sistema demonstrou que, para telas do mesmo padrão estrutural já suportado, é possível:

```text
1. Criar uma nova tela por JSON.
2. Adicionar essa tela ao lançador por JSON.
3. Exibir o novo item do lançador sem alterar código.
4. Abrir a nova tela pelo chip declarado.
5. Retornar com Esc conforme barra_de_menus da tela interna.
```

Resultado principal:

```text
A inclusão de novas telas simples por JSON está funcional para o padrão cabecalho + dashboard + barra_de_menus + item de lancador.
```

Resultado secundário:

```text
O próximo gargalo funcional não é mais a criação de telas por JSON, mas a execução visual de arranjo lado_a_lado no renderer.
```

## Recomendação de gestão

Fechar H-0010A com a evidência de que o fluxo mínimo de lançador com tela destino evoluiu para validação de múltiplas telas declarativas.

Registrar o próximo ciclo como:

```text
H-0011 — Renderização de arranjo lado_a_lado
```

Escopo preliminar do H-0011:

```text
- implementar execução visual de corpo.arranjo = lado_a_lado;
- aplicar o arranjo a elementos de corpo console/lancador conforme contrato;
- respeitar que dashboard possui posicionamento próprio;
- não criar nova tela;
- não alterar navegação;
- não alterar contratos ou ADRs;
- preservar comportamento declarativo validado no H-0010A.
```

