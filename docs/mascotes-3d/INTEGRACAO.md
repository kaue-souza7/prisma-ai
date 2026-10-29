> **Nota do Prisma.AI:** este documento é a referência original do pacote de mascotes.
> Para a integração efetiva no app (backend `/static/mascotes` + wrapper `Mascot3D`),
> consulte [`INTEGRACAO_APP.md`](INTEGRACAO_APP.md).

# Integração no site — contratos, eventos e limitações

**Status:** proposta de integração independente.  
**Importante:** nada neste pacote está conectado ao site, ao backend, à autenticação ou ao banco de dados. A stack real do frontend ainda precisa ser confirmada (lacuna L-03).

## 1. O que pode ser reaproveitado

O site pode escolher entre 3 níveis:

1. **Somente os GLBs** — em qualquer engine WebGL/glTF.
2. **GLBs + controlador** — usando `CharacterController` sobre um `AnimationMixer` já existente.
3. **Palco pronto** — usando `MascotViewer`/`createMascotExperience`, que criam renderer, câmera, luzes, carregamento e pausas.

Os arquivos essenciais são:

```text
src/assets/models/catalisador.glb
src/assets/models/mentor.glb
src/assets/models/analista.glb
src/core/catalog.js
src/core/CharacterController.js
src/core/AnimationStateMachine.js
src/core/events.js            (simulação; opcional no site)
src/core/EventRouter.js       (simulação; opcional no site)
src/viewer/MascotViewer.js    (opcional)
```

## 2. API pública

### 2.1 Fábrica de palco

```js
import { createMascotExperience } from './src/index.js';

const mascot = await createMascotExperience({
  container: document.querySelector('#mascote'),
  modelBaseUrl: '/assets/mascotes',
  reducedMotion: null, // null = segue prefers-reduced-motion
  fade: 0.25,
  pixelRatio: null,    // null = devicePixelRatio limitado a 2
});

await mascot.showCharacter('mentor');
```

O container precisa ter largura/altura mensuráveis. O palco observa resize, visibilidade da viewport, scroll e mudança de visibilidade do documento.

### 2.2 Operações equivalentes às solicitadas

| Operação | Assinatura | Comportamento |
|---|---|---|
| Carregar | `await mascot.loadCharacter(characterId)` | Carrega e cacheia o GLB. Não troca necessariamente o personagem visível. Retorna o `CharacterController`. |
| Exibir | `await mascot.showCharacter(characterId, { reset = true })` | Torna o personagem ativo, esconde o anterior, aplica idle e contexto. Retorna o controlador. |
| Tocar direto | `await mascot.playAnimation(animationId)` | Interrompe estados não bloqueados, limpa a fila e inicia o ID. É o atalho de teste/demo. |
| Disparar por prioridade | `await mascot.triggerAnimation(animationId, priority)` | Respeita prioridade, locks, proteção de texto e fila. É o método recomendado para o site. |
| Movimento reduzido | `mascot.setReducedMotion(enabled)` | Aplica a todos os controladores carregados; troca para poses estáticas e crossfades de 200 ms. |
| Parar | `mascot.stopAnimation()` | Limpa a fila, reinicia o contexto de texto e retorna ao idle do personagem ativo. |
| Remover | `mascot.destroy()` | Para o RAF, remove listeners, libera renderer e controladores. |

IDs de personagem: `catalisador`, `mentor`, `analista`.  
IDs de animação: exatamente `M-01…M-11`, `A-01…A-07`, `C-01…C-12`.

### 2.3 Controlador de baixo nível

Se o site já tem um `AnimationMixer`, use apenas:

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { CharacterController } from './src/core/CharacterController.js';

const gltf = await new GLTFLoader().loadAsync('/assets/mascotes/mentor.glb');
const mentor = new CharacterController({
  characterId: 'mentor',
  gltf,
  fade: 0.25,
  reducedMotion: false,
});

mentor.play('M-01', { source: 'load' }); // idle

// No seu loop:
function update(deltaSeconds) {
  mentor.update(deltaSeconds); // só se mentor.isRunning()
}

