---
name: RELATORIO_QA_ADR-0028
description: Relatório de QA da ADR-0028 — apresentações de conteúdo multinível no console e alternância verbosa — versão corrigida após PATCH_ADR
metadata:
  type: relatorio_qa
  adr_auditada: ADR-0028
  data: "2026-07-17"
  auditor: independente (contexto limpo)
  status_literal: ADR_REJECTED
---

# Relatório de QA — ADR-0028

## 1. Identificação

| Campo | Valor |
|---|---|
| Relatório | RELATORIO_QA_ADR-0028.md |
| ADR auditada | ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md |
| Data | 2026-07-17 |
| Ciclo precedente | PATCH_ADR (versão corrigida) |
| Status declarado recebido | ADR_PATCHED |

---

## 2. Objetivo

Auditar a ADR-0028 em sua versão corrigida para verificar se:

- a autoridade incorreta foi removida e a correta adotada;
- todas as decisões explícitas do usuário (DU-01 a DU-10) foram formalizadas;
- não há resíduos normativos matriciais;
- o escopo exclusivo de `console` com conteúdo multinível foi respeitado;
- as apresentações e regras normativas do contrato correto foram contempladas;
- as decisões deliberadamente adiadas não foram preenchidas;
- o documento está internamente coerente.

---

## 3. Autoridades lidas

| Documento | Status de leitura |
|---|---|
| `CONTRATO_APRESENTACAO_DISTRIBUICAO_CONTEUDO_MULTINIVEL.md` (em `/home/tiago/Downloads/`) | Lido integralmente |
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | Lido integralmente (1367 linhas) |
| `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` | Lido integralmente |
| `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md` | Lido via contexto anterior |
| `docs/adr/INDICE_ADR.md` | Lido integralmente |
| `docs/contratos/contrato_console.md` | Lido integralmente |
| `docs/contratos/contrato_json_console.md` | Lido parcialmente (seções 1–4) |

O arquivo `ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md` não foi usado como
autoridade neste QA, conforme determinado.

**Nota sobre o caminho do contrato externo:** O prompt indica `/mnt/data/` como
caminho. O arquivo não existe nesse caminho. Ele foi encontrado e lido de
`/home/tiago/Downloads/CONTRATO_APRESENTACAO_DISTRIBUICAO_CONTEUDO_MULTINIVEL.md`.
O conteúdo do documento é o correto e sua leitura não foi comprometida.

---

## 4. Escopo auditado

Arquivo único: `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`

Verificações executadas: todas as 29 verificações obrigatórias do escopo do QA,
incluindo fidelidade às decisões DU-01 a DU-10, ausência de conteúdo matricial,
compatibilidade com ADR-0026 e ADR-0027, modelo hierárquico, todas as
apresentações, ambos os modos, tecla V, paginação, impossibilidade geométrica,
validações, terminologia, decisões adiadas, responsabilidades das camadas,
demonstração, testes, validação manual, escopo negativo, documentos afetados,
ausência de implementação antecipada e estado Git.

---

## 5. Estado Git

```yaml
branch: master
head: f6982d0
git_status_short: "?? docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md"
arquivo_auditado: não rastreado (novo, não commitado)
outros_arquivos_modificados: nenhum
outros_arquivos_nao_rastreados: nenhum além da ADR-0028
workspace_limpo: true (exceto a ADR-0028 nova não commitada)
```

O arquivo foi criado nesta sessão (PATCH_ADR). Não há commit. O escopo do patch
foi respeitado: apenas `docs/adr/ADR-0028-...` é novo ou modificado. Nenhum
outro arquivo aparece no git status.

---

## 6. Fidelidade às decisões do usuário (DU-01 a DU-10)

### DU-01 — Escopo exclusivo console/multinível

**Resultado: CONFORME**

