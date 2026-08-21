# Relatório QA — H-0076

## Verificações focais

- Leitura integral da ADR-0049 e do contrato: o handoff preserva as lacunas deliberadas de whitespace, algoritmo de justificação, última linha, ausência de vãos, largura inválida e erros.
- Handoff: define núcleo novo, integração exclusiva do popup, arquivos autorizados, alteração condicional de `texto_ansi.py`, relatório de implementação e exceção operacional focal para arquivo adicional.
- Popup: cobre a migração de `_quebrar_texto` e `_justificar_linha`; mantém `_formatar_linha` apenas para responsabilidades estruturais/geometria e explicita compatibilidades locais.
- ANSI: exige reutilização das primitivas existentes, largura visual, CSI indivisível e fechamento/restabelecimento de SGR sem duplicar parser.
- Fronteira H-0077: preserva `conteudo_externo.py` e os demais consumidores reservados; exige demonstração reproduzível dessa preservação.
- Testes e aceite: exigem núcleo, integração real do popup, recomposição por largura, comportamento ANSI, ausência de implementação concorrente e o comando focal prescrito.

## Achados materiais

Nenhum.

## Status final

`H1_HANDOFF_APPROVED`
