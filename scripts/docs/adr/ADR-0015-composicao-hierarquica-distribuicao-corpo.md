---
name: adr-0015-composicao-hierarquica-distribuicao-corpo
description: Formaliza composição hierárquica do corpo como árvore, grupo como nó estrutural, arranjo e distribuição por container, arredondamento determinístico, preenchimento de área alocada, regras dinâmicas de dimensão, sincronização de cortes e bloqueio do H-0019
metadata:
  type: adr
  scope: scripts
  status: aceita
  data: "2026-07-10"
  rastreabilidade:
    contratos_afetados:
      - docs/contratos/contrato_composicao_corpo.md
      - docs/contratos/contrato_tela_json.md
      - docs/contratos/contrato_json_tela_minima.md
    handoffs_afetados:
      - docs/handoff/H-0019-layout-horizontal-plano-corpo.md
---

# ADR-0015 — Composição hierárquica e distribuição de área do corpo

## Status

aceita

## Data

2026-07-10

---

## Contexto

Os contratos anteriores (ADR-0010, ADR-0011) estabeleceram `corpo.elementos[]`
como lista plana de elementos funcionais e `arranjo` como campo do `corpo`. A
ADR-0011 formalizou os valores `vertical`/`horizontal` para `corpo.arranjo`.

O H-0019 especificou o layout horizontal plano do corpo. A revisão pós-auditoria
do H-0019 (2026-07-09) rejeitou explicitamente a regra de N+1 vãos iguais e
adotou particionamento contíguo da largura disponível. Essa revisão revelou que
o `contrato_composicao_corpo.md` (seção 5.6) e `docs/NOMENCLATURA.md` (seção 10)
ainda registravam a regra antiga de "3 vãos iguais" — contradição normativa que
esta ADR formaliza e resolve.

Adicionalmente, foram identificadas necessidades de formalizar:

- a composição hierárquica do corpo como árvore (com nó estrutural `grupo`);
- regras de arranjo e distribuição por container;
- arredondamento determinístico para terminais com células inteiras;
- preenchimento de área alocada;
- regras dinâmicas de dimensão (mínimo/preferido/máximo);
- sincronização de cortes entre grupos.

Esta ADR é a autoridade normativa sobre todos esses tópicos. Onde houver
conflito com documentos anteriores (incluindo `docs/NOMENCLATURA.md`), esta
ADR prevalece.

---

## Decisão 1 — Corpo como árvore de composição

O corpo passa a ser modelado conceitualmente como **árvore de composição**.

### Tipos de nós

**Nós funcionais:**
- `console`
- `dashboard`
- `lancador`

**Nó estrutural:**
- `grupo`

`grupo` **não é** novo tipo funcional de corpo. É nó estrutural de composição.

---

## Decisão 2 — Grupo

`grupo`:
- não tem borda própria;
- não tem moldura visual;
- não tem título visual próprio;
- não tem conteúdo próprio;
- não é navegável por `[✥]`;
- não possui ação, item, chip, origem de dados ou `tela_destino`;
- recebe uma área do container pai;
- redistribui essa área entre seus filhos diretos;
- declara seu próprio `arranjo`;
- declara sua própria `distribuicao`;
- pode conter filhos funcionais e, em ciclo futuro, grupos aninhados.

---

## Decisão 3 — Nível

**Nível** é o conjunto de filhos diretos de um mesmo container.

Regras:
- `corpo.elementos[]` é o nível 1;
- `grupo.elementos[]` cria o próximo nível;
- cada grupo aninhado cria um novo nível;
- a profundidade máxima suportada é **3 níveis**;
- estruturas que exigirem nível 4 ou superior devem ser rejeitadas com
  erro estrutural determinístico.

---

## Decisão 4 — Arranjo por container

Cada container (`corpo` ou `grupo`) declara o **arranjo dos seus filhos diretos**.

Valores:
- `vertical`
- `horizontal`

Regras:
- `arranjo = horizontal` reparte largura entre filhos diretos;
- `arranjo = vertical` reparte altura entre filhos diretos;
- o arranjo de um container **não obriga** o arranjo dos containers filhos.

---

## Decisão 5 — Distribuição por container

A distribuição pertence ao **mesmo container** que declara o arranjo.

Regras:
- container horizontal: distribuição reparte colunas/largura;
- container vertical: distribuição reparte linhas/altura;
- distribuição aloca área, não apenas conteúdo;
- elemento funcional deve preservar a área alocada;
- sobra horizontal vira padding/espaços em branco;
- sobra vertical vira linhas em branco.

