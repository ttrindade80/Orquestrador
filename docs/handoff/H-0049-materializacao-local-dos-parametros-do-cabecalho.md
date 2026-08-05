# H-0049 — materialização local dos parâmetros do cabeçalho

## Objetivo e autoridade

Implementar uma única capacidade coesa: declarar os parâmetros locais de
apresentação no `cabecalho` de cada JSON estrutural de tela, validá-los no
loader, transportá-los pelo modelo e consumi-los no renderer, preservando
`config/estilo.json` como fonte exclusiva da aparência global compartilhada.

Estado de entrada: `ITEM-0015`, ADR-0008 aplicada,
`ADR_APPLICATION_APPROVED`, schema local suficiente e sem bloqueios
documentais. Este handoff aplica somente o schema já determinado por
`docs/contratos/contrato_cabecalho.md`; não cria ADR, campo, enumeração,
default, alias, fallback, política de geometria ou abstração pública.

## P06 — baseline migratório aprovado

Este patch documental transporta para o handoff a decisão normativa aprovada
no P05. O baseline de migração para descrições que devem conservar o resultado
observável anterior é:

```yaml
patch:
  identificador: P06
  predecessor_imediato:
    status: ADR_APPLICATION_APPROVED
    patch_h0049_liberado: true

baseline_migratorio:
  cabecalho:
    apresentacao:
      descricao:
        capitalizacao: preservar
      titulo:
        capitalizacao: maiusculas
```

`preservar` é uma escolha declarada para a descrição e não um default ou
fallback. Depois do corte por `max_caracteres`, a operação é identidade:
mantém exatamente o texto cortado, sem `upper()`, `lower()`, `isalpha()`,
locale, normalização Unicode, inserção, remoção ou reinterpretação de
caracteres. Prefixo, sufixo, frases posteriores e string vazia permanecem
literais. `inicio_de_frase` continua sendo uma escolha explícita, suportada e
obrigatoriamente testada; não é o baseline de preservação. `maiusculas`
continua sendo conversão integral por `str.upper()`.

O título não participa desta correção: seu baseline continua sendo
`capitalizacao: maiusculas`, com `posicao: esquerda`, `recuo_lateral: 0` e
`formato_na_borda: com_espacos_laterais`.

```yaml
evidencia_do_baseline_anterior:
  telas_estruturais_auditadas: 72
  descricoes_que_mudariam_com_inicio_de_frase: 17
  relatorio_normativo: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P05.md
```

## Schema normativo e semântica já decidida

Todos os objetos abaixo são fechados e todos os campos são obrigatórios:

```json
{
  "cabecalho": {
    "titulo": "Texto do título",
    "descricao": "Texto da descrição",
    "apresentacao": {
      "titulo": {
        "posicao": "<valor válido>",
        "recuo_lateral": 0,
        "capitalizacao": "<valor válido>",
        "formato_na_borda": "<valor válido>"
      },
      "descricao": {
        "max_caracteres": 1,
        "alinhamento": "<valor válido>",
        "recuo": 0,
        "capitalizacao": "<valor válido>"
      }
    }
  }
}
```

Valores e regras a aplicar, sem interpretação adicional:

| Caminho | Tipo/domínio | Regra de consumo |
|---|---|---|
| `cabecalho.titulo`, `cabecalho.descricao` | `string` | conteúdos concretos da tela |
| `apresentacao.titulo.posicao` | `esquerda` \| `centro` \| `direita` | posiciona o bloco do título na borda superior |
| `apresentacao.titulo.recuo_lateral` | inteiro ≥ 0 | distância do canto correspondente; ignorado no centro |
| `apresentacao.titulo.capitalizacao` | `maiusculas` \| `inicio_de_frase` | transformação antes da renderização |
| `apresentacao.titulo.formato_na_borda` | somente `com_espacos_laterais` | bloco `espaço + título + espaço` integrado à borda |
| `apresentacao.descricao.max_caracteres` | inteiro de 1 a 200, inclusive | cortar a descrição antes de capitalizar e alinhar |
| `apresentacao.descricao.alinhamento` | `esquerda` \| `centro` \| `direita` | posiciona o texto dentro da largura útil |
| `apresentacao.descricao.recuo` | inteiro ≥ 0 | distância da borda correspondente; ignorado no centro |
| `apresentacao.descricao.capitalizacao` | `maiusculas` \| `inicio_de_frase` \| `preservar` | transformação após o corte contratual |

```yaml
cabecalho.apresentacao.descricao.max_caracteres:
  tipo: inteiro
  minimo: 1
  maximo: 200
  limites_inclusivos: true
```

`inicio_de_frase` tem semântica normativa fechada e não é sinônimo de aplicar
`upper()` ao texto inteiro. Para a descrição, a entrada do algoritmo é o texto
já cortado por `max_caracteres`; o algoritmo é:

1. receber o texto já cortado por `max_caracteres`;
2. percorrer os caracteres na ordem original;
3. localizar o primeiro caractere `c` para o qual `c.isalpha()` retorne
   `True`;
4. substituir somente esse caractere pelo resultado exato de `c.upper()`;
5. incorporar integralmente o resultado, mesmo quando `upper()` produzir mais
   de um caractere;
6. preservar literalmente todos os caracteres anteriores;
7. preservar literalmente todos os caracteres posteriores;
8. encerrar a busca após a primeira substituição;
9. não converter o restante para minúsculas;
10. não modificar frases posteriores;
11. devolver o texto original quando não houver caractere alfabético;
12. devolver string vazia para entrada vazia.

O critério alfabético é a semântica de `str.isalpha()` do Python. A
transformação é a semântica exata de `str.upper()` do Python, sem locale, sem
normalização Unicode prévia, sem regex, sem lista manual de letras, sem
limitação a ASCII e sem biblioteca externa. A expansão de `upper()` é sempre
incorporada por inteiro. O título continua sujeito somente à limitação
geométrica já existente da linha superior; a descrição pode sofrer o corte
geométrico já existente depois do corte contratual por `max_caracteres`. Não
introduzir nova política de overflow.

Exemplos normativos:

| Entrada | Resultado |
|---|---|
| `execução da API REST` | `Execução da API REST` |
| `  execução concluída` | `  Execução concluída` |
| `123 - execução` | `123 - Execução` |
| `área útil` | `Área útil` |
| `çalışma` | `Çalışma` |
| `Δ resultado` | `Δ resultado` |
| `ßeta` | `SSeta` |
| `123 --` | `123 --` |
| `""` | `""` |

## Manifesto de implementação autorizado

### JSONs estruturais de tela — 72 alterações nominais

