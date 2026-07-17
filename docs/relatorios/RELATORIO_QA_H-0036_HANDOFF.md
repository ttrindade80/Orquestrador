# Relatório de QA do H-0036

## 1. Identificação

```yaml
etapa_executada: QA_HANDOFF
handoff: H-0036
arquivo_auditado: docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
data: "2026-07-17"
papel: auditor independente de handoff
```

## 2. Escopo da auditoria

Esta auditoria verificou se o H-0036 é fiel à ADR-0026, exequível sem nova decisão arquitetural, nominal quanto a arquivos, suficiente para implementação/testes/demo/QA e compatível com H-0035/ADR-0025.

Nenhuma correção foi feita no handoff. Nenhuma ADR, contrato, código, teste, fixture ou configuração foi alterado. Este relatório é o único arquivo criado nesta etapa.

## 3. Autoridades e evidências examinadas

Foram examinados:

```text
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_ADR-0026.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

Também foram consultados os arquivos técnicos e testes citados nominalmente pelo H-0036 para confirmação de existência e função: `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`, `tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_renderizador.py`, `tela/teste_distribuicao_matricial.py`, `demo/teste_demo.py`, `demo/teste_diagnostico.py`, `demo/teste_demo_distribuicao.py`, `demo/teste_explorar_barra_de_menus.py` e telas permanentes existentes em `config/telas/demo/`.

## 4. Estado Git

Comandos executados antes da criação deste relatório:

```bash
git status --short
git diff --check
git ls-files --others --exclude-standard
git branch --show-current
git rev-parse --short HEAD
```

Estado verificado:

```yaml
branch: master
head: fb9e5be
stage: vazio
commit_novo: nao_realizado
diff_check: sem_erros
modificados_acumulados_adr_0026:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
nao_rastreados_acumulados_adr_0026:
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
handoff_em_auditoria:
  - docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
arquivos_inesperados_antes_deste_relatorio: []
```

Após este relatório, o único arquivo novo esperado desta etapa é:

```text
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
```

## 5. Fidelidade à ADR-0026

O H-0036 preserva corretamente o princípio conceitual da ADR-0026: conteúdo de runtime do console vem de JSON externo, o envelope conceitual mínimo é `{tipo, formato, dados}`, o foco inicial é `tipo: "multinivel"` e o renderizador continua responsável por representação física calculada.

Entretanto, o handoff deixa de ser fiel às decisões deferidas quando transforma pontos não decididos em trabalho implementável: carregamento por caminho de arquivo, fixture em caminho fixo, demo com carregamento direto de documento externo, estabelecimento de primeira convenção de diretório e schema interno de `dados[]` a ser escolhido pela implementação.

## 6. Decisão de vínculo e mecanismo utilizado

Localização no handoff:

```yaml
autoridade_normativa_usada: H-0036 §8 e §25 citam ADR-0026, contrato_console §19.1 e contrato_json_console §11.2
mecanismo_documentado: loader recebe caminho de arquivo; demo script carrega diretamente a fixture
ponto_de_entrada: demo/demo_console_multinivel.py
camada_responsavel: loader/modelo/renderizador/demo
forma_de_entrega_ao_console: arquivo JSON em config/conteudo/h0036_console_multinivel.json carregado pelo demo/loader
```

Confirmação nos contratos:

- `contrato_tela_json.md` §31.2 define apenas o envelope conceitual e afirma que ele não define mecanismo de vínculo.
- `contrato_tela_json.md` §31.3 deixa não decididos nome de campo, formato, caminho, identificador lógico ou outro mecanismo.
- `contrato_console.md` §19.5 deixa não decididos assinatura, argumentos, transporte e ciclo de vida do produtor.
- `contrato_console.md` §19.7 mantém deferidos vínculo, protocolo e comportamento diante de fonte ausente ou inválida.
- `contrato_json_console.md` §11.2 declara que o envelope não substitui contrato, schema, validações nem mecanismo de integração.
- `contrato_json_console.md` §11.8 deixa deferidos vínculo, schema completo, validações, comportamento de erro e APIs/classes/módulos do consumidor.
- `NOMENCLATURA.md` §17.5 deixa não decididos caminho, localização e ciclo de vida do documento externo.

Conclusão: a decisão de vínculo e o mecanismo de entrega não estão confirmados por autoridade normativa ativa. O H-0036 inventa mecanismo suficiente para implementar, o que bloqueia o handoff.

## 7. Separação dos escopos

O H-0036 distingue corretamente a etapa `CRIAR_HANDOFF` da futura implementação em §11.2. A restrição de criação do autor não foi copiada como limitação geral da implementação.

O problema não está na separação autor/implementador, mas na autorização da implementação futura para decidir ou executar mecanismos ainda deferidos.

## 8. Arquivos autorizados para a futura implementação

A lista do H-0036 §12 é nominal e cita arquivos existentes reais:

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
demo/teste_diagnostico.py
```