---

## Decisão 6 — Modos de distribuição

### Modo `igual`

Divide a área disponível igualmente entre filhos diretos.

### Modo `percentual`

- `distribuicao.valores[]` declara percentuais explícitos;
- quantidade de valores deve ser igual à quantidade de filhos diretos;
- soma dos valores deve ser exatamente 100;
- valores devem ser positivos;
- soma diferente de 100 é inválida.

Exemplo: `[40, 20, 40]` significa 40%, 20%, 40%.

### Modo `fracao`

- `distribuicao.valores[]` declara pesos relativos;
- quantidade de valores deve ser igual à quantidade de filhos diretos;
- todos os valores devem ser positivos;
- denominador implícito é a soma dos pesos;
- fração de cada filho é `valor_do_filho / soma_dos_valores`.

Exemplos:
- `[1, 1, 1]` significa `1/3`, `1/3`, `1/3`.
- `[2, 1, 2]` significa `2/5`, `1/5`, `2/5`, equivalente a 40%, 20%, 40%.

### Distribuição restrita/dinâmica

Conceitos de mínimo, preferido, máximo, restante e conteúdo são formalizados
na Decisão 11.

---

## Decisão 7 — Quantidade de valores

Regra obrigatória:

```
len(distribuicao.valores) == len(elementos)
```

A contagem considera somente filhos diretos do container onde a distribuição
é declarada.

**Não contar:**
- netos;
- descendentes internos de grupo;
- elementos visuais resultantes de expansão.

---

## Decisão 8 — Arredondamento determinístico

Como terminal usa células inteiras, percentuais/frações devem ser convertidos
pelo **método dos maiores restos**.

Regras:
- soma final das áreas alocadas deve ser exatamente igual à área disponível
  do container;
- empates de resto são resolvidos pela ordem declarada em `elementos[]`.

**Algoritmo:**
1. calcular tamanho ideal real de cada filho;
2. tomar a parte inteira;
3. somar partes inteiras;
4. calcular o resto necessário para fechar a área total;
5. distribuir unidades restantes aos maiores restos;
6. em empate, priorizar ordem declarada.

**Exemplos:**
- 68 linhas com `[1, 1, 1]` resulta em `[23, 23, 22]`.
- 68 linhas com `[2, 1, 2]` resulta em `[27, 14, 27]`.

---

## Decisão 9 — Contato entre molduras

### Horizontal

- não existe vão externo entre molduras;
- molduras adjacentes ficam coladas;
- pode aparecer `││`, `╮╭`, `╯╰`;
- primeira moldura inicia no primeiro caractere útil;
- última moldura termina no último caractere útil.

**Esta decisão supersede a regra de "3 vãos iguais"** registrada em
`contrato_composicao_corpo.md` seção 5.6 e em `docs/NOMENCLATURA.md`
seção 10. A regra correta é **particionamento contíguo** da largura
disponível — consequência natural de dividir a área entre os filhos
diretos sem vão externo. A regra de "N+1 vãos" foi rejeitada
explicitamente pelo usuário na revisão pós-auditoria do H-0019 (2026-07-09).

### Vertical

- não existe linha vazia externa automática entre molduras;
- base de uma caixa pode ser seguida imediatamente pelo topo da próxima;
- linha em branco interna pertence ao elemento, não ao vão entre elementos.

---

## Decisão 10 — Preenchimento de espaço vazio

A distribuição define **área alocada**. O renderer deve preservar a área
alocada. Se o conteúdo não preencher a área, o restante deve ser preenchido
com branco.

**Horizontal:** preencher com espaços; preservar largura da faixa.

**Vertical:** preencher com linhas em branco; preservar altura da faixa.

---

## Decisão 11 — Regras dinâmicas de dimensão

Conceitos futuros registrados:

- `minimo`: menor dimensão permitida;
- `preferido`: dimensão desejada;
- `maximo`: maior dimensão permitida;
- `restante`: recebe espaço remanescente;
- `conteudo`: dimensão ajustada ao conteúdo renderizado.

**Decisão:** `ajustado ao conteúdo` deve ser tratado como `preferido`,
não como `minimo`.

**Justificativa:**
- permite combinar `preferido = conteudo` com `maximo = 30%`;
- evita contradição quando conteúdo exigiria mais espaço que o máximo;
- se o conteúdo exceder o máximo, o elemento recebe o máximo e aplica
  overflow/paginação.

---

## Decisão 12 — Paginação