§6 declara explicitamente que a ADR se aplica exclusivamente a dados multinível
em componentes `console`. Lista explícita de exclusões: `dashboard`, `lancador`,
componentes genéricos, distribuição matricial, `tipo: matriz`, telas sem
conteúdo multinível externo.

### DU-02 — Origem atual por arquivo JSON externo

**Resultado: CONFORME**

§7 descreve a origem atual como documento JSON externo armazenado em arquivo,
com os quatro passos do ponto de entrada.

### DU-03 — Origem futura pelo Pipeline

**Resultado: CONFORME**

§8 descreve a integração futura, preservando: dados em formato JSON; fronteira
semântica estável; conteúdo separado do JSON estrutural; independência do
`console` quanto ao mecanismo produtor.

### DU-04 — Integração futura fora de escopo

**Resultado: CONFORME**

§43 adia explicitamente: protocolo (item 10), comando (item 11), transporte
(item 12), persistência intermediária (item 13), timeout (item 14),
indisponibilidade (item 15). §42 lista "integração concreta com o projeto
Pipeline" e "protocolo de transporte entre projetos" como fora de escopo.

### DU-05 — Quatro apresentações

**Resultado: CONFORME**

D8 e §36 listam os quatro cenários. §§17–20 detalham as regras de cada um.
Os cenários 3 e 4 estão em seções separadas (§19 e §20), registrando a
distinção estrutural mesmo dentro do modo conceitual `conjuntos_campos`.

### DU-06 — Alternância visual por cenário

**Resultado: CONFORME**

§§21 e 22 definem modo não verboso e verboso. D11/§23 define a alternância
por `V` com mesmos dados, mesma tela, mesmo documento, sem trocar a
apresentação ou o cenário.

### DU-07 — Barra de menus com `[V] Verboso`

**Resultado: CONFORME**

§23 define que a barra de menus das demonstrações de dados do `console` deve
apresentar `[V] Verboso`. D11 define reversibilidade.

### DU-08 — Estado da sessão

**Resultado: CONFORME**

§24 lista explicitamente sete comportamentos que a alternância NÃO deve ter:
reescrever JSON externo, reescrever JSON estrutural, alterar fixture, substituir
dados, persistir preferência global, vazar para outro console, alterar identidade
do cenário.

### DU-09 — Modo inicial pela configuração declarativa

**Resultado: CONFORME**

§25/D12 determinam que o modo inicial vem do campo de excesso do JSON externo.
Se ausente, o comportamento é adiado (item 3 do §43). Nenhum valor padrão foi
inventado.

### DU-10 — Responsabilidade do renderizador

**Resultado: CONFORME**

D14 e §35.4 listam explicitamente os resultados físicos que pertencem ao
renderizador: área útil, larguras, alturas, recuos, colunas iniciais, linhas
físicas, quebras, truncamentos, páginas, repetições visuais, posições finais,
impossibilidade geométrica e recuperação após redimensionamento.

---

## 7. Autoridade externa

**Resultado: CONFORME**

§3.3 nomeia `CONTRATO_APRESENTACAO_DISTRIBUICAO_CONTEUDO_MULTINIVEL.md` como
autoridade normativa desta ADR. O documento incorreto
(`ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md`) é explicitamente
desautorizado no mesmo §3.3 com a declaração: "não é autoridade para esta
decisão. Qualquer regra derivada exclusivamente desse documento foi removida
nesta versão corrigida."

§5 (autoridades lidas) lista somente o contrato correto como autoridade
normativa externa, além de ADR-0026, ADR-0027 e INDICE_ADR.md.

Nenhuma regra residual derivada exclusivamente do documento incorreto foi
encontrada.

---

## 8. Escopo exclusivo de console

**Resultado: CONFORME**

§6 é dedicado à declaração do escopo exclusivo. A formulação "Quando esta ADR
mencionar 'conteúdo', 'dados', 'apresentação' ou 'renderização', trata-se sempre
de conteúdo multinível exibido no `console`" garante que todo o corpo normativo
esteja circunscrito ao escopo declarado.