// Exemplos:
mentor.triggerAnimation('M-07', 1); // erro, prioridade máxima do Mentor
mentor.triggerAnimation('M-08', 3); // queued se M-07 ainda estiver em curso
mentor.setTextActive(true);         // M-08 protegido enquanto o texto estiver ativo
mentor.endText();                   // encerra M-08 → fila/próximo/idle
mentor.setContext({ panelOpen: true });
mentor.setVisible(false);           // pausa loops fora da viewport
mentor.setPaused(true, 'busy');     // pausa durante carregamento pesado/scroll
```

Métodos principais do controlador:

| Método | Uso |
|---|---|
| `play(id, options)` | Solicita uma animação. `force`, `priority`, `queue`, `source`, `clearQueue` e `interruptLocked` são opções. |
| `playAnimation(id)` | Atalho `force:true` + `clearQueue:true` para testes e demo. |
| `triggerAnimation(id, priority)` | Solicitação respeitando a máquina de estados; use no site. |
| `stopAnimation({toIdle=true})` | Interrompe, limpa fila e volta ao idle. |
| `setReducedMotion(enabled)` | Alterna entre movimento normal e pose estática. |
| `setTextActive(bool)` / `endText()` | Abre/fecha a janela de proteção de M-08. O encerramento de M-08 e C-06 respeita 0,5 s / 0,6 s de saída, conforme a especificação; continue chamando `update()` nesse intervalo. |
| `setContext(partial)` | Atualiza `panelOpen`, `recommendationActive`, `positiveProgressActive`, etc. |
| `setVisible(bool)` | Suspende atualização fora do palco. |
| `setPaused(bool, reason)` | Empilha motivos de pausa (por exemplo `scroll`, `busy`, `modal`). |
| `update(dt)` | Avança o mixer; chame apenas quando `isRunning()` for verdadeiro. |
| `getState()` | Snapshot com `currentId`, `queue`, `progress`, `reducedMotion`, `textActive`, `loadingReplacement`, `context` etc. |
| `on(event, listener)` | Eventos do controlador. |
| `dispose()` | Libera o mixer e listeners. |

Eventos emitidos: `animationstart`, `statechange`, `transition`, `queued`, `ignored`, `text`, `motionmode`, `visibility`, `stopped`, `log`, `error`.

### 2.4 Estado retornado

```js
{
  characterId: 'mentor',
  currentId: 'M-08',
  currentName: 'Explicando',
  currentKind: 'presentation',
  currentPriority: 3,
  currentLoop: true,
  renderedClip: 'MENTOR_M08_EXPLAINING',
  duration: 2,
  progress: 0.42,
  queue: [{ id: 'M-07', name: 'Encorajador', priority: 1 }],
  reducedMotion: false,
  loadingReplacement: false,
  textActive: true,
  visible: true,
  running: true,
  lastDecision: 'texto ativo: reação aguarda o fim do texto',
  context: { ... },
}
```

## 3. Regras de prioridade e conflito

A prioridade numérica é **menor = mais alta**. As máquinas aplicam:

### Mentor

- **M-07** (prioridade 1) interrompe qualquer estado não bloqueado; nunca deve ser omitido após erro.
- **M-10** (2) interrompe idle/loops; uma reação curta em curso não é interrompida por ele.
- **M-08** (3) é a apresentação; enquanto `textActive` estiver verdadeiro, reações entram na fila.
- **M-03/M-06** (4) interrompem o idle, mas não atropelam uma reação curta.
- **M-01** (5) só entra quando a fila está vazia.
- Reações curtas não são interrompidas, exceto por prioridade 1 ou por `playAnimation` explícito em contexto de teste.

### Analista

- **A-07** é lock: uma vez iniciada, não é interrompida.
- **A-03** e **A-05** são mutuamente exclusivos na mesma abertura do painel. O site deve declarar:
  ```js
  analyst.setContext({ panelOpen: true, recommendationActive: true, positiveProgressActive: false });
  ```
  Com `recommendationActive`, A-05 é ignorada. Com `positiveProgressActive`, A-03 é ignorada.
- A-02/A-04/A-06 interrompem o idle; A-01 é o fallback.

### Catalisador

- **C-12** é lock e prioridade absoluta. **C-11 é bloqueada enquanto C-12 estiver ativa e nunca deve ser disparada no mesmo evento de conclusão de trilha.**
- C-11 interrompe C-01/C-03/C-06/C-07.
- C-05 é lock.
- C-08/C-10 têm prioridade 4; C-06 tem 5; C-01 tem 6.
- C-06 text protection: como a especificação não impõe a mesma exceção do Mentor, reações de prioridade maior podem substituir C-06; para preservar leitura, a integração pode manter `textActive` e escolher não disparar eventos durante o texto.

### Regras que o site deve garantir fora do controlador

- **Frequência e cadência por sessão/missão/trilha:** o controlador impede duplicações imediatas e respeita prioridades, mas não conhece IDs de sessão, missão ou trilha. Regras como “M-02 1× por sessão”, “M-05 1× por missão”, “C-05 1× por usuário”, “C-12 1× por trilha”, “A-05 1× por abertura de painel” e “M-09 1× por verificação” devem ser verificadas pela camada de eventos do site, que tem esse contexto. O catálogo registra a intenção comportamental; o `MascotEventRouter` é apenas uma simulação e reinicia o estado ao reproduzir um cenário.

- Não disparar C-11/M-10 após erro.
- M-07 é obrigatória em qualquer erro.
- C-10 nunca deve ser acompanhada de expressão de preocupação/frustração.
- A-03 e A-05 não podem coexistir na mesma sessão de painel.
- C-12 e C-11 não podem coexistir.
- A-07 começa **após a saída de C-12** (≈2,9 s), não no mesmo instante.
- Animações não devem competir com leitura ativa, feedback textual importante ou carregamento. Use `setTextActive`, `setPaused('busy')` e `stopAnimation` conforme o estado da UI.

## 4. Eventos esperados do site (proposta para L-05)

A lacuna L-05 ainda não tem contrato aprovado. Esta é uma proposta de payload que o backend/frontend pode emitir; o site deve confirmar os nomes e adaptar a camada de eventos.

```json
{
  "type": "answer.evaluated",
  "character": "mentor",
  "payload": {
    "correct": false,
    "difficulty": "standard",
    "attempt": 2,
    "missionId": "T2-M3",
    "isHardQuestion": false
  }
}
```

Mapeamento proposto de eventos de UX para animações:

| Evento de UX | Personagem | Sequência | Observações |
|---|---|---|---|
| Início do onboarding | Catalisador | C-02 → C-03 | C-02 uma vez por onboarding. |
| Resposta do onboarding | Catalisador | C-04 → C-03 | C-04 a cada resposta; variações L-02 pendentes. |
| Final do onboarding | Catalisador | C-05 → C-06 | C-05 lock; texto ativo em C-06. |
| Usuário digitando | Mentor | M-04 | Encerrar com M-03 ou M-01. |
| Backend processando | Mentor | M-03 | Se `< 500 ms`, ir direto para M-08. Com reduced motion, usar loading da UI. |
| Acerto de questão | Mentor | M-10 | Nunca após erro. |
| Erro de questão | Mentor | M-07 → M-08 | M-07 obrigatória, sem exceção. |
| Acerto difícil | Mentor | M-05 → M-10 | Máximo 1× por missão. |
| Dificuldade recorrente | Mentor | M-06 → M-08 | Máximo 1× por missão; A-03 no painel depois. |
| Pergunta de verificação | Mentor | M-09 | Até o usuário começar a digitar; então M-04. |
| Início de nova missão | Mentor | M-02 | Uma vez por sessão/chat. |
| Conclusão de missão | Catalisador | C-11 → C-06 | Também M-11 no Mentor, em sua tela. |
| Próxima missão | Catalisador | C-07 | Retorna ao idle. |
| Protocolo D33 Nível 3 | Catalisador | C-10 → C-06 | Nunca acompanhado de julgamento. |
| Retorno após inatividade | Catalisador | C-08 → C-06 | Não mencionar o tempo ausente. |
| Painel de progresso aberto | Analista | A-02 | Uma vez por abertura. |
| Recomendação de reforço | Analista | A-03 | Contexto `recommendationActive:true`. |
| Progresso positivo | Analista | A-05 | Só se `recommendationActive:false`. |
| Atualização do painel | Analista | A-06 | Uma vez por atualização visível. |
| Síntese calculando | Analista | A-04 | Com reduced motion, loading da UI. |
| Síntese apresentada | Analista | A-02 → A-05 | Sem recomendação ativa. |
| Conclusão de trilha | Catalisador + Analista | C-12 → C-06; A-07 após ~2,9 s | C-12 tem prioridade absoluta; A-07 em outra tela/painel. |
| Acerto inesperado/100% Expresso | Catalisador/Mentor | C-09 → C-11 / M-05 → M-10 | Máximo 1× por missão. |

### Exemplo de adaptador

```js
import { CHARACTERS } from './src/core/catalog.js';

