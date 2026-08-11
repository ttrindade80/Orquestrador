# H-0056 — pop-up básico: exibição textual e `[Esc] Voltar`

```yaml
handoff: H-0056
item: ITEM-0017
adr: ADR-0044
patch_adr: P01
patch_handoff: P02
adr_aplicada: true
qa_aplicacao: ADR_APPLICATION_APPROVED
qa_adr_patch: ADR_PATCH_APPROVED_WITH_NOTES
qa_aplicacao_patch: ADR_APPLICATION_PATCH_APPROVED
entrega: exibição mínima textual e retorno por Esc
status: concluido
```

## 1. Autoridade estrutural incorporada

O bloqueio decisório original foi resolvido pela ADR-0044 P01 /
D-POP-25, aplicada documentalmente e aprovada em QA. O handoff passa a
autorizar a retomada documentalmente exequível, sem alterar seu escopo.

O JSON estrutural da tela possui o campo geral opcional literal `popups`, fora
de `cabecalho`, `corpo` e `barra_de_menus`. Ele é um mapa/objeto de cardinalidade
`0..N`; a ausência e `popups: {}` são válidas. Cada chave é o ID estável da
declaração e não há `id` interno obrigatório redundante.

Cada entrada contém somente configuração estrutural/interativa. O conteúdo
concreto chega pronto do chamador no envelope runtime, e a declaração pode ser
reutilizada em várias aberturas sem ser consumida ou alterada. A resolução
ocorre por `popups[ID]`; ID inexistente é rejeitado e impede a abertura. A
declaração estrutural e a instância runtime são entidades distintas.

O envelope runtime demonstrativo permanece:

```yaml
conteudo_popup:
  tipo: texto
  texto: "Exemplo de pop-up."
```

O stub demonstrativo deve produzir esse envelope diretamente em runtime, sem
arquivo JSON externo persistente e sem colocar o conteúdo em
`popups.popup_basico`.

## 2. Escopo reservado para a retomada

Implementar somente uma instância de pop-up modal sobre a mesma tela normal
ativa. A tela inferior permanece materializada, preserva a mesma instância e
fica sem receber interação enquanto o pop-up estiver aberto. A sobreposição é
física sobre o corpo da tela, sem inserir o pop-up em `corpo.elementos[]`, sem
substituir a tela e sem criar pilha genérica de telas.

O caso demonstrativo deve exibir, usando o estilo vigente:

- moldura e título configuráveis;
- uma frase curta de conteúdo `tipo: texto`, sem wrapping;
- área própria de chips;
- somente o chip de tecla física `Esc`, com texto demonstrativo `Voltar`.

O alinhamento configurável aceita somente `esquerda`, `centralizado` e
`justificado`. Os vãos borda superior→conteúdo, conteúdo→chips e
chips→borda inferior aceitam somente `0|1`. O espaçamento horizontal interno
aceita somente inteiros `1..5`. Valores fora desses domínios devem ser
rejeitados; não há default silencioso.

A geometria deve usar o corpo da tela ativa como referência, calcular tamanho
intrínseco suficiente para título, frase curta, chip e espaçamentos, e
centralizar horizontal e verticalmente dentro do corpo. Não implementar
wrapping, palavra longa, crescimento complexo, chips multilinha, resize
integral, quadro mínimo, paginação ou casos-limite de terminal; esses pontos
pertencem a H-0057 ou estão fora da capacidade.

`Esc` é consumido pelo modal e fecha a instância, devolvendo exatamente:

```yaml
status: ABORTADO
```

Sem `valor` ou qualquer payload. O rótulo `Voltar` não é ação de negócio. Toda
tecla não declarada é consumida como entrada sem efeito e não pode alcançar a
tela inferior. Depois do fechamento, a mesma tela anterior volta a receber
interação. Enter, confirmação, seleção, payload, binding de retorno e ação do
chamador ficam fora deste handoff.

## 3. Caminhos resolvidos para implementação posterior

### Arquivos existentes a alterar, após o desbloqueio

- `tela/renderizacao/tela.py` — receber a instância runtime opcional, calcular
  o retângulo do corpo e compor a sobreposição sobre o quadro já materializado.
- `demo/demo.py` — manter a instância modal no estado runtime, abrir o caso
  demonstrativo por acionamento determinístico que referencia `popup_basico`,
  fornece o envelope pronto, intercepta todas as teclas no modal e devolve
  `ABORTADO` por `Esc`, preservando `tela_atual` e o modelo subjacente.
- `config/telas/demo/demo.json` — declarar `popups` no nível geral e adicionar
  o acionamento demonstrativo sem substituir a tela por uma tela destino.

### Primitivas existentes a reutilizar, sem usar a barra como área do pop-up

- `tela/renderizacao/geometria_caixa.py` — `_borda_de_estilo`, `_linha_topo`,
  `_linha_base` e `_caixa`, sem caracteres de moldura próprios do pop-up.
- `tela/carregamento/estilo.py` — `EstiloResolvido` materializado; consumir
  borda, delimitadores, capitalização e cores vigentes.
- `tela/renderizacao/composicao_corpo.py` — referência da caixa física e das
  alturas internas do corpo; não transformar pop-up em elemento funcional.
- `tela/renderizacao/barra_menus.py` — não chamar `_linhas_barra` nem usar
  `barra_de_menus` para a área própria de chips do pop-up. A aparência deve
  consumir o estilo vigente por primitiva própria do pop-up.