Em cada arquivo a seguir, manter `cabecalho.titulo` e
`cabecalho.descricao` como strings e acrescentar exclusivamente
`cabecalho.apresentacao` completo. Preencher os oito valores com o
`baseline_de_migracao` abaixo. Não inserir campo implícito, alias ou
compatibilidade.

```yaml
baseline_de_migracao:
  titulo:
    posicao: esquerda
    recuo_lateral: 0
    capitalizacao: maiusculas
    formato_na_borda: com_espacos_laterais

  descricao:
    max_caracteres: 200
    alinhamento: esquerda
    recuo: 1
    capitalizacao: preservar
```

O bloco migratório completo para as 72 telas estruturais, fixtures
preexistentes e documentos que precisam conservar a descrição observável é:

```json
{
  "apresentacao": {
    "titulo": {
      "posicao": "esquerda",
      "recuo_lateral": 0,
      "capitalizacao": "maiusculas",
      "formato_na_borda": "com_espacos_laterais"
    },
    "descricao": {
      "max_caracteres": 200,
      "alinhamento": "esquerda",
      "recuo": 1,
      "capitalizacao": "preservar"
    }
  }
}
```

`preservar` é o baseline migratório da descrição; não é default nem fallback.
Depois do corte por `max_caracteres`, o resultado permanece exatamente como
se encontra, inclusive prefixo, sufixo, frases posteriores e string vazia.
O baseline anterior com `inicio_de_frase` é rejeitado para preservação porque
alteraria descrições literais.

```yaml
impacto_do_baseline_anterior:
  telas_estruturais_auditadas: 72
  descricoes_alteradas_por_inicio_de_frase: 17
evidencia_normativa:
  relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P05.md
```

Esse baseline preserva a aparência vigente porque:

- `formato_na_borda: com_espacos_laterais` já produz os espaços imediatamente
  anteriores e posteriores ao título;
- `recuo_lateral: 0` preserva a posição física atual do bloco do título;
- `recuo: 1` preserva o espaço físico atual entre a borda esquerda e a
  descrição;
- os valores `3` e `10` pertencem a uma configuração global que nunca foi
  consumida;
- esses valores são obsoletos e não representam o quadro visual vigente;
- a implementação não deve migrar, reinterpretar nem compensar `3` e `10`.

- `config/telas/demo/demo.json`
- `config/telas/demo/destino_minimo.json`
- `config/telas/demo/grupo_minimo.json`
- `config/telas/demo/h0029_dashboard_fracao.json`
- `config/telas/demo/h0029_dashboard_igual.json`
- `config/telas/demo/h0029_dashboard_percentual.json`
- `config/telas/demo/h0029_grupo_fracao.json`
- `config/telas/demo/h0029_grupo_igual.json`
- `config/telas/demo/h0029_grupo_pai_distribuido.json`
- `config/telas/demo/h0029_grupo_percentual.json`
- `config/telas/demo/h0030_console_unico.json`
- `config/telas/demo/h0030_dashboard_unico.json`
- `config/telas/demo/h0030_matriz_2x2.json`
- `config/telas/demo/h0030_matriz_2x4.json`
- `config/telas/demo/h0030_matriz_3x2.json`
- `config/telas/demo/h0035_catalogo.json`
- `config/telas/demo/h0035_centralizado_h_colunas.json`
- `config/telas/demo/h0035_console_com.json`
- `config/telas/demo/h0035_console_sem.json`
- `config/telas/demo/h0035_dashboard_com.json`
- `config/telas/demo/h0035_dashboard_sem.json`
- `config/telas/demo/h0035_esquerda_margens_min_max.json`
- `config/telas/demo/h0035_h_margens_limitadas.json`
- `config/telas/demo/h0035_h_uniforme.json`
- `config/telas/demo/h0035_lancador_com.json`
- `config/telas/demo/h0035_lancador_sem.json`
- `config/telas/demo/h0035_matriz_fixa_cabe.json`
- `config/telas/demo/h0035_matriz_fixa_quadro_minimo.json`
- `config/telas/demo/h0035_minimo_fixo_excedido.json`
- `config/telas/demo/h0035_pref_colunas.json`
- `config/telas/demo/h0035_pref_linhas.json`
- `config/telas/demo/h0035_quatro_centralizados.json`
- `config/telas/demo/h0035_resto_horizontal.json`
- `config/telas/demo/h0035_resto_vertical.json`
- `config/telas/demo/h0035_tres_centralizados.json`
- `config/telas/demo/h0035_um_centralizado.json`
- `config/telas/demo/h0035_uma_coluna.json`
- `config/telas/demo/h0035_uma_linha.json`
- `config/telas/demo/h0035_v_margens_min.json`
- `config/telas/demo/h0035_v_margens_min_max.json`
- `config/telas/demo/h0035_v_uniforme.json`
- `config/telas/demo/h0036_console_conjuntos.json`
- `config/telas/demo/h0036_console_hierarquia.json`
- `config/telas/demo/h0036_console_tabela.json`
- `config/telas/demo/h0037_console_alternavel_tres_niveis.json`
- `config/telas/demo/h0037_console_nao_verboso.json`
- `config/telas/demo/h0037_console_tabela_alternavel.json`
- `config/telas/demo/h0037_console_verboso_dois_niveis.json`
- `config/telas/demo/h0040_nav_console_grade_2x3.json`
- `config/telas/demo/h0040_nav_console_nao_focalizavel.json`
- `config/telas/demo/h0040_nav_console_unico_linear.json`
- `config/telas/demo/h0040_nav_degenere_um_item.json`
- `config/telas/demo/h0040_nav_degenere_uma_coluna.json`
- `config/telas/demo/h0040_nav_degenere_uma_linha.json`
- `config/telas/demo/h0040_nav_dois_consoles.json`
- `config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json`
- `config/telas/demo/h0040_nav_tres_consoles_em_grupo.json`
- `config/telas/demo/h0041_selecao_multipla_oito_itens.json`
- `config/telas/demo/h0044_fluxo_execucao_integrado.json`
- `config/telas/demo/h0045_dois_consoles_paginas_independentes.json`
- `config/telas/demo/h0045_fluxo_execucao_paginado.json`
- `config/telas/demo/h0045_paginacao_conjunto_vazio.json`
- `config/telas/demo/h0045_paginacao_console_unico.json`
- `config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json`
- `config/telas/demo/h0045_paginacao_politicas_quebra.json`
- `config/telas/demo/h0045_validacao_continuacao.json`
- `config/telas/demo/h0045_validacao_fluxo_continuo.json`
- `config/telas/demo/h0045_validacao_manter_junto.json`
- `config/telas/demo/h0045_validacao_nova_pagina.json`
- `config/telas/demo/h0045_validacao_vazio.json`
- `config/telas/demo/resultado_execucao.json`
- `config/telas/demo/stub_b.json`