export function onAnswerEvaluated({ correct, isHardQuestion }, mentor) {
  if (correct) {
    if (isHardQuestion) mentor.triggerAnimation('M-05', 2);
    mentor.triggerAnimation('M-10', 2);
    return;
  }

  // Erro: M-07 é obrigatória e inicia o acolhimento.
  // M-08 entra na fila e só começa quando M-07 terminar.
  // Nunca há C-11/M-10 em contexto de erro.
  mentor.triggerAnimation('M-07', 1);
  mentor.triggerAnimation('M-08', 3);
  mentor.setTextActive(true);
}

// Evento separado, disparado pelo sinal de dificuldade recorrente do backend.
export function onRecurringDifficulty(mentor) {
  mentor.triggerAnimation('M-06', 4);
  mentor.triggerAnimation('M-08', 3);
  mentor.setTextActive(true);
}

export function onMentorTextFinished(mentor) {
  mentor.endText();
}
```

Para eventos genéricos, o adaptador deve chamar o **controlador do personagem correto**. A demo usa o `MascotEventRouter` apenas para simulação; ele não deve ser confundido com o contrato de produção.

### Conclusão de trilha com dois personagens

```js
const catalyst = await catalystViewer.loadCharacter('catalisador');
const analyst = await analystViewer.loadCharacter('analista');

