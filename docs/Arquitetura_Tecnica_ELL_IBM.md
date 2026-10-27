# ELL IBM — Documento de Arquitetura Técnica

**Versão:** 1.0  
**Status:** Consolidado a partir das decisões aprovadas  
**Escopo:** desenvolvimento local e validação do MVP  
**Idioma:** Português (Brasil)

## 1. Objetivo e convenções

Este documento consolida a arquitetura técnica do ELL IBM, distingue decisões aprovadas de detalhes pendentes e registra a ordem de implementação. Ele complementa o PRD: o PRD descreve produto e requisitos funcionais; este documento descreve a organização técnica.

- **Aprovado:** decisão explicitamente validada.
- **Pendente:** detalhe ainda não escolhido; nenhuma alternativa é presumida.
- **Fora do escopo atual:** item não decidido nem executado nesta etapa.

## 2. Resumo executivo

O ELL IBM será desenvolvido inicialmente como uma aplicação modular em um **monólito modular**, com backend centralizado. A stack aprovada é **FastAPI + Python**, **React + Vite + TypeScript**, **PostgreSQL** e **Docker Compose** para execução local. O **IBM watsonx Orchestrate** coordenará os agentes de IA.

O backend será autoridade para autenticação, autorização, integridade, persistência e regras determinísticas de negócio. Os agentes apoiam personalização, tutoria e avaliação, mas não podem alterar diretamente pontos, conquistas, desbloqueios ou estado persistente sem validação do backend.

Os fluxos textuais têm prioridade. O áudio não é prioridade de implementação neste momento. O painel administrativo completo permanece no escopo do produto, mas será desenvolvido depois da experiência principal. O trabalho atual limita-se a desenvolvimento local e validação; implantação e operação em produção ficam sob responsabilidade do usuário.

## 3. Princípios arquiteturais

1. Modularidade antes de microserviços; extrair serviços apenas se houver justificativa concreta.
2. Backend como autoridade sobre dados, permissões e regras de negócio.
3. Gamificação determinística: a IA não concede livremente pontos ou desbloqueios.
4. Orquestração de IA com contexto mínimo necessário e validação pelo backend.
5. Isolamento dos dados de cada usuário e privacidade por desenho.
6. Persistência para retomar a jornada após interrupções.
7. Feedback visual claro em operações demoradas, falhas e novas tentativas.
8. Execução local reproduzível com Docker Compose.
9. Não introduzir RAG, banco vetorial ou camadas extras de controle de consumo sem necessidade demonstrada.
10. Não definir hospedagem nem implantação produtiva nesta etapa.

## 4. Escopo e limites

### Incluído

- Jornada de aprendizagem com **doze trilhas** (Meu primeiro salário / Orçamento na prática / Pagamentos do dia a dia / Cartão e fatura / Metas e reserva / Guardar sem perder o controle / Juros e parcelas / Dívida que cresce / Inflação e poder de compra / Onde o dinheiro rende / Golpes e proteção de dados / Desafio integrador). Decisão revisada em D1; estrutura detalhada em `docs/CONTRATO_CURRICULAR_12_TRILHAS.md`.
- Conteúdo educacional estruturado.
- Catalisador, Mentor e Analista de Progresso, coordenados por watsonx Orchestrate.
- Perfil, respostas, avaliações, progresso, gamificação e histórico relevante de conversas.
- Autenticação e autorização para Usuário e Administrador.
- Painel administrativo completo, implementado após o sistema principal.
- Testes automatizados, validação dos fluxos críticos, documentação técnica e ambiente local.

### Fora do escopo desta etapa

- Provedor de hospedagem, implantação, operação ou escalabilidade em produção.
- Implementação prioritária de áudio.
- Banco vetorial, embeddings ou RAG como requisitos iniciais.
- Microserviços sem justificativa.
- Cotas, orçamentos ou limites artificiais de chamadas de IA.

**Nota sobre áudio:** o PRD contempla funcionalidades de áudio, mas a decisão arquitetural atual é priorizar texto e adiar o áudio. Isso não altera silenciosamente o PRD; uma mudança formal de escopo deve ser registrada nele.

## 5. Visão geral da arquitetura

