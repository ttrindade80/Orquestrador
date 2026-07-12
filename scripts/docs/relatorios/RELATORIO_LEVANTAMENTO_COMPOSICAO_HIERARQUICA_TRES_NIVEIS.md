# RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS

## 1. Objetivo e escopo

Levantamento documental e tecnico neutro sobre a suficiência da base atual para especificar e futuramente implementar composição hierárquica do corpo em ate 3 níveis.

Escopo cumprido: localizar fatos, comparar autoridades, registrar evidências e classificar lacunas, ambiguidades, divergências de implementação e cobertura de testes. Não houve correção documental, ADR, handoff, implementação, alteração de testes, commit ou QA de outro artefato.

## 2. Estado Git inicial

- Branch: `master`.
- Commit: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`.
- `git status --short`: `?? tela/__pycache__/`.
- `git diff --stat`: sem saída.
- `git diff --cached --stat`: sem saída.

O diretório `tela/__pycache__/` já estava não rastreado e não foi alterado.

## 3. Método e buscas executadas

Buscas e verificações executadas:

- `git status --short`
- `git rev-parse --abbrev-ref HEAD`
- `git log -1 --oneline`
- `git diff --stat`
- `git diff --cached --stat`
- `find . -maxdepth 4 -type d -path '*docs/relatorios*' -print`
- `find docs -maxdepth 4 -type f | sort`
- `find tela tests -maxdepth 4 -type f | sort` (`tests` inexistente)
- `find . -maxdepth 4 -type f -name '*.json' -o -name '*.md' | sort`
- `rg -n "grupo|corpo|filho|filhos|direto|diretos|nível|nivel|profund|aninh|recurs|arranjo|distribui|percentual|fra[cç][aã]o|horizontal|vertical|dashboard|console|lan[cç]ador|loader|renderizador|modelo|JSON" docs tela tests . -g '!tela/__pycache__/**' -g '!**/.git/**'`
- `rg -n "grupo dentro de grupo|grupo aninhado|exatamente 1|mais de 1|fora de escopo|horizontal.*grupo|grupo.*horizontal|3 níveis|nivel 4|profundidade" docs/handoff docs/relatorios docs/contratos docs/adr -g '*.md'`
- `rg -n "ADR-0018|status: proposta|aceita|aplicada|aprovada" ...`
- Leituras numeradas com `nl -ba` dos artefatos citados nas seções seguintes.

## 4. Artefatos consultados

Autoridades e documentação ativa:

- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`

Evidências de implementação, teste e exemplo:

- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `config/telas/orquestrador.json`
- `config/telas/grupo_minimo.json`

Relatórios e handoffs foram usados apenas para contexto histórico ou localização de artefatos, sem prevalência normativa.

## 5. Hierarquia de autoridade aplicada

1. Decisão explícita registrada em autoridade ativa.
2. Documentação normativa ativa.
3. ADR aprovada e aplicada.
4. Contrato ativo.
5. Handoff aprovado.
6. Implementação.
7. Relatórios.
8. Exemplos e documentos históricos.

`docs/adr/INDICE_ADR.md` afirma registrar ADRs aceitas (`docs/adr/INDICE_ADR.md:13-17`) e lista ADR-0018 como `aceita` (`docs/adr/INDICE_ADR.md:48`). O arquivo da ADR-0018, porém, ainda traz `metadata.status: proposta` e seção `Status` como `proposta` (`docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:4-7`, `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:24-27`). Essa divergência foi classificada como achado documental, mas os contratos ativos já incorporam a ADR-0018.

## 6. Terminologia encontrada

- `corpo`: região variável da tela; contém objetos em arranjo vertical ou horizontal (`docs/NOMENCLATURA.md:203-208`).
- Tipos funcionais: `console`, `lancador`, `dashboard` (`docs/contratos/contrato_composicao_corpo.md:81-89`).
- `grupo`: único nó estrutural, não funcional (`docs/contratos/contrato_composicao_corpo.md:114-130`).
- `nivel`: conjunto de filhos diretos de um mesmo container (`docs/contratos/contrato_composicao_corpo.md:132-137`; `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:93-103`).
- `arranjo`: valores finais `vertical` e `horizontal`; `sobreposto` e `lado_a_lado` são aliases transicionais (`docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md:70-96`).
- `distribuicao`: pertence ao container e reparte área entre filhos diretos (`docs/contratos/contrato_composicao_corpo.md:290-320`).

