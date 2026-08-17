# RELATORIO_IMPLEMENTACAO_H-0074

```yaml
item: ITEM-0026
adr: ADR-0048
handoff: H-0074
status: IMPLEMENTATION_COMPLETED
data: 2026-08-16
```

## Arquivos efetivamente alterados

Lista fechada do H-0074, todos tocados com necessidade material:

- `tela/modelo.py`
- `tela/navegacao.py`
- `tela/selecao.py`
- `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`
- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json`
- `tela/teste_navegacao.py`
- `tela/teste_loader.py`
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0074.md` (este arquivo)

Arquivos de §6.2 e §6.3 (demo, loaders genéricos, estilo, H-0063, contratos, ADRs, persistência, pop-up) não foram alterados por esta execução.

## `filho_default`

Campo obrigatório por pai aplicável a `dois_niveis_por_foco`. Valor = ID estável de exatamente um filho direto daquele pai. Sem default global, sem mapa paralelo, sem índice ordinal, sem fallback para o primeiro filho.

Leitura: `NoConteudo.campos["filho_default"]` (tipagem inalterada). Ausência → `TelaCampoObrigatorioAusente`. ID inexistente, filho de outro pai ou identidade duplicada/vazia → `TelaEstruturaInvalida`. Duplicidade é rejeitada antes de formar baseline, mesmo com `filho_default` coincidente.

## Fronteira de validação

`construir_modelo`, depois de `_propagar_conteudo_externo` e da montagem de `ModeloTela`, chama `validar_filho_default_dois_niveis` por import local (ciclo com `navegacao.py`). Todo consumidor aplicável atravessa a checagem; a demo não é chamada exclusiva. Consoles sem conteúdo associado (H-0063 no momento da construção) são ignorados. H-0063 permanece fora: autoridade persistida `preset_default` do Estilo.

## Remoção dos fallbacks

- `_reconciliar_ids_dois_niveis`: se nenhum ID marcado pertence aos filhos do pai, usa `filho_default` quando identifica exatamente um filho direto; caso contrário omite a escolha — nunca `pai.filhos[0]`.
- `entrar_nivel_filhos`: posiciona só no filho cujo ID está em `estado["selecoes"]`; se nenhum, devolve o estado inalterado (`return dict(estado)`). Não usa `filhos[0][0]`.

## Baseline e candidato

No início: baseline persistida = `filho_default` carregado; candidato runtime = essa baseline, em `estado["selecoes"]`. Cursor permanece distinto. `alternar` altera só o candidato. Esta etapa não grava o documento externo. H-0075 não foi antecipado.

## Fixtures

H-0055 conteúdo: `pai_01→filho_01_02`, `pai_02→filho_02_03`, `pai_03→filho_03_01`, `pai_04→filho_04_04`, `pai_05→filho_05_02` (posições 2, 3, 1, 4, 2). Helpers `_arvore_h0055*` : `pai_a→a2`, `pai_b→b1`. H-0072 conteúdo: `h0072_pai_01→h0072_filho_01_02`, `h0072_pai_02→h0072_filho_02_03`. JSON estrutural H-0055/H-0072/H-0063 intocado.

## Testes focais

15 testes do H-0074 (navegação + loader via `construir_modelo`): **15 passed**.

Cobertura: default válido; pais independentes; baseline do documento; cursor sem alterar escolha; `alternar` sem escrever origem; campo ausente; ID inexistente; ID de outro pai; identidade duplicada sem baseline; ausência de escolha válida sem primeiro filho; estrutura preservada; toroides H-0055; fronteira `construir_modelo`; H-0072 reconciliada.

## Suíte canônica

`PYTHONDONTWRITEBYTECODE=1 python -m pytest`: **42 errors during collection**. Causa histórica, não causal desta implementação: vários `.py` fora da lista (incl. `tela/carregamento/tela_json.py`, `demo/demo.py`) terminam com o literal `\n` (backslash + n), o que o interpretador rejeita. Evidência focal: `git show HEAD:tela/carregamento/tela_json.py | tail -c 8` já contém `}\n\\n`; `python demo/demo.py h0055_dois_niveis_por_foco` falha em `demo.py:2926` com o mesmo `SyntaxError`.

Com hook só de runtime (sem gravar arquivos fora da lista) sobre testes que compilam: **1227 passed**. Falhas remanescentes (estilo H-0065+, PTY, subprocess) apontam `JSONDecodeError Extra data` em JSON estruturais preservados (ex.: `h0063_estilo_estrutura_navegacao_dois_niveis.json`) ou `SyntaxError` em `demo.py` — o mesmo lixo histórico, não `filho_default`. Nenhum `TelaCampoObrigatorioAusente`/`TelaEstruturaInvalida` de `filho_default` na suíte aplicável.

## Demonstração e hashes

Fixture: `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`

- HASH_ANTES: `54fdb90080d404e31ef6fbe7cfb6809df38229399183b8756277c184aad2efe2`
- HASH_DEPOIS: `54fdb90080d404e31ef6fbe7cfb6809df38229399183b8756277c184aad2efe2`
- Iguais. Fixture não restaurada nem regravada.

Confirmação semântica (carga + `inicializar_escolhas_dois_niveis` + movimento + `alternar`): cada pai inicia no seu `filho_default`; posições 1–4 distintas; cursor muda e escolha não; Espaço altera só runtime.

## VALIDACAO_MANUAL_NECESSARIA

A observação visual TTY do §11 não foi declarada aprovada. `demo/demo.py` não inicia (literal `\n` histórico no arquivo preservado). Procedimento para o usuário, quando o ponto de entrada parsear:

1. `sha256sum config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`
2. `python demo/demo.py h0055_dois_niveis_por_foco`
3. Conferir os 5 pais nos filhos da tabela H-0055, não no primeiro da lista; ao menos duas posições diferentes.
4. Mover cursor entre pais/filhos — escolha inalterada.
5. Espaço em um pai — só runtime; demais pais intactos; sem Aplicar.
6. Encerrar.
7. `sha256sum` de novo no mesmo arquivo; hashes iguais.
8. Reabrir restaura os `filho_default` do documento.

O JSON estrutural `h0055_dois_niveis_por_foco.json` (preservado) também termina com `\n` no HEAD; `carregar_tela` direto falha com Extra data até esse lixo ser tratado fora deste handoff.

## Desvios

- Helpers de `teste_loader.py` copiam o JSON estrutural para temp removendo o literal `\n` só na cópia, para `carregar_tela` + `construir_modelo` exercitarem a fixture real sem alterar arquivos preservados.
- Removido o mesmo literal `\n` no EOF de `tela/modelo.py`, `tela/navegacao.py` e `tela/teste_navegacao.py` (já presente no HEAD nesses arquivos autorizados) para o módulo parsear.

## Bloqueios

Nenhum bloqueio de implementação no código autorizado. Bloqueio operacional do TTY: arquivos preservados com literal `\n` (`demo/demo.py`, JSON estrutural H-0055). Não alterados.

`git diff --check` nos arquivos autorizados: limpo. Nenhuma escrita persistente. H-0075 não antecipado.
