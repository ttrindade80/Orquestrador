# Relatório de criação — H-0075

```yaml
etapa: CRIAR_HANDOFF
handoff: H-0075
item: ITEM-0026
adr: ADR-0048
data: 2026-08-16
status: HANDOFF_CREATED
predecessor: H-0074 (implementado, MANUAL_VALIDATION_APPROVED)
```

## Capacidade

H-0075 fecha a segunda metade do ITEM-0026: candidato divergente → Aplicar
→ snapshot → pop-up genérico → ABORTADO (sem escrita) ou CONFIRMADO
(persistência fail-closed de `filho_default` no documento externo da tela
aberta) → nova baseline e candidato equalizado. Não reimplementa H-0074.

## Mecanismos de Estilo reutilizados

Chip canônico `chip_aplicar` / `tecla ⏎` / `regra_ativo:
candidato_divergente`; ponte `aplicar_disponivel` já avaliada em
`barra_menus.py`; intercepto de Enter antes de Todos; dataclass frozen com
`deepcopy`; `abrir_popup` + modalidade de `demo.py`; resultados
`CONFIRMADO`/`ABORTADO`; técnica atômica tempfile + `fsync` + `os.replace`;
consumo da solicitação no mesmo evento de Confirmar; descarte da tentativa
após ABORTADO ou após CONFIRMADO; falha sem popup de erro.

## Mecanismos que não se aplicam

`persistir_configuracao_estilo` / `aplicar_candidato` (validam Estilo e
publicam global); `config/estilo.json`; `estado["estilo"]`; overlay H-0069;
`preset_default`; `SolicitacaoAplicacaoEstilo` e seu slot de sessão;
`ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO`; `ControladorTelaEstilo`.

## Controlador e fronteira de Aplicar

Controlador em `tela/selecao.py` (candidato já vive em
`estado["selecoes"]`). `aplicar_disponivel_filho_default` compara mapas
pai→filho (baseline = `campos["filho_default"]`; candidato = mescla da
`lista_foco` no documento compartilhado). Ativo se qualquer pai diverge;
cursor irrelevante. Tela aplicável: conteúdo externo com
`caminho_origem`, console `dois_niveis_por_foco`, não a tela de Estilo.
H-0055/H-0072 são fixtures, não destinos hardcoded. Enter inativo é no-op
(não Todos).

## Snapshot

`SolicitacaoAplicacaoFilhoDefault` (frozen): `caminho_destino`, `baseline`,
`candidato` (todos os pais). CONFIRMADO consome esse candidato, nunca
`selecoes` posteriores. Vários pais divergentes entram no mesmo mapa;
não persiste só o pai do cursor. Em H-0072, prevalece o primeiro console
da `lista_foco` que divergir por pai.

## Pop-up

Declaração `popups.popup_confirmacao_aplicacao_filho_default` (`tipo:
texto`, Voltar/Confirmar) nos JSON estruturais H-0055 e H-0072.
`popup.py` não muda. Envelope textual sem `filho_default`. ABORTADO fecha
a tentativa, preserva candidato/baseline/arquivo, mantém Aplicar se houver
divergência. CONFIRMADO persiste no mesmo evento.

## Persistência e destino

`carregar_conteudo_externo` hoje descarta `caminho_arquivo`. Proveniência:
catálogo `id_tela → id_conteudo` →
`resolver_caminho_conteudo_externo` (mesma composição da carga) → override
opcional `estado["caminhos_conteudo_externo"][id_tela]` (cópia/teste) →
`ConteudoExterno.caminho_origem` (runtime, não schema JSON). Snapshot
congela esse Path. Escrita:
`aplicar_filho_default_no_documento` sobre `deepcopy(_raw)` (só
`filho_default` divergente) + `validar_conteudo_externo` + checagem de IDs
+ `persistir_conteudo_externo` em `conteudo_externo.py`. Não usar a função
de Estilo.

## Fail-closed

Um `os.replace` do documento completo; temporário removido em falha;
arquivo e baseline anteriores intactos; candidato preservado; Aplicar
ativo; tentativa descartada sem retry automático. Monkeypatch da primitiva
de escrita nos testes.

## Arquivos futuros autorizados

`tela/selecao.py`; `tela/carregamento/conteudo_externo.py`; `tela/modelo.py`
(só `caminho_origem`); `demo/demo.py`; JSON estrutural H-0055 e H-0072
(chip + popups); `tela/teste_filho_default_h0075.py`;
`demo/teste_demo_filho_default_h0075.py`; acréscimos focais em
`tela/teste_loader.py`; `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0075.md`.

Não autorizados: `popup.py`, renderers, `estilo.py`, `config/estilo.json`,
conteúdo JSON H-0055/H-0072 (escrita só em cópia), contratos, ADR,
nomenclatura, backlog, ITEM-0023/0024.

Delta H-0074 no worktree não é reaberto. Resíduos EOF históricos ficam
para o FECHAMENTO.

## Testes

26 itens no handoff §12, todos em `tmp_path`/cópia: Aplicar, snapshot,
modalidade, ABORTADO, CONFIRMADO, preservação de campos, vários pais,
H-0055, H-0072, falha, ausência de publicação de estilo, regressão H-0074.

## Demonstração

Prova de arquivo = teste automatizado da cópia H-0055. TTY opcional sobre
cópia com override de caminho; nunca CONFIRMADO no fixture do repositório.
Critérios visuais enumerados no handoff §13.

## Bloqueios

Nenhum. Caminho, Aplicar, pop-up, snapshot e escrita atômica fecham-se no
código vigente com extensão mínima de transporte de Path.