## 7. Modelo hierárquico documentado

A documentação ativa define o corpo como árvore de composição com nós funcionais e nó estrutural (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:58-73`; `docs/contratos/contrato_composicao_corpo.md:74-89`). `grupo` recebe área do pai, redistribui entre filhos diretos e declara `arranjo` e `distribuicao` próprios (`docs/contratos/contrato_composicao_corpo.md:118-130`).

Grupo pode conter grupo: sim, pela regra de níveis e grupos aninhados (`docs/contratos/contrato_composicao_corpo.md:132-137`; `docs/contratos/contrato_json_tela_minima.md:187-193`). A formulação "`em ciclo futuro`" em `grupo` (`docs/contratos/contrato_composicao_corpo.md:129-130`) e a pendência de implementação (`docs/contratos/contrato_composicao_corpo.md:990-994`) indicam que a autorização normativa existe, mas a implementação/testes ainda aguardam ciclo próprio.

A composição é conceitualmente recursiva como árvore, mas a documentação enumera a contagem dos níveis: `corpo.elementos[]` é nível 1; cada `grupo.elementos[]` cria o próximo nível; profundidade máxima 3; nível 4 ou superior deve gerar erro estrutural determinístico (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:93-103`; `docs/contratos/contrato_tela_json.md:194-198`).

Não há proibição normativa de terceiro nível; há limite explícito até 3 níveis. A contagem exclui o corpo raiz: nível 1 é a lista de filhos diretos de `corpo`, não o próprio corpo (`docs/contratos/contrato_composicao_corpo.md:132-137`).

Ambiguidade residual: um `grupo` declarado como filho no nível 3 exigiria seu próprio `elementos[]`, criando próximo nível pela regra documental (`docs/contratos/contrato_composicao_corpo.md:134-135`). Como nível 4 é inválido (`docs/contratos/contrato_composicao_corpo.md:136-137`), a leitura operacional mais coerente é que o nível 3 contenha terminais; a documentação não explicita essa restrição por uma frase própria.

## 8. Análise de multiplicidade

`elementos[]` é lista no corpo e em grupos (`docs/contratos/contrato_tela_json.md:169-175`; `docs/contratos/contrato_json_tela_minima.md:195-203`). A regra de distribuição exige `len(distribuicao.valores) == len(elementos)` e conta somente filhos diretos (`docs/contratos/contrato_composicao_corpo.md:312-320`), o que pressupõe multiplicidade por container.

Não foi encontrada regra normativa ativa limitando um nível a um único grupo. A implementação atual, porém, limita `grupo.elementos` a exatamente 1 item (`tela/loader.py:269-273`) e os testes validam essa rejeição (`tela/teste_loader.py:645-654`). Essa limitação decorre de H-0012/H-0014 histórico e diverge da norma ativa de árvore e distribuição por container.

Mistura de grupos e terminais no mesmo container é permitida por `corpo.elementos[]` poder conter elementos funcionais e `grupo` (`docs/contratos/contrato_json_tela_minima.md:172-190`). A ordem declarada é normativa para desempate de arredondamento (`docs/contratos/contrato_composicao_corpo.md:623-627`) e para associação posicional de distribuição (`docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:160-180`).

## 9. Análise de arranjo e distribuição

