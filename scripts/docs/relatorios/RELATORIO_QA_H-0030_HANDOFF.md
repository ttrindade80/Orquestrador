---
name: QA-H0030-catalogo-telas-utilizaveis
description: Auditoria independente do handoff H-0030 — Catalogo de telas utilizaveis
metadata:
  type: relatorio_qa
  data: 2026-07-13
  handoff_auditado: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
---

# QA-H0030 — Catálogo de telas utilizáveis

## 1. Escopo

Auditoria independente do handoff:

```text
docs/handoff/H-0030-catalogo-telas-utilizaveis.md
```

Nenhum JSON, código, teste, contrato, ADR, índice ou handoff foi corrigido nesta etapa. A única saída criada é este relatório.

## 2. Status final

```yaml
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: PATCH_REQUIRED
proxima_categoria: CORRIGIR_HANDOFF
```

O handoff é conceitualmente aderente à decisão do usuário e às capacidades já aprovadas, mas contém defeitos que impedem aprovação sem patch.

## 3. Evidências verificadas

```yaml
handoff_auditado:
  arquivo_existe: sim
  caminho: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  titulo: "H-0030 — Catálogo de telas utilizáveis"
  estado_git: "nao_rastreado"
relatorio_qa:
  caminho: docs/relatorios/QA-H0030-catalogo-telas-utilizaveis.md
  existia_antes: nao
git:
  head: "9ae4aa4 fix: corrige distribuicao com cardinalidade unitaria"
  status_antes_do_relatorio:
    - "?? docs/handoff/H-0030-catalogo-telas-utilizaveis.md"
  diff_rastreado: vazio
  diff_cached: vazio
identidade:
  outro_handoff_h0030: nao_confirmado
  busca_local: "find docs/handoff -maxdepth 1 -type f -name '*0030*'"
lancador_real:
  arquivo: config/telas/orquestrador.json
  itens_atuais:
    - {id: item_destino_minimo, chip: d, tela_destino: destino_minimo}
    - {id: item_grupo_minimo, chip: g, tela_destino: grupo_minimo}
  chips_1_a_5_livres_no_estado_atual: sim
h0030_jsons:
  existentes_antes_da_implementacao: 0
h0029:
  arquivos_permanentes_encontrados: 7
  commit_head_confere_com_estado_informado: sim
qa_pos_h0029_001:
  artefato: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_COMANDOS_DEMO.md
  status: CORRIGIDO
  sustenta_monkeypatch_documentado: sim
```

Documentos e artefatos consultados em trechos necessários: contratos ativos de tela JSON, composição do corpo, lançador, JSON de lançador, console e dashboard; ADR-0020; índices; `config/telas/orquestrador.json`; `tela/demo.py`; exemplos permanentes atuais; testes canônicos diretamente relacionados; H-0028 e H-0029 nos pontos de preservação.

## 4. Verificações obrigatórias

```yaml
QA-H0030-01:
  resultado: PARCIAL
  nota: "Arquivo existe e identidade confere; arquivo esta nao rastreado."
QA-H0030-02:
  resultado: OK
  nota: "Define etapa futura de implementacao; nao aprova a si mesmo nem cria ADR."
QA-H0030-03:
  resultado: OK_COM_RESSALVA
  nota: "Capacidade e coesa; nao amplia semantica de console, dashboard ou matriz."
QA-H0030-04:
  resultado: FALHA
  nota: "Lista nominal omite arquivo de teste necessario para manter suite canonica apos alterar o orquestrador."
QA-H0030-05:
  resultado: OK
  nota: "Ids, arquivos e tela_destino dos cinco itens sao consistentes."
QA-H0030-06:
  resultado: OK
  nota: "Estado real tem 2 itens; proposta final de 7 itens e coerente; chips 1-5 livres."
QA-H0030-07:
  resultado: OK
QA-H0030-08:
  resultado: OK
QA-H0030-09:
  resultado: OK
  nota: "ADR-0020 cobre 2x2, 3x2 e 2x4 por permitir dimensoes 2-4 por eixo."
QA-H0030-10:
  resultado: PARCIAL
  nota: "Ha caminho real pelo demo apos integracao; monkeypatch e complementar, mas cobertura prevista nao prova esse caminho."
QA-H0030-11:
  resultado: FALHA
  nota: "Testes previstos nao cobrem suficientemente demo.py, Esc e preservacao dos fluxos existentes."
QA-H0030-12:
  resultado: OK
QA-H0030-13:
  resultado: OK
QA-H0030-14:
  resultado: OK
QA-H0030-15:
  resultado: FALHA
  nota: "Relatorio IMP exigido nao lista factual e separadamente todos os campos requeridos pelo prompt."
QA-H0030-16:
  resultado: OK
QA-H0030-17:
  resultado: PARCIAL
  nota: "Handoff criado aparece como arquivo nao rastreado; nenhum outro diff rastreado foi observado."
QA-H0030-18:
  resultado: FALHA
  nota: "Ha ambiguidade em condicao de bloqueio e especificacoes com placeholder JSON."
```

