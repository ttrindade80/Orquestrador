# H-0061 — Infraestrutura de estilo em runtime

```yaml
handoff: H-0061
item: ITEM-0010
adr: ADR-0046
capacidade: infraestrutura de estilo em runtime
estado_normativo: ADR_APPLICATION_APPROVED
```

## 1. Objetivo e fronteira

Entregar as primitivas de runtime que permitem carregar e materializar o estilo
inicial, manter uma configuração candidata independente, comparar candidato e
baseline, persistir somente os quatro `preset_default` autorizados e publicar a
materialização global de forma controlada, sempre na ordem persistência →
publicação. A capacidade também deve promover a configuração persistida com
sucesso a nova baseline e manter candidato e baseline sincronizados depois da
aplicação.

H-0061 entrega infraestrutura reutilizável, não uma tela. H-0062 consumirá as
primitivas para seleção e edição interativa; H-0063 consumirá a materialização
local e a operação de aplicação para demonstração e confirmação. F4, a tela de
seleção, a política `dois_niveis_por_foco`, amostras, a demonstração integrada,
o pop-up e os fluxos visuais `ABORTADO`/`CONFIRMADO` não pertencem a este
handoff.

## 2. Estado atual comprovado

### 2.1 Carregamento e representação vigente

`config/estilo.json` é a configuração concreta global. O arquivo contém
`_meta`, os catálogos e `preset_default` de `borda`, `chip`,
`indicadores.selecionado` e `indicadores.incluido`, o par direto de
`indicadores.concluido`, além de `cor_inativo` e `cor_alerta`. Os quatro
`preset_default` atualmente são, respectivamente, `Borda Curva`, `Colchete`,
`Seta` e `Círculo`.

Em `tela/carregamento/estilo.py`, `carregar_estilo(caminho_base=None)` lê o
arquivo, valida JSON, seções, catálogos, defaults, tipos, campos obrigatórios e
comprimento `len(valor) == 1` dos caracteres. Resolve os presets ativos e
retorna um `EstiloResolvido`, `dataclass(frozen=True)`, com 20 campos planos:
sete de borda, cinco de chip, seis de indicadores e as duas cores semânticas.
Falhas levantam `EstiloErro` e não produzem materialização parcial. O
`caminho_base` permite carregar uma configuração em uma raiz controlada de
teste.

Os consumidores recebem o `EstiloResolvido` já resolvido; o módulo de
renderização não abre `config/estilo.json` em cada render. A fachada pública
`tela/loader.py` reexporta `EstiloResolvido`, `EstiloErro` e
`carregar_estilo`.

### 2.2 Testes diretamente relevantes

`tela/teste_loader.py` contém o caso positivo com a configuração real, verifica
os 20 campos materializados, a imutabilidade do objeto e os valores iniciais,
além da cobertura de erro do loader. A mesma unidade usa `_ESTILO_VALIDO` como
conteúdo controlado e diretórios temporários para ausência, JSON inválido,
defaults, catálogos, tipos, caracteres e cores. Há também testes de
`cor_inativo` e `cor_alerta`.

`tela/teste_navegacao.py` e `tela/teste_renderizador.py` aparecem como
consumidores/testes de regressão de `EstiloResolvido`; a suíte existente deve
continuar aceitando a materialização inicial e os objetos de estilo fornecidos
por seus chamadores.

### 2.3 Limitações atuais frente à ADR-0046

O módulo atual cobre somente leitura, validação e materialização inicial. Não
há, no código inspecionado, primitiva para snapshot completo da configuração,
candidato independente, comparação semântica, edição limitada aos quatro
defaults, persistência, publicação/substituição global, baseline pós-sucesso ou
materialização local sem publicação. Também não há cobertura do ciclo de vida
persistência → publicação nem de sua falha fechada.

## 3. Arquivos autorizados para `IMPLEMENTAR H-0061`

O executor pode alterar somente os caminhos abaixo:

| Tipo | Caminho autorizado | Finalidade |
|---|---|---|
| Runtime | `tela/carregamento/estilo.py` | Estender o carregamento/materialização e concentrar as primitivas de configuração, candidato, baseline, persistência e publicação, preservando `EstiloResolvido` e `carregar_estilo`. |
| Fachada pública | `tela/loader.py` | Reexportar somente as primitivas públicas que consumidores posteriores precisarem, se a implementação as tornar públicas. |
| Testes | `tela/teste_loader.py` | Acrescentar cobertura focal usando os helpers e temporários já existentes, sem mudar a configuração real. |
| Relatório | `docs/relatorios/IMP-0061-infraestrutura-estilo-runtime.md` | Registrar a execução futura conforme a seção 11. |

Não é necessária fixture persistente adicional: o conteúdo controlado de
`_ESTILO_VALIDO` e `tmp_path`/diretório temporário são suficientes para testar
persistência isolada. Se o executor concluir que uma fixture adicional é
indispensável, deve parar e solicitar a exceção operacional da seção 12 antes
de criar qualquer caminho.