Containers que podem declarar `arranjo`: `corpo` e `grupo` (`docs/contratos/contrato_composicao_corpo.md:269-279`). `grupo` declara arranjo próprio e o arranjo do pai não obriga o dos filhos (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:107-119`).

Containers que podem declarar `distribuicao`: `corpo` e `grupo` (`docs/contratos/contrato_tela_json.md:200-206`; `docs/contratos/contrato_json_tela_minima.md:214-231`). A distribuição pertence ao mesmo container do arranjo e conta apenas filhos diretos (`docs/contratos/contrato_composicao_corpo.md:290-320`).

Modos ativos: `igual`, `percentual`, `fracao`; percentual soma 100 e fracao usa pesos positivos (`docs/contratos/contrato_composicao_corpo.md:551-588`). Arredondamento usa maiores restos e desempate por ordem declarada (`docs/contratos/contrato_composicao_corpo.md:618-638`).

Sem `distribuicao`, a construção é orientada pelo conteúdo e não equivale a `igual` (`docs/contratos/contrato_composicao_corpo.md:533-549`). Com distribuição explícita, a área alocada é preservada e sobra vira preenchimento interno (`docs/contratos/contrato_composicao_corpo.md:642-659`).

Regras para espaço distribuível, bordas e contato existem para vertical/horizontal: sem vão externo entre molduras no horizontal (`docs/contratos/contrato_composicao_corpo.md:514-527`) e sem linha externa automática no vertical (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:213-235`). Conteúdo maior que cota permanece lacuna fora de escopo (`docs/contratos/contrato_composicao_corpo.md:590-609`).

Contradição histórica já resolvida: regra antiga de "3 vãos iguais" foi supersedida por particionamento contíguo (`docs/contratos/contrato_composicao_corpo.md:521-527`; `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:223-228`).

## 10. Análise dos tipos permitidos

Filhos do corpo podem ser funcionais (`console`, `dashboard`, `lancador`) e `grupo` estrutural (`docs/contratos/contrato_json_tela_minima.md:172-190`). Filhos de grupo podem ser funcionais e grupos aninhados até nível 3 (`docs/contratos/contrato_json_tela_minima.md:187-193`).

Containers: `corpo` e `grupo`. Terminais/funcionais do corpo: `console`, `dashboard`, `lancador` (`docs/contratos/contrato_composicao_corpo.md:76-89`, `docs/contratos/contrato_composicao_corpo.md:114-130`). `dashboard` é passivo e opcional; `console` é o único navegável por `[✥]`; `lancador` não é navegável por `[✥]` (`docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md:125-145`).

Dashboard, console e lançador podem aparecer como elementos funcionais do corpo e, pela regra de filhos de grupo, como filhos funcionais de grupos. A documentação não explicita cardinalidade por container para `dashboard`; o contrato diz "Zero ou um por tela" (`docs/contratos/contrato_composicao_corpo.md:87-89`), o que pode limitar múltiplos dashboards em grupos distintos dentro da mesma tela. Isso deve ser preservado como restrição documental até decisão contrária.

## 11. Análise do JSON, loader e modelo

JSON conceitual permite grupos aninhados até nível 3 (`docs/contratos/contrato_json_tela_minima.md:187-193`). Campos mínimos de grupo: `id`, `tipo=grupo`, `arranjo`, `elementos[]`; `distribuicao` opcional (`docs/contratos/contrato_json_tela_minima.md:195-212`).

Loader atual não valida recursivamente: percorre apenas `corpo.elementos[]` e chama `_validar_grupo` para grupo de primeiro nível (`tela/loader.py:414-432`). `_validar_grupo` exige exatamente 1 filho interno (`tela/loader.py:269-273`), rejeita grupo aninhado (`tela/loader.py:302-306`) e rejeita arranjo `horizontal`/`lado_a_lado` em grupo (`tela/loader.py:243-251`). Isso diverge da documentação ativa para três níveis e arranjo por container.

Validação de distribuição existe apenas para `corpo.distribuicao` (`tela/loader.py:148-217`, `tela/loader.py:443-448`), com mensagens que mencionam `corpo.distribuicao`, não caminhos recursivos de grupos. Não há evidência de validação de `grupo.distribuicao`.

Modelo atual preserva a árvore somente para um grupo com um nível interno: `ElementoCorpo.elementos` existe para `grupo`, mas `_construir_elementos_internos_grupo` não recursa e assume que o loader rejeitou grupo dentro de grupo (`tela/modelo.py:127-133`). `elemento_por_id` e `elementos_por_tipo` só percorrem `modelo.corpo.elementos` diretos (`tela/modelo.py:90-106`), não a árvore integral.

## 12. Análise do renderizador

