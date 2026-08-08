# Relatório QA do handoff H-0051

status: H2_HANDOFF_PATCH_REQUIRED

Foram identificados dois achados materiais.

## H-0051-A — autorização aberta de arquivo de teste

- requisito: o manifesto nominal deve ser fechado; caminho de teste não
  enumerado exige parada e autorização antes de leitura ou alteração.
- evidência focal: H-0051 §6.3 declara que, se `pytest` encontrar outro arquivo,
  corrigi-lo “está dentro do escopo” (`docs/handoff/H-0051-paginacao-universal-pageup-pagedown.md:223-226`).
- impacto: um caminho desconhecido pode ser alterado sem a parada exigida por
  §5, violando o limite de escopo e transferindo ao implementador uma decisão
  de autorização material.
- correção necessária: remover essa autorização aberta e exigir
  `LEITURA_ADICIONAL_NECESSARIA`, com caminho e alvo exatos, antes de qualquer
  leitura ou alteração fora da lista nominal.

## H-0051-B — representação canônica inexequível no escopo autorizado

- requisito: produzir observavelmente `[PgUp][PgDn] Páginas`, preservando dois
  controles com regras de ativo/inativo independentes e sem deixar a forma
  concreta para decisão material do implementador.
- evidência focal: o handoff deixa a materialização em aberto e admite “outra
  materialização” (`...md:194-202`); as fixtures declaram dois chips separados
  com regras distintas (`config/telas/demo/h0045_paginacao_console_unico.json:325-340`).
  O renderer preservado monta cada chip como tecla + padding + texto
  (`tela/renderizacao/barra_menus.py:118-157`) e junta chips com separador
  (`.../barra_menus.py:845-876`); não há agrupamento visual configurável nesse
  caminho.
- impacto: dois chips não produzem literalmente a sequência canônica usando
  apenas as fixtures; um chip combinado perde a distinção de estado e
  acionamento entre PageUp e PageDown. O implementador teria de aceitar uma
  representação divergente ou alterar um arquivo declarado preservado, logo o
  resultado não é concretamente executável pelo escopo fechado.
- correção necessária: fechar a materialização exata e enumerar/autorizá-la,
  incluindo o proprietário de renderização necessário para agrupar visualmente
  os dois controles sem perder seus IDs e estados, ou redefinir explicitamente
  o critério observável.