Cada uma das 72 telas estruturais deve ser migrada com
`descricao.capitalizacao: preservar`, para manter literalmente as descrições
existentes. Registrar como evidência do impacto do baseline anterior:

```yaml
impacto_do_baseline_anterior:
  telas_estruturais_auditadas: 72
  descricoes_alteradas_por_inicio_de_frase: 17
```

Não é necessário repetir nominalmente os 17 caminhos neste handoff; a
evidência nominal permanece no relatório P05 citado acima. A lista das 72
telas não pode ser alterada.

### Critério executivo de classificação

A classificação é determinada pela estrutura da raiz e pelo loader do
contrato, não pela presença textual de um campo ou pelo nome do arquivo. A
busca abaixo pode ser usada somente como auxílio de inspeção; sua ocorrência
não classifica o documento:

```zsh
rg -l '"cabecalho"' config/telas --glob '*.json'
```

```yaml
tela_estrutural:
  estrutura:
    - schema
    - id
    - cabecalho
    - corpo
    - barra_de_menus
  loader: carregar_tela
  migra_no_h0049: true

conteudo_externo:
  estrutura:
    - dados
    - formato
    - tipo
  loader: carregar_conteudo_externo
  migra_no_h0049: false
```

### JSONs de conteúdo externo preservados

Os oito arquivos abaixo possuem raiz `dados`, `formato` e `tipo`; são
conteúdos externos de console que fornecem dados para consoles, não são raízes
estruturais de tela, não são carregados por `carregar_tela` e não recebem
`cabecalho.apresentacao`. Eles não são autorizados para alteração, devem
manter os hashes registrados e continuam sendo validados pelo loader próprio
de conteúdo externo.

```yaml
jsons_de_conteudo_externo_preservados:
  - caminho: config/telas/demo/h0035_console_com_conteudo.json
    sha256: 1ec153da3e18830562c8c695f83b45a79143e9a9600f54864fde295071b8e71e
  - caminho: config/telas/demo/h0035_console_sem_conteudo.json
    sha256: fa684bfabd2d76a2eccc5b1abd1f408378542db070012e9ce88787c22dba0337
  - caminho: config/telas/demo/h0036_conjuntos_conteudo.json
    sha256: 1a3a9a1e9c1addd316feb1bebca6c79148efc10de02b7a9f4207b6924f731dcc
  - caminho: config/telas/demo/h0036_hierarquia_conteudo.json
    sha256: e25774c1f92e55b8d8ffa39fe03c1534d1ec7d36989e1146ea5fc4dbd3cca3ac
  - caminho: config/telas/demo/h0036_tabela_conteudo.json
    sha256: eacd1e366526dae88fbc64d52f28f39186d9ec2147cf82d5dcb3c059c3df4dd5
  - caminho: config/telas/demo/h0037_dois_niveis_conteudo.json
    sha256: 0463452913a87c715163778dab539d5b6a16e65e81cb7e6589b3b3b76672a317
  - caminho: config/telas/demo/h0037_tabela_conteudo.json
    sha256: 60042955a4651c19ad7081e3b8e88a693bc820db37d444e8fc7a210f04fa6fcc
  - caminho: config/telas/demo/h0037_tres_niveis_conteudo.json
    sha256: 887fde5901ec198831e6aa505ad7e3af6b815731d1ca0dbbb3ab35f1c9d719b1
```

### Entradas e saídas da implementação futura

```yaml
entradas_reais:
  telas_estruturais: 72
  conteudos_externos_preservados: 8

alteracoes:
  telas_estruturais_migradas: 72
  conteudos_externos_alterados: 0
```

### Loader

Alterar somente `tela/carregamento/tela_json.py`, no símbolo
`carregar_tela`. Antes da validação do corpo, validar o `cabecalho` completo:
exigir os três níveis de objetos, rejeitar campos desconhecidos nos quatro
objetos fechados, validar os tipos, enumerações e limites da tabela acima e
emitir `TelaCampoObrigatorioAusente` ou `TelaEstruturaInvalida` com caminho
preciso do campo. Não aplicar default, não consultar
`config/elementos/cabecalho.json`, não ler estilo alternativo e não alterar a
superfície pública do loader. A saída continua contendo o dicionário validado
integralmente em `cabecalho` e em `_raw`.

Carregar e validar todos os 72 JSONs estruturais nominalmente enumerados neste
handoff usando `carregar_tela`. Não exigir nem permitir que `carregar_tela`
aceite qualquer um dos oito conteúdos externos.

Para `cabecalho.apresentacao.descricao.capitalizacao`, a enumeração do loader
é exatamente:

```yaml
valores:
  - maiusculas
  - inicio_de_frase
  - preservar
```

O campo continua obrigatório; sua ausência continua inválida; `preservar` não
é default nem fallback; valores desconhecidos continuam inválidos. O loader
não aceita `preservar` automaticamente para
`cabecalho.apresentacao.titulo.capitalizacao`, cujo domínio permanece
`maiusculas` ou `inicio_de_frase`.

O relatório de implementação deverá registrar nominalmente:

```yaml
jsons_estruturais_migrados: 72
jsons_de_conteudo_preservados:
  - config/telas/demo/h0035_console_com_conteudo.json
  - config/telas/demo/h0035_console_sem_conteudo.json
  - config/telas/demo/h0036_conjuntos_conteudo.json
  - config/telas/demo/h0036_hierarquia_conteudo.json
  - config/telas/demo/h0036_tabela_conteudo.json
  - config/telas/demo/h0037_dois_niveis_conteudo.json
  - config/telas/demo/h0037_tabela_conteudo.json
  - config/telas/demo/h0037_tres_niveis_conteudo.json
hashes_de_preservacao_verificados: true
```

### Verificação operacional dos conteúdos externos

Independentemente do carregamento estrutural, a implementação deverá:

1. confirmar os hashes SHA-256 dos oito documentos;
2. carregar os oito documentos com `carregar_conteudo_externo`;
3. confirmar que todos permanecem válidos;
4. confirmar que nenhum recebeu `cabecalho.apresentacao`;
5. confirmar que não aparecem no diff da implementação.

Essa verificação não altera os arquivos. Pode ser executada por comando Python
no procedimento de validação; não é necessário criar fixture ou novo teste
persistente.

Comando obrigatório de validação dos hashes:

```zsh
sha256sum -c <<'EOF'
1ec153da3e18830562c8c695f83b45a79143e9a9600f54864fde295071b8e71e  config/telas/demo/h0035_console_com_conteudo.json
fa684bfabd2d76a2eccc5b1abd1f408378542db070012e9ce88787c22dba0337  config/telas/demo/h0035_console_sem_conteudo.json
1a3a9a1e9c1addd316feb1bebca6c79148efc10de02b7a9f4207b6924f731dcc  config/telas/demo/h0036_conjuntos_conteudo.json
e25774c1f92e55b8d8ffa39fe03c1534d1ec7d36989e1146ea5fc4dbd3cca3ac  config/telas/demo/h0036_hierarquia_conteudo.json
eacd1e366526dae88fbc64d52f28f39186d9ec2147cf82d5dcb3c059c3df4dd5  config/telas/demo/h0036_tabela_conteudo.json
0463452913a87c715163778dab539d5b6a16e65e81cb7e6589b3b3b76672a317  config/telas/demo/h0037_dois_niveis_conteudo.json
60042955a4651c19ad7081e3b8e88a693bc820db37d444e8fc7a210f04fa6fcc  config/telas/demo/h0037_tabela_conteudo.json
887fde5901ec198831e6aa505ad7e3af6b815731d1ca0dbbb3ab35f1c9d719b1  config/telas/demo/h0037_tres_niveis_conteudo.json
EOF
```

Validação focal do loader de conteúdo externo, usando sua assinatura real
`carregar_conteudo_externo(caminho_base, id_conteudo, raiz_telas=None)`:

```zsh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path

from tela.carregamento.conteudo_externo import carregar_conteudo_externo

caminhos = [
    Path("config/telas/demo/h0035_console_com_conteudo.json"),
    Path("config/telas/demo/h0035_console_sem_conteudo.json"),
    Path("config/telas/demo/h0036_conjuntos_conteudo.json"),
    Path("config/telas/demo/h0036_hierarquia_conteudo.json"),
    Path("config/telas/demo/h0036_tabela_conteudo.json"),
    Path("config/telas/demo/h0037_dois_niveis_conteudo.json"),
    Path("config/telas/demo/h0037_tabela_conteudo.json"),
    Path("config/telas/demo/h0037_tres_niveis_conteudo.json"),
]

for caminho in caminhos:
    nome_base = caminho.stem
    raiz_esperada = str(caminho.parent)
    documento = carregar_conteudo_externo(None, nome_base, raiz_esperada)
    if set(documento) != {"dados", "formato", "tipo"}:
        raise SystemExit(f"FALHA: raiz inesperada em {caminho}")
    if "cabecalho" in documento:
        raise SystemExit(f"FALHA: cabecalho em {caminho}")
PY
```

### Modelo

Alterar somente `tela/modelo.py`, nos símbolos `ModeloTela` e
`construir_modelo`. A representação vigente é o `dict` validado; portanto,
ela deve continuar sendo usada, sem criar dataclass, tipo público ou
abstração nova. Transportar integralmente `titulo`, `descricao` e
`apresentacao`, preservar os valores declarados sem transformação e manter o
comportamento inerte/imutável vigente. O modelo não abre arquivo, não resolve
estilo global e não armazena estado vivo na configuração.

### Renderer e geometria

Alterar somente:

- `tela/renderizacao/tela.py`, em `_geometria_por_console` e
  `renderizar_tela`;
- `tela/renderizacao/geometria_caixa.py`, em `_linha_topo`,
  `_linha_conteudo` e `_caixa`.

Fazer ambos os caminhos que calculam a caixa de cabeçalho consumirem os oito
parâmetros locais, de modo que a contagem de linhas para geometria e a saída
física não divirjam. Remover o `upper()` incondicional do título e os espaços,
recuos e alinhamentos locais fixos substituídos pelos parâmetros. Aplicar as
transformações contratuais, respeitar largura útil e usar exclusivamente os
caracteres de borda recebidos do estilo global resolvido. O renderer não pode
abrir JSON, ler configuração ou introduzir fallback.

### Capitalização da descrição no renderer

O renderer deve consumir os três valores declarados para a descrição:

```yaml
preservar:
  resultado: texto_cortado
inicio_de_frase:
  comportamento: algoritmo_normativo_ja_aprovado
maiusculas:
  resultado: texto_cortado.upper()
```

Para `preservar`, `texto_capitalizado = texto_cortado`. Para
`inicio_de_frase`, manter o algoritmo baseado no primeiro `isalpha()` e no
resultado integral de `upper()`. Para `maiusculas`, manter a conversão
integral por `str.upper()`. A ordem permanece corte por `max_caracteres`,
capitalização, alinhamento e recuo, e limitação geométrica. Não reintroduzir
fallback.

## Fontes e fronteiras

```yaml
json_da_tela:
  contem:
    - textos concretos
    - parametros_declarativos_locais_do_cabecalho
config_estilo_json:
  contem:
    - caracteres_de_borda
    - cores
    - aparencia_global_compartilhada
  nao_contem:
    - parametros_locais_do_cabecalho
runtime:
  contem: estado_vivo_da_execucao
  nao_e_persistido_no_json_da_tela: true
```

Depois da migração atômica dos 72 JSONs estruturais, de nenhuma referência
residual e da aprovação dos testes, remover
`config/elementos/cabecalho.json`. Não mover seu conteúdo para
`config/estilo.json`.

## Testes e demonstração autorizados

Alterar os testes existentes, e somente eles:

- `tela/teste_loader.py`: atualizar helpers e entradas de testes para o schema
  válido quando a finalidade não for testar o cabeçalho; acrescentar testes
  `test_h0049_*` para schema completo, ausências, campos desconhecidos nos
  quatro objetos, tipos, enumerações, domínio de `max_caracteres` com `1` e
  `200` aceitos e `0`, valores negativos, `201` e valores não inteiros
  rejeitados, zero permitido para recuos, erro rastreável e ausência de
  fallback global. Incluir teste que carregue cada um dos 72 JSONs estruturais
  nominais com `carregar_tela` e teste separado dos oito conteúdos externos
  com `carregar_conteudo_externo`, sem permitir o uso do loader estrutural para
  esses oito arquivos.
- `tela/teste_modelo.py`: acrescentar testes `test_h0049_*` que comprovem
  transporte literal dos oito campos e dos textos, ausência de transformação,
  inércia/imutabilidade e distinção entre duas apresentações locais.
- `tela/testes_renderizador/fundamentos.py`: atualizar modelos fabricados
  para o schema completo e acrescentar testes `test_h0049_*` para as três
  posições, recuos, as capitalizações do título e as três capitalizações da
  descrição, o único formato permitido, os três
  alinhamentos, truncamento contratual, largura reduzida, impossibilidade
  geométrica, borda global, remoção do `upper()` incondicional, a semântica
  normativa de `inicio_de_frase` e ausência de decisões locais fixas.

Os testes positivos da descrição devem distinguir `preservar`,
`inicio_de_frase` e `maiusculas`. A cobertura mínima de `preservar` deve ser
equivalente a:

```text
"desc fab" → "desc fab"
"Desc fab" → "Desc fab"
"  execução da API REST" → "  execução da API REST"
"123 - execução" → "123 - execução"
"ßeta" → "ßeta"
"" → ""
```

Para `inicio_de_frase`, manter cobertura equivalente a `"desc fab"` →
`"Desc fab"`, `"  execução"` → `"  Execução"`, `"123 - execução"` →
`"123 - Execução"`, `"ßeta"` → `"SSeta"` e `""` → `""`. Para
`maiusculas`, manter cobertura de conversão integral por `str.upper()`.

Os testes negativos devem rejeitar valor desconhecido, `null`, inteiro, lista,
objeto e ausência de `capitalizacao`; ausência não pode ser tratada como
`preservar`.

É proibida a criação de fixture persistente. Documentos de entrada, modelos e
variações devem ser fabricados em memória dentro dos três arquivos de testes
já autorizados acima. Não é autorizado arquivo adicional. Se os testes não
puderem ser expressos nesses arquivos existentes, a implementação deve parar
com `IMPLEMENTATION_BLOCKED`, sem criar fixture. Temporários ficam fora do
repositório e são removidos ao fim.

A demonstração automatizada deve renderizar dois modelos/telas fabricados em
memória, com os mesmos textos e estilo global, mas apresentações locais
distintas, e provar linhas físicas diferentes e coerentes sem ler configuração
global de cabeçalho. Deve também comparar uma tela real migrada com o quadro
baseline pré-migração usando `recuo_lateral: 0` e `recuo: 1`. Os valores `3` e
`10` não devem ser migrados, reinterpretados nem compensados; pertencem à
configuração global não consumida e são obsoletos.

## Manifesto adicional de fixtures preexistentes (P04)

A descoberta exaustiva do patch P03 encontrou **58 ocorrências antigas de
cabeçalho** (`cabecalho` com `titulo`+`descricao` e sem `apresentacao`,
incluindo `cabecalho=` como argumento nomeado de `ModeloTela(...)`)
distribuídas por **13 arquivos de teste**. Dois desses arquivos já pertencem
ao manifesto original de três arquivos autorizados a fabricar cenários novos
do H-0049 (`tela/teste_modelo.py`,
`tela/testes_renderizador/fundamentos.py`) e não constituem bloqueio. Os
onze arquivos restantes precisam ser acrescentados nominalmente ao manifesto
de testes autorizados, exclusivamente para adequar fixtures preexistentes:

```yaml
testes_autorizados:
  originais: 3
  acrescentados_no_p04: 11
  total: 14

arquivos_originais:
  - tela/teste_loader.py
  - tela/teste_modelo.py
  - tela/testes_renderizador/fundamentos.py

arquivos_acrescentados_no_p04:
  - tela/teste_resultado_execucao.py
  - tela/teste_navegacao.py
  - tela/testes_renderizador/integracao.py
  - tela/testes_renderizador/composicao_corpo.py
  - tela/testes_renderizador/comum.py
  - tela/testes_renderizador/lancador.py
  - tela/testes_renderizador/matriz_participantes.py
  - tela/testes_renderizador/selecao.py
  - demo/teste_demo_navegacao.py
  - demo/teste_demo_paginacao.py
  - demo/teste_diagnostico.py
```

Somente 13 dos 14 arquivos autorizados contêm ocorrências antigas
identificadas pelo P03 (os 11 acima mais os dois já originais). `tela/
teste_loader.py` permanece autorizado exclusivamente para os testes novos
`test_h0049_*` do schema; a descoberta não encontrou nele nenhuma ocorrência
antiga, portanto ele não recebe nenhuma adequação por este manifesto
adicional.

### Política corrigida de fixtures

Substitui a redação anterior de "alterar os testes existentes, e somente
eles" pelos três arquivos originais. A redação vigente é:

> Novos cenários específicos do H-0049 devem ser criados somente em
> `tela/teste_loader.py`, `tela/teste_modelo.py` e
> `tela/testes_renderizador/fundamentos.py`. Fixtures em memória
> preexistentes nos demais onze arquivos nominalmente autorizados podem ser
> adequadas exclusivamente para incluir o bloco obrigatório
> `cabecalho.apresentacao`. Essa adequação não permite criar cenário,
> fixture, helper compartilhado, arquivo, comportamento ou expectativa nova.

Mantêm-se integralmente:

- proibição absoluta de fixture JSON persistente;
- proibição de novo arquivo de teste;
- proibição de novo cenário fora dos três arquivos originais;
- proibição de ampliar a função dos testes existentes.

### Bloco obrigatório das fixtures válidas

Toda fixture preexistente que represente uma tela ou `ModeloTela` válido deve
receber dentro de `cabecalho`:

```json
{
  "apresentacao": {
    "titulo": {
      "posicao": "esquerda",
      "recuo_lateral": 0,
      "capitalizacao": "maiusculas",
      "formato_na_borda": "com_espacos_laterais"
    },
    "descricao": {
      "max_caracteres": 200,
      "alinhamento": "esquerda",
      "recuo": 1,
      "capitalizacao": "preservar"
    }
  }
}
```

Regras: preservar `titulo`; preservar `descricao`; preservar todos os outros
campos; não usar os valores obsoletos `3`/`10`; não criar default; não usar
fallback; não ler configuração externa; não criar helper global novo. Um
helper local preexistente pode ser atualizado uma única vez quando ele for a
origem de várias fixtures do mesmo arquivo — por exemplo `_tela_base` em
`tela/teste_resultado_execucao.py`, `_modelo_matriz_render_h0028` em
`tela/testes_renderizador/matriz_participantes.py`, `_modelo_horizontal` e
`_modelo_hierarquico` em `tela/testes_renderizador/composicao_corpo.py`, ou
`_h0034_modelo_lancador` em `tela/testes_renderizador/lancador.py`. Nos
arquivos sem fábrica compartilhada (por exemplo `tela/teste_navegacao.py`,
onde cada teste fabrica seu próprio `ModeloTela` inline), a adequação deve
tocar cada ocorrência individualmente, sem criar um helper novo para
consolidá-las.

Nas 58 ocorrências antigas distribuídas em 13 arquivos, toda adequação de
fixture preexistente deve declarar `descricao.capitalizacao: preservar`.
Isso inclui fixtures válidas, objetos `ModeloTela`, documentos inválidos por
outra regra, helpers locais, os quatro arquivos com falha observada e os sete
arquivos anteriormente mascarados pelo fallback. A entrada e a expectativa de
`tela/testes_renderizador/fundamentos.py::teste_modelo_fabricado` permanecem
inalteradas:

