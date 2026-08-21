# Preparação da validação manual — ITEM-0027

## Arquivos criados/alterados

- Criado `config/telas/demo/h0077_texto_amplo_justificado.json`.
- Criado `config/telas/demo/h0077_texto_amplo_justificado_conteudo.json`.
- Alterado `demo/demo.py` para registrar o conteúdo externo do cenário e o
  envelope runtime do popup longo.
- Criado este relatório.

## Corpo longo

O corpo usa um console único, sem tabela, associado pelo catálogo real de
conteúdo externo a um documento `conteudo.v1` com apresentação `hierarquia` e
um único nó textual longo. A tela declara `politica_exibicao.verboso: true`,
para que o consumidor real recomponha o parágrafo com a largura útil corrente
durante o resize.

O caminho do corpo usa `compor_texto(texto, largura_util)` em modo normal. Não
foi inventado campo JSON de justificação: a API declarativa existente não
oferece solicitação de `modo="justificado"` para o corpo.

## Popup longo

O acionamento estrutural `w` aponta para `popup_texto_amplo_h0077`. O popup é
aberto por `abrir_popup(...)`, com conteúdo textual runtime longo e declaração
real `alinhamento: "justificado"`. A recomposição usa o caminho real do
popup, que chama `compor_texto(..., modo="justificado",
justificar_ultima=False)`.

## Comando e teclas

```zsh
python demo/demo.py h0077_texto_amplo_justificado
```

Com a tela aberta:

- `w`: abre o popup de texto longo justificado;
- `Esc`: fecha o popup;
- `w` novamente: reabre o popup;
- `Esc` fora do popup: encerra a demonstração.

## Verificações automáticas

- `python -m json.tool config/telas/demo/h0077_texto_amplo_justificado.json >/dev/null`
- `python -m json.tool config/telas/demo/h0077_texto_amplo_justificado_conteudo.json >/dev/null`
- carregamento direto por `_carregar_modelo_por_id(...)`, confirmando o modelo
  `h0077_texto_amplo_justificado` e o conteúdo externo `hierarquia`;
- inicialização não interativa do comando com `s`, sem erro de arquivo/configuração;
- abertura, fechamento e reabertura não interativos com `w`, `Esc`, `w`, `Esc`, `s`;
- renderização de corpo e popup nas larguras 120, 80 e 50, com linhas físicas
  limitadas à largura solicitada e sem erro de geometria.

## Roteiro curto de resize

1. Iniciar na largura larga e observar várias linhas do corpo.
2. Reduzir para largura média; conferir recomposição, margem direita e
   preservação da sequência do texto.
3. Estreitar bastante; conferir mais linhas, nenhuma linha além da moldura e
   ausência de resíduos.
4. Voltar à largura larga e verificar que o corpo recupera a composição sem
   duplicações ou perda visível.
5. Pressionar `w`, repetir o ciclo de resize com o popup aberto, estreitar e
   ampliar novamente; observar justificação, moldura, altura, bordas e ausência
   de linhas antigas.
6. Pressionar `Esc`, reabrir com `w` e repetir em outra largura.

## Bloqueios

Não existe hoje configuração declarativa real para solicitar justificação no
corpo normal da TUI. O cenário deixa o corpo longo e responsivo no caminho
real de conteúdo externo e concentra a observação de justificação explícita
no popup, único consumidor declarativo existente para esse modo. Cumprir
justificação também no corpo exigiria alteração funcional fora do escopo desta
etapa; essa alteração não foi feita.

A validação visual manual permanece pendente para o usuário; este relatório não
declara aprovação.
