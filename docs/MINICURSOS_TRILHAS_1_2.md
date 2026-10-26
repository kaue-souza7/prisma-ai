# Módulos imersivos — Trilhas 1 e 2

**Status:** implementado e validado nas Trilhas 1 e 2.  
**Rotas:** `/student/learn/{mission_id}`  
**Fontes:** `backend/app/modules/content/lesson_flows.py` e migrations `0004_immersive_lesson_flow.py`.

> As Trilhas 3 a 6 seguem o mesmo modelo e estão documentadas em
> [`MINICURSOS_TRILHAS_3_6.md`](MINICURSOS_TRILHAS_3_6.md).

---

## 1. Modelo conceitual

| Conceito | Implementação |
|---|---|
| Trilha | `phases` |
| Módulo | `missions` (cada missão existente foi tratada como um módulo) |
| Tela/etapa | Item do `missions.lesson_flow` (JSONB) |
| Questão | `activities` referenciada por `activity_order` |
| Conteúdo de leitura | `content_items` referenciado por `content_type` + `content_order` |
| Progresso da experiência | `user_mission_progress.current_step` e `completed_steps` |
| Respostas | `user_responses`, com a regra de pontuação existente |

O modelo preserva as tabelas e regras já existentes. O roteiro não duplica o
conteúdo: ele referencia os itens editoriais e as atividades versionadas.

### Estrutura de uma etapa

```json
{ "type": "reading", "content_type": "explanation", "content_order": 1 }
```

```json
{ "type": "question", "activity_order": 2 }
```

```json
{
  "type": "summary",
  "agent": "analyst",
  "title": "Seu contracheque agora faz sentido",
  "body": "Texto de síntese...",
  "highlights": ["Conceito 1", "Conceito 2"]
}
```

Tipos suportados: `intro`, `reading`, `question`, `scenario`, `summary`.

---

## 2. Trilha 1 — Primeiro salário

| Módulo | Foco | Etapas | Duração estimada |
|---|---|---:|---:|
| 1.1 De onde vem o dinheiro? | Bruto, líquido, descontos, FGTS e cálculo | 10 | ~6 min |
| 1.2 O que importa primeiro? | Necessidade, desejo, prioridade e contexto | 9 | ~5 min |
| 1.3 Meu primeiro plano | Distribuição da renda, dívidas, objetivos e reserva | 9 | ~6 min |

**Total estimado da trilha:** ~17 minutos, sem contar revisões.

Cada roteiro intercala leitura, questões e síntese. A missão 1.3 termina com uma
simulação de decisão financeira.

---

## 3. Trilha 2 — Seu dinheiro no digital

| Módulo | Foco | Etapas | Duração estimada |
|---|---|---:|---:|
| 2.1 Como vou pagar? | Pix, débito, crédito, fatura e parcelamento | 9 | ~5 min |
| 2.2 Entendendo o cartão | Limite, fechamento, vencimento e rotativo | 9 | ~5 min |
| 2.3 Antes de confirmar | Conferência, sinais de fraude, MED e ocorrência | 10 | ~7 min |

**Total estimado da trilha:** ~17 minutos, sem contar revisões.

A missão 2.3 termina com um cenário de decisão que combina orçamento,
pagamento e segurança.

---

## 4. Experiência imersiva

A rota `/student/learn/{mission_id}` é protegida e fica **fora do `StudentLayout`**:

- sem sidebar;
- sem menu principal;
- sem abas inferiores;
- sem dashboard;
- sem lista de questões empilhadas.

Cada etapa ocupa a tela. O topo contém apenas:

- botão de saída;
- marca discreta;
- progresso da experiência;
- controle de efeitos sonoros.

### Fluxo de leitura

1. Conteúdo em bloco curto.
2. Botão **Continuar**.
3. A etapa é marcada como concluída e o cursor avança.

Não há avanço automático.

### Fluxo de questão

1. Uma questão por tela.
2. Seleção de alternativa ou resposta aberta.
3. **Confirmar resposta**.
4. Feedback do Mentor ou do Analista.
5. Se correta/aberta: **Continuar**.
6. Se incorreta: **Tentar novamente**, sem apagar o histórico.

A resposta só é aceita uma vez por tentativa. O botão de confirmação some
depois do resultado.

### Conclusão

A tela final mostra:

- síntese;
- pontos efetivamente concedidos;
- etapas e duração;
- competências trabalhadas;
- conquistas novas, quando disponíveis na sessão;
- próximo módulo recomendado;
- retorno à jornada.

---

## 5. Persistência e retomada

### Banco

`user_mission_progress` ganhou:

- `current_step` — etapa atual;
- `completed_steps` — lista de etapas concluídas.

### Endpoints

```http
GET  /api/v1/journey/missions/{id}/lesson
POST /api/v1/journey/missions/{id}/lesson/progress
POST /api/v1/journey/missions/{id}/start
POST /api/v1/journey/missions/{id}/submit
```

`GET /lesson` devolve:

- missão, fase e competências;
- etapas resolvidas;
- atividade pública sem gabarito;
- última resposta do usuário por atividade;
- etapa atual e etapas concluídas;
- duração estimada;
- próximo módulo.

### Regras

- A resposta é salva em `user_responses`.
- Uma questão correta entra em `completed_steps`.
- Uma resposta aberta registrada entra em `completed_steps`.
- Uma resposta incorreta não avança a etapa.
- O cursor só avança pelo endpoint de progresso, nunca pelo `submit`.
- Ao recarregar depois de uma resposta, o feedback é restaurado.
- Etapas já concluídas não duplicam registros.
- Pontos e conquistas continuam sendo calculados pelo backend.

---

## 6. Efeitos e acessibilidade

- Som sintetizado via Web Audio API, sem arquivos externos.
- Vibração via `navigator.vibrate`, quando suportado.
- Efeitos desativados por padrão.
- Preferência persistida em `localStorage` (`ell-learning-effects`).
- Controle acessível no topo, com `aria-pressed` e rótulo dinâmico.
- Celebração visual no resumo.
- `prefers-reduced-motion` desativa animações.
- Confete oculto em telas pequenas para preservar leitura.
- Foco visível em alternativas, botões e saída.

---

## 7. Validação executada

### Backend

- 53 testes passando.
- Fluxo de lição, persistência, retomada, bloqueio e Fase 2 cobertos em
  `backend/tests/test_lesson_api.py`.

### Frontend

- 29 testes passando.
- `LessonPlayerPage` cobre início, leitura, confirmação, feedback, erro com
  retomada e saída.
- Build TypeScript/Vite aprovado.

### Navegador

Chrome headless, dados reais:

- desktop 1440×1000: introdução, leitura, questão, feedback, retomada e resumo;
- mobile 390×844;
- ausência de sidebar e navegação inferior na experiência;
- apenas um `radiogroup` por tela;
- saída sempre acessível;
- sem overflow horizontal;
- sem erros de console.

---

## 8. Decisões pedagógicas pendentes de validação

- Duração estimada de 6–7 minutos por módulo.
- Quantidade de 3 módulos por trilha.
- Repetição da questão após erro, em vez de avanço com lacuna.
- Critério de conclusão baseado em todas as atividades corretas/abertas.
- Nível de profundidade dos textos de introdução e síntese.
- Uso de efeitos sonoros e vibração por padrão desativado.
