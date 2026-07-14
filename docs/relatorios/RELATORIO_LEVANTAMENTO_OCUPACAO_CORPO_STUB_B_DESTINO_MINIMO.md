# Levantamento — ocupação do corpo em stub_b e destino_minimo

## 1. Escopo e raiz real

Comando de identificação da raiz:

```bash
git rev-parse --show-toplevel
```

Resultado observado:

```text
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1
```

O caminho solicitado para saída já é o caminho relativo real a partir dessa raiz:

```text
scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
```

Este levantamento não altera `stub_b.json`, `destino_minimo.json`, `orquestrador.json`,
código, contratos, ADRs ou testes. A única criação é este relatório.

## 2. Localização dos JSONs

Busca por arquivos com nome exato:

```bash
rg --files | rg '(^|/)(stub_b|destino_minimo|orquestrador)\.json$'
```

Ocorrências encontradas:

| Arquivo | Caminho | Classificação |
|---|---|---|
| `orquestrador.json` | `scripts/config/telas/orquestrador.json` | arquivo ativo de tela raiz |
| `destino_minimo.json` | `scripts/config/telas/destino_minimo.json` | arquivo ativo de tela, referenciado por `orquestrador.json` |
| `stub_b.json` | `scripts/config/telas/stub_b.json` | arquivo ativo de configuração de tela, coberto por loader/testes; não foi identificado item de lançador atual apontando para ele |

Não foram encontrados arquivos com esses nomes exatos em caminhos duplicados,
históricos ou de teste. Há menções textuais em documentação e testes, mas não
cópias homônimas dos JSONs.

Evidência de caminho ativo no código:

- `scripts/tela/loader.py:566-584` carrega `config/telas/<id_tela>.json`.
- `scripts/tela/loader.py:140-142` define a base padrão como o pai de `tela/`, isto é, `scripts/`.
- `scripts/tela/demo.py:226` carrega modelo por `id_tela` via `carregar_tela(None, id_tela)`.
- `scripts/config/telas/orquestrador.json:114-118` declara item com `tela_destino: "destino_minimo"`.

## 3. Comparação declarativa relevante

### 3.1 Corpo

| Campo | `orquestrador.json` | `destino_minimo.json` | `stub_b.json` |
|---|---|---|---|
| `id` | `orquestrador` | `destino_minimo` | `stub_b` |
| `corpo.arranjo` | `vertical` (`scripts/config/telas/orquestrador.json:23-24`) | `sobreposto` (`scripts/config/telas/destino_minimo.json:8-9`) | `sobreposto` (`scripts/config/telas/stub_b.json:8-9`) |
| `corpo.distribuicao` | `{"modo":"fracao","valores":[2,1,2]}` (`scripts/config/telas/orquestrador.json:25-28`) | ausente | ausente |
| filhos diretos | 3: `console`, `dashboard`, `lancador` (`scripts/config/telas/orquestrador.json:29-127`) | 1: `dashboard` (`scripts/config/telas/destino_minimo.json:10-24`) | 1: `dashboard` (`scripts/config/telas/stub_b.json:10-24`) |
| dimensões/margens/espaços/padding/bordas explícitos no corpo | não há campos explícitos desse tipo no objeto `corpo`; a diferença material é `distribuicao` | idem | idem |

Diferenças materiais:

```yaml
arquivo: scripts/config/telas/destino_minimo.json
caminho_json: corpo.arranjo
valor_atual: "sobreposto"
valor_na_referencia: "vertical"
possivel_efeito: Nenhum efeito material para o comportamento investigado; o renderer normaliza "sobreposto" para "vertical".
evidencia: scripts/tela/renderizador.py:1245-1250; scripts/tela/loader.py:33-37
```