```yaml
evidencia_de_preservacao:
  arquivo: tela/testes_renderizador/fundamentos.py
  teste: teste_modelo_fabricado
  entrada: "desc fab"
  resultado_anterior: "desc fab"
  resultado_com_inicio_de_frase: "Desc fab"
  resultado_com_preservar: "desc fab"
```

Não autorizar alteração de fixture, expectativa, snapshot, quadro, string
esperada ou asserção para acomodar a mudança de baseline.

### Contagens e regras preservadas

```yaml
jsons:
  total: 80
  estruturais: 72
  conteudos_externos: 8

fixtures:
  ocorrencias_antigas: 58
  arquivos_com_ocorrencias: 13
  arquivos_autorizados: 14
  arquivos_adicionais: 11
  falhas_observadas: 4
  mascarados_pelo_fallback: 7

parametros:
  max_caracteres:
    minimo: 1
    maximo: 200
  titulo:
    capitalizacao: maiusculas
  descricao:
    alinhamento: esquerda
    recuo: 1

proibicoes:
  fixture_persistente: true
  alteracao_funcional_de_teste: true
  default: true
  fallback: true
  valores_obsoletos_3_10: true
```

Os oito conteúdos externos e seus hashes permanecem intocados.

### Fixtures inválidas por outro motivo

Alguns testes fabricam documentos deliberadamente inválidos para verificar
outra regra (distribuição matricial inválida, percentual cuja soma não é
100, fração com peso zero, IDs duplicados, outra estrutura inválida não
relacionada ao cabeçalho). Essas fixtures devem receber
`cabecalho.apresentacao` completo e válido para que a validação alcance o
defeito que o teste pretende verificar. A implementação deve preservar a
classe de exceção esperada, a mensagem ou caminho esperado quando testado, a
ordem material que permite alcançar a validação-alvo e todas as asserções do
teste. Não é autorizado alterar a expectativa para aceitar
`TelaCampoObrigatorioAusente`. Os pontos identificados que exigem atenção
nesta regra são:

- `demo/teste_diagnostico.py::teste_telas_h0035_diagnostico` — a fixture
  `tela_inv` (distribuição matricial `ordem: diagonal`) deve continuar
  alcançando `TelaEstruturaInvalida` pela distribuição matricial, não por
  `cabecalho`;
- `tela/testes_renderizador/composicao_corpo.py::test_rejeicoes_loader_preservadas`
  (helper `_tela_horizontal`) — os dois casos (percentual soma ≠ 100 e
  fração com peso zero) devem continuar alcançando `TelaEstruturaInvalida`
  pelo motivo de distribuição horizontal; como o teste não faz asserção de
  texto sobre a mensagem, é responsabilidade da implementação garantir que a
  fixture receba uma `apresentacao` válida, para que a falha não seja
  mascarada por um erro de cabeçalho que coincide em classe de exceção;
- `tela/testes_renderizador/integracao.py::test_h0045_p04_ids_duplicados_impedem_qualquer_renderizacao`
  — deve continuar alcançando `TelaEstruturaInvalida` com
  `"id de console duplicado" in str(exc)`, não por `cabecalho`.

### Fixtures negativas específicas do H-0049

Fixtures criadas especificamente para provar rejeição de ausência de
`cabecalho.apresentacao`, de um subobjeto de apresentação, de um dos oito
parâmetros, de tipo inválido, de enumeração inválida ou de limite inválido
podem e devem permanecer incompletas na dimensão explicitamente testada.
Esses casos devem existir somente nos três arquivos originais autorizados
para novos cenários. A descoberta do P04 não encontrou nenhum caso desse
tipo nos onze arquivos acrescentados — nenhum deles testa intencionalmente a
ausência de `cabecalho.apresentacao` ou de algum de seus campos; a ausência
observada neles é incidental, anterior ao contrato do H-0049.

### Escopo por arquivo

- `tela/teste_resultado_execucao.py`: autorizar somente a atualização de
  `_tela_base` (linha 69) e de qualquer outra fábrica preexistente
  equivalente. Preservar perfil `resultado_execucao`, envelopes, estados,
  ações, resultados, nomes dos testes, asserções e quantidade de testes.
- `tela/testes_renderizador/integracao.py`: autorizar o documento inválido de
  IDs duplicados, os oito objetos `ModeloTela` diretos identificados, e
  helpers locais que originem essas fixturas. Preservar todas as
  expectativas de integração e renderização.
- `demo/teste_diagnostico.py`: autorizar somente a fixture do teste
  `teste_telas_h0035_diagnostico` e outras ocorrências nominalmente
  comprovadas pelo P03/P04. O teste deve voltar a alcançar
  `TelaEstruturaInvalida` pela distribuição matricial inválida. Não alterar
  a exceção esperada.
- `tela/testes_renderizador/composicao_corpo.py`: autorizar `_tela_horizontal`,
  os nove objetos `ModeloTela` diretos identificados (incluindo os helpers
  compartilhados `_modelo_horizontal` e `_modelo_hierarquico`), e helpers
  locais que originem essas estruturas. Os casos de percentual e fração
  inválidos devem continuar produzindo `TelaEstruturaInvalida`, não erro de
  cabeçalho.
- Demais sete arquivos mascarados pelo fallback do renderer
  (`tela/teste_navegacao.py`, `tela/testes_renderizador/comum.py`,
  `tela/testes_renderizador/lancador.py`,
  `tela/testes_renderizador/matriz_participantes.py`,
  `tela/testes_renderizador/selecao.py`, `demo/teste_demo_navegacao.py`,
  `demo/teste_demo_paginacao.py`): autorizar somente a inclusão de
  `apresentacao` nas fábricas preexistentes de `ModeloTela`. Não alterar
  navegação, paginação, seleção, lançadores, matrizes, participantes,
  composição, comandos ou resultados observáveis.

### Proibição de alteração funcional

Nos onze arquivos acrescentados, proibir mudanças em: nomes de testes;
decorators; marcas; parâmetros de testes; asserções; mensagens esperadas;
classes de exceção esperadas; snapshots ou quadros; strings de saída;
quantidade de testes; `skip`; `xfail`; filtros de coleta; imports, salvo
formatação automaticamente necessária e sem mudança semântica; comportamento
produtivo. A única mudança material permitida é o bloco
`cabecalho.apresentacao` nas estruturas preexistentes.

### Preservação visual

O baseline migratório `0/1`, com `descricao.capitalizacao: preservar`, deve
produzir o mesmo quadro anteriormente esperado. Se
qualquer teste exigir alteração de snapshot, quadro ou string esperada após
a adequação, a implementação deve parar com:

```yaml
status: IMPLEMENTATION_BLOCKED
motivo: baseline_0_1_nao_preservou_resultado_observavel
```