```text
Frontend — React + Vite + TypeScript
  Áreas do estudante e, posteriormente, painel administrativo
                    │ API REST
                    ▼
Backend — FastAPI
  Autenticação/autorização | Perfil | Jornada | Conteúdo
  Gamificação/progresso | Avaliações | Conversas/contexto
  Regras de negócio | Validação | Integração de IA
          │                              │
          ▼                              ▼
     PostgreSQL                 IBM watsonx Orchestrate
                                Catalisador | Mentor
                                Analista de Progresso
```

O diagrama é lógico e não define topologia produtiva. A forma exata de integração FastAPI–Orchestrate permanece pendente.

## 6. Stack aprovada

| Camada | Tecnologia | Situação |
|---|---|---|
| Backend | Python + FastAPI | Aprovada |
| Frontend | React + Vite + TypeScript | Aprovada |
| Banco principal | PostgreSQL | Aprovada |
| Execução local | Docker Compose | Aprovada |
| Coordenação de agentes | IBM watsonx Orchestrate | Aprovada |
| Modelos de IA | Granite disponíveis no ambiente do usuário | Modelo específico pendente |
| Banco vetorial/RAG | Não adotar inicialmente | Reavaliar se necessário |
| Hospedagem produtiva | Não definida | Fora do escopo atual |

Bibliotecas específicas, gerenciadores de dependências, ferramentas de migração e cliente de integração ainda não foram escolhidos.

## 7. Organização do backend

O backend será um monólito modular FastAPI, com responsabilidades e interfaces claras.

1. **Autenticação e autorização:** cadastro, verificação de e-mail, login, recuperação de senha, sessão e papéis.
2. **Perfil do estudante:** dados necessários à personalização, preferências e configurações.
3. **Jornada de aprendizagem:** trilhas, atividades, objetivos, respostas, avaliações e retomada.
4. **Conteúdo educacional:** conteúdo estruturado, critérios de avaliação, revisão e publicação.
5. **Gamificação e progresso:** pontos, conquistas e desbloqueios com regras determinísticas.
6. **Avaliações e indicadores:** resultados e indicadores agregados.
7. **Conversas e contexto:** histórico relevante, associação a usuário/atividade e seleção de contexto.
8. **Orquestração de IA:** integração com Orchestrate, validação de respostas e tratamento de falhas.

A estrutura física de diretórios será definida durante a implementação. Regras críticas não devem ficar espalhadas pelo frontend nem depender exclusivamente de respostas da IA.

## 8. Frontend e experiência

O frontend será modular, responsivo e baseado em componentes reutilizáveis, com rotas protegidas, estado de sessão centralizado e camada de API separada dos componentes visuais.

### Áreas do estudante

- **Início:** resumo e próximos passos.
- **Minha jornada:** doze trilhas, atividades e desbloqueios.
- **Mentor e agentes:** interações com IA.
- **Conquistas e progresso:** pontos, conquistas, resultados e evolução.
- **Meu perfil:** perfil, preferências e configurações da conta.

### Áreas administrativas

- Visão geral.
- Gestão educacional.
- Avaliações e critérios.
- Usuários.
- Configurações administrativas.

O painel é parte do escopo completo, mas vem depois da experiência principal. Bibliotecas de roteamento, formulários, estado e componentes visuais permanecem pendentes.

### Feedback de interface

- Mostrar estados de processamento em chamadas de backend ou IA.
- Comunicar atrasos e falhas com mensagens compreensíveis.
- Permitir nova tentativa quando apropriado e preservar texto digitado sempre que possível.
- Exibir barra de progresso apenas quando o progresso for mensurável; não inventar percentuais ou etapas.
- Operações simples serão síncronas por padrão; usar execução assíncrona quando justificada.

## 9. Dados e PostgreSQL

PostgreSQL será o banco principal. O backend valida integridade e relações.

### Grupos lógicos de entidades

- Usuários, credenciais e papéis.
- Perfis e preferências.
- Trilhas, atividades, objetivos e conteúdo.
- Versões e estados de publicação.
- Respostas e avaliações.
- Progresso, pontos e conquistas.
- Conversas e interações com agentes.
- Indicadores agregados e eventos de auditoria administrativa.

Essa lista não é o esquema físico final. Tabelas, campos, chaves, cardinalidades, índices e migrações permanecem pendentes.

### Conteúdo e memória

