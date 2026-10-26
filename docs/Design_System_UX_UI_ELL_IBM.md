ELL IBM
# Documento 3 — Design System e UX/UI
Versão consolidada • Aprovação explícita registrada

## 1. Objetivo e status
Este documento consolida as diretrizes visuais, os padrões de interação e os princípios de experiência do ELL IBM. O usuário aprovou explicitamente todas as propostas registradas, incluindo os ajustes da revisão final. As diretrizes orientam o design e a implementação; não significam que todos os recursos avançados precisam estar implementados na primeira versão do MVP.
Escopo: experiência do estudante e administrativa, identidade dos agentes de IA, componentes compartilhados, acessibilidade, responsividade, aprendizagem, gamificação, configurações e privacidade.

## 2. Princípios de experiência
- Clareza educacional acima do efeito visual: a expressividade apoia a compreensão e não compete com instruções, conteúdo ou resultados.
- Identidade consistente e adaptação contextual: componentes, tipografia, cores e padrões de interação são compartilhados; a composição varia conforme área, dispositivo e tarefa.
- Aprendizagem no ritmo do estudante: não haverá prazos obrigatórios para atividades como padrão, nem contagens regressivas ou alertas de vencimento. Regras institucionais específicas só se aplicam quando definidas separadamente.
- Feedback útil: mensagens explicam o que ocorreu e orientam o próximo passo, inclusive em erros, resultados e recuperação.
- Acessibilidade incorporada: contraste, legibilidade, teclado, leitores de tela, foco visível, alternativas a interações visuais e respeito à preferência por movimento reduzido.
- Personalização controlada: tema claro/escuro e intensidade das animações podem ser ajustados sem romper a identidade visual.
- Implementação progressiva: recursos avançados podem ser planejados para fases posteriores, conforme validação e capacidade do MVP.

## 3. Identidade visual

### 3.1 Direção criativa
Digital vibrante e imersivo: cores expressivas, gradientes, cartões interativos e microanimações, mantendo clareza e foco educacional. A base será profissional e limpa; efeitos marcantes ficam reservados a agentes, conquistas e momentos importantes.

### 3.2 Paleta global

### 3.3 Identidade cromática dos agentes

### 3.4 Tipografia
- Space Grotesk: títulos e cabeçalhos da plataforma.
- Inter: corpo de texto e interface geral.
- IBM Plex Sans: textos e mensagens dos agentes.
- IBM Plex Mono: dados técnicos ou elementos monoespaçados quando aplicável.

### 3.5 Temas e preferências visuais
- Disponibilizar tema claro e escuro. O tema escuro usa #17152B como base; o claro utiliza superfícies luminosas e limpas, preservando a paleta.
- Na primeira utilização, seguir a preferência do sistema operacional. Se a pessoa selecionar manualmente um tema, persistir essa preferência.
- Oferecer personalização visual moderada: tema claro/escuro e intensidade das animações. Manter a paleta da marca e as identidades cromáticas dos agentes.
- Agrupar opções simples de acessibilidade visual nas configurações gerais, incluindo tema e redução de animações; isso não substitui os requisitos gerais de acessibilidade.

## 4. Sistema de componentes e linguagem visual
- Base híbrida: componentes limpos e profissionais com cartões vibrantes e efeitos especiais reservados a agentes, conquistas e momentos significativos.
- Ícones lineares para navegação e ferramentas; ícones expressivos para conquistas e gamificação.
- Ilustrações híbridas: vetores em orientação e conteúdo educacional; elementos 3D ou expressivos em boas-vindas, conquistas e momentos especiais.
- Densidade visual equilibrada, evitando sobrecarga e falta de contexto.
- Linguagem textual consistente: hierarquia tipográfica clara, textos concisos na interface e mensagens conversacionais dos agentes, com expressividade adequada.
- Formulários adaptativos: campos diretos para tarefas simples, etapas para processos longos e entrada conversacional quando útil.
- Dados administrativos orientados à tarefa: tabelas para operações detalhadas, listas/cartões para consultas rápidas e indicadores para resumos.
- Gráficos adaptados à tarefa: indicadores simples no cotidiano, gráficos detalhados para análise e pistas acessíveis que não dependem apenas de cor.
- Consistência entre áreas, adaptando a composição ao contexto; o painel administrativo prioriza clareza e eficiência.