O renderizador não percorre a estrutura recursivamente. No modo vertical, expande um `grupo` de primeiro nível iterando seus elementos internos (`tela/renderizador.py:1107-1117`). No modo vertical com distribuição, aplica a cota do slot do grupo ao funcional interno (`tela/renderizador.py:1083-1094`). No modo horizontal, grupo não é expandido e vira slot visualmente vazio (`tela/renderizador.py:808-809`, `tela/renderizador.py:846-856`).

Distribuição vertical/horizontal é calculada para o `corpo` raiz (`tela/renderizador.py:1018-1054`, `tela/renderizador.py:1057-1102`). Não há evidência de cálculo de distribuição por `grupo`.

Capacidades implementadas e alinhadas com documentação ativa no corpo raiz: distribuição vertical explícita por percentual/fração/igual, maiores restos, ausência sem fallback `igual`, distribuição horizontal explícita e particionamento contíguo (`tela/renderizador.py:203-254`, `tela/renderizador.py:257-289`, `tela/renderizador.py:1010-1102`).

Comportamento que poderia funcionar parcialmente por consequência técnica: um grupo vertical de primeiro nível com um funcional interno renderiza como lista plana, mas isso não implementa três níveis nem distribuição por container.

## 13. Análise dos testes

Coberturas localizadas:

- Um nível/lista plana: `orquestrador` com 3 filhos diretos (`config/telas/orquestrador.json:23-128`; `tela/teste_loader.py:201-213`).
- Dois níveis mínimos: `grupo_minimo` com `corpo.elementos[]` contendo 1 grupo e dashboard interno (`config/telas/grupo_minimo.json:8-31`; `tela/teste_loader.py:542-590`; `tela/teste_renderizador.py:342-428`).
- Três níveis: cobertura ausente; documentação indica testes futuros (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:347-353`, `docs/contratos/contrato_composicao_corpo.md:990-994`).
- Múltiplos grupos irmãos nível 1/2/3: cobertura ausente. No nível de implementação atual, grupos com 2 filhos são rejeitados (`tela/teste_loader.py:645-654`).
- Mistura de grupos e terminais no mesmo container: cobertura ausente.
- Arranjos verticais aninhados: cobertura parcial de um grupo vertical mínimo (`tela/teste_renderizador.py:342-428`).
- Arranjos horizontais aninhados: teste negativo de grupo horizontal (`tela/teste_loader.py:666-681`); cobertura positiva ausente.
- Distribuição percentual/fracionária aninhada: cobertura ausente. Há cobertura no corpo raiz vertical (`tela/teste_renderizador.py:3576-3627`) e horizontal (`tela/teste_renderizador.py:3948-4058`).
- Estruturas inválidas: cobertura de grupo sem elementos, vazio, dois elementos, aninhado, horizontal, tipo interno desconhecido (`tela/teste_loader.py:629-690`).
- Profundidade acima do permitido: cobertura ausente para nível 4 normativo; o teste atual rejeita qualquer grupo aninhado, antes de distinguir nível 4 (`tela/teste_loader.py:656-664`).
- Regressões: preservação de ausência de distribuição e capacidades verticais/horizontais no corpo raiz (`tela/teste_renderizador.py:3520-3550`, `tela/teste_renderizador.py:3764-4182`).

Classificação das ausências:

- Testes de três níveis, grupos irmãos por nível, mistura grupo+terminal e distribuição em grupos: `COBERTURA_AUSENTE` para regra já documentada.
- Testes de nível 4 com erro determinístico específico: `COBERTURA_AUSENTE` para regra já documentada.
- Testes de conteúdo maior que cota: fora do escopo normativo atual (`docs/contratos/contrato_composicao_corpo.md:590-609`).

## 14. Compatibilidade e preservações

Preservações sustentadas:

- Lista plana continua válida e equivale a nível 1 (`docs/contratos/contrato_tela_json.md:194-198`).
- Tipos funcionais permanecem fechados: `console`, `dashboard`, `lancador` (`docs/contratos/contrato_composicao_corpo.md:81-89`).
- `grupo` não é funcional e não gera borda/título/conteúdo próprio (`docs/contratos/contrato_composicao_corpo.md:114-130`; `tela/teste_renderizador.py:381-399`).
- Ausência de `distribuicao` preserva construção orientada pelo conteúdo (`docs/contratos/contrato_composicao_corpo.md:533-549`; `tela/teste_renderizador.py:3520-3550`).
- Distribuição vertical e horizontal no corpo raiz têm cobertura de implementação/testes (`tela/teste_renderizador.py:3576-3627`, `tela/teste_renderizador.py:3948-4058`).
- JSONs ativos existentes continuam carregáveis; `grupo_minimo` exemplifica dois níveis (`config/telas/grupo_minimo.json:8-31`).
- Mensagens diagnósticas existem para vários erros do loader, mas não distinguem caminho recursivo de grupo aninhado além do id local (`tela/loader.py:253-309`).

## 15. Matriz normativa

| Tema | Autoridade principal | Regra encontrada | Evidência | Situação | Impacto para três níveis |
| ---- | -------------------- | ---------------- | --------- | -------- | ------------------------ |
| definição de grupo | ADR-0015 / contrato | Nó estrutural, não funcional, sem borda, redistribui área | `docs/adr/ADR-0015...:76-90`; `docs/contratos/contrato_composicao_corpo.md:114-130` | REGRA_ATIVA_SUFICIENTE | Base conceitual suficiente |
| recursividade | contrato JSON mínimo | `grupo` pode aparecer em `corpo.elementos[]` ou `grupo.elementos[]` | `docs/contratos/contrato_json_tela_minima.md:187-190` | REGRA_ATIVA_PARCIAL | Autoriza árvore, mas precisa explicitar efeito de grupo no nível 3 |
| profundidade máxima | ADR-0015 / contrato | Máximo 3 níveis; nível 4 rejeitado | `docs/adr/ADR-0015...:93-103`; `docs/contratos/contrato_tela_json.md:194-198` | REGRA_ATIVA_SUFICIENTE | Define limite solicitado |
| contagem dos níveis | ADR-0015 / contrato | `corpo.elementos[]` é nível 1; cada grupo cria próximo nível | `docs/contratos/contrato_composicao_corpo.md:132-137` | REGRA_ATIVA_SUFICIENTE | Evita contar corpo raiz como nível |
| multiplicidade por nível | contratos | `elementos[]` é lista; distribuição conta filhos diretos | `docs/contratos/contrato_tela_json.md:169-175`; `docs/contratos/contrato_composicao_corpo.md:312-320` | REGRA_ATIVA_PARCIAL | Permite múltiplos filhos, mas não explicita "múltiplos grupos irmãos" em frase própria |
| tipos de filhos permitidos | contrato JSON mínimo | Funcionais + `grupo` estrutural | `docs/contratos/contrato_json_tela_minima.md:172-193` | REGRA_ATIVA_SUFICIENTE | Define terminais e containers |
| mistura de grupos e terminais | contrato JSON mínimo | `elementos[]` pode conter funcionais e `grupo` | `docs/contratos/contrato_json_tela_minima.md:172-190` | REGRA_ATIVA_PARCIAL | Permitido por composição, sem exemplo/teste |
| arranjo em grupos | ADR-0015 / contrato | Cada container (`corpo` ou `grupo`) declara arranjo | `docs/contratos/contrato_composicao_corpo.md:269-279` | REGRA_ATIVA_SUFICIENTE | Necessário para níveis internos |
| distribuição em grupos | contrato | `corpo` e `grupo` podem declarar distribuição | `docs/contratos/contrato_json_tela_minima.md:214-231` | REGRA_ATIVA_SUFICIENTE | Autoriza distribuição por container |
| associação aos filhos diretos | contrato | `len(valores) == len(elementos)`; conta somente filhos diretos | `docs/contratos/contrato_composicao_corpo.md:312-320` | REGRA_ATIVA_SUFICIENTE | Evita contar descendentes |
| composição vertical aninhada | contrato | Arranjo do container filho independente | `docs/adr/ADR-0015...:107-119` | REGRA_ATIVA_SUFICIENTE | Suporta vertical por nível |
| composição horizontal aninhada | contrato | Mesmo mecanismo por container | `docs/contratos/contrato_composicao_corpo.md:269-279` | REGRA_ATIVA_SUFICIENTE | Suporta horizontal por nível |
| validação do loader | implementação | Rejeita grupo aninhado, 2 filhos e grupo horizontal | `tela/loader.py:269-306`, `tela/loader.py:243-251` | IMPLEMENTACAO_DIVERGENTE | Bloqueia três níveis hoje |
| representação do modelo | implementação | Apenas um nível interno de grupo; sem recursão | `tela/modelo.py:127-133` | IMPLEMENTACAO_DIVERGENTE | Não preserva árvore integral de 3 níveis |
| recursão do renderizador | implementação | Expande só grupo de primeiro nível no vertical; não recursa | `tela/renderizador.py:1107-1117` | IMPLEMENTACAO_DIVERGENTE | Não renderiza três níveis |
| testes de três níveis | testes | Ausentes; ADR prevê testes futuros | `docs/adr/ADR-0015...:347-353` | COBERTURA_AUSENTE | Falta cobertura executável |
| compatibilidade retroativa | contrato | Lista plana permanece válida | `docs/contratos/contrato_tela_json.md:194-198` | REGRA_ATIVA_SUFICIENTE | Preserva telas existentes |

## 16. Matriz documentação x implementação x testes

| Capacidade ou restrição | Documentação | Implementação | Testes | Classificação |
| ----------------------- | ------------ | ------------- | ------ | ------------- |
| Corpo como árvore até 3 níveis | Define (`docs/contratos/contrato_tela_json.md:194-198`) | Não implementa; rejeita grupo aninhado (`tela/loader.py:302-306`) | Ausentes para 3 níveis | IMPLEMENTACAO_DIVERGENTE |
| Nível 4 rejeitado | Define (`docs/contratos/contrato_composicao_corpo.md:832-835`) | Rejeita antes qualquer aninhamento | Ausente específico | COBERTURA_AUSENTE |
| Múltiplos filhos em grupo | Implícito por `elementos[]` e distribuição | Rejeita `len(sub)>1` (`tela/loader.py:269-273`) | Teste espera rejeição (`tela/teste_loader.py:645-654`) | TESTE_SEM_AUTORIDADE |
| Grupo horizontal | Documentado por arranjo por container | Rejeitado (`tela/loader.py:243-251`) | Teste espera rejeição (`tela/teste_loader.py:666-681`) | TESTE_SEM_AUTORIDADE |
| Distribuição em grupo | Documentada | Sem validação/cálculo em grupo | Ausente | IMPLEMENTACAO_DIVERGENTE |
| Distribuição raiz vertical | Documentada | Implementada (`tela/renderizador.py:1057-1102`) | Coberta (`tela/teste_renderizador.py:3576-3627`) | ALINHADO |
| Distribuição raiz horizontal | Documentada | Implementada (`tela/renderizador.py:1018-1054`) | Coberta (`tela/teste_renderizador.py:3948-4058`) | ALINHADO |
| Ausência de distribuição sem fallback `igual` | Documentada em contratos | Implementada (`tela/renderizador.py:1103-1123`) | Coberta (`tela/teste_renderizador.py:3520-3550`) | ALINHADO |
| Ordem declarada em arredondamento | Documentada | Implementada em helpers | Coberta (`tela/teste_renderizador.py:3478-3501`) | ALINHADO |
| Mensagem com caminho recursivo | Exige erro determinístico, sem detalhe de formato | Mensagens locais, sem caminho completo | Sem cobertura | REGRA_ATIVA_PARCIAL |
| Dashboard em múltiplos grupos | `dashboard` zero ou um por tela | Não há validação global dessa cardinalidade | Sem cobertura | AMBIGUIDADE_NORMATIVA |

## 17. Achados classificados com evidências

### ACH-001 — Implementação rejeita grupo aninhado

- Classificação: `IMPLEMENTACAO_DIVERGENTE`.
- Severidade: alta.
- Autoridade envolvida: ADR-0015 e contratos ativos.
- Evidência normativa: grupos aninhados criam novo nível e máximo é 3 (`docs/contratos/contrato_composicao_corpo.md:132-137`; `docs/contratos/contrato_json_tela_minima.md:187-190`).
- Evidência de código: `_validar_grupo` rejeita `tipo_item == "grupo"` (`tela/loader.py:302-306`).
- Impacto: impede nível 2 contendo grupo que contenha nível 3.
- Impede handoff? Não necessariamente; handoff pode especificar implementação usando norma ativa.
- Exige decisão do usuário? Não, se a política de até 3 níveis for considerada já decidida.
- Correção documental localizada? Não; é implementação futura.
- Exige ADR? Não pelo achado isolado.

### ACH-002 — Implementação limita grupo a exatamente 1 filho

- Classificação: `IMPLEMENTACAO_DIVERGENTE`.
- Severidade: alta.
- Autoridade: contratos de `elementos[]` e distribuição por filhos diretos.
- Evidência normativa: `elementos[]` é lista e distribuição conta filhos diretos (`docs/contratos/contrato_tela_json.md:169-175`; `docs/contratos/contrato_composicao_corpo.md:312-320`).
- Evidência de código: `len(sub) > 1` gera erro (`tela/loader.py:269-273`).
- Impacto: impede multiplicidade em grupos internos e múltiplos terminais/grupos no mesmo container.
- Impede handoff? Não, mas precisa ser tratado no futuro handoff.
- Exige decisão? Não identificada.

### ACH-003 — Implementação rejeita `grupo.arranjo = horizontal`

- Classificação: `IMPLEMENTACAO_DIVERGENTE`.
- Severidade: alta.
- Autoridade: ADR-0015 / contrato.
- Evidência normativa: cada container (`corpo` ou `grupo`) declara arranjo; valores `horizontal` e `vertical` (`docs/contratos/contrato_composicao_corpo.md:269-279`).
- Evidência de código: rejeição de `horizontal` e `lado_a_lado` em grupo (`tela/loader.py:243-251`).
- Impacto: impede combinação vertical/horizontal entre níveis.
- Impede handoff? Não.
- Exige decisão? Não, salvo revisão da política já documentada.

### ACH-004 — Modelo e renderizador não preservam/percorrem árvore integral

- Classificação: `IMPLEMENTACAO_DIVERGENTE`.
- Severidade: alta.
- Evidência normativa: corpo como árvore de composição (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:58-73`).
- Evidência de modelo: sem recursão; loader já teria rejeitado grupo dentro de grupo (`tela/modelo.py:127-133`).
- Evidência de renderer: expande apenas `elemento.elementos` de grupo de primeiro nível no vertical (`tela/renderizador.py:1107-1117`); no horizontal grupo vira área vazia (`tela/renderizador.py:808-809`, `tela/renderizador.py:846-856`).
- Impacto: três níveis não renderizam hoje.
- Impede handoff? Não.
- Exige decisão? Não.