Nenhuma formulação genérica incorretamente abrangente foi identificada.

---

## 9. Origem atual e futura

**Resultado: CONFORME**

A distinção entre as origens está adequadamente separada em seções dedicadas:

- §7: origem atual por arquivo;
- §8: origem futura por script do Pipeline;
- §9: fronteira estável em JSON;
- §43 itens 10–15: protocolo não decidido.

---

## 10. Compatibilidade com ADR-0026

**Resultado: CONFORME**

§10 declara que a ADR-0026 permanece autoridade ativa. Identifica as três
decisões preservadas: separação entre JSON estrutural e conteúdo externo;
envelope conceitual `{tipo, formato, dados}`; princípio declarativo. §39
(compatibilidade) reitera que a ADR-0026 não é substituída.

Nenhuma reinserção de dados no JSON estrutural foi detectada.

---

## 11. Compatibilidade com ADR-0027

**Resultado: CONFORME**

§11 declara preservação do carregamento separado, entrega conjunta, ponto de
entrada como responsável pela associação, schema multinível (três apresentações,
três tipos de nível, designadores, 20 validações mínimas) e fixtures permanentes.

§33 declara que V-01 a V-15 complementam as 20 validações da ADR-0027 (D13),
sem substituí-las.

D3 reitera explicitamente as decisões D2 e D8 da ADR-0027.

Protocolo futuro do Pipeline não foi fixado.

---

## 12. Ausência de conteúdo matricial

**Resultado: CONFORME**

Busca textual por "matriz", "matrici" e "matrix" no arquivo produziu apenas
referências históricas e de exclusão de escopo:

- §3.3: menção ao arquivo incorreto como autoridade removida;
- §6: `tipo: matriz` listado como fora de escopo;
- §39: ADR-0025/H-0035 (distribuição matricial de nível único) listados como
  não afetados;
- §42: conteúdo matricial listado explicitamente no escopo negativo;
- §46 linha 1: verificação de integridade confirmando ausência;
- §46 linha 2: verificação de integridade confirmando ausência.

Todas as ocorrências são de exclusão ou referência histórica. Nenhuma regra
normativa derivada de conteúdo matricial foi encontrada.

---

## 13. Modelo hierárquico

**Resultado: CONFORME**

§13 (7 subseções) cobre: árvore, raiz única, identificadores de níveis, relações
pai–filho, quantidade declarada, compatibilidade dos dados, determinismo e
estabilidade entre páginas. A raiz única, os identificadores independentes de
designação, e a rejeição por dados incompatíveis estão presentes.

---

## 14. Designadores

**Resultado: CONFORME**

§15 (6 subseções) cobre: presença opcional, nove tipos mínimos (nenhum, símbolo
fixo, decimal, alfabético minúsculo, alfabético maiúsculo, romano minúsculo,
romano maiúsculo, composto, personalizado), componentes (prefixo, valor, sufixo),
compostos com ancestrais, escopo de reinício (global, por pai, por página, sem
reinício) e largura/alinhamento do designador.

D5 confirma que designadores não definem a hierarquia.

---

## 15. Tabela multinível

**Resultado: CONFORME**

§17 (12 subseções) cobre: cabeçalho obrigatório (17.1), colunas declaradas com
identificador/origem/ordem/largura/alinhamento/excesso (17.2), caminho completo
por linha lógica (17.3), ordem das linhas (17.4), política de ancestrais (17.5),
margens e espaços estruturais (17.6), preenchimento de célula (17.7), largura
das colunas com seis políticas (17.8), alinhamento horizontal e vertical (17.9),
excesso não verboso por célula (17.10), excesso verboso com altura calculada
(17.11), paginação com repetição de cabeçalho e indivisibilidade (17.12).

Coluna sem origem é inválida (V-14). Tabela sem cabeçalho é inválida (V-01).

---

## 16. Hierarquia indentada

**Resultado: CONFORME**