O conteúdo educacional estruturado ficará no PostgreSQL. O backend selecionará o conteúdo pertinente e fornecerá a cada agente contexto compatível com sua função. O conteúdo publicado será a referência pedagógica, mas não garante por si só que toda resposta da IA será correta; são necessários testes com perguntas representativas, respostas inesperadas e lacunas de conteúdo.

O histórico relevante será persistido e associado ao usuário e, quando aplicável, à atividade/jornada. O backend monta o contexto necessário e impede acesso cruzado. Não haverá RAG, embeddings ou banco vetorial inicialmente. Retenção, exclusão e critérios de seleção do contexto ainda precisam ser definidos.

## 10. Autenticação, papéis e privacidade

Há exatamente dois papéis:

- **Usuário:** acessa apenas o próprio perfil, jornada, respostas, interações e progresso.
- **Administrador:** acessa funcionalidades administrativas autorizadas.

Ser administrador não implica acesso irrestrito a todos os dados pessoais. O backend deve aplicar autorização em operações protegidas.

### Cadastro e primeiro acesso

- Cadastro do usuário com e-mail e senha.
- Verificação de e-mail e recuperação de senha.
- Cadastro de administradores não público; concessão controlada.
- Após verificar e-mail e entrar, o usuário configura o perfil inicial com apenas os dados necessários à personalização.
- Depois, entra na experiência principal.
- O administrador é encaminhado ao painel após validação de permissões.

### Linha de base de segurança aprovada

- Hash seguro de senhas usando biblioteca estabelecida.
- Autorização no backend.
- Segredos e chaves fora do código-fonte e do controle de versão.
- Proteção de dados pessoais e histórico de aprendizagem.
- Logs sem senhas, tokens ou conteúdo sensível desnecessário.
- Testes de isolamento, inclusive tentativas de acesso a dados de outro usuário.

Bibliotecas, estratégia de sessão, expiração/revogação, serviço de e-mail, criação da primeira conta administrativa e critérios verificáveis de segurança permanecem pendentes.

## 11. Agentes e IBM watsonx Orchestrate

| Agente | Responsabilidade | Identidade visual aprovada |
|---|---|---|
| Catalisador | Personalização | Coral/laranja `#FF6B6B` → `#FCA048` |
| Mentor | Tutoria e apoio ao estudante | Azul/ciano `#2F80ED` → `#56CCF2` |
| Analista de Progresso | Avaliação e análise do progresso | Verde/mint `#11998E` → `#38EF7D` |

O Orchestrate coordena os agentes. O backend controla acesso ao contexto, valida respostas e persiste resultados. Agentes não alteram diretamente pontos, recompensas, desbloqueios ou estado persistente. O conteúdo educacional orienta cada agente de acordo com sua função.

A decisão de usar watsonx Orchestrate está aprovada; a integração técnica exata, autenticação entre sistemas, contratos de entrada/saída, timeouts, tratamento de falhas e seleção de modelos Granite específicos permanecem pendentes.

A IA será usada conforme necessidade funcional. Não haverá camada adicional de cotas, orçamento, limites de chamadas ou otimização artificial do consumo. Permanecem necessários o tratamento básico de indisponibilidade e os limites técnicos indispensáveis à estabilidade.

## 12. API REST

- Endpoints agrupados por módulo.
- Modelos tipados de entrada/saída e validação.
- Frontend desacoplado da implementação interna do backend.
- Documentação automática do FastAPI.
- Formato consistente de erros.
- Autenticação e autorização no backend.

Endpoints, campos, códigos HTTP, versionamento, paginação e formato definitivo dos erros serão especificados no desenho detalhado.

## 13. Fluxos críticos de referência

### Primeiro acesso

1. Usuário cria conta com e-mail e senha.
2. Sistema envia verificação de e-mail.
3. Após verificar, usuário entra.
4. Backend valida sessão e permissões.
5. Usuário completa o perfil inicial.
6. Sistema abre a experiência principal.

### Atividade com IA

1. Frontend envia resposta/solicitação pela API.
2. Backend valida sessão, autorização e contexto.
3. Backend recupera conteúdo e contexto relevantes.
4. Quando necessário, solicita apoio ao fluxo coordenado pelo Orchestrate.
5. Backend valida a resposta do agente.
6. Backend persiste interação e estado de aprendizagem aplicável.
7. Regras determinísticas calculam pontos, conquistas ou desbloqueios elegíveis.
8. Frontend apresenta resultado e progresso atualizado.