Também autoriza novos arquivos:

```text
config/telas/demo/h0036_console_com_conteudo.json
config/conteudo/h0036_console_multinivel.json
demo/demo_console_multinivel.py
demo/teste_demo_console_multinivel.py
docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md
```

Os caminhos são nominais, mas não estão todos autorizados normativamente: `config/conteudo/` e o arquivo fixo da fixture estabelecem localização/convenção nova para documento externo, tema explicitamente deferido por `NOMENCLATURA.md` §17.5 e ADR-0026 §14.

Além disso, a lista não resolve como o documento externo será associado ao elemento `console` sem inventar API, classe, campo ou protocolo, também deferidos nos contratos.

## 9. Arquivos preservados ou proibidos

O H-0036 preserva nominalmente ADR-0026, relatórios da ADR-0026, contratos ativos, ADR-0025, H-0035, relatório de implementação H-0035, arquivos históricos e arquivos não relacionados. Também proíbe script produtor final, `tipo: "matriz"`, navegação multinível, expansão/recolhimento, paginação interativa, cache e atualização automática.

Não foi encontrada contradição simples do tipo "mesmo arquivo autorizado e proibido". A contradição material é de autoridade: arquivos novos autorizados dependem de decisão ainda deferida.

## 10. Capacidade coesa e escopo negativo

O H-0036 pretende uma capacidade coesa: consumo pelo console de conteúdo externo JSON estruturado como multinível.

O escopo negativo está bem enumerado quanto a produtor final, subprocesso, `tipo: "matriz"`, cache, atualização automática, navegação, expansão/recolhimento e paginação interativa. Porém, o próprio escopo positivo exige carregamento por caminho de arquivo, demo com carregamento direto da fixture e definição prática de schema interno, excedendo as decisões ativas.

## 11. Estrutura e validação do documento externo

O H-0036 preserva o envelope:

```json
{
  "tipo": "multinivel",
  "formato": {},
  "dados": []
}
```

Também preserva a proibição de resultados físicos calculados no documento externo.

Defeito material: o handoff exige validações e provas de níveis, hierarquia, identificadores, campos obrigatórios e filhos incompatíveis, mas reconhece em §14.1, §15.2 e §25 que o schema interno de `dados[]` não está decidido e será estabelecido pela implementação ou por exceção operacional. Isso deixa uma semântica material para o executor.

## 12. Fixture permanente

O H-0036 autoriza nominalmente a fixture `config/conteudo/h0036_console_multinivel.json` e exige `tipo: "multinivel"`, níveis, identificadores únicos, texto reconhecível, ausência de geometria e identificador exclusivo com `"H-0036"`.

O arquivo ainda não existe e sua criação é nominal. Porém, o caminho e a nova convenção `config/conteudo/` não estão autorizados por autoridade ativa. O próprio H-0036 §12.2 declara que a criação desse diretório estabelece "a primeira convenção de localização de documentos externos de conteúdo".

## 13. Demonstração real e smoke test

O H-0036 define:

```text
ponto de entrada: demo/demo_console_multinivel.py
comando: python demo/demo_console_multinivel.py
tela: config/telas/demo/h0036_console_com_conteudo.json
fixture: config/conteudo/h0036_console_multinivel.json
```