§18 (8 subseções) cobre: linha lógica por nó (18.1), recuo declarado em espaços
com proibição de tabulação implícita do terminal (18.2), margens e espaços
independentes sem combinação implícita (18.3), alinhamento natural dos
designadores (18.4), alinhamento justificado com escopo (18.5), excesso não
verboso com cálculo da largura disponível (18.6), excesso verboso com continuação
na coluna inicial do conteúdo (18.7), paginação com preservação de ancestrais
(18.8).

---

## 17. Conjuntos com campos nome–valor (dois níveis)

**Resultado: CONFORME**

§19 (8 subseções) cobre: estrutura conjunto–campo (19.1), linha nome–valor com
quatro componentes (19.2), separador configurável com espaços independentes
antes e depois (19.3), justificação dos nomes com escopo (19.4), coluna inicial
do valor calculada com nove componentes (19.5), espaçamentos nome–valor
separados (19.6), excesso não verboso com prioridade de preservação (19.7),
excesso verboso com continuação na coluna inicial do valor (19.8).

---

## 18. Conjuntos, subconjuntos e campos (três níveis)

**Resultado: CONFORME**

§20 (5 subseções) cobre: estrutura conjunto–subconjunto–campo com exemplo (20.1),
designadores independentes por nível (20.2), quantidade declarada (20.3),
espaçamento adicional entre subconjuntos (20.4), repetição de contexto na
paginação (20.5). Os cenários 3 e 4 têm seções próprias (§19 e §20) conforme
DU-05.

---

## 19. Modo não verboso

**Resultado: CONFORME**

§21 lista seis regras: uma linha física por conteúdo, sem continuação, excedente
truncado, marcador cabe integralmente, dados originais inalterados, JSON não
armazena texto previamente truncado. Aplica por apresentação: tabela (linha por
célula), hierarquia (linha por nó), nome–valor (linha por linha lógica). Modo
não verboso configurado para mais de uma linha é explicitamente inválido (final
do §21).

---

## 20. Modo verboso

**Resultado: CONFORME**

§22 lista seis regras: múltiplas linhas físicas, quebras pelo renderizador,
continuação com alinhamento definido, limite máximo de linhas, política final
ao exceder, linhas não armazenadas no JSON. Aplica por apresentação: tabela
(altura pela célula de maior altura), hierarquia (continuação na coluna inicial
do conteúdo), nome–valor (continuação na coluna inicial do valor). Modo verboso
com limite de uma linha não é equivalente automático a não verboso. Modo verboso
sem regra de continuação é explicitamente inválido.

---

## 21. Tecla V

**Resultado: CONFORME**

§23 define: tecla `V` alterna entre verboso e não verboso durante a sessão; barra
de menus deve apresentar `[V] Verboso`; alternância usa mesmos dados, mesma tela,
mesmo documento, não troca apresentação, não persiste, é reversível; segunda
ativação retorna ao modo anterior.

§24 lista sete comportamentos que a alternância não deve ter.

---

## 22. Paginação

**Resultado: CONFORME**

§30 (4 subseções) cobre: responsabilidades separadas entre JSON (declara) e
renderizador (calcula), comportamento por modo de apresentação (cabeçalho em
tabela, ancestrais em hierarquia, conjunto/subconjunto em conjuntos), contexto
repetido como contexto visual que não altera dados nem numeração, indicador de
continuação configurável, paginação não corrige largura.

§31 trata blocos indivisíveis com política para bloco maior que uma página.

Repetição de cabeçalho: §30.1. Repetição de ancestrais em hierarquia: §30.1 e
§18.8. Conjunto e subconjunto: §30.1 e §20.5. Sem duplicação semântica: §30.2.
Sem reinício de numeração: §30.2. Bloco maior que página exige política: §31.

---

## 23. Impossibilidade geométrica

**Resultado: CONFORME**