### Retomada

1. Recuperar progresso persistido.
2. Identificar próxima atividade ou estado retomável.
3. Recuperar histórico relevante conforme regras de contexto.
4. Continuar sem duplicar pontos ou recompensas por repetição/interrupção.

### Publicação administrativa

1. Administrador autorizado cria/edita conteúdo.
2. Conteúdo passa por revisão.
3. Administrador autorizado publica versão aprovada.
4. Backend registra a ação.
5. Jornada e agentes passam a usar o conteúdo publicado conforme as regras de disponibilização.

Esses fluxos são referências de alto nível; contratos e estados detalhados permanecem pendentes.

## 14. Continuidade e recuperação de erros

O sistema deve persistir respostas e progresso em pontos apropriados e permitir retomada. Deve evitar duplicidade de respostas, pontos e recompensas; usar novas tentativas quando seguras; preservar texto digitado sempre que possível; apresentar erros compreensíveis; registrar diagnósticos sem expor dados sensíveis; e tratar falhas/respostas inesperadas dos agentes.

Pontos exatos de salvamento, política de retry, timeouts, códigos de erro, idempotência técnica e tratamento de atividades incompletas serão definidos posteriormente.

## 15. Painel administrativo e governança

### Gestão e publicação

O painel inclui visão geral, gestão educacional, avaliações e critérios, usuários e configurações administrativas. O fluxo previsto permite criar/editar, revisar e publicar uma versão aprovada. O backend valida e persiste alterações; agentes e jornada usam o conteúdo publicado.

Versionamento, histórico de revisões, rollback, estados de conteúdo, permissões detalhadas e regras de aprovação ainda serão especificados.

### Auditoria

As principais ações administrativas registram o que ocorreu, quando, qual administrador executou, qual objeto foi afetado e o resultado. A auditoria deve respeitar privacidade e evitar conteúdo pessoal desnecessário. Formato, retenção, proteção e visualização dos eventos estão pendentes.

### Indicadores

Direção inicial aprovada: número de usuários, participação por fase, conclusão de atividades, evolução geral do progresso e resultados agregados de avaliações. Fórmulas, filtros, atualização e regras de acesso a dados individuais serão definidos posteriormente.

## 16. Segurança, observabilidade e testes

### Observabilidade mínima

Sem depender de plataforma externa paga, prever logs estruturados, erros e tempos de resposta do FastAPI, observabilidade da integração com Orchestrate, identificadores de requisição, mensagens amigáveis e monitoramento básico local. Ferramentas, campos, retenção e critérios de alerta permanecem pendentes.

### Testes aprovados

- Unitários para regras de negócio, gamificação, progresso e desbloqueios.
- Integração entre FastAPI e PostgreSQL.
- Autenticação/autorização e isolamento entre usuários.
- Componentes e fluxos críticos do frontend.
- Ponta a ponta para jornadas essenciais.
- Falhas de IA: indisponibilidade, erro e resposta inesperada.
- Validação integrada de segurança, módulos e fluxos críticos.

A validação será progressiva, priorizando caminhos críticos. Ferramentas e metas de cobertura ainda serão definidas.

## 17. Dependências e execução local

Frontend e backend terão dependências separadas, versões registradas para instalações reproduzíveis e configuração fora do código-fonte. Segredos não serão versionados. A execução local deverá funcionar com Docker Compose e evitar custos de hospedagem; serviços externos necessários e seus possíveis custos devem ser avaliados.

Pendências: gerenciadores de dependências/arquivos de lock, variáveis de ambiente, volumes, migrações, backup/restauração local, configuração dos containers e serviços externos (incluindo e-mail e IA). Não se define infraestrutura ou procedimento de produção.

## 18. Git e documentação

O código será mantido em Git; alterações serão validadas antes da integração; a automação de validação será mínima e sem dependência obrigatória de serviços pagos. Repositório, branches, revisão e CI ainda não foram definidos. Releases produtivos estão fora do escopo.

Documentação mínima: arquitetura e módulos, configuração/execução local, variáveis de ambiente, endpoints e contratos, execução dos testes e registro de decisões. Formato e ferramentas permanecem pendentes.

## 19. Ordem de implementação aprovada

### Etapa 1 — Base técnica

