"""
Contrato do JSONB `activities.content`.

O contrato é versionado e validado na carga de conteúdo. O gabarito
(`correct_answer` / `correct_choice`) e os critérios de avaliação de
respostas abertas (`evaluation_criteria`) nunca são enviados ao estudante
antes da submissão da resposta.
"""
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ActivityContentBase(BaseModel):
    """Campos comuns a todas as atividades."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    prompt: str = Field(min_length=1, max_length=2000)
    competency_codes: list[str] = Field(min_length=1)
    hint: Optional[str] = Field(default=None, max_length=1000)
    feedback_neutral: Optional[str] = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def validate_competency_codes(self):
        for code in self.competency_codes:
            if not code.strip():
                raise ValueError("competency_codes não pode conter código vazio.")
        return self


class ActivityOption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str = Field(min_length=1, max_length=50)
    label: str = Field(min_length=1, max_length=500)


class ChoiceActivityContent(ActivityContentBase):
    """Atividade objetiva de múltipla escolha."""

    options: list[ActivityOption] = Field(min_length=2, max_length=6)
    correct_answer: str = Field(min_length=1, max_length=50)
    feedback_correct: str = Field(min_length=1, max_length=2000)
    feedback_incorrect: str = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def validate_options(self):
        values = [option.value for option in self.options]
        if len(values) != len(set(values)):
            raise ValueError("Os valores das alternativas devem ser únicos.")
        if self.correct_answer not in values:
            raise ValueError("correct_answer deve corresponder a uma alternativa existente.")
        return self


class SimulationActivityContent(ActivityContentBase):
    """Simulação com uma decisão objetiva e feedback explicativo."""

    scenario: str = Field(min_length=1, max_length=3000)
    options: list[ActivityOption] = Field(min_length=2, max_length=6)
    correct_choice: str = Field(min_length=1, max_length=50)
    feedback_correct: str = Field(min_length=1, max_length=2000)
    feedback_incorrect: str = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def validate_options(self):
        values = [option.value for option in self.options]
        if len(values) != len(set(values)):
            raise ValueError("Os valores das alternativas devem ser únicos.")
        if self.correct_choice not in values:
            raise ValueError("correct_choice deve corresponder a uma alternativa existente.")
        return self


class OpenTextActivityContent(ActivityContentBase):
    """Resposta aberta: registrada agora e avaliada pela IA na Etapa 2."""

    feedback_static: str = Field(min_length=1, max_length=2000)
    evaluation_criteria: list[str] = Field(min_length=1)
    max_length: int = Field(default=2000, ge=100, le=5000)

    @model_validator(mode="after")
    def validate_criteria(self):
        for criterion in self.evaluation_criteria:
            if not criterion.strip():
                raise ValueError("evaluation_criteria não pode conter item vazio.")
        return self


ACTIVITY_CONTENT_MODELS = {
    "multiple_choice": ChoiceActivityContent,
    "simulation": SimulationActivityContent,
    "open_text": OpenTextActivityContent,
}

ActivityContent = Union[
    ChoiceActivityContent,
    SimulationActivityContent,
    OpenTextActivityContent,
]


def validate_activity_content(activity_type: str, content: dict) -> ActivityContent:
    """
    Valida o conteúdo de acordo com o tipo da atividade.

    Levanta ValueError com uma mensagem legível para falhas de contrato.
    """
    model = ACTIVITY_CONTENT_MODELS.get(activity_type)
    if model is None:
        raise ValueError(f"Tipo de atividade não suportado: {activity_type!r}.")
    try:
        return model.model_validate(content)
    except Exception as exc:
        raise ValueError(
            f"Conteúdo inválido para a atividade do tipo {activity_type!r}: {exc}"
        ) from exc