§32 estabelece: renderizador calcula largura e altura mínimas; paginação não
resolve impossibilidade horizontal; quando nem a unidade mínima couber, o
renderizador aciona a política; a configuração deve definir a resposta (quadro
mínimo, fallback, erro, rejeição). Relaciona às ADRs vigentes (ADR-0017 e
ADR-0023) sem inventar política nova. Lacunas são adiadas para a aplicação
documental.

---

## 24. Validações

**Resultado: CONFORME COM RESSALVA**

As 15 validações (V-01 a V-15) cobrem:

| Código | Condição auditada | Presente |
|---|---|---|
| V-01 | Tabela sem cabeçalho | Sim |
| V-02 | Referência a nível filho inexistente (cobre "filho inexistente") | Sim |
| V-03 | Múltiplas raízes | Sim |
| V-04 | Folha que declara filhos | Sim |
| V-05 | Contêiner obrigatório sem nível filho declarado | Sim — ver achado QA-002 |
| V-06 | Campo nome–valor sem origem do valor | Sim |
| V-07 | Medidas negativas | Sim |
| V-08 | Largura máxima inferior à mínima | Sim |
| V-09 | Modo não verboso configurado para mais de uma linha | Sim |
| V-10 | Modo verboso sem regra de alinhamento da continuação | Sim |
| V-11 | Justificação sem escopo | Sim |
| V-12 | Designador composto que depende de ancestral inexistente | Sim |
| V-13 | Dados incompatíveis com a estrutura declarada | Sim |
| V-14 | Coluna de tabela sem nível ou campo de origem | Sim |
| V-15 | Condição excepcional possível sem política explícita | Sim |

Ver achado QA-002 sobre V-05.

---

## 25. Diferenças terminológicas

**Resultado: CONFORME COM RESSALVA**

§34 registra dez diferenças materiais entre o contrato externo e o schema atual
do projeto (ADR-0027), cobrindo os tipos de nível, os nomes dos modos de
apresentação e os blocos de configuração. A ADR não renomeia, não declara
migração e não escolhe entre os nomes. Ver achado QA-003 sobre terminologia
não registrada entre `contrato_console.md` e a ADR.

---

## 26. Decisões adiadas

**Resultado: CONFORME**

§43 lista 15 itens adiados. Correspondência com o §43 do contrato externo:

| Item do contrato externo | Equivalente na ADR |
|---|---|
| 1 nomes das propriedades | §43 item 1 |
| 2 versão do schema | §43 item 2 |
| 3 valores padrão | §43 item 3 |
| 4 marcador de truncamento | §43 item 4 |
| 5 estilos obrigatórios | §43 item 5 |
| 6 limites de profundidade | §43 item 6 |
| 7 política de fallback | §43 item 7 |
| 8 integração com distribuição matricial | Não listado — fora de escopo (ver observação QA-005) |
| 9 estratégia de navegação entre páginas | §43 item 8 |
| 10 formato de mensagens de validação | §43 item 9 |

Os itens 10–15 da ADR cobrem a integração Pipeline, que não aparece no contrato
externo mas foi adicionada adequadamente.

Nenhum item declarado como adiado foi preenchido silenciosamente em outra seção.

---

## 27. Responsabilidades das camadas

**Resultado: CONFORME COM RESSALVA**

§35 divide responsabilidades entre ponto de entrada (35.1), loader (35.2),
modelo (35.3) e renderizador (35.4). A separação é compatível com ADR-0026
e ADR-0027.

Ver achado QA-001 sobre inconsistência terminológica entre D3 e §35.1.

---

## 28. Demonstração e testes futuros

**Resultado: CONFORME**

§36 exige, para cada um dos quatro cenários: tela estrutural identificável,
conteúdo JSON externo identificado, associação permanente, ponto de entrada real,
comando exato de abertura, identidade semântica verificável, possibilidade de
observar os dois modos na mesma tela.