Não recalcular ou atualizar expectativa para fazer o teste passar.

### Critérios de bloqueio do P06

O bloqueio não pode pressupor `inicio_de_frase` como baseline. Manter
`status: BLOCKED_DOCUMENTATION` se ocorrer qualquer uma das condições abaixo:

- `preservar` não conservar o resultado observável;
- qualquer expectativa precisar ser alterada;
- `inicio_de_frase` deixar de funcionar como opção explícita suportada e testada;
- `maiusculas` deixar de funcionar;
- o loader aceitar valor inválido;
- o título aceitar `preservar`;
- alguma das 72 telas usar baseline diferente sem decisão nominal;
- alguma fixture antiga usar `inicio_de_frase` como baseline de preservação;
- houver necessidade de arquivo fora do manifesto;
- surgir nova decisão normativa.

### Estado parcial da implementação

A próxima execução deve:

1. registrar o estado atual do worktree;
2. identificar as alterações parciais já produzidas pelo H-0049;
3. preservar alterações parciais válidas;
4. não executar `git restore`, `reset`, limpeza ou reaplicação
   indiscriminada;
5. alterar somente os onze novos arquivos no escopo adicional (além do
   escopo já autorizado nos três arquivos originais e no restante do
   manifesto de 72 JSONs);
6. concluir as validações abaixo;
7. remover `config/elementos/cabecalho.json` somente após aprovação da
   suíte integral;
8. criar `IMP-0049` somente depois da conclusão integral.

### Validação focal futura

Exigir:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_resultado_execucao.py \
  tela/teste_navegacao.py \
  tela/testes_renderizador/integracao.py \
  tela/testes_renderizador/composicao_corpo.py \
  tela/testes_renderizador/comum.py \
  tela/testes_renderizador/lancador.py \
  tela/testes_renderizador/matriz_participantes.py \
  tela/testes_renderizador/selecao.py \
  demo/teste_demo_navegacao.py \
  demo/teste_demo_paginacao.py \
  demo/teste_diagnostico.py
```

Resultado obrigatório: todos os testes passam; nenhum erro de coleta;
nenhum `cabecalho.apresentacao` ausente fora de negativas intencionais;
nenhuma mudança na quantidade coletada desses arquivos.

### Validação das negativas originais

Executar também os testes focais do H-0049 em `tela/teste_loader.py`,
`tela/teste_modelo.py` e `tela/testes_renderizador/fundamentos.py`. As
negativas intencionais do schema devem continuar passando.

### Inventário AST futuro

Reexecutar o inventário AST estendido usado no P03. Cada ocorrência
remanescente de cabeçalho sem `apresentacao` deve ser classificada
nominalmente. Permitir somente ocorrências cujo teste tenha finalidade
explícita de rejeitar `cabecalho.apresentacao` ou algum de seus campos. O
relatório `IMP-0049` deverá registrar:

```yaml
inventario_fixture:
  ocorrencias_incompativeis_antes: 58
  arquivos_com_ocorrencias_antes: 13
  ocorrencias_incompativeis_restantes: 0
  negativas_intencionais_h0049:
    quantidade:
    testes: []
```

`ocorrencias_incompativeis_restantes: 0` exclui as negativas intencionais
registradas separadamente.

A definição de fixture compatível para o inventário futuro exige, nos blocos
migratórios das fixtures antigas:

```yaml
descricao:
  capitalizacao: preservar
```

Negativas intencionais específicas do schema permanecem registradas
separadamente e não autorizam `inicio_de_frase` como baseline de preservação.

### Conferência do diff futuro

Exigir diff focal dos onze arquivos:

```zsh
git diff -- \
  tela/teste_resultado_execucao.py \
  tela/teste_navegacao.py \
  tela/testes_renderizador/integracao.py \
  tela/testes_renderizador/composicao_corpo.py \
  tela/testes_renderizador/comum.py \
  tela/testes_renderizador/lancador.py \
  tela/testes_renderizador/matriz_participantes.py \
  tela/testes_renderizador/selecao.py \
  demo/teste_demo_navegacao.py \
  demo/teste_demo_paginacao.py \
  demo/teste_diagnostico.py
```

O diff deve conter somente adequações do cabeçalho nas fixtures ou helpers
locais preexistentes.

### Relatório futuro de implementação

`IMP-0049` deve registrar adicionalmente:

```yaml
baseline_migratorio_final:
  titulo:
    capitalizacao: maiusculas
  descricao:
    capitalizacao: preservar

preservacao_observavel:
  fixture_desc_fab:
    entrada: "desc fab"
    resultado: "desc fab"
    expectativa_alterada: false
  telas_auditadas: 72
  telas_que_mudariam_com_inicio_de_frase: 17

capitalizacoes_da_descricao_testadas:
  preservar: true
  inicio_de_frase: true
  maiusculas: true
```

Manter os demais campos já exigidos pelo P04 e P05.

```yaml
fixtures_preexistentes_adequadas:
  arquivos:
    - tela/teste_resultado_execucao.py
    - tela/teste_navegacao.py
    - tela/testes_renderizador/integracao.py
    - tela/testes_renderizador/composicao_corpo.py
    - tela/testes_renderizador/comum.py
    - tela/testes_renderizador/lancador.py
    - tela/testes_renderizador/matriz_participantes.py
    - tela/testes_renderizador/selecao.py
    - demo/teste_demo_navegacao.py
    - demo/teste_demo_paginacao.py
    - demo/teste_diagnostico.py

  arquivos_adicionados_ao_manifesto: 11
  novas_fixtures_criadas: 0
  fixtures_persistentes_criadas: 0
  novos_testes_criados: 0
  testes_removidos: 0
  testes_renomeados: 0
  testes_ignorados: 0
  assercoes_funcionais_alteradas: 0
  expectativas_alteradas: 0