catalyst.triggerAnimation('C-12', 1); // lock, prioridade absoluta
// No site, C-06 só entra depois da saída de C-12; a demo agenda o texto.
setTimeout(() => {
  analyst.triggerAnimation('A-07', 1); // após ~2,9 s
}, 2900);
setTimeout(() => {
  catalyst.triggerAnimation('C-06', 5);
  catalyst.setTextActive(true);
}, 3800);
```

## 5. Movimento reduzido e acessibilidade

`prefers-reduced-motion` é respeitado no boot pelo `MascotViewer` quando `reducedMotion` é `null`. O site pode sobrescrever com `mascot.setReducedMotion(true)` quando tiver uma configuração própria.

| Situação | Comportamento |
|---|---|
| Intervalo de atualização | 200 ms de crossfade estático, sem avanço de tempo do clipe. |
| Idle / loops | Congelados em pose-chave. |
| Reações curtas/celebrações | Pose estática; após a duração, retorna ao idle estático. |
| Explicando / apresentando | Pose estática de fala, mantida até `endText()`/fim do conteúdo; o encerramento respeita o atraso de 0,5 s (M-08) / 0,6 s (C-06). |
| M-03 / A-04 (processamento) | O personagem renderiza idle estático e o app mostra o indicador de loading da interface (`loadingReplacement:true` no estado). |
| C-12/C-05/A-07 | Pose estática de celebração; a API sinaliza `reducedMotion:true`. |
| Loops fora da viewport | `IntersectionObserver` no palco ou `controller.setVisible(false)` pausa o mixer. |
| Scroll ativo | O palco pausa por 160 ms; o site pode empilhar `setPaused(true, 'scroll')`. |

**Nunca use a animação como único vetor de informação.** Todo feedback precisa de equivalente textual (acerto, erro, encorajamento, conclusão). A demo exibe textos e estados; o site deve fazer o mesmo.

Também é possível mapear a configuração de intensidade do Design System:

- **Normal** → `setReducedMotion(false)`.
- **Reduzido** → `setReducedMotion(true)`.
- **Desativado** → `setReducedMotion(true)` + `stopAnimation()`/idle estático, com o palco opcionalmente oculto.

## 6. Desempenho e ciclo de vida

- **Lazy loading:** carregue apenas o GLB do personagem presente na tela. O `MascotViewer` faz isso automaticamente. O analista não deve carregar na tela de atividade; o Mentor não deve carregar no painel.
- **Um GLB por mascote:** 1,48–1,57 MiB; ~36,3 mil triângulos no palco de referência; 96 draw calls no desktop com shadow map.
- **Sombras:** desativadas abaixo de 760 px de viewport; a sombra de contato permanece.
- **DPR:** limitado a 2 por padrão.
- **Loops:** pause com `IntersectionObserver` (já embutido no palco) ou `setVisible(false)` se usar o controlador sozinho.
- **Scroll/carregamento pesado:** o palco pausa durante scroll; use `setPaused(true, 'busy')` ao abrir modais, carregar dados ou durante leitura importante.
- **Documento oculto:** o palco pausa via `visibilitychange`.
- **Tempo por frame:** a atualização do controlador foi medida em ~0,004 ms/frame em Chromium headless (host de desenvolvimento), mas isso **não substitui** medição em dispositivo móvel real. O requisito de 2 ms deve ser confirmado no aparelho de referência do produto.
- **Dispose:** chame `destroy()` ao desmontar a tela; ao usar o controlador diretamente, pare o mixer e remova os listeners.

## 7. Integração no Three.js existente

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { CharacterController } from './src/core/CharacterController.js';

const controller = new CharacterController({
  characterId: 'analista',
  gltf,
  fade: 0.25,
  reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
});

scene.add(gltf.scene);
controller.play('A-01');

const clock = new THREE.Clock();
renderer.setAnimationLoop(() => {
  const dt = clock.getDelta();
  controller.update(dt);
  renderer.render(scene, camera);
});

// No unmount:
controller.dispose();
gltf.scene.removeFromParent();
```