```yaml
arquivo: scripts/config/telas/stub_b.json
caminho_json: corpo.arranjo
valor_atual: "sobreposto"
valor_na_referencia: "vertical"
possivel_efeito: Nenhum efeito material para o comportamento investigado; o renderer normaliza "sobreposto" para "vertical".
evidencia: scripts/tela/renderizador.py:1245-1250; scripts/tela/loader.py:33-37
```

```yaml
arquivo: scripts/config/telas/destino_minimo.json
caminho_json: corpo.distribuicao
valor_atual: ausente
valor_na_referencia: {"modo": "fracao", "valores": [2, 1, 2]}
possivel_efeito: Ausencia mantém o dashboard em altura natural e deixa a sobra como preenchimento externo entre corpo e barra; distribuicao explicita faz a moldura do filho ocupar a cota da area util.
evidencia: scripts/tela/renderizador.py:797-806; scripts/tela/renderizador.py:1290-1354; scripts/docs/contratos/contrato_composicao_corpo.md:595-618; scripts/docs/contratos/contrato_composicao_corpo.md:713-721
```

```yaml
arquivo: scripts/config/telas/stub_b.json
caminho_json: corpo.distribuicao
valor_atual: ausente
valor_na_referencia: {"modo": "fracao", "valores": [2, 1, 2]}
possivel_efeito: Ausencia mantém o dashboard em altura natural e deixa a sobra como preenchimento externo entre corpo e barra; distribuicao explicita faz a moldura do filho ocupar a cota da area util.
evidencia: scripts/tela/renderizador.py:797-806; scripts/tela/renderizador.py:1290-1354; scripts/docs/contratos/contrato_composicao_corpo.md:595-618; scripts/docs/contratos/contrato_composicao_corpo.md:713-721
```

```yaml
arquivo: scripts/config/telas/destino_minimo.json
caminho_json: corpo.elementos
valor_atual: um filho direto, tipo dashboard
valor_na_referencia: tres filhos diretos, tipos console/dashboard/lancador
possivel_efeito: O vetor [2,1,2] da referencia nao e copiavel: valores de fracao sao posicionais e a quantidade deve coincidir com a quantidade de filhos diretos.
evidencia: scripts/docs/contratos/contrato_composicao_corpo.md:374-381; scripts/tela/loader.py:163-167; scripts/tela/loader.py:700-702
```

```yaml
arquivo: scripts/config/telas/stub_b.json
caminho_json: corpo.elementos
valor_atual: um filho direto, tipo dashboard
valor_na_referencia: tres filhos diretos, tipos console/dashboard/lancador
possivel_efeito: O vetor [2,1,2] da referencia nao e copiavel: valores de fracao sao posicionais e a quantidade deve coincidir com a quantidade de filhos diretos.
evidencia: scripts/docs/contratos/contrato_composicao_corpo.md:374-381; scripts/tela/loader.py:163-167; scripts/tela/loader.py:700-702
```

### 3.2 Cabeçalho e barra_de_menus

Os três arquivos têm `cabecalho`, `corpo` e `barra_de_menus`. As diferenças de
título, descrição e texto de `chip_esc` explicam conteúdo/rotulagem, não a
ocupação vertical da moldura do elemento do corpo.

`barra_de_menus.distribuicao` é materialmente igual nos três arquivos: objeto
canônico com `modo: "horizontal_responsiva"`, mesmas regras de ordem, linhas,
espaçamentos, colunas e overflow. Portanto a diferença investigada não vem da
barra.

## 4. Rastreamento no código

### 4.1 Loader e validação

`scripts/tela/loader.py` é o loader efetivo. Ele:

- monta o caminho `config/telas/<id_tela>.json` (`scripts/tela/loader.py:566-584`);
- valida `schema`, `id`, `cabecalho`, `corpo`, `barra_de_menus` e `corpo.elementos`;
- aceita `corpo.arranjo` em `{None, "vertical", "horizontal", "sobreposto", "lado_a_lado"}` (`scripts/tela/loader.py:33-37`, `scripts/tela/loader.py:688-695`);
- define modos válidos de `corpo.distribuicao` como `igual`, `percentual`, `fracao` (`scripts/tela/loader.py:39-42`);
- só valida `corpo.distribuicao` quando o campo existe (`scripts/tela/loader.py:697-702`).