```

Registrar ainda: os quatro arquivos que já falhavam
(`tela/teste_resultado_execucao.py`, `tela/testes_renderizador/
integracao.py`, `tela/testes_renderizador/composicao_corpo.py`,
`demo/teste_diagnostico.py`); os sete arquivos que estavam mascarados pelo
fallback (`tela/teste_navegacao.py`, `tela/testes_renderizador/comum.py`,
`tela/testes_renderizador/lancador.py`, `tela/testes_renderizador/
matriz_participantes.py`, `tela/testes_renderizador/selecao.py`,
`demo/teste_demo_navegacao.py`, `demo/teste_demo_paginacao.py`); resultado
focal; resultado integral; inventário AST final; preservação do
comportamento.

### Critérios de aceite adicionais

Exigir cumulativamente, além dos critérios já vigentes na seção "Saídas,
preservação e aceite":

1. onze arquivos acrescentados ao manifesto;
2. treze arquivos com fixtures antigas tratados, considerando os dois já
   autorizados;
3. 58 ocorrências antigas reconciliadas;
4. nenhuma fixture incompatível remanescente;
5. negativas intencionais registradas separadamente;
6. nenhuma fixture persistente criada;
7. nenhum teste criado, removido, renomeado ou ignorado;
8. nenhuma asserção ou expectativa funcional alterada;
9. quatro arquivos que falhavam agora aprovados;
10. sete arquivos mascarados aprovados após remoção do fallback;
11. suíte focal aprovada;
12. suíte integral aprovada;
13. baseline visual preservado.

## Validação obrigatória

Executar, após implementar:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py -k h0049
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_modelo.py -k h0049
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/testes_renderizador/fundamentos.py -k h0049
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
rg -n \
  'config/elementos/cabecalho\.json|elementos/cabecalho' \
  tela config demo docs \
  --glob '*.py' \
  --glob '*.json' \
  --glob '*.md'
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --maxfail=0
```

Resultado obrigatório da suíte integral:

```yaml
resultado_obrigatorio:
  falhas: 0
  erros: 0
  reducao_de_testes: false
  fixture_antiga_incompativel: false
  fallback_de_apresentacao: false
```

`--maxfail=0` permite enumerar todas as falhas; `-q` reduz somente a
verbosidade. Nenhuma falha pode ser ocultada por filtro, `skip`, `xfail` ou
redução de coleta, e a quantidade de testes deve ser comparada com a coleta
válida do ciclo. A configuração global obsoleta só pode ser removida depois
da aprovação desta suíte integral. O relatório `IMP-0049` só pode ser criado
após a conclusão integral.

A busca deve não retornar ocorrência operacional; referências históricas já
existentes em relatórios não são consumidoras e não devem ser alteradas. Os
testes automatizados substituem validação manual se cobrirem integralmente os
efeitos físicos. Se sobrar comportamento dependente de terminal real, executar
uma única verificação manual agrupada, com duas configurações distinguíveis e
resultado humano observável.

## Saídas, preservação e aceite

Entradas reais são os 72 JSONs estruturais nominais e os oito conteúdos
externos preservados. As saídas são o modelo com
`apresentacao` transportada, linhas físicas do cabeçalho, resultados de testes
e `docs/relatorios/IMP-0049-materializacao-local-dos-parametros-do-cabecalho.md`.
Esse relatório, com máximo normal de 900 palavras, deve registrar somente
arquivos alterados/criados/removidos, quantidade e lista dos JSONs, fluxo de
dados, hardcodings removidos, testes, demonstração, preservação visual,
desvios autorizados e bloqueios.

Aceitar cumulativamente apenas se:

1. exatamente 72 telas estruturais forem migradas;
2. exatamente 72 telas forem aceitas por `carregar_tela`;
3. exatamente oito conteúdos externos forem preservados;
4. exatamente oito conteúdos externos forem aceitos por
   `carregar_conteudo_externo`;
5. os hashes dos oito conteúdos permanecerem inalterados;
6. nenhum conteúdo externo estiver presente no diff;
7. nenhum `cabecalho.apresentacao` for inserido em documentos de conteúdo;
8. os demais critérios técnicos já existentes forem preservados.

Os demais critérios técnicos incluem schema obrigatório e fechado, transporte
integral pelo modelo, consumo dos oito campos pelo renderer, ausência de
hardcoding, fallback ou consumidor residual, preservação da borda global,
remoção do arquivo global obsoleto, demonstração do baseline e das variações,
testes focais e suíte integral, relatório factual e ausência de alterações fora
do manifesto de implementação.

## Arquivos preservados e bloqueio

Preservar ADRs, contratos, nomenclatura, backlog, histórico,
`config/estilo.json` (somente leitura), composição, corpo, consoles,
dashboards, lançadores, barra de menus, navegação, seleção, paginação,
bindings, ações, estado vivo e APIs públicas não relacionadas.

Se um arquivo fora deste manifesto for estritamente necessário, ou se algum
JSON não puder ser migrado, campo contratual for insuficiente, a geometria
exigir nova política, o baseline demandar comportamento contrário ao contrato
ou a suíte falhar por causa material insolúvel no escopo, parar antes de
alterar e informar:

```yaml
status: IMPLEMENTATION_BLOCKED
arquivo:
motivo:
escopo_da_alteracao:
consequencia_de_nao_alterar:
```

Acrescentar `IMPLEMENTATION_BLOCKED` quando algum dos 72 caminhos não for
aceito pelo loader estrutural; algum dos oito conteúdos externos mudar de
hash; algum conteúdo externo aparecer no diff; algum documento não
corresponder à classificação da auditoria; for encontrado outro JSON sob
`config/telas` não contemplado no total de 80; ou o total deixar de fechar em
`72 + 8 = 80`.

## Verificação interna deste handoff

- Schema, tipos, enumerações, limites e semânticas estão integralmente
  determinados pelo contrato copiado acima.
- A lista nominal de 72 JSONs estruturais e o manifesto de preservação de oito
  conteúdos externos são completos para o fluxo loader → modelo → renderer →
  geometria → testes → relatório.
- A remoção do arquivo global tem pré-condições verificáveis.
- Testes, demonstração, preservação visual e relatório são executáveis sem
  decisão documental nova.
- Não há autorização genérica para diretórios, nem contradição entre escopo,
  validação e critérios de aceite.

## Resposta terminal futura da implementação

```yaml
status: IMPLEMENTATION_COMPLETED
relatorio: docs/relatorios/IMP-0049-materializacao-local-dos-parametros-do-cabecalho.md
handoff: H-0049
jsons_estruturais_migrados: 72
jsons_de_conteudo_preservados: 8
hashes_de_preservacao_verificados: true
configuracao_obsoleta_removida: true
proxima_acao: QA_IMPLEMENTACAO
```

## Consolidação final

```yaml
estado_final: IMPLEMENTATION_APPROVED
handoff:
  id: H-0049
  estado: concluido
item:
  id: ITEM-0015
  estado: concluido
ADR:
  id: ADR-0008
  status: aceita_e_aplicada
implementacao:
  status_final: IMPLEMENTATION_APPROVED
  jsons_estruturais: 72
  conteudos_externos_preservados: 8
  hashes_verificados: 8
  fixtures_incompativeis_restantes: 0
  testes_focais_h0049: 34
  testes_onze_arquivos: 514
  suite_integral: 998_passed
  consumidores_residuais: 0
  configuracao_obsoleta_removida: true
validacao_manual:
  necessaria: false
  resultado: NAO_APLICAVEL
bloqueios: []
```