Não autorizar alterações em renderizadores, demos, telas, contratos, ADRs,
nomenclatura, configuração real ou outros módulos de carregamento. A extensão
deve preservar os consumidores existentes por meio da representação
`EstiloResolvido` e das fachadas atuais.

## 4. Arquivos preservados

Devem permanecer inalterados durante a implementação:

```text
docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md
docs/contratos/contrato_estilo.md
docs/nomenclatura/01_NUCLEO_COMUM.md
docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
docs/nomenclatura/10_ESTILO.md
config/estilo.json
```

Também permanecem preservados todos os demais arquivos fora da lista da seção
3. `config/estilo.json` é entrada real e autoridade persistida; H-0061 não deve
alterar seus valores para preparar ou testar a capacidade.

## 5. Entradas, fixtures, temporários e saídas

### Entrada real

`config/estilo.json` deve ser lido como configuração concreta global na
materialização inicial. A infraestrutura pode receber uma raiz/caminho
controlado para testes, aproveitando a convenção existente de `caminho_base`.

### Fixtures

Usar somente uma cópia controlada da estrutura completa de estilo em
`tela/teste_loader.py` ou um documento criado sob o diretório temporário do
teste. A fixture deve conter todos os campos necessários à materialização e
não pode substituir silenciosamente a entrada real no caso positivo.

### Temporários

Se a persistência usar arquivo intermediário, ele deve ficar no mesmo diretório
do destino explícito, com nome temporário não conflitante, para que a
substituição do destino possa ser controlada. O intermediário deve ser fechado,
validado conforme aplicável e removido tanto após sucesso quanto após falha.
Não preservar evidência em `/tmp`; testes devem usar o diretório temporário
gerenciado pelo teste e limpá-lo ao final.

### Saídas

A única saída persistente real permitida é a atualização explícita de
`config/estilo.json` por uma operação de persistência chamada pelo fluxo
posterior. A operação deve preparar uma configuração completa, não editar
quatro linhas isoladas nem deixar um arquivo parcial. O destino só pode ser
substituído depois que a escrita completa tiver terminado sem erro; falha antes
da substituição deixa o arquivo anterior intacto.

Testes de persistência devem apontar para uma raiz temporária. É proibido
chamar a persistência contra a raiz real do repositório. Sobrescrita só ocorre
quando o caminho de destino é fornecido explicitamente à operação; não usar
varredura, glob ou remoção ampla.

## 6. Primitivas mínimas esperadas

Não são impostos nomes de funções, classes ou um novo módulo. A implementação
pode reorganizar internamente `tela/carregamento/estilo.py`, desde que ofereça
capacidades equivalentes às seguintes:

1. Obter ou criar um snapshot completo da configuração persistida, incluindo
   campos fora do escopo de edição, para servir de baseline.
2. Criar candidato independente derivado dessa baseline, sem compartilhar
   mutabilidade com ela.
3. Alterar no candidato somente estes caminhos:
   `borda.preset_default`, `chip.preset_default`,
   `indicadores.selecionado.preset_default` e
   `indicadores.incluido.preset_default`.
4. Comparar candidato e baseline semanticamente, sem depender da ordem textual
   ou da formatação JSON.
5. Validar e materializar um candidato completo em memória, sem persistir e
   sem publicar. A materialização deve manter a validação fechada vigente e
   produzir uma representação integral utilizável pelos consumidores.
6. Persistir uma configuração candidata completa no destino explícito,
   preservando integralmente todos os campos fora dos quatro caminhos.
7. Detectar e propagar falha de persistência sem sinalizar sucesso, sem
   publicar e sem descartar o candidato.
8. Publicar uma materialização somente depois de a persistência completa e
   válida retornar sucesso.
9. Substituir o estilo global vigente por uma única troca controlada de uma
   materialização integral e imutável; nenhum consumidor pode observar um
   objeto global parcialmente alterado.
10. Promover a configuração efetivamente persistida com sucesso a nova
    baseline somente depois da persistência e da publicação concluídas.
11. Sincronizar o candidato com essa nova baseline após sucesso, de modo que a
    comparação seguinte não apresente diferença espúria.
12. Produzir e transportar uma materialização local derivada do candidato para
    consumidores posteriores, sem registrá-la como global e sem alterar o
    objeto global vigente.

`EstiloResolvido` continua sendo representação materializada, não substituto
da configuração candidata completa. O candidato precisa conservar a estrutura
necessária para regravar o documento inteiro e preservar metadados, catálogos,
cores e demais campos que não podem ser editados no ITEM-0010.

## 7. Invariantes de aplicação

O caminho de sucesso deve ser observável como:

```text
candidato válido
→ configuração completa preparada
→ persistência completa e bem-sucedida
→ publicação/substituição global integral
→ nova baseline
→ candidato == baseline semanticamente
```

Preparar, comparar ou materializar um candidato nunca persiste nem publica.
Publicar nunca pode preceder a persistência. A publicação deve operar sobre uma
materialização integral já pronta e não sobre mutações campo a campo.