Ponto decisivo: `_validar_distribuicao_corpo` registra que a distribuição é
opcional e que a ausência preserva construção por conteúdo (`scripts/tela/loader.py:150-155`).
Para `modo: "igual"`, não exige `valores`; os pesos equivalentes são derivados no
renderer (`scripts/tela/loader.py:159-167`, `scripts/tela/loader.py:192-195`).

### 4.2 Modelo interno

`scripts/tela/modelo.py` transporta a distribuição sem inventar default:

- `Corpo.distribuicao` é opcional; `None` significa ausência declarada e não
  materializa `igual` (`scripts/tela/modelo.py:57-65`);
- `construir_modelo` atribui `corpo_raw.get("distribuicao")` diretamente ao
  modelo (`scripts/tela/modelo.py:299-303`).

### 4.3 Cálculo da área entre cabeçalho e barra

`renderizar_tela` calcula:

```text
l_corpo_disponivel = altura - l_cab - l_barra
```

Evidência:

- cabeçalho é montado antes do corpo (`scripts/tela/renderizador.py:1235-1243`);
- a barra é pré-computada quando `altura` existe (`scripts/tela/renderizador.py:1269-1273`);
- a área útil do corpo é `altura - l_cab - l_barra` (`scripts/tela/renderizador.py:1281`);
- o mesmo cálculo é refeito antes da inserção de preenchimento externo (`scripts/tela/renderizador.py:1317-1329`).

Essa área é passada ao container raiz:

```text
_renderizar_container(arranjo_corpo, distribuicao_corpo, elementos, ..., l_corpo_disponivel)
```

Evidência: `scripts/tela/renderizador.py:1283-1286`.

### 4.4 Como a área é atribuída ao corpo

No container vertical, há dois caminhos:

1. Com `distribuicao` e `altura_disponivel`: calcula pesos, reparte cotas e chama
   `_caixa_de_elemento(..., altura_alvo=cota)`. A moldura do elemento ocupa a
   cota (`scripts/tela/renderizador.py:797-806`, `scripts/tela/renderizador.py:820-824`).
2. Sem `distribuicao`: cada elemento usa sua altura natural (`scripts/tela/renderizador.py:827-845`).

Depois disso, `renderizar_tela` só evita preenchimento externo quando o corpo
vertical foi distribuído (`scripts/tela/renderizador.py:1290-1298`). Sem
distribuição, calcula `l_corpo_fill` e insere linhas físicas de espaços entre o
último bloco do corpo e a barra (`scripts/tela/renderizador.py:1339-1354`).

### 4.5 Pesos e modos

`_pesos_distribuicao` implementa:

- `igual` -> `[1] * n_filhos`;
- `percentual`/`fracao` -> `valores` declarados, posicionais.

Evidência: `scripts/tela/renderizador.py:203-216`.

`_distribuir_alturas` reparte `altura_disponivel` por maiores restos e garante
soma exata das cotas (`scripts/tela/renderizador.py:219-250`).

### 4.6 Testes existentes que cobrem o comportamento

Testes existentes relevantes, sem execução neste levantamento:

- `scripts/tela/teste_loader.py:837-915`: valida ausência sem fallback, `igual`
  explícito sem `valores`, `percentual` e `fracao`.
- `scripts/tela/teste_renderizador.py:3518-3575`: ausência preserva altura natural
  e gera preenchimento externo; `igual` explícito reparte a área.
- `scripts/tela/teste_renderizador.py:3692-3716`: `orquestrador.json` real declara
  fração `[2,1,2]`, distribui a altura e não gera preenchimento externo.