- Ambiente local e Docker Compose.
- FastAPI, React/Vite/TypeScript e PostgreSQL.
- Autenticação inicial.
- Estrutura modular e contratos iniciais.

### Etapa 2 — Sistema principal

- Jornada e conteúdo educacional.
- Integração dos três agentes via fluxo de orquestração.
- Gamificação e avaliações.
- Perfil, progresso persistente e continuidade.
- Prioridade aos fluxos textuais.

### Etapa 3 — Validação

- Testes unitários, integração e ponta a ponta.
- Segurança e isolamento entre usuários.
- Integração entre módulos.
- Falhas e respostas inesperadas dos agentes.
- Fluxos críticos do estudante.

A validação também ocorre progressivamente desde o início; esta etapa consolida a rodada integrada.

### Etapa 4 — Painel administrativo

- Gestão educacional e conteúdo.
- Revisão e publicação.
- Auditoria administrativa.
- Gestão de usuários.
- Indicadores administrativos.

A ordem define prioridade, não exclusão de funcionalidades.

## 20. Revisão de consistência

1. **Monólito modular e Orchestrate:** compatíveis; o monólito organiza o domínio de negócio e Orchestrate coordena agentes.
2. **IA e regras determinísticas:** compatíveis; backend mantém autoridade sobre persistência, pontos e desbloqueios.
3. **Conteúdo estruturado e RAG:** conteúdo no PostgreSQL e contexto selecionado pelo backend; RAG não é requisito inicial.
4. **Áudio:** PRD contempla áudio, mas a implementação está sem prioridade; registrar formalmente no PRD se o escopo mudar.
5. **Painel administrativo:** incluído no escopo completo, posterior ao sistema principal.
6. **Papéis e privacidade:** dois papéis; Administrador não tem acesso irrestrito automaticamente.
7. **Consumo de IA:** sem cotas artificiais, mantendo tratamento de falhas e limites técnicos necessários à estabilidade.
8. **Local e produção:** Docker Compose e validação local incluídos; produção excluída.
9. **Testes:** começam progressivamente e também são consolidados na etapa de validação.
10. **Modelo de dados:** entidades definidas em nível lógico, sem presumir esquema físico ainda não aprovado.

Não foi identificado conflito que impeça iniciar a implementação. As pendências de detalhamento podem ser fechadas nas etapas correspondentes, antes de depender delas.

## 21. Registro consolidado das decisões aprovadas

1. Monólito modular inicial.
2. FastAPI/Python; React/Vite/TypeScript.
3. PostgreSQL; sem banco vetorial inicial.
4. Autenticação própria com e-mail/senha, verificação e recuperação.
5. Docker Compose local; hospedagem produtiva não definida.
6. FastAPI como backend e watsonx Orchestrate como coordenador.
7. Dados estruturados/histórico no PostgreSQL; contexto de IA controlado pelo backend.
8. Áudio sem prioridade de implementação neste momento.
9. Síncrono por padrão, assíncrono quando justificado, feedback claro.
10. Linha de base de segurança, observabilidade e testes.
11. Frontend modular, responsivo, rotas protegidas e camada de API.
12. Testes unitários, integração, frontend, ponta a ponta e falhas de IA.
13. Git, validação antes de integrar e CI mínimo.
14. Documentação técnica concisa.
15. Escopo local e validação do MVP, sem produção.
16. Módulos de backend por responsabilidade.
17. API REST tipada, validada e documentada pelo FastAPI.
18. Dependências separadas, versões registradas e configuração fora do código.
19. Modelo lógico para usuários, conteúdo, respostas, avaliações, progresso e conversas.
20. Histórico relevante persistido; contexto montado pelo backend; sem RAG inicial.
21. Erros consistentes, recuperação apropriada e prevenção de duplicidade.
22. Sem cotas artificiais ou otimização artificial do consumo de IA.
23. Orchestrate coordena Mentor e Analista de Progresso; backend valida e aplica regras. Catalisador é lógica determinística no backend (D4).
24. Conteúdo estruturado orienta agentes e será testado.
25. Conteúdo educacional no PostgreSQL, fornecido por contexto.
26. Painel administrativo completo, desenvolvido depois do sistema principal.
27. Papéis Usuário e Administrador; autorização no backend.
28. Cadastro de usuário; concessão administrativa controlada.
29. Configuração inicial do perfil após verificação e login.
30. Persistência/retomada sem duplicar recompensas.
31. Cinco áreas do estudante: Início, Minha jornada, Mentor e agentes, Conquistas e progresso, Meu perfil.
32. Cinco áreas administrativas: Visão geral, Gestão educacional, Avaliações e critérios, Usuários, Configurações administrativas.
33. Revisão e publicação de conteúdo aprovado.
34. Auditoria das principais ações administrativas.
35. Indicadores agregados de usuários, participação, conclusão, evolução e avaliações.
36. Ordem de implementação: base técnica, sistema principal, validação e painel administrativo.

