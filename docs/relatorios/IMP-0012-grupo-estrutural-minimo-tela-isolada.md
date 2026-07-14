# Implementação — H-0012 Grupo estrutural mínimo em tela isolada

## Status

IMPLEMENTATION_COMPLETED

## Escopo implementado

Implementado o suporte mínimo ao tipo estrutural `grupo` em tela isolada,
conforme handoff H-0012 (`docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`)
aprovado em auditoria (`QA_APPROVED_WITH_NOTES`, 0 bloqueantes).

Resumo do que foi feito:

1. Criada a tela isolada `config/telas/grupo_minimo.json` com exatamente
   1 elemento de `tipo = "grupo"` contendo exatamente 1 elemento funcional
   (`dashboard`) com `fonte: "literal"`.
2. Alterado `tela/loader.py` para reconhecer `tipo = "grupo"` como tipo
   estrutural (separado da taxonomia funcional fechada) e validar os
   invariantes do H-0012.
3. Alterado `tela/modelo.py` para representar o grupo estrutural expondo
   os elementos funcionais internos como `ElementoCorpo` acessíveis ao
   renderer.
4. Alterado `tela/renderizador.py` para percorrer o grupo e renderizar o
   elemento funcional interno pelo mesmo despacho da lista plana, sem
   gerar caixa visual própria para o container.
5. Ampliados os testes permitidos cobrindo aceitação e rejeição do grupo.
6. Criado este relatório.

O Orquestrador e seus JSONs não foram alterados; a saída do diagnóstico
do Orquestrador é byte-a-byte idêntica à do HEAD base `6c91279`.

## Arquivos criados

- `config/telas/grupo_minimo.json`
- `docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md`

## Arquivos alterados

- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`

## Decisões locais

Não houve decisão arquitetural nova. As decisões de implementação abaixo
estão todas cobertas pelo handoff H-0012 (seções F-1, F-2, F-3) e não
introduzem registry, subclasses de elemento, estado de runtime nem
alteração de contrato/ADR.

- **Loader**: introduzido `TIPOS_ESTRUTURAIS_VALIDOS = {"grupo"}`, distinto
  de `TIPOS_CORPO_VALIDOS` (`console`, `lancador`, `dashboard`). A taxonomia
  funcional permanece fechada. Para `tipo == "grupo"`, a função
  `_validar_grupo` aplica os invariantes do ciclo:
  `arranjo != "lado_a_lado"` (se presente), campo `elementos` presente e
  lista com exatamente 1 item, item interno com `id`/`tipo`, `tipo` interno
  funcional e não `grupo`. O elemento do grupo é preservado no dict de
  saída do loader (incluindo os sub-elementos inertos), seguindo o padrão
  já existente de preservação declarativa.

- **Loader / exceção**: adicionada `TelaGrupoInvalido(TelaErro)` para
  violações estruturais específicas do grupo (ausência/vazio/excesso de
  elementos, aninhamento, `lado_a_lado`, item interno inválido). É uma
  exceção de validação, consistente com a família existente
  (`TelaCampoObrigatorioAusente`, `TelaEstruturaInvalida`, etc.) — não é
  registry, não é subclassificação de elemento. Tipo funcional desconhecido
  dentro do grupo continua levantando `TelaTipoDesconhecido` (reutilizado).

- **Modelo**: adicionado o campo `elementos: list = field(default_factory=list)`
  em `ElementoCorpo`, preenchido com os `ElementoCorpo` internos quando
  `tipo == "grupo"` e vazio para tipos funcionais (solução preferida
  sugerida pelo handoff em F-2.a). Para o grupo, `elementos` (cru) é
  excluído de `_campos_inertes` por já estar estruturado; `arranjo`
  permanece inerte. O conjunto aceito pelo construtor passou a ser
  `TIPOS_CORPO_VALIDOS | TIPOS_ESTRUTURAIS_VALIDOS`. Não há recursão:
  grupo dentro de grupo é rejeitado pelo loader antes de chegar ao modelo
  (item interno é sempre funcional).

- **Renderer**: extraído o despacho de elemento funcional em
  `_caixa_de_elemento` (console/dashboard/lancador → caixa bordeada,
  idêntico ao comportamento anterior). No laço principal, `tipo == "grupo"`
  percorre `elemento.elementos` e despacha cada interno pelo mesmo
  mecanismo, sem emitir borda/título/linha extra. A lista plana segue
  pelo mesmo despacho. A saída do Orquestrador é byte-a-byte idêntica à
  anterior (verificado por diff).

## Preservações

- Orquestrador não alterado (`config/telas/orquestrador.json`).
- destino_minimo não alterado (`config/telas/destino_minimo.json`).
- stub_b não alterado (`config/telas/stub_b.json`).
- demo.py não alterado (`tela/demo.py`).
- diagnostico.py não alterado (`tela/diagnostico.py`).
- teste_demo.py não alterado (`tela/teste_demo.py`).
- teste_diagnostico.py não alterado (`tela/teste_diagnostico.py`).
- Nenhum contrato em `docs/contratos/` foi alterado.
- Nenhuma ADR em `docs/adr/` foi alterada.
- `docs/NOMENCLATURA.md` e `docs/INDICE.md` não foram alterados.
- `docs/handoff/` não foi alterado pelo executor.
- Nenhum commit foi realizado.
- Nenhum `__pycache__` ou `.pyc` permanece no repositório.

## Testes executados

### Validade do JSON da tela isolada

```bash
python -m json.tool config/telas/grupo_minimo.json >/dev/null && echo "grupo_minimo.json OK"
```

Resultado: `grupo_minimo.json OK` (exit 0).

### JSONs de produção inalterados

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
python -m json.tool config/telas/stub_b.json >/dev/null && echo "stub_b.json OK"
```