- `scripts/tela/teste_renderizador.py:3753-3761`: `destino_minimo`, `grupo_minimo`
  e `stub_b` hoje não declaram distribuição e chegam ao modelo com
  `modelo.corpo.distribuicao is None`.

## 5. Autoridades ativas consultadas

- `scripts/docs/contratos/contrato_composicao_corpo.md`
- `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `scripts/docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`
- código ativo em `scripts/tela/loader.py`, `scripts/tela/modelo.py` e
  `scripts/tela/renderizador.py`

Pontos normativos centrais:

- Arranjo e distribuição são distintos; `arranjo = "vertical"` sozinho não
  reparte altura (`scripts/docs/contratos/contrato_composicao_corpo.md:342-350`).
- A distribuição explícita de container vertical reparte linhas/altura, aloca
  área e transforma excedente em preenchimento interno
  (`scripts/docs/contratos/contrato_composicao_corpo.md:352-372`).
- Ausência de `distribuicao` preserva altura natural e pode deixar sobra como
  preenchimento externo (`scripts/docs/contratos/contrato_composicao_corpo.md:595-607`).
- `igual` só é válido quando declarado explicitamente
  (`scripts/docs/contratos/contrato_composicao_corpo.md:613-618`).
- A composição do corpo se aplica a todos os elementos funcionais, incluindo
  `dashboard` (`scripts/docs/contratos/contrato_composicao_corpo.md:1387-1391`).

## 6. Causa comprovada da diferença

Categorias:

- `CAMPO_DECLARATIVO_AUSENTE`
- `DEFAULT_APLICADO`
- `SUPORTE_EXISTENTE_NAO_ATIVADO`
- `VALOR_DECLARATIVO_DIFERENTE` apenas de forma secundária para `corpo.arranjo`,
  sem efeito causal comprovado porque `sobreposto` é normalizado para `vertical`

Causa real:

`destino_minimo.json` e `stub_b.json` não declaram `corpo.distribuicao`. O loader
preserva essa ausência como `None`; o modelo não materializa `igual`; o renderer,
mesmo recebendo `altura`, renderiza o único `dashboard` em altura natural e coloca
a sobra como preenchimento externo antes da `barra_de_menus`. No `orquestrador.json`,
`corpo.distribuicao` está declarado; por isso a altura útil calculada entre o
cabeçalho e a barra é repartida entre os filhos e absorvida dentro das molduras.

Não foi comprovado que a causa seja `TIPO_DE_CORPO_COM_SEMANTICA_DIFERENTE`: o
contrato diz que `dashboard`, `console` e `lancador` são elementos funcionais do
corpo e seguem a mesma fonte declarativa de posicionamento
(`scripts/docs/contratos/contrato_composicao_corpo.md:1387-1391`).

Não foi comprovado que a causa seja `SUPORTE_DE_CODIGO_AUSENTE`: o suporte para
distribuição vertical explícita já existe no loader, modelo e renderer.

## 7. Alterações mínimas necessárias

### 7.1 `destino_minimo.json`

```yaml
arquivo: scripts/config/telas/destino_minimo.json
alteracao_necessaria:
  - caminho_json: corpo.distribuicao
    operacao: adicionar
    valor_atual: ausente
    valor_proposto:
      modo: igual
    origem_do_valor: contrato ativo e suporte existente; "igual" explícito é o modo mínimo para um único filho direto, pois não exige valores e deriva peso [1]
    suporte_existente: sim; loader valida e preserva, modelo transporta, renderer reparte altura útil quando altura é fornecida
    evidencia: scripts/tela/loader.py:150-195; scripts/tela/modelo.py:299-303; scripts/tela/renderizador.py:203-216; scripts/tela/renderizador.py:797-806; scripts/docs/contratos/contrato_composicao_corpo.md:613-618