A composição aloca área. A paginação acontece **dentro** da área alocada.

Se um `console` recebe 10 linhas e tem conteúdo para 100 linhas, o
compositor **não aumenta automaticamente** o console. O console pagina
dentro das 10 linhas, conforme política declarada.

---

## Decisão 13 — Terminal muito pequeno

Registrado como decisão conceitual:
- área menor que a mínima normal deve ter política determinística;
- representação compacta futura com `...` é permitida;
- `...` é política de overflow/compactação, não fallback de composição;
- não pode haver truncamento silencioso;
- não pode haver fallback silencioso para outro arranjo.

---

## Decisão 14 — Sincronização de cortes entre grupos

Sincronização automática só é garantida quando grupos irmãos possuem:
- mesmo eixo interno de arranjo;
- mesma quantidade de filhos diretos;
- mesma distribuição declarada;
- mesma dimensão disponível no eixo distribuído;
- mesma assinatura de restrições dimensionais.

**Assinatura de restrições inclui:**
- `minimo`;
- `preferido`;
- `maximo`;
- `overflow`;
- `restante`;
- `conteudo`.

Se restrições diferentes alterarem os cortes, a sincronização automática
não é garantida.

---

## Decisão 15 — Sincronização explícita futura

Permitir mecanismo futuro conceitual:

```json
{
  "sincronizacao": {
    "grupo": "colunas_principais",
    "cortes": "obrigatorio"
  }
}
```

Regra:
- se `cortes = obrigatorio` e os grupos não puderem alinhar cortes, o
  renderer deve gerar **erro determinístico**;
- não deve ajustar silenciosamente;
- não deve ignorar sincronização declarada.

Schema final deste campo **não é fechado nesta ADR**.

---

## Decisão 16 — Bloqueio do H-0019

- H-0019 fica **bloqueado** por esta ADR;
- H-0019 **não deve ser implementado** na forma atual;
- H-0019 **deve ser revisado** após atualização documental;
- revisão do H-0019 deve remover qualquer regra conflitante com ADR-0015;
- retomada do H-0019 deve citar ADR-0015 como autoridade superior.

---

## Decisão 17 — Ciclos futuros

- H-0020 será responsável por criar/expandir grupos conforme planejamento futuro;
- hierarquia em 3 níveis ocorrerá em ciclo posterior;
- testes específicos de verificação dos níveis serão criados depois que H-0019
  e a hierarquia em 3 níveis estiverem implementados;
- ADR-0015 **não implementa** esses testes.

---

## Consequências

### Positivas

- A composição do corpo passa a ser extensível por árvore sem exigir novo
  tipo funcional.
- Distribuição de área é determinística e verificável.
- Particionamento contíguo elimina a ambiguidade da regra de vãos.
- Conceitos de mínimo/preferido/máximo são registrados de forma coerente.
- `ajustado ao conteúdo` como `preferido` (não `minimo`) permite combinação
  com restrição de máximo sem contradição.

### Negativas / Restrições

- H-0019 fica bloqueado e precisa de revisão antes de ser implementado.
- `docs/NOMENCLATURA.md` seção 10 ainda registra a regra antiga de "3 vãos
  iguais" — essa referência deve ser atualizada em ciclo futuro; NOMENCLATURA.md
  não é modificado por esta ADR; a ADR-0015 é autoridade superior sobre este
  ponto e prevalece.
- Testes de hierarquia em 3 níveis aguardam ciclos futuros (H-0020 e seguintes).
- Schema do mecanismo de sincronização explícita não é fechado nesta ADR.

---

## Contratos afetados

| Contrato | Alteração |
|---|---|
| `docs/contratos/contrato_composicao_corpo.md` | ADR-0015 adicionada; corpo como árvore; grupo como nó estrutural; nível e profundidade; arranjo e distribuição por container; modos de distribuição; arredondamento determinístico; preenchimento; conceitos dinâmicos; sincronização; regra de "3 vãos" removida/rebaixada |
| `docs/contratos/contrato_tela_json.md` | Grupo registrado; composição hierárquica como árvore; distribuição por container |
| `docs/contratos/contrato_json_tela_minima.md` | `corpo.elementos[]` pode conter grupos estruturais; distribuição opcional por container |

---

## Handoffs afetados

| Handoff | Status |
|---|---|
| `docs/handoff/H-0019-layout-horizontal-plano-corpo.md` | `BLOCKED_BY_ADR_0015_PENDING_REVISION` — deve ser revisado antes de qualquer implementação |