Recomendações:

- O GLB já vem com o personagem apoiado em `y=0`; ajuste escala/posição no container.
- Se a cena tiver tone mapping diferente, os tokens de cor continuam sendo a base; valide a leitura em tema claro/escuro.
- Não presuma `AnimationMixer` global compartilhado entre personagens: cada altura de rig tem seu próprio mixer.
- Para múltiplos mascotes simultâneos, instancie um `CharacterController` por GLTF; a demo usa um palco por vez.
- O GLB usa `KHR_materials_clearcoat`, `KHR_materials_unlit` e `KHR_materials_emissive_strength`, suportados pelo Three.js e pela maioria dos carregadores glTF 2.0.

## 8. Limitações conhecidas

1. **Sem integração real** — esta entrega não foi conectada ao site, backend, auth ou banco.
2. **Stack real desconhecida (L-03)** — a referência é Three.js; a adaptação para outra engine precisa ser validada.
3. **Sem variações C-04 (L-02)** — a animação base existe; o pool de 3–4 variações está pendente.
4. **Sem TTS/lip-sync** — a boca usa fala genérica.
5. **Sem arquivo `.blend`** — a fonte é o pipeline procedural; o GLB pode ser refinado em DCC.
6. **Cross-character C-12 → A-07** — ambos os clipes existem, mas a orquestração de duas telas é do site. A demo registra a reação secundária; não a executa oculta.
7. **Tema claro/palco em breakpoints do site** — não validados (L-06/L-07).
8. **FPS mobile físico** — não medido neste ambiente.
9. **Variações de intensidade “Desativado”** — não há uma terceira máquina; é um modo de composição do site.
10. **Acessórios** — livro/tablet são mantidos na mão esquerda; em gestos amplos eles acompanham o braço. Isso é coerente com a posse, mas pode exigir ajuste de arte se o layout do site usar outra mão.

## 9. Como confirmar antes de integrar

1. Confirmar a stack de renderização do site e o modo de carregamento de GLB.
2. Revisar a lacuna L-05 e o contrato real de eventos com backend.
3. Validar tokens de cor/materiais no tema claro e escuro do produto.
4. Confirmar os breakpoints e o tamanho do palco por tela (L-07).
5. Medir FPS, memória e tempo de carregamento em dispositivo móvel de referência.
6. Revisar as expressões com designers/animadores e decidir sobre o pool C-04.
7. Rodar `npm run validate` e a demo em Chrome/Safari/Firefox atuais no ambiente do produto.