Também exige identidade semântica presente, placeholder ausente, maximização, restauração e redimensionamentos.

Esses critérios são materialmente observáveis, mas a demonstração depende do mecanismo não autorizado de carregamento direto da fixture pelo demo e de uma localização fixa para o documento externo. O smoke test, portanto, não está confirmado como exequível sem nova decisão documental.

## 14. Testes focais, integrados e suíte canônica

O H-0036 lista comandos exatos para a suíte canônica:

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_explorar_barra_de_menus.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console_multinivel.py
```

Os oito scripts históricos existem no repositório. O nono script é autorizado como novo arquivo. A suíte canônica está nominalmente definida.

Não foram executados testes nesta etapa, pois o escopo era auditoria documental do handoff e a implementação não existe.

## 15. Validação manual

O H-0036 reconhece corretamente que a mudança visual exige validação manual em TTY real. O roteiro informa demo, termos, redimensionamentos, quadro mínimo e recuperação, e impede aprovação visual pelo executor/QA em nome do usuário.

A validação manual está bem especificada, mas não corrige o bloqueio documental do mecanismo de entrega.

## 16. Relatório de implementação esperado

O H-0036 autoriza nominalmente:

```text
docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md
```

O conteúdo mínimo exigido é suficiente em termos de rastreabilidade factual: arquivos, mecanismo, fixtures, testes, demo, smoke, preservações, exceções e validação manual. O problema é que o mecanismo a registrar não possui autorização normativa ativa.

## 17. Exceção operacional

O H-0036 §22 contém regra de parada para arquivo fora da lista nominal, exigindo arquivo, motivo, escopo, mudança esperada, autorização explícita, registro e auditoria.

Defeito: a exceção é usada para cobrir decisões materiais já previsíveis, como criação de `config/conteudo/` e schema interno de `dados[]`. A própria cláusula diz que a autorização não permite criar nova semântica, arquitetura ou política. Portanto, ela não pode suprir decisões normativas ativas que a ADR-0026 e os contratos deixaram deferidas.

## 18. Critérios de aceite

Os critérios são observáveis em parte: envelope carregado, placeholder preservado/ausente, identidade semântica, suíte canônica e ausência de `tipo: "matriz"` ou script produtor final.

Não são plenamente independentes nem exequíveis enquanto:

- a forma de entrega ao console não estiver decidida;
- o caminho/localização do documento externo não estiver decidido;
- o schema interno de `dados[]` e suas validações não estiverem decididos.

## 19. Coerência e exequibilidade

O H-0036 é internamente organizado, mas sua seção §25 conclui "OK" para itens que os contratos deixam em aberto. Em especial, trata o envelope mínimo como se fosse forma suficiente de entregar o documento ao console. Essa inferência não é autorizada pelas autoridades ativas.

Classificação de exequibilidade: bloqueada documentalmente.

## 20. Ausência de implementação antecipada

Não foram encontrados patches, diffs ou código implementado no handoff. O documento não declara execução de testes da futura implementação nem aprovação própria.

Há, contudo, especificação antecipada de mecanismo de arquivo, caminho fixo, diretório de fixture e schema a ser estabelecido pela implementação. Isso não é implementação antecipada de código, mas é decisão arquitetural/documental antecipada sem autoridade.

## 21. Achados

### QAH-0036-001

```yaml
id: QAH-0036-001
severidade: bloqueante
arquivo: docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
secao_ou_trecho: §§10, 11.1, 14.1, 16.2, 25
autoridade_ou_regra_afetada: ADR-0026 §14; contrato_tela_json.md §§31.2-31.3; contrato_console.md §§19.5, 19.7; contrato_json_console.md §§11.2, 11.6, 11.8; regra crítica de decisão de vínculo do QA_HANDOFF
evidencia: |
  O handoff define carregamento de documento externo "a partir de caminho de
  arquivo", função de loader que recebe caminho, demo script que carrega
  diretamente a fixture e ponto de entrada que entrega esse conteúdo ao console.
  As autoridades ativas definem apenas envelope conceitual e deixam não
  decididos vínculo, caminho, identificador, mecanismo, transporte, ciclo de vida
  e APIs/classes/módulos do consumidor.
