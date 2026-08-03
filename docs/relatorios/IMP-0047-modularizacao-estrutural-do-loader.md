# IMP-0047 — Modularização estrutural do loader

## Resultado

Implementação do H-0047 concluída em `master`, partindo de
`998a133c49d86d4227a467f9b572050debc679dd`. A mudança foi exclusivamente
estrutural: `tela/loader.py` tornou-se fachada e a lógica foi distribuída
entre os módulos nominais de `tela/carregamento/`. Nenhum teste, configuração,
`tela/modelo.py`, `tela/renderizador.py` ou `tela/renderizacao/` foi alterado.

## Arquivos e responsabilidades

Foram criados os 14 arquivos previstos: `__init__.py`, `erros.py`,
`taxonomia.py`, `caminho_base.py`, `distribuicao_corpo.py`,
`validacao_matricial.py`, `lancador_config.py`, `grupos.py`,
`envelope_pre_adr_0028.py`, `d23_console.py`,
`perfil_resultado_execucao.py`, `conteudo_externo.py`, `estilo.py` e
`tela_json.py`. As responsabilidades seguem integralmente a seção 4.2 do
handoff: erros (12 classes), taxonomia (6 constantes), resolução de caminho
(2 funções), distribuição de corpo (2), validação matricial (11), configuração
de lançador (1), grupos (5), envelope/D23 (2), política D23 (1), perfil (1),
conteúdo externo (6), estilo (12 funções e `EstiloResolvido`) e orquestração
macro (4 funções).

`__init__.py` contém somente docstring e não reexporta símbolos.

## Fachada e compatibilidade

`tela/loader.py` passou de 3.143 para 35 linhas. Contém somente imports
nominais diretos dos 24 símbolos aprovados, sem `FunctionDef`, `ClassDef`,
`Lambda`, wrapper ou lógica substantiva. A identidade entre fachada e
proprietários internos foi comprovada para todos os reexports. `_ID_TELA_RAIZ`
permanece exclusivamente em `tela.carregamento.tela_json` e não é reexportado.
`tela/modelo.py` continua importando exclusivamente
`TIPOS_CORPO_VALIDOS` e `TIPOS_ESTRUTURAIS_VALIDOS` de `tela.loader`; nenhum
consumidor externo foi migrado para caminhos internos.

## Integridade e validação

As provas estruturais da seção 7 passaram: importação isolada dos módulos,
grafo acíclico com referências reais, ausência estática/dinâmica de importação
da fachada pelos módulos internos, fachada sem definições, propriedade nominal
única dos 96 símbolos, identidade das constantes mutáveis e preservação da
assinatura, default literal, identidade e mensagem de `TelaIdIncorreto`.

Os 12 testes focais da seção 8 passaram, totalizando 311 casos. A suíte
canônica passou com `970 passed` e a demonstração da seção 9 passou com `7/7`
verificações.

Durante a extração foi materializado o default literal
`esperado="orquestrador"` de `TelaIdIncorreto`, conforme o handoff. O
decorador `@dataclass(frozen=True)` de `EstiloResolvido`, já existente no
baseline, foi preservado. Não houve pedido de exceção operacional nem
alteração fora do manifesto.

O defeito estrutural de `_CAMPOS_ENVELOPE_PRE_ADR_0028` — constante
materializada e não referenciada — foi preservado e não corrigido, conforme o
handoff. Nenhum defeito funcional adicional foi encontrado ou corrigido.