impacto_esperado: O dashboard "Teste" passa a receber a cota integral da área útil entre cabecalho e barra_de_menus, com preenchimento interno da moldura e sem sobra externa acumulada antes da barra.
necessita_codigo: nao
necessita_decisao_documental: nao
```

Não se recomenda copiar `{"modo":"fracao","valores":[2,1,2]}` de
`orquestrador.json`: esse valor é posicional e exige três filhos diretos. Em
`destino_minimo.json`, há um único filho direto; portanto `[2,1,2]` seria
incompatível com a regra `len(distribuicao.valores) == len(elementos)`.

### 7.2 `stub_b.json`

```yaml
arquivo: scripts/config/telas/stub_b.json
alteracao_necessaria:
  - caminho_json: corpo.distribuicao
    operacao: adicionar
    valor_atual: ausente
    valor_proposto:
      modo: igual
    origem_do_valor: contrato ativo e suporte existente; "igual" explícito é o modo mínimo para um único filho direto, pois não exige valores e deriva peso [1]
    suporte_existente: sim; loader valida e preserva, modelo transporta, renderer reparte altura útil quando altura é fornecida
    evidencia: scripts/tela/loader.py:150-195; scripts/tela/modelo.py:299-303; scripts/tela/renderizador.py:203-216; scripts/tela/renderizador.py:797-806; scripts/docs/contratos/contrato_composicao_corpo.md:613-618
impacto_esperado: O dashboard "STUB B" passa a receber a cota integral da área útil entre cabecalho e barra_de_menus, com preenchimento interno da moldura e sem sobra externa acumulada antes da barra.
necessita_codigo: nao
necessita_decisao_documental: nao
```

Também aqui não se recomenda copiar `[2,1,2]`, pelo mesmo motivo: o arquivo tem
um único filho direto em `corpo.elementos`.

## 8. Classificação da próxima natureza de trabalho

`ALTERACAO_DECLARATIVA_COBERTA_PELO_SUPORTE_EXISTENTE`

O ajuste identificado é adicionar `corpo.distribuicao: {"modo": "igual"}` nos
dois JSONs. Essa alteração não foi executada neste levantamento.

## 9. Validação futura

### 9.1 Testes automatizados

Sem executar agora, os seguintes testes poderiam comprovar posteriormente:

- validação sintática:
  - `python -m json.tool scripts/config/telas/destino_minimo.json`
  - `python -m json.tool scripts/config/telas/stub_b.json`
- loader/modelo:
  - confirmar que `carregar_tela(..., "destino_minimo")["corpo"]["distribuicao"]["modo"] == "igual"`;
  - confirmar que `carregar_tela(..., "stub_b")["corpo"]["distribuicao"]["modo"] == "igual"`;
  - confirmar que `construir_modelo(...).corpo.distribuicao` não é `None`.
- renderizador:
  - teste focal com `largura=42, altura=24` verificando que a altura da única
    moldura de dashboard em `destino_minimo` soma exatamente
    `altura - L_cabecalho - L_barra`;
  - mesmo teste para `stub_b`;
  - verificar ausência de linhas externas `" " * largura` entre a borda inferior
    do dashboard e a caixa de `Menus`;
  - comparar a mecânica com o caso existente do `orquestrador.json`, sem exigir
    os mesmos pesos `[2,1,2]`.
- regressão:
  - reexecutar as suítes existentes de loader, modelo, renderizador e demo que
    cobrem JSONs reais.

### 9.2 Pseudo-TTY

Após a alteração declarativa, poderiam ser usados cenários automatizados com
altura controlada para:

- `altura=24`;
- altura maior, por exemplo `30`;
- altura mínima suficiente para o conteúdo natural;
- altura insuficiente, esperando erro determinístico quando aplicável.

O objetivo seria confirmar que a cota do único dashboard acompanha a área útil
disponível e que a barra permanece posicionada após o corpo.

### 9.3 Validação humana em TTY real

Para observação real da interface em terminal:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Não há aprovação visual declarada neste levantamento.