impacto: |
  A implementação exigiria escolher uma forma concreta de entrega ao console
  sem autoridade normativa ativa. O handoff deixa de ser implementável sem nova
  decisão arquitetural/documental.
correcao_necessaria: |
  Produzir decisão normativa ativa suficiente para a forma de entrega do
  documento externo ao console, ou reescrever o handoff sem inventar mecanismo.
```

### QAH-0036-002

```yaml
id: QAH-0036-002
severidade: bloqueante
arquivo: docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
secao_ou_trecho: §§12.2, 15.1, 16.1, 16.2, 22
autoridade_ou_regra_afetada: ADR-0026 §§12, 14; NOMENCLATURA.md §17.5; contrato_tela_json.md §31.3
evidencia: |
  O handoff autoriza `config/conteudo/h0036_console_multinivel.json` e registra
  que `config/conteudo/` "estabelece a primeira convenção de localização de
  documentos externos de conteúdo". A NOMENCLATURA §17.5 declara caminho,
  localização e ciclo de vida do documento externo como não decididos.
impacto: |
  O handoff escolhe caminho convencional e nome fixo para fonte externa sem
  autoridade ativa. A exceção operacional não pode criar nova convenção
  arquitetural, pois ela mesma proíbe nova semântica, arquitetura ou política.
correcao_necessaria: |
  Decidir documentalmente localização/ciclo de vida/convenção de fixture, ou
  remover essa escolha do handoff até haver autoridade ativa.
```

### QAH-0036-003

```yaml
id: QAH-0036-003
severidade: bloqueante
arquivo: docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
secao_ou_trecho: §§14.1, 15.2, 17.1-17.5, 20, 22, 25
autoridade_ou_regra_afetada: contrato_json_console.md §§11.2, 11.8; contrato_console.md §19.3; regra de validação estrutural do QA_HANDOFF
evidencia: |
  O handoff exige níveis declarados, três níveis hierárquicos, identificadores
  únicos, hierarquia, filhos incompatíveis, campos obrigatórios e testes de
  inválidos, mas afirma que a validação interna de `dados[]` e o schema interno
  serão definidos pela implementação ou por exceção operacional. O contrato
  ativo declara schema completo e validações como decisões deferidas.
impacto: |
  Os testes, fixture, renderização e critérios de aceite dependem de semântica
  material não decidida. O executor teria que inventar schema ou pedir decisão
  ad hoc, impedindo implementação completa e auditável a partir do handoff.
correcao_necessaria: |
  Documentar o schema/validações mínimos de `dados[]` em autoridade normativa
  ativa, ou limitar o handoff estritamente ao envelope sem exigir validações e
  provas que dependem do schema completo.
```

## 22. Observações

```yaml
observacoes:
  - id: OBS-QAH-0036-001
    descricao: O checkout real tem raiz Git no diretório atual; os caminhos ativos do repositório usam docs/, tela/, demo/ e config/, não scripts/docs/.
  - id: OBS-QAH-0036-002
    descricao: A suíte canônica de oito scripts do H-0035 foi preservada nominalmente, e o H-0036 adiciona nominalmente um nono script futuro.
```

## 23. Classificação final

```yaml
status_literal: H3_BLOCKED_DOCUMENTATION
status_normalizado: Bloqueado por falta de decisão documental ativa para mecanismo de entrega, localização da fonte externa e schema/validações de dados multinível
relatorio: docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
achados_bloqueantes: 3
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
decisao_de_vinculo_confirmada: false
mecanismo_documentado_confirmado: false
arquivos_autorizados_confirmados: false
fixture_confirmada: false
demonstracao_confirmada: false
suite_canonica_confirmada: true
validacao_manual: obrigatoria_definida_nao_executada_nesta_auditoria
arquivos_inesperados: []
git:
  branch: master
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  diff_check: sem_erros
  arquivo_criado_nesta_etapa: docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
proxima_categoria: FLUXO_DOCUMENTAL
```