### Novos arquivos estritamente necessários, após o desbloqueio

- `tela/renderizacao/popup.py` — validação focal, cálculo simples de
  geometria, renderização textual e sobreposição independente da barra.
- `tela/teste_popup.py` — testes unitários de domínios, envelope, geometria,
  centralização, overlay, chip e ausência de paginação/barra.
- `demo/teste_demo_popup.py` — testes de abertura, bloqueio modal, `Esc`,
  retorno sem payload, preservação da tela e reativação.
- `demo/fixtures/h0056_popup_texto.py` — stub controlado que entrega em
  runtime o envelope já pronto; não carregar JSON externo nem criar loader ou
  produtor no pop-up.
- `docs/relatorios/IMP-0056-popup-basico-exibicao-voltar.md` — relatório
  obrigatório da implementação.

### Configuração estrutural demonstrativa fechada

Em `config/telas/demo/demo.json`, no nível geral e fora de `cabecalho`, `corpo`
e `barra_de_menus`, declarar o mapa abaixo. O ID `popup_basico` é a chave da
declaração e deve ser usado pelo acionamento demonstrativo; não adicionar
`id` dentro da entrada.

```json
"popups": {
  "popup_basico": {
    "tipo": "texto",
    "titulo": "Mensagem",
    "alinhamento": "centralizado",
    "espacamento_superior": 1,
    "espacamento_conteudo_chips": 1,
    "espacamento_inferior": 1,
    "espacamento_horizontal": 2,
    "chips": [
      {
        "id": "popup_basico_voltar",
        "tipo": "especifico",
        "tecla": "Esc",
        "texto": "Voltar",
        "referencia_regra": {
          "resultado": {
            "status": "ABORTADO"
          }
        },
        "regra_existencia": "sempre",
        "regra_ativo": "sempre",
        "forma_exibicao": "ativo"
      }
    ]
  }
}
```

Essa declaração usa a entidade canônica `chip`: `id`, `tipo`, `tecla`, `texto`,
`referencia_regra`, `regra_existencia`, `regra_ativo` e `forma_exibicao`. A
referência delega ao contrato do pop-up o resultado não confirmatório de
`Esc`; `texto: Voltar` é somente visual, sem ação de negócio. Os valores
`sempre` são relativos à instância aberta de `popup_basico`: o chip existe e
permanece ativo enquanto ela estiver aberta, independentemente da tela
subjacente. `forma_exibicao: ativo` usa a aparência ativa derivada do estilo
universal, sem cor, borda, símbolo ou formatação próprios. O chip do pop-up é
distinto de item da `barra_de_menus`; a área própria do pop-up consome `chip`,
mas não é `barra_de_menus` nem usa sua ordem canônica.

Essa declaração contém configuração, não conteúdo runtime. A abertura
demonstrativa deve seguir: tela ativa → acionamento determinístico → chamador
referencia `popup_basico` → chamador fornece o envelope textual pronto →
runtime resolve `popups["popup_basico"]` → valida → cria a instância →
renderiza sobre o corpo.

## 4. Testes e demonstração reservados

Os testes focais já definidos devem cobrir os três valores de alinhamento,
`0|1`, `1..5`, rejeições, cálculo simples de largura/altura sem wrapping,
centralização no corpo, tela subjacente preservada, captura de entrada, `Esc`
e retorno sem payload, `texto: Voltar` somente visual e sem ação de negócio,
independência da `barra_de_menus` e ausência de paginação. Acrescentar
explicitamente testes para:

- leitura de `popups` no nível geral, inclusive ausência e mapa vazio válidos;
- resolução de `popups["popup_basico"]` pela chave do mapa;
- rejeição de ID inexistente;
- aceitação da declaração sem `id` interno redundante;
- rejeição de conteúdo armazenado dentro da declaração;
- duas aberturas sucessivas da mesma declaração sem alteração da configuração;
- aceitação do chip somente quando a declaração canônica contém `id`, `tipo`,
  `tecla`, `texto`, `acao` ou `referencia_regra`, `regra_existencia`,
  `regra_ativo` e `forma_exibicao`, com rejeição da ausência de qualquer campo
  obrigatório;
- `texto: Voltar` sem ação de negócio, `Esc` encerrando sem confirmação com
  `status: ABORTADO` e sem payload;
- consumo da entidade `chip` na área própria do pop-up sem convertê-la em
  `barra_de_menus` e sem aplicar sua ordem canônica.

Não testar múltiplos tipos de retorno nem marcações neste handoff. Depois,
executar:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

A demonstração deve:

1. abrir a tela demo;
2. disparar a abertura de `popup_basico`;
3. comprovar visualmente moldura, título, texto e `[Esc] Voltar`;
4. acionar uma tecla não declarada e comprovar ausência de efeito na tela inferior;
5. pressionar `Esc`;
6. comprovar retorno à mesma tela;
7. interagir novamente com a tela inferior.

A inspeção visual final em TTY real é do usuário.

## 5. Exclusões

Não incluir H-0057, H-0058 ou H-0059; wrapping, resize completo, listas,
marcação, Espaço, Enter, confirmação, payload, compatibilidade de tipos,
envelopes completos, paginação, console, região permanente e execução de
negócio permanecem fora deste handoff.