Falha de persistência deve manter simultaneamente a configuração persistida
anterior, a materialização global anterior e o candidato disponível. A tentativa
falha não pode transformar a configuração parcialmente escrita em baseline.
Uma falha de publicação, se puder ser reportada pela infraestrutura, também não
pode expor materialização global parcial nem promover a baseline; o erro deve
ser propagado para a integração posterior com o candidato ainda disponível.

## 8. Preservação integral da configuração

Os testes devem comparar a estrutura JSON carregada antes e depois da
persistência. A única diferença semântica permitida está exatamente nestes
quatro caminhos:

```text
borda.preset_default
chip.preset_default
indicadores.selecionado.preset_default
indicadores.incluido.preset_default
```

Devem permanecer iguais `_meta`, catálogos completos, presets não escolhidos,
`indicadores.concluido`, `indicadores.selecionado.off`, `cor_inativo`,
`cor_alerta` e qualquer outro campo presente na configuração de entrada. A
ordenação ou formatação textual do JSON não constitui diferença semântica.

## 9. Testes automatizados exigidos

Acrescentar testes reproduzíveis para:

- materialização inicial preservada a partir de `config/estilo.json`;
- criação de candidato independente;
- mutação do candidato sem mutar a baseline;
- materialização local sem publicação;
- comparação semântica candidato × baseline;
- persistência dos quatro campos permitidos;
- preservação de todos os demais campos e catálogos;
- publicação somente depois do sucesso da persistência;
- falha de persistência sem publicação, sem atualização da baseline e sem
  perda do candidato;
- substituição global integral, sem objeto parcialmente alterado;
- nova baseline após sucesso;
- candidato sincronizado após sucesso;
- ausência de regressão nos consumidores existentes e na imutabilidade de
  `EstiloResolvido`.

Comandos para o executor:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py
```

Os testes devem usar raiz temporária para qualquer escrita e não podem alterar
permanentemente `config/estilo.json`.

## 10. Demonstração técnica automatizável

H-0061 não exige validação visual TTY. A demonstração deve ser um teste ou
fixture executável que registre/asserta a sequência:

```text
baseline A
→ candidato B
→ materialização B sem publicação
→ global continua A
→ persistência bem-sucedida
→ publicação
→ global passa integralmente a B
→ baseline passa a B
→ candidato passa a B
```

O mesmo teste deve injetar uma falha controlada antes da conclusão da
persistência:

```text
baseline A
→ candidato B
→ falha de persistência
→ global continua A
→ baseline continua A
→ candidato B continua disponível
```

As observações devem ser feitas por objetos/configurações retornados pela
infraestrutura e por leitura do destino temporário, nunca por alteração ou
leitura ambígua do arquivo real de produção.

## 11. Critérios de aceite

1. O carregamento inicial continua retornando materialização integral válida e
   preserva os consumidores e testes existentes.
2. A baseline é um snapshot completo e o candidato é independente dela.
3. Somente os quatro `preset_default` autorizados podem ser editados pelo
   caminho do ITEM-0010.
4. Candidato pode ser validado/materializado e transportado localmente sem
   persistência e sem publicação.
5. A comparação candidato × baseline é semântica e considera a configuração
   completa.
6. A persistência escreve configuração completa, preserva todos os demais
   campos e só retorna sucesso depois da gravação controlada do destino.
7. A publicação ocorre somente após sucesso de persistência e substitui o
   objeto global por uma materialização integral, sem mutação observável por
   campos.
8. Falha de persistência deixa intactos o arquivo anterior, o global anterior
   e a baseline anterior, mantendo o candidato disponível.
9. Após sucesso completo, a configuração persistida vira a nova baseline e o
   candidato fica semanticamente igual a ela.
10. Os testes automatizados e a demonstração técnica das seções 9 e 10 passam
    em raízes isoladas, sem alterar `config/estilo.json`.
11. Nenhum código de F4, tela de seleção, amostras, demonstração integrada,
    pop-up ou fluxo E2E é criado neste handoff.

Código de saída zero isoladamente não constitui aceite; cada comportamento
acima deve estar coberto por assertivas reproduzíveis.

## 12. Relatório esperado da implementação

Criar exatamente:

```text
docs/relatorios/IMP-0061-infraestrutura-estilo-runtime.md
```

O relatório deve registrar somente:

- arquivos criados/alterados;
- comportamento entregue;
- testes;
- demonstração;
- desvios/exceções;
- bloqueios.

Não reproduzir este handoff nem a ADR.

## 13. Exceção operacional focal

Antes de alterar qualquer arquivo fora da seção 3, o executor deve parar e
solicitar autorização usando exatamente:

```yaml
caminho:
motivo:
escopo:
mudanca_esperada:
```

Sem autorização, o arquivo externo não pode ser lido para orientar a
implementação nem ser modificado.

## 14. Bloqueios

Nenhum bloqueio material conhecido para a implementação isolada. As decisões
normativas necessárias estão na ADR-0046 e no contrato de estilo; detalhes de
nomes e organização física permanecem deliberadamente reversíveis. Qualquer
necessidade de ampliar arquivos autorizados deve seguir a exceção operacional
da seção 13, sem criar decisão normativa nova.