§37 exige provas semânticas de: qual tela, qual JSON, qual apresentação, qual
modo inicial, que `V` alterou o modo, que segunda ativação restaurou, que dados
não mudaram, que não vazou para outra tela, que se recupera após
redimensionamento.

Código de saída zero não é prova suficiente (§37, destaque em negrito).

---

## 29. Validação manual em TTY real

**Resultado: CONFORME**

§38 exige explicitamente: fixtures permanentes, telas permanentes, ponto de
entrada real, comandos exatos de abertura, identidade semântica observável e
validação humana em TTY real.

---

## 30. Escopo negativo

**Resultado: CONFORME**

§42 lista explicitamente 33 itens fora de escopo, incluindo: conteúdo matricial,
dashboard, lancador, outros componentes, implementação, alteração de JSONs
existentes, criação de demonstrações, alteração da barra de menus, alteração de
código, navegação interativa, expansão e recolhimento, edição de dados,
persistência do modo além da sessão, integração concreta com Pipeline, commit,
QA e criação de handoff.

---

## 31. Documentos afetados

**Resultado: CONFORME COM RESSALVA**

§41 lista nove documentos/diretórios afetados, todos adequadamente justificados.
A lista não transforma a ADR em aplicação antecipada: todos os itens estão
corretamente projetados para etapa futura.

Ver achado QA-004 sobre `docs/contratos/contrato_barra_de_menus.md`.

---

## 32. Ausência de implementação antecipada

**Resultado: CONFORME**

O arquivo contém somente decisões normativas, regras, critérios e verificações
de integridade. Não há código, diff, fixture criada, JSON criado, declaração de
tarefa concluída ou referência a implementação já realizada neste ciclo.

---

## 33. Achados

### QA-001 — Inconsistência textual entre D3 e §35.1

| Campo | Valor |
|---|---|
| ID | QA-001 |
| Seções | D3 e §35.1 item 4 |
| Classificação | **Médio** |
| Impacto | Textual — leitores podem interpretar de formas opostas a mesma instrução |
| Exige decisão do usuário | Não |

**Evidência:**

D3, item 2:
> "entregar os dois documentos **conjuntamente** ao fluxo interno de
> carregamento, modelo e renderização."

§35.1, item 4:
> "entregar os dois documentos **separadamente** ao fluxo interno;"

"Conjuntamente" (juntos) e "separadamente" (apartados) são opostos diretos.
O intent é "entregar ambos ao fluxo enquanto os mantém distintos", que é a
formulação da ADR-0027 ("as duas entradas separadas ao fluxo"). Mas a ADR-0028
usa as duas palavras opostas em seções diferentes para a mesma ação.

**Regra afetada:** DU-03 (carregamento separado e entrega conjunta); ADR-0027 D2
e D8.

**Correção necessária:** Harmonizar a formulação de D3 e §35.1. Uma das formas
corretas: "entregar os dois documentos como entradas separadas ao fluxo"
(consistente com ADR-0027). A correção não exige nova decisão do usuário — a
intenção é clara da ADR-0027.

---

### QA-002 — V-05 com qualificador "obrigatório" ausente no contrato

| Campo | Valor |
|---|---|
| ID | QA-002 |
| Seção | §33, validação V-05 |
| Classificação | **Baixo** |
| Impacto | Potencial enfraquecimento da validação em relação ao contrato (R-013) |
| Exige decisão do usuário | Não |

**Evidência:**

V-05 na ADR:
> "Contêiner **obrigatório** sem nível filho declarado — INVÁLIDO"

R-013 no contrato externo:
> "Um nível do tipo contêiner DEVE declarar o nível de seus filhos."

R-013 torna inválido qualquer contêiner sem nível filho declarado, sem qualificar
como "obrigatório". A ADR adiciona o qualificador "obrigatório" que não aparece
no contrato, o que pode ser interpretado como "somente contêineres marcados como
obrigatórios precisam declarar filhos", enfraquecendo a validação.

**Regra afetada:** Contrato externo R-013.

