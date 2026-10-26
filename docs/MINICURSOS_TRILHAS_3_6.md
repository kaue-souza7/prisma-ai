# Módulos imersivos — Trilhas 3 a 6

**Status:** implementado e validado nas Trilhas 3, 4, 5 e 6.  
**Rotas:** `/student/learn/{mission_id}`  
**Fontes:** `backend/app/modules/content/seeds/phase_3_v1.py` a
`phase_6_v1.py` e migrations `0005`–`0009`.

---

## 1. Modelo

As Trilhas 3 a 6 seguem exatamente o modelo das Trilhas 1 e 2:

| Conceito | Implementação |
|---|---|
| Trilha | `phases` |
| Módulo | `missions` |
| Tela/etapa | Item do `missions.lesson_flow` (JSONB) |
| Questão | `activities` referenciada por `activity_order` |
| Conteúdo de leitura | `content_items` referenciado por `content_type` + `content_order` |
| Progresso | `user_mission_progress.current_step` e `completed_steps` |
| Respostas | `user_responses` |

O roteiro não duplica o conteúdo: ele referencia os itens editoriais e as
atividades versionadas. A carga usa upsert por chave natural e preserva IDs de
atividades já respondidas.

### Novas migrations

| Migration | Conteúdo |
|---|---|
| `0005_phase_3_content.py` | Fase 3, missões 1–3 |
| `0006_phase_4_content.py` | Fase 4, missões 1–3 |
| `0007_phase_5_content.py` | Fase 5, missões 1–3 |
| `0008_phase_6_content.py` | Fase 6, missões 1–4 |
| `0009_lesson_flows_phases_3_6.py` | Roteiros imersivos das Fases 3–6 |

### Conquistas

| Fase | Chave | Nome |
|---|---|---|
| 3 | `fase_3_concluida` | Poupador consciente |
| 4 | `fase_4_concluida` | Mestre dos juros |
| 5 | `fase_5_concluida` | Investidor iniciante |
| 6 | `fase_6_concluida` | Guardião digital |

---

## 2. Trilha 3 — Por que poupar

| Módulo | Foco | Etapas | Duração estimada |
|---|---|---:|---:|
| 3.1 Um objetivo que faz sentido | Meta com valor e prazo, valor mensal e ajuste | 9 | ~5 min |
| 3.2 Guardar sem perder o controle | Essenciais, lazer, assinaturas e economia realista | 9 | ~5 min |
| 3.3 E se acontecer algo inesperado? | Reserva de emergência e imprevisto | 10 | ~7 min |

**Total estimado da trilha:** ~17 minutos, sem contar revisões.

A missão 3.3 termina com uma simulação em que a geladeira quebra e a reserva
precisa ser usada sem comprometer a meta do curso.

---

## 3. Trilha 4 — Juros: a favor e contra você

| Módulo | Foco | Etapas | Duração estimada |
|---|---|---:|---:|
| 4.1 O tempo e os juros | Juros simples, compostos e efeito do tempo | 9 | ~5 min |
| 4.2 Parcelas não contam a história inteira | Custo total, preço à vista e custo do crédito | 9 | ~5 min |
| 4.3 O que acontece quando a dívida cresce? | Atraso, mínimo, teto legal e saída de dívidas | 10 | ~7 min |

**Total estimado da trilha:** ~17 minutos, sem contar revisões.

A missão 4.3 termina com a comparação de três propostas fictícias de crédito,
considerando o total e o tamanho da parcela.

---

## 4. Trilha 5 — Onde o dinheiro rende

| Módulo | Foco | Etapas | Duração estimada |
|---|---|---:|---:|
| 5.1 O que meu dinheiro consegue comprar? | Inflação, poder de compra e rendimento real | 9 | ~5 min |
| 5.2 Guardar ou investir? | Reserva, risco e prazo do objetivo | 9 | ~5 min |
| 5.3 Rendimento, prazo e liquidez | Comparação de alternativas fictícias e FGC | 10 | ~7 min |

**Total estimado da trilha:** ~17 minutos, sem contar revisões.

As alternativas, taxas e instituições citadas são fictícias e não constituem
recomendação de investimento.

---

## 5. Trilha 6 — Proteção digital

| Módulo | Foco | Etapas | Duração estimada |
|---|---|---:|---:|
| 6.1 A mensagem suspeita | Phishing e verificação por canal oficial | 9 | ~5 min |
| 6.2 Antes de enviar um Pix | Falso parente, falso banco e Pix por engano | 9 | ~5 min |
| 6.3 Protegendo meus dados | Códigos, senhas e sites suspeitos | 10 | ~7 min |
| 6.4 Desafio integrador | Orçamento, crédito, imprevisto e fraude | 6 | ~5 min |

**Total estimado da trilha:** ~22 minutos, sem contar revisões.

### Decisão de implementação: missão 6.4

O desafio integrador proposto no documento editorial foi carregado como
**missão 6.4 — Desafio integrador**, em vez de quatro atividades extras na
missão 6.3. A missão é obrigatória, tem quatro simulações de 20 pontos e só é
desbloqueada depois das missões 6.1–6.3. Assim, a conclusão da Fase 6 coincide
com o encerramento da jornada.

### Competências no desafio

As quatro simulações trabalham a competência local `6.4.1 — Integrar as
competências da jornada`. O documento editorial associa cada etapa a códigos de
fases anteriores; o contrato atual do banco exige que os códigos existam na
missão da atividade. A referência cruzada permanece registrada no documento,
mas a evidência é consolidada na competência integradora.

---

## 6. Estrutura de cada roteiro

- Introdução do Catalisador com objetivo e competências.
- Leitura e questão intercaladas (explicação, exemplo e dica).
- Resposta aberta registrada sem avaliação determinística.
- Simulação final nas missões 3.3, 4.3, 5.3 e 6.3.
- Síntese do Analista com pontos-chave e próximo passo.

O desafio 6.4 usa introdução, quatro cenários e síntese, sem itens de leitura
adicionais.

---

## 7. Validação executada

### Backend

```text
docker compose exec backend alembic upgrade head
→ 0009 (head)

docker compose exec backend pytest -q
→ 101 passed

docker compose exec backend alembic check
→ No new upgrade operations detected
```

Os testes cobrem:

- contrato JSONB de todas as atividades das Fases 3–6;
- competências existentes e evidência objetiva das essenciais;
- publicação dos itens de conteúdo;
- cobertura de todos os módulos pelos roteiros;
- referências de leitura e atividades válidas em cada roteiro;
- disponibilidade do módulo por API após concluir as fases anteriores.

### Frontend

```text
docker compose exec frontend npm test -- --run
→ 29 passed (11 arquivos)

docker compose exec frontend npm run build
→ tsc -b && vite build aprovados
```

---

## 8. Conteúdo carregado

| Fase | Missões | Competências | Atividades | Itens de conteúdo | Roteiros |
|---|---:|---:|---:|---:|---:|
| 3 | 3 | 9 | 13 | 9 | 3 |
| 4 | 3 | 9 | 13 | 9 | 3 |
| 5 | 3 | 9 | 13 | 9 | 3 |
| 6 | 4 | 10 | 17 | 9 | 4 |

Total das Trilhas 3–6: **13 módulos, 37 competências, 56 atividades,
36 itens de conteúdo e 13 roteiros imersivos**.