## 5. Navegação e responsividade
- Desktop: barra lateral fixa. Celular: navegação inferior. Tablet: navegação e composição adaptadas ao espaço.
- Estratégia mobile-first, com layouts flexíveis e reorganização contextual dos componentes.
- Simplificar ou reorganizar elementos em telas menores quando necessário, preservando funções essenciais, legibilidade e acessibilidade.
- Atalhos e ações rápidas contextuais e adaptáveis, sem criar inconsistências entre áreas.

## 6. Experiência do estudante

### 6.1 Áreas principais
- Início.
- Minha jornada.
- Mentor e agentes.
- Conquistas e progresso.
- Meu perfil.

### 6.2 Página inicial e jornada
- Página inicial híbrida e personalizada, priorizando próxima ação recomendada, progresso, acesso aos agentes e conquistas recentes.
- Jornada híbrida: trilha visual para o progresso geral; cartões e listas para módulos e atividades.
- Objetivos de aprendizagem, indicadores de progresso e materiais complementares adaptam a apresentação ao contexto e à complexidade.
- Permitir retomar atividades interrompidas e salvar conteúdo para depois, com orientação clara sobre estado e próximo passo.
- Notas pessoais integradas à experiência de aprendizagem de modo contextual.
- Busca e descoberta combinam pesquisa textual, filtros/categorias e recomendações contextuais.

### 6.3 Atividades, exercícios e avaliações
- Distinção adaptativa: componentes consistentes, com rótulos, instruções e indicadores ajustados ao tipo de atividade.
- Explicar regras de avaliação sem separação visual excessiva entre prática e avaliação.
- Oferecer revisão de respostas antes do envio quando pertinente.
- Adaptar feedback durante exercícios e nos resultados; explicar o ocorrido e orientar o próximo passo.
- Ao concluir atividade ou módulo, apresentar confirmação, resumo e próximo passo; usar celebrações para marcos relevantes.
- Indicadores orientam, não pressionam. Não usar prazos obrigatórios, contagens regressivas ou alertas de vencimento como padrão.

### 6.4 Agentes de IA
- Usar mascotes/personagens como direção visual conceitual; as artes finais ainda devem ser projetadas e validadas.
- Evolução visual por progresso, combinando níveis predefinidos com recompensas especiais por conquistas.
- Interação híbrida e adaptativa: chat aberto, sugestões de ação, cartões e etapas guiadas conforme agente e tarefa.
- Histórico por agente e visão unificada das conversas recentes.
- Animações e reações expressivas contextuais, respeitando acessibilidade e preferência por movimento reduzido.
- Texto como experiência inicial padrão. A identidade pode acomodar expansão futura para áudio/voz, sem pressupor implementação no MVP.

### 6.5 Gamificação, conquistas e compartilhamento
- Indicadores cotidianos claros e celebrações expressivas para marcos significativos.
- Competição equilibrada e opcional: progresso individual como padrão e rankings opcionais por turma/grupo.
- Compartilhamento controlado e opcional de conquistas.
- Estados de sucesso, erro e progresso com sinais acessíveis que não dependem apenas de cor.

### 6.6 Onboarding, estados vazios, carregamento e erros
- Onboarding híbrido e personalizado: boas-vindas, configuração breve, introdução contextual e ajuda dos agentes.
- Estados vazios contextualizados com explicação, ilustração quando útil e ação recomendada.
- Carregamento adaptativo: skeletons, indicadores ou animações contextuais, respeitando redução de movimento.
- Erros e recuperação em linguagem simples, com caminhos de ação/tentativa novamente e preservação da entrada sempre que possível.
- Confirmações proporcionais ao risco, explicando consequências e oferecendo desfazer quando possível; ações rotineiras permanecem simples.
- Ajuda híbrida e contextual, combinando central de ajuda, dicas e suporte conversacional.