### D10 — Trilha personalizada como dado (23/10/2026)

**Status: implementada no MVP sem IA; sujeita a validação de produto/pedagógica.**

A sequência de fases deixa de ser exclusivamente fixa. O onboarding gera uma
trilha determinística a partir de objetivo, nível, contexto de vida e urgência;
a trilha é persistida em `profiles.trail` e o backend continua sendo a
autoridade sobre desbloqueios.

- A primeira fase da trilha começa disponível; as seguintes exigem todas as
  missões obrigatórias das fases anteriores da trilha.
- Dentro de cada fase, as missões obrigatórias continuam sequenciais.
- Pontos, conquistas e conclusão permanecem em `progress/service.py`.
- O estudante pode aceitar a trilha sugerida ou voltar à ordem padrão.
- Uma trilha vinda do futuro Catalisador IA só é persistida após validação de
  `phase_order` contra as fases ativas (`apply_generated_trail`).
- Esta decisão estende D4/D6 e não autoriza a IA a alterar estado diretamente.

O contrato e a ordem de integração estão em
`docs/AGENTES_INTEGRACAO_ORCHESTRATE.md`.

## 22. Pendências técnicas para detalhamento

### Autenticação e segurança

- Bibliotecas, sessão, expiração/revogação, provedor de e-mail, criação da primeira conta administrativa e critérios verificáveis.

### Integração de IA

> **Decisão confirmada (D7):** spike técnico obrigatório antes de iniciar a Etapa 2. Bloqueado por falta de acesso ao ambiente watsonx Orchestrate. A Etapa 1 pode iniciar em paralelo.

**Checklist do spike — a ser executado assim que o acesso ao Orchestrate estiver disponível:**
- [ ] Autenticar o backend FastAPI no watsonx Orchestrate.
- [ ] Enviar um prompt real em português e receber resposta de um modelo Granite.
- [ ] Medir latência de ponta a ponta (FastAPI → Orchestrate → Granite → FastAPI).
- [ ] Documentar o contrato de entrada/saída (formato do payload, campos obrigatórios, estrutura da resposta).
- [ ] Testar comportamento de timeout e falha (Orchestrate indisponível).
- [ ] Confirmar qual modelo Granite usar para o Mentor e para o Analista de Progresso.
- [ ] Estimar custo por chamada e projetar custo por sessão de usuário.
- [ ] Definir estratégia de fallback: se Orchestrate indisponível, apresentar conteúdo estático da missão.

Até a conclusão do spike, nenhuma decisão de implementação que dependa da integração com Orchestrate deve ser finalizada.

### Dados e conteúdo

- Esquema físico, migrações, retenção/exclusão, perfil inicial, seleção de contexto, versionamento, revisão, publicação e rollback.

### API e frontend

- Endpoints, campos, códigos HTTP, versionamento, bibliotecas, salvamento/retomada e operações assíncronas.

### Testes e execução local

- Ferramentas/metas de cobertura, padrão de logs, dependências, variáveis, volumes, migrações e backup/restauração local.

### Administração

- Permissões detalhadas, fórmulas de indicadores, escopo/retencão da auditoria e regras de publicação.

### Evolução futura

- Reavaliar áudio depois dos fluxos textuais; considerar RAG/busca semântica apenas se necessário; considerar extração de módulos se justificada; decidir hospedagem produtiva separadamente.

## 23. Critério de prontidão

A arquitetura de alto nível está consolidada e a implementação pode começar pela Etapa 1. As pendências podem ser detalhadas quando necessárias, mas decisões que afetem segurança, contratos, persistência ou integração devem ser fechadas antes que os componentes dependam delas.

Mudanças em decisões aprovadas devem ser registradas neste documento e, quando afetarem requisitos de produto, também no PRD.

**Fim do documento.**