**Correção necessária:** Reformular V-05 para "Contêiner sem nível filho
declarado — INVÁLIDO", alinhando com R-013. A correção não exige nova decisão
do usuário.

---

### QA-003 — Diferença "modo normal" vs "modo não verboso" não registrada em §34

| Campo | Valor |
|---|---|
| ID | QA-003 |
| Seção | §34 (diferenças terminológicas) |
| Classificação | **Baixo** |
| Impacto | Incompletude da tabela de diferenças terminológicas |
| Exige decisão do usuário | Não |

**Evidência:**

`contrato_console.md` §6 usa o termo "**modo normal**" (oposto de "modo
verboso") como padrão estabelecido do projeto:
> "**modo normal é o default** — instância sem declaração explícita de modo
> inicia em normal"

A ADR-0028 usa "**modo não verboso**" (§§21–22, D9) para o mesmo conceito.

A tabela em §34 registra diferenças entre o contrato externo e o schema ADR-0027,
mas não registra a diferença entre "modo normal" (estabelecido em
`contrato_console.md`) e "modo não verboso" (introduzido pela ADR-0028).

Esta diferença está dentro do escopo de §34, que se propõe a registrar
diferenças terminológicas para reconciliação futura.

**Regra afetada:** §34 (completude da tabela de diferenças terminológicas).

**Correção necessária:** Acrescentar à tabela de §34 a linha correspondente à
diferença entre "modo normal" (`contrato_console.md`) e "modo não verboso"
(ADR-0028). A correção não exige nova decisão do usuário.

---

### QA-004 — `contrato_barra_de_menus.md` ausente de §41 e do frontmatter

| Campo | Valor |
|---|---|
| ID | QA-004 |
| Seção | §41 (documentos afetados) e frontmatter (`contratos_afetados`) |
| Classificação | **Baixo** |
| Impacto | Potencial omissão de documento afetado pela semântica de `[V]` |
| Exige decisão do usuário | Não |

**Evidência:**

§23 define comportamento de `[V] Verboso` na barra de menus:
> "A barra de menus das demonstrações de dados do `console` deve apresentar:
> `[V] Verboso`"

`docs/contratos/contrato_barra_de_menus.md` existe no projeto e governa a barra
de menus. Ele não está listado em §41 nem no frontmatter `contratos_afetados`.

**Mitigação parcial:** `contrato_console.md` (que está em §41) já estabelece em
sua seção 14 que `[V]` existe quando a instância de `console` declara modo
verboso, o que cobre a semântica de existência do chip. Portanto, a omissão não
é necessariamente bloqueante — mas a aplicação documental futura deverá avaliar
se `contrato_barra_de_menus.md` precisa ser atualizado para refletir a semântica
da tecla `V` nas demonstrações de dados do `console`.

**Correção necessária:** Avaliar e, se aplicável, adicionar
`docs/contratos/contrato_barra_de_menus.md` à lista de §41 com nota de avaliação
("avaliar se chip `[V]` já está coberto pelo contrato_console.md"). A correção
não exige nova decisão do usuário.

---

### QA-005 — Item 8 do §43 do contrato externo implicitamente omitido

| Campo | Valor |
|---|---|
| ID | QA-005 |
| Seção | §43 da ADR |
| Classificação | **Observação** |
| Impacto | Omissão implícita coerente com o escopo, mas não explicitamente justificada |
| Exige decisão do usuário | Não |

**Evidência:**

O contrato externo (§43, item 8) adia deliberadamente:
> "a integração com o contrato de distribuição matricial"

A ADR-0028 não inclui esse item em seu §43, nem o menciona no §42 (escopo
negativo). A omissão é coerente com o escopo exclusivo de `console`/multinível,
mas não é declarada explicitamente.

**Nota:** §6 e §42 já excluem conteúdo matricial do escopo, o que implica que
a integração matricial não é pertinente a esta ADR. A omissão é logicamente
consistente.

**Correção sugerida:** Nenhuma obrigatória. A observação é registrada para
informação do auditor sobre a diferença entre os §43 do contrato e da ADR.

---

### QA-006 — Ambiguidade latente entre padrão do `contrato_console.md` e adiamento da ADR

| Campo | Valor |
|---|---|
| ID | QA-006 |
| Seção | §25 e D12 |
| Classificação | **Observação** |
| Impacto | Ambiguidade interpretativa sobre qual padrão se aplica quando `formato.excesso.modo` estiver ausente |
| Exige decisão do usuário | Não (para esta ADR) |

**Evidência:**

`contrato_console.md` §6 estabelece:
> "**modo normal é o default** — instância sem declaração explícita de modo
> inicia em normal"

ADR-0028 §25:
> "Se o campo estiver ausente do documento de conteúdo, o comportamento não
> está definido por esta ADR. A definição do valor padrão é adiada para a
> etapa de schema ou aplicação documental."

Os dois enunciados têm escopos ligeiramente diferentes: o `contrato_console.md`
fala do default do `console` como instância; a ADR fala do campo específico do
documento JSON externo de conteúdo. São camadas distintas. A aplicação documental
deverá reconciliar explicitamente qual padrão prevalece quando o campo estiver
ausente do documento externo. A ADR está correta em adiar, mas a ambiguidade
existe.

**Nota:** A ADR §25 já refere o adiamento ao §43 item 3, o que é correto.

**Correção sugerida:** Nenhuma obrigatória para esta ADR. A aplicação documental
deverá endereçar explicitamente a reconciliação.

---

## 34. Conclusão

A ADR-0028 (versão corrigida) apresenta:

- remoção completa e declarada da autoridade incorreta;
- adoção do contrato correto como autoridade normativa;
- ausência total de regras normativas matriciais;
- escopo rigorosamente limitado a `console` com conteúdo multinível;
- cobertura normativa completa das quatro apresentações;
- semântica corretamente definida para alternância verboso/não verboso;
- estado de visualização da sessão explicitamente separado da persistência;
- decisões adiadas não preenchidas;
- compatibilidade com ADR-0026 e ADR-0027 preservada;
- responsabilidades das camadas adequadamente separadas;
- validações conformes ao contrato externo com uma ressalva (V-05);
- demonstrações e testes futuros com critérios semânticos definidos.

O documento contém **um defeito documental corrigível** (QA-001): inconsistência
textual direta entre D3 ("conjuntamente") e §35.1 ("separadamente") para a mesma
ação de entrega dos documentos ao fluxo. A correção não exige nova decisão
arquitetural nem nova decisão do usuário — apenas harmonização da formulação com
a ADR-0027. Os demais achados (QA-002, QA-003, QA-004) são de baixa severidade
e também corrigíveis sem nova decisão.

---

## 35. Status literal

`ADR_REJECTED`

Motivação: defeito documental corrigível identificado (QA-001 — inconsistência
textual entre D3 e §35.1 sem necessidade de nova decisão do usuário).

---

## 36. Status normalizado

```yaml
status_literal: ADR_REJECTED
motivo_rejeicao: QA-001 — inconsistência textual entre D3 (conjuntamente) e §35.1 (separadamente) para a mesma ação de entrega dos documentos ao fluxo
bloqueio_decisao_usuario: false
bloqueio_arquitetural: false
defeito_corrigivel: true
```

---

## 37. Próxima categoria permitida

```yaml
proxima_categoria: PATCH_ADR
descricao: >
  Corrigir os defeitos documentais identificados nos achados QA-001, QA-002,
  QA-003 e QA-004. Após o patch, submeter novamente a QA_ADR antes de
  qualquer outra etapa.
restricoes:
  - alterar somente docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
  - nenhum outro arquivo pode ser alterado
  - nenhuma etapa subsequente (aplicação documental, handoff, implementação) pode ser iniciada antes de nova QA aprovada
```