## 7. Notificações, perfil e privacidade
- Notificações adaptativas com central interna, preferências e lembretes contextuais.
- Frequência de lembretes adaptativa e controlável; não criar pressão por prazos de aprendizagem inexistentes.
- Perfil híbrido e evolutivo: avatar personalizável, informações essenciais, conquistas, progresso e controles de privacidade.
- Configurações adaptativas, com opções simples e agrupamentos claros.
- Controles de privacidade centralizados e contextuais, explicando visibilidade, uso dos dados e efeitos das escolhas.
- Rodapé minimalista, contendo apenas informações institucionais e links essenciais.

## 8. Experiência administrativa
Áreas administrativas previstas:
- Visão geral.
- Gestão educacional.
- Avaliações e critérios.
- Usuários.
- Configurações administrativas.
O painel administrativo compartilha identidade, tipografia, acessibilidade e componentes com a área do estudante, mas prioriza eficiência operacional, leitura de dados e clareza. O painel completo permanece no escopo do produto, com implementação posterior ao núcleo principal do estudante, conforme a arquitetura definida.

## 9. Acessibilidade e qualidade transversal
- Contraste adequado e legibilidade em ambos os temas.
- Navegação por teclado, foco visível e rótulos para leitores de tela.
- Mensagens de erro claras e instruções acionáveis.
- Alternativas para interações que dependam de visão, movimento ou cor.
- Preferência por redução de movimento respeitada em transições, celebrações, carregamentos e reações dos agentes.
- Feedback visual acompanhado por texto, ícone, rótulo ou outra pista que não dependa apenas de cor.
- Funções essenciais acessíveis em diferentes dispositivos e tamanhos de tela.

## 10. Prioridades de implementação e limites do MVP
1. Base: tokens de cor, tipografia, temas, componentes compartilhados, navegação responsiva e requisitos de acessibilidade.
1. Experiência principal do estudante: início, jornada, atividades, agentes em texto, perfil, progresso e estados de interface.
1. Feedback e continuidade: recuperação de erros, retomada, salvamento para depois, notificações e preferências essenciais.
1. Administração: implementar a experiência administrativa após o núcleo principal do estudante, mantendo padrões compartilhados.
1. Evolução: artes finais dos mascotes, progressão visual, celebrações avançadas, voz/áudio e efeitos especiais conforme validação e capacidade do MVP.

## 11. Checklist de aceitação visual e UX
- [ ] A identidade global e as cores dos agentes estão aplicadas consistentemente.
- [ ] Tema claro e escuro permanecem legíveis e respeitam a preferência do sistema ou a escolha manual.
- [ ] Navegação funciona em desktop, tablet e celular, com funções essenciais acessíveis.
- [ ] Movimento reduzido, teclado, foco, leitores de tela e alternativas a sinais somente por cor foram considerados.
- [ ] Exercícios e avaliações são distinguíveis por contexto, rótulos e instruções.
- [ ] Atividades podem ser retomadas sem pressão de prazos obrigatórios.
- [ ] Erros, carregamentos, estados vazios e confirmações orientam sobre o ocorrido e o próximo passo.
- [ ] Gamificação e agentes são expressivos sem prejudicar a clareza educacional.
- [ ] O painel administrativo usa os mesmos fundamentos visuais e prioriza eficiência.
- [ ] Recursos futuros não são apresentados como se já estivessem implementados.

## 12. Governança do documento
Este documento representa a consolidação aprovada das propostas de Design System e UX/UI do ELL IBM. Mudanças futuras de paleta, tipografia, navegação, acessibilidade, regras de aprendizagem ou escopo devem ser registradas como revisões explícitas, preservando rastreabilidade entre decisões de produto, arquitetura e implementação.

| Token | Hex | Uso orientativo |
| --- | --- | --- |
| Roxo elétrico | #6C3BFF | Cor primária e destaque de marca |
| Azul elétrico | #2775FF | Ações e destaques complementares |
| Coral | #FF6B6B | Energia, chamadas e identidade do Catalisador |
| Laranja | #FCA048 | Destaques e extensão da identidade do Catalisador |
| Base escura | #17152B | Fundo de referência para o tema escuro |

| Agente | Cores | Personalidade visual |
| --- | --- | --- |
| Catalisador | #FF6B6B → #FCA048 | Energético e mobilizador |
| Mentor | #2F80ED → #56CCF2 | Acolhedor e orientador |
| Analista de Progresso | #11998E → #38EF7D | Analítico e orientado a progresso |
