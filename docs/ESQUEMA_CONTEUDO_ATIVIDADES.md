# Esquema do conteúdo das atividades

**Arquivo:** `docs/ESQUEMA_CONTEUDO_ATIVIDADES.md`  
**Versão do contrato:** 1 (`schema_version: 1`)  
**Status:** contrato técnico implementado; conteúdo da Fase 1 carregado pela migration `0002`.  
**Fonte de verdade no código:** `backend/app/modules/content/activity_schema.py`  
**Fonte do conteúdo da Fase 1:** `backend/app/modules/content/seeds/phase_1_v1.py`

---

## 1. Onde o conteúdo vive

Cada atividade é uma linha da tabela `activities`:

| Coluna | Papel |
|---|---|
| `mission_id` | Missão à qual a atividade pertence. |
| `order` | Ordem de apresentação dentro da missão. |
| `activity_type` | `multiple_choice`, `open_text` ou `simulation`. |
| `content` | JSONB com enunciado, alternativas, gabarito e feedbacks. |
| `points_value` | Pontos exibidos para a atividade (não é a pontuação da missão). |
| `is_active` | Atividades inativas não entram na conclusão da missão. |

O gabarito fica **somente** no backend. A API do estudante remove as chaves
privadas antes de retornar a missão.

O conteúdo educacional de apoio (explicações, exemplos e dicas) fica em
`content_items`, não em `activities.content`. Ele é retornado por
`GET /api/v1/content/missions/{mission_id}` e só inclui itens publicados.

---

## 2. Campos comuns

Todas as atividades usam os mesmos campos de base:

| Campo | Tipo | Obrigatório | Regra |
|---|---|---|:---:|
| `schema_version` | inteiro | não | Hoje deve ser `1`. Ausência é interpretada como versão 1. |
| `prompt` | string | sim | Enunciado principal, de 1 a 2.000 caracteres. |
| `competency_codes` | array de string | sim | Pelo menos um código existente na missão. Ex.: `["1.1.1"]`. |
| `hint` | string | não | Ajuda opcional, até 1.000 caracteres. |
| `feedback_neutral` | string | não | Usado quando a resposta não pode ser avaliada. |

Os códigos de competência obedecem ao padrão `fase.missão.competência`
(`1.1.1`, `1.2.3`, `1.3.2`). O código é persistido em `competencies.code` e é a
ligação entre atividade, evidência de aprendizagem e painel de progresso.

---

## 3. `multiple_choice`

```json
{
  "schema_version": 1,
  "prompt": "Uma proposta informa salário de R$ 2.000 bruto. O que isso significa?",
  "competency_codes": ["1.1.1"],
  "options": [
    { "value": "a", "label": "Que você receberá exatamente R$ 2.000." },
    { "value": "b", "label": "Que o valor é anterior aos descontos." }
  ],
  "correct_answer": "b",
  "feedback_correct": "Exato! O bruto é o valor combinado antes dos descontos.",
  "feedback_incorrect": "O bruto ainda não sofreu os descontos. Revise a diferença."
}
```

| Campo | Tipo | Obrigatório | Regra |
|---|---|---|:---:|
| `options` | array de objeto | sim | 2 a 6 alternativas. |
| `options[].value` | string | sim | Único na atividade; até 50 caracteres. |
| `options[].label` | string | sim | Texto visível, até 500 caracteres. |
| `correct_answer` | string | sim | Deve ser igual a um `options[].value`. **Privado.** |
| `feedback_correct` | string | sim | Explica por que a alternativa correta está certa. |
| `feedback_incorrect` | string | sim | Explica o erro sem constranger. |

A resposta do estudante usa `response_data.selected_option`.

---

## 4. `simulation`

A simulação usa a mesma estrutura de alternativas, mas apresenta um cenário e
um campo de gabarito próprio.

```json
{
  "schema_version": 1,
  "prompt": "O que você faz com o seu primeiro salário?",
  "competency_codes": ["1.3.1", "1.3.2"],
  "scenario": "Você recebeu R$ 1.800 líquidos. Essenciais: R$ 1.100...",
  "options": [
    { "value": "a", "label": "Pago essenciais e a conta atrasada; guardo o restante." },
    { "value": "b", "label": "Pago essenciais e compro o tênis." }
  ],
  "correct_choice": "a",
  "feedback_correct": "Boa decisão! Você priorizou o essencial e evitou juros.",
  "feedback_incorrect": "Revise a ordem: essenciais, dívidas com juros, objetivos e desejos."
}
```

| Campo | Tipo | Obrigatório | Regra |
|---|---|---|:---:|
| `scenario` | string | sim | Contexto da decisão, até 3.000 caracteres. |
| `options` | array de objeto | sim | 2 a 6 alternativas, com valores únicos. |
| `correct_choice` | string | sim | Deve corresponder a uma alternativa. **Privado.** |
| `feedback_correct` / `feedback_incorrect` | string | sim | Feedbacks explicativos. |