### ACH-005 — Testes atuais pressupõem restrições antigas sem autoridade ativa superior

- Classificação: `TESTE_SEM_AUTORIDADE`.
- Severidade: média.
- Evidência: testes esperam erro para grupo com 2 elementos, grupo aninhado e grupo horizontal (`tela/teste_loader.py:645-681`).
- Autoridade superior em conflito: ADR-0015/contratos permitem árvore, arranjo e distribuição por container.
- Impacto: testes deverão ser revistos em implementação futura.
- Impede handoff? Não, mas deve ser explicitado.
- Exige decisão? Não, se restrições forem reconhecidas como históricas.

### ACH-006 — Cobertura de três níveis ausente

- Classificação: `COBERTURA_AUSENTE`.
- Severidade: média.
- Evidência normativa: testes de níveis aguardam ciclo futuro (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:347-353`; `docs/contratos/contrato_composicao_corpo.md:990-994`).
- Impacto: não há prova executável de três níveis, múltiplos grupos irmãos ou distribuição aninhada.
- Impede handoff? Não.
- Exige decisão? Não.

### ACH-007 — Ambiguidade de `grupo` no nível 3

- Classificação: `AMBIGUIDADE_NORMATIVA`.
- Severidade: bloqueante.
- Evidência: cada `grupo.elementos[]` cria próximo nível (`docs/contratos/contrato_composicao_corpo.md:134-135`); nível 4 é inválido (`docs/contratos/contrato_composicao_corpo.md:136-137`); `grupo` pode aparecer em `grupo.elementos[]` até nível 3 (`docs/contratos/contrato_json_tela_minima.md:187-190`).
- Formulação ambígua: não há frase explícita dizendo se `grupo` pode ser filho no nível 3 ou se nível 3 deve conter apenas terminais.
- Impacto: um futuro handoff precisa evitar criar política implícita para grupo em nível 3.
- Impede handoff? Pode impedir se o handoff precisar aceitar `grupo` como elemento do nível 3.
- Exige decisão? Sim, se o usuário quiser permitir grupo como nó no nível 3 sem criar nível 4; caso contrário pode ser correção documental localizada para explicitar a consequência do limite.

### ACH-008 — Divergência de status da ADR-0018

- Classificação: `CONTRADICAO_NORMATIVA`.
- Severidade: média.
- Evidência: índice lista ADR-0018 como aceita (`docs/adr/INDICE_ADR.md:48`), mas o arquivo declara status `proposta` (`docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:4-7`, `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:24-27`).
- Impacto: afeta a autoridade formal da semântica de ausência/distribuição, embora contratos ativos já a incorporem.
- Impede handoff? Não necessariamente para três níveis, mas deve ser saneado antes de usar ADR-0018 como autoridade primária.
- Exige decisão? Não; parece correção documental localizada se o índice e aplicação já registram aceite.

### ACH-009 — Cardinalidade de `dashboard` por tela pode limitar composições aninhadas

- Classificação: `REGRA_ATIVA_PARCIAL`.
- Severidade: baixa.
- Evidência: `dashboard` tem presença "Zero ou um por tela" (`docs/contratos/contrato_composicao_corpo.md:87-89`), mas grupos podem conter filhos funcionais (`docs/contratos/contrato_json_tela_minima.md:187-193`).
- Impacto: múltiplos grupos irmãos contendo dashboards poderiam violar cardinalidade por tela.
- Impede handoff? Só se o cenário exigir mais de um dashboard.
- Exige decisão? Sim, se a composição de três níveis exigir múltiplos dashboards na mesma tela.

## 18. Perguntas objetivas que dependem de decisão do usuário

1. No nível 3, `grupo` deve ser proibido explicitamente por criar nível 4 via `grupo.elementos[]`, ou existe uma forma válida de `grupo` no nível 3 que não cria novo nível?
2. A restrição "dashboard: zero ou um por tela" deve continuar valendo mesmo quando dashboards aparecem dentro de múltiplos grupos?
3. A divergência de status da ADR-0018 deve ser tratada como correção documental localizada antes de novos handoffs que citem a ADR-0018 como autoridade primária?

## 19. Conclusão

A documentação normativa ativa é majoritariamente suficiente para especificar composição hierárquica em até três níveis: define árvore, `grupo`, contagem dos níveis, profundidade máxima, arranjo por container, distribuição por container, associação aos filhos diretos, arredondamento e preservações de compatibilidade.

Há, porém, ambiguidades localizadas que precisam ser resolvidas antes de um handoff que aceite todos os casos solicitados: especialmente a presença de `grupo` no nível 3 e a cardinalidade de `dashboard` por tela em estruturas aninhadas. A implementação e os testes atuais estão atrás da documentação: rejeitam aninhamento, múltiplos filhos em grupo e grupo horizontal.

## 20. Status processual final

`L3_DECISAO_DO_USUARIO_E_ADR_NECESSARIAS`

Justificativa: a regra geral de três níveis existe, mas pelo menos uma política plausível permanece ambígua para especificação implementável completa (`grupo` no nível 3) e pode exigir decisão explícita antes de handoff abrangente. A divergência de implementação/testes, por si só, não exige ADR.

## 21. Próxima categoria permitida

Decisão do usuário sobre as ambiguidades normativas identificadas e, se confirmada mudança/clarificação de política, criação ou ajuste de ADR/documentação em etapa própria. Esta categoria não foi executada neste levantamento.