Resultado: todos `OK` (exit 0).

### Testes unitários

| Comando | Exit code | [FALHOU] | Traceback | Total/Passaram |
|---|---|---|---|---|
| `python tela/teste_loader.py` | 0 | 0 | 0 | 61 / 61 |
| `python tela/teste_modelo.py` | 0 | 0 | 0 | 49 / 49 |
| `python tela/teste_renderizador.py` | 0 | 0 | 0 | 112 / 112 |
| `python tela/teste_diagnostico.py` | 0 | 0 | 0 | 28 / 28 (não alterado) |
| `python tela/teste_demo.py` | 0 | 0 | 0 | 95 / 95 (não alterado) |

### Pipeline de diagnóstico (integridade do Orquestrador)

```bash
python tela/diagnostico.py
```

Resultado: exit 0. Saída comparada com a do HEAD base (`6c91279`) via
`diff` — **idêntica**. O Orquestrador não mudou.

### Loader sobre a tela isolada

```bash
python -c "from tela.loader import carregar_tela; r=carregar_tela(None,'grupo_minimo'); print(r['id'], r['corpo']['elementos'][0]['tipo'])"
```

Resultado: `grupo_minimo grupo` — carrega e valida sem erro (exit 0).

### Cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Resultado: ambos vazios.

```bash
git status --short
```

Resultado:

```text
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? config/telas/grupo_minimo.json
?? docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
?? docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
?? docs/relatorios/LEVANTAMENTO_H-0012_POS_AUDITORIA.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF_POS_AJUSTES.md
```

Os arquivos `M` (alterados) e os `??` criados pelo executor
(`config/telas/grupo_minimo.json` e este relatório) estão todos dentro da
lista de arquivos permitidos do H-0012. Os demais `??` (handoff H-0012 e
três relatórios de auditoria/levantamento) são os documentos não
rastreados esperados, anteriores à implementação, e não foram tocados.

Nenhum arquivo fora da lista de permitidos foi criado ou alterado.
Nenhum commit foi realizado.

## Cobertura dos critérios de aceite

- CA-01..CA-07 (tela isolada): atendidos por `grupo_minimo.json` e por
  `teste_loader.py` / `teste_modelo.py`.
- CA-08 (carrega sem erro): atendido.
- CA-09..CA-13 (rejeições de grupo): atendidos por `teste_loader.py`
  (`TelaGrupoInvalido` para sem elementos / vazio / 2+ / aninhado /
  `lado_a_lado`; `TelaTipoDesconhecido` para tipo interno desconhecido).
- CA-12b (rejeição de `lado_a_lado`): atendido.
- CA-14 (lista plana inalterada): atendido (orquestrador, destino_minimo,
  stub_b carregam sem erro).
- CA-15..CA-19 (modelo): atendidos por `teste_modelo.py`
  (`elemento.elementos` expõe o interno como `ElementoCorpo`;
  `elemento_por_id`/`elementos_por_tipo` operam no grupo; grupo distinto
  de funcional).
- CA-20..CA-24 (renderer): atendidos por `teste_renderizador.py`
  (caixa do dashboard interno aparece; valor literal aparece; grupo não
  gera caixa própria — 3 caixas totais; saída == lista plana equivalente;
  Orquestrador inalterado).
- CA-25..CA-29 (testes exit 0): atendidos.
- CA-30..CA-39 (escopo/rastreabilidade): atendidos — JSONs de produção,
  contratos, ADRs, NOMENCLATURA, INDICE, demo, diagnóstico e seus testes
  intactos; sem commit; sem `__pycache__`/`.pyc`.

## Resultado final

Pronto para QA Codex.

Todos os comandos obrigatórios encerram com código de saída 0, sem linhas
`[FALHOU]` e sem traceback. A saída do Orquestrador é idêntica à do HEAD
base. Somente arquivos permitidos foram criados/alterados.