A resposta do estudante usa `response_data.choice`.

---

## 5. `open_text`

```json
{
  "schema_version": 1,
  "prompt": "Explique com suas palavras por que o valor na conta é menor.",
  "competency_codes": ["1.1.1", "1.1.2"],
  "feedback_static": "Resposta registrada. O Mentor fará a análise personalizada.",
  "evaluation_criteria": [
    "Menciona que o bruto é anterior aos descontos.",
    "Cita ao menos um desconto.",
    "Explica que o líquido é o valor recebido."
  ],
  "max_length": 2000
}
```

| Campo | Tipo | Obrigatório | Regra |
|---|---|---|:---:|
| `feedback_static` | string | sim | Devolvido imediatamente após o registro. |
| `evaluation_criteria` | array de string | sim | Critérios que a IA usará na Etapa 2. **Privado.** |
| `max_length` | inteiro | não | Entre 100 e 5.000; padrão 2.000. |

A resposta do estudante usa `response_data.text`. Quando o Mentor está
configurado, ele avalia a resposta imediatamente com base nos
`evaluation_criteria` e devolve um veredito (`correct`, `incorrect` ou
`ambiguous`) com feedback em português. O veredito é persistido em
`user_responses` (`is_correct`, `feedback`, `evaluation_status`) para continuar
visível quando o estudante reabrir a lição.

Se o agente estiver indisponível ou retornar um formato inválido, a resposta é
registrada com `evaluation_status=unavailable` e o `feedback_static` do
conteúdo, sem bloquear a conclusão da missão. A avaliação aberta é formativa:
não altera a pontuação objetiva da missão.

---

## 6. Contrato de submissão

`POST /api/v1/journey/missions/{mission_id}/submit`

```json
{
  "activity_id": 10,
  "response_data": { "selected_option": "b" }
}
```

| Tipo | Chave aceita em `response_data` |
|---|---|
| `multiple_choice` | `selected_option` |
| `simulation` | `choice` |
| `open_text` | `text` |

A resposta inclui `is_correct`, `score`, `feedback`, `attempt_number`,
`mission_completed`, `points_earned` e `new_achievements`.

---

## 7. Dados privados e sanitização

O endpoint `GET /api/v1/journey/missions/{id}` remove:

- `correct_answer`
- `correct_choice`
- `evaluation_criteria`
- `feedback_correct`
- `feedback_incorrect`

Os feedbacks de acerto/erro também podem revelar o gabarito antes da submissão.
Eles são devolvidos somente na resposta do `POST /submit`. As chaves permanecem
no banco e são usadas apenas pelo backend. Qualquer novo campo que revele a
resposta correta deve ser adicionado a `PRIVATE_ACTIVITY_KEYS` em
`backend/app/modules/journey/router.py` e coberto por teste.

---

## 8. Validação e versionamento

A carga de conteúdo valida todos os registros com Pydantic. As regras incluem:

1. `activity_type` conhecido;
2. `prompt` e feedbacks não vazios;
3. alternativas com valores únicos e entre 2 e 6 itens;
4. gabarito correspondendo a uma alternativa;
5. `competency_codes` existindo na missão;
6. pelo menos um critério para resposta aberta;
7. campos desconhecidos rejeitados (`extra="forbid"`).

Testes de contrato: `backend/tests/test_content_schema.py`.

**Mudanças de conteúdo:** o seed `phase_1_v1.py` é imutável. Correções
editoriais devem gerar uma nova versão (`phase_1_v2.py`) e uma nova migration.
**Mudança de campos:** incrementar `schema_version` e manter compatibilidade de
leitura durante a transição.

---

## 9. Checklist antes de publicar uma missão

- [ ] A missão tem objetivo, descrição e competências com códigos únicos.
- [ ] Cada competência essencial tem pelo menos uma evidência objetiva.
- [ ] Toda atividade aponta para códigos de competência existentes.
- [ ] O gabarito corresponde a uma alternativa válida.
- [ ] Os feedbacks explicam o raciocínio, não apenas "certo/errado".
- [ ] A resposta aberta tem critérios observáveis e feedback estático.
- [ ] O conteúdo de apoio está em `content_items`, revisado e publicado.
- [ ] `python -m pytest tests/test_content_schema.py` passa.
- [ ] A migration foi aplicada em ambiente limpo (`alembic upgrade head`).
- [ ] O endpoint do estudante não devolve campos privados.

---

## 10. Exemplo de carga

A migration `0002_phase_1_content.py` chama `seed_phase_1()`, que faz upsert por
chave natural:

- missão: `(phase_id, number)`;
- competência: `(mission_id, code)`;
- atividade: `(mission_id, order)`;
- item de conteúdo: `(mission_id, order, content_type)`.

Isso preserva IDs de atividades já respondidas quando o conteúdo é atualizado.