## 5. Achados

```yaml
- id: QA-H0030-BLOQ-001
  severidade: bloqueante
  arquivo: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  trecho: "linhas 164-172, 858-863; tela/teste_demo.py linhas 143-179 e 905-1105"
  regra_ou_autoridade: "Etapa QA-H0030-11; suite canonica direta dos seis scripts; handoff README exige criterios verificaveis."
  problema: >
    O handoff exige alterar config/telas/orquestrador.json para acrescentar cinco itens
    e exige codigo de saida 0 nos seis scripts canonicos, mas proibe alterar
    tela/teste_demo.py. Esse teste possui snapshots literais e fluxos de subprocess
    baseados no orquestrador atual com apenas os chips d/g. A alteracao declarativa
    do lancador tende a mudar a renderizacao do orquestrador e quebrar esse script,
    sem que o executor esteja autorizado a atualizar as expectativas ou acrescentar
    cobertura equivalente.
  impacto: >
    Implementacao conforme o handoff pode ficar impossivel: ou a suite canonica falha,
    ou o executor viola a lista de arquivos proibidos, ou deixa de provar a navegacao
    real pelo demo.
  correcao_necessaria: >
    Corrigir o handoff para autorizar e exigir ajuste proporcional em tela/teste_demo.py,
    ou documentar cobertura equivalente executavel que preserve a suite canonica sem
    depender de snapshots obsoletos.

- id: QA-H0030-ALTO-001
  severidade: alto
  arquivo: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  trecho: "linhas 821-856, 867-911, 919-928"
  regra_ou_autoridade: "QA-H0030-10 e QA-H0030-11 do prompt; contrato do lancador; demo.py como ponto de entrada real vigente."
  problema: >
    Os criterios automatizados se limitam a loader, modelo e renderizador para as cinco
    telas e a checagens estaticas do lancador. Nao ha exigencia automatizada de abrir
    cada tela pelo demo.py via chips 1-5, nem de validar o ciclo chip -> tela destino
    -> Esc -> orquestrador, nem de preservar d/g/Esc nos fluxos existentes.
  impacto: >
    O handoff promete telas como demonstracoes executaveis, mas nao obriga evidencia
    automatizada do caminho real de demonstracao. A validacao manual futura nao substitui
    smoke test do ponto de entrada quando a entrega altera o lancador usado pelo demo.
  correcao_necessaria: >
    Acrescentar criterios de smoke test do demo.py para os cinco chips novos, retorno
    por Esc, saida por Esc na raiz e preservacao de d/g, preferencialmente no teste_demo.py.

- id: QA-H0030-MEDIO-001
  severidade: medio
  arquivo: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  trecho: "linhas 843-847"
  regra_ou_autoridade: "QA-H0030-09 e QA-H0030-11; ADR-0020 D7-D15; contrato_composicao_corpo.md secoes da matriz."
  problema: >
    A cobertura automatizada prevista para as matrizes exige apenas renderizacao sem
    excecao, saida nao vazia e presenca textual de regioes de dashboard. Ela nao exige
    verificacoes automatizadas ou pseudo-TTY de grade integral, dimensoes 2x2/3x2/2x4,
    ausencia de lacunas, ausencia de sobreposicoes, intersecoes alinhadas ou comportamento
    sob redimensionamento.
  impacto: >
    Uma matriz visualmente errada pode passar pelos criterios automatizados do handoff,
    deixando para validacao manual defeitos que sao parte da capacidade de fixture de
    integracao repetivel.
  correcao_necessaria: >
    Especificar testes geometricos proporcionais para as tres matrizes, incluindo
    contagem de linhas/colunas, alinhamento de divisorias e ausencia de lacunas ou
    sobreposicoes indevidas em dimensoes deterministicas.

- id: QA-H0030-MEDIO-002
  severidade: medio
  arquivo: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  trecho: "linhas 810-817"
  regra_ou_autoridade: "QA-H0030-01 e QA-H0030-18; docs/handoff/README.md."
  problema: >
    A condicao BLOCKED_ID_CONFLICT diz parar se o identificador H-0030 ja estiver em
    uso em qualquer documento do projeto. Como o proprio handoff auditado ja usa H-0030,
    a regra e ambigua e pode ser interpretada literalmente como bloqueio do proprio ciclo.
  impacto: >
    Um executor conservador pode bloquear a implementacao mesmo sem existir outro handoff
    ativo com H-0030.
  correcao_necessaria: >
    Especificar que o bloqueio vale para outro artefato ou outro handoff ativo com o
    identificador H-0030, excluindo o arquivo auditado.

- id: QA-H0030-BAIXO-001
  severidade: baixo
  arquivo: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  trecho: "linhas 461, 549, 651"
  regra_ou_autoridade: "QA-H0030-04 e QA-H0030-18; contrato_tela_json.md exige barra_de_menus obrigatoria."
  problema: >
    As especificacoes normativas de dashboard e matrizes usam placeholder JSON
    `"barra_de_menus": { "...": "identica a especificada na secao 6.1" }`.
    A intencao e compreensivel, mas os blocos nao sao JSONs finais copiaveis.
  impacto: >
    Pode gerar erro de transcricao ou implementacoes divergentes, embora a secao 6.1
    forneca a barra completa.
  correcao_necessaria: >
    Substituir placeholders por JSON completo ou declarar explicitamente que os blocos
    sao esquematicos e que a barra completa da secao 6.1 deve ser materializada em cada
    arquivo.

- id: QA-H0030-BAIXO-002
  severidade: baixo
  arquivo: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  trecho: "linhas 915-928"
  regra_ou_autoridade: "QA-H0030-15."
  problema: >
    O relatorio de implementacao esperado nao exige registrar factual e separadamente
    identificadores, rotulos, chips, destinos, limitacoes, validacao manual pendente,
    estado Git com arquivos nao rastreados e preservacoes, embora alguns desses itens
    aparecam agregados.
  impacto: >
    A proxima auditoria pode receber evidencia incompleta ou agregada demais para
    comparar com git status e com os criterios do ciclo.
  correcao_necessaria: >
    Expandir a secao 16 para listar todos os campos exigidos pelo QA-H0030-15.

- id: QA-H0030-OBS-001
  severidade: observacao
  arquivo: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  trecho: "estado Git observado"
  regra_ou_autoridade: "QA-H0030-17."
  problema: >
    O arquivo auditado existe no disco e esta nao rastreado: `?? docs/handoff/H-0030-catalogo-telas-utilizaveis.md`.
    Nao havia diff rastreado ou cached antes da criacao deste relatorio.
  impacto: >
    Nao bloqueia a auditoria, mas deve constar como divergencia material em relacao a
    qualquer retorno que descreva criacao do arquivo sem mudanca rastreavel.
  correcao_necessaria: "Registrar o estado Git real no proximo ciclo; nao corrigir nesta auditoria."
```

## 6. Itens conformes relevantes

- O arquivo auditado existe e o titulo declarado confere.
- Nao ha outro arquivo `*0030*` em `docs/handoff/` alem do handoff auditado.
- O `orquestrador.json` real possui exatamente dois itens atuais (`d`, `g`); chips `1` a `5` estao livres no estado auditado.
- Os cinco arquivos `config/telas/h0030_*.json` ainda nao existem.
- As sete telas `h0029_*` existem em `config/telas/` e foram preservadas nesta auditoria.
- ADR-0020 cobre documentalmente matrizes 3x2 e 2x4, pois permite dimensoes de 2 a 4 por eixo.
- A referencia `QA-POS-H0029-001` foi encontrada em relatorio real e sustenta o mecanismo de monkeypatch documentado, sem dispensar o caminho real pelo lancador.

## 7. Conclusao

```yaml
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: PATCH_REQUIRED
relatorio: docs/relatorios/QA-H0030-catalogo-telas-utilizaveis.md
handoff_auditado: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
achados_bloqueantes: 1
achados_altos: 1
achados_medios: 2
achados_baixos: 2
observacoes: 1
proxima_categoria: CORRIGIR_HANDOFF
```
