import pytest
import os
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("SECRET_KEY", "testsecretkey1234567890abcdefghij")

from app.modules.progress.service import (
    calculate_level,
    LEVEL_THRESHOLDS,
    POINTS_FIRST_ATTEMPT,
    POINTS_AFTER_REINFORCEMENT,
    POINTS_ONBOARDING,
    _level_name,
    _next_level_threshold,
)


# ─────────────────────────────────────────────
# Regras de nível (D6)
# ─────────────────────────────────────────────

def test_level_1_at_zero_points():
    assert calculate_level(0) == 1


def test_level_2_at_threshold():
    assert calculate_level(300) == 2


def test_level_2_just_below_threshold():
    assert calculate_level(299) == 1


def test_level_3_at_threshold():
    assert calculate_level(700) == 3


def test_level_4_at_threshold():
    assert calculate_level(1200) == 4


def test_level_5_at_threshold():
    assert calculate_level(1800) == 5


def test_level_5_above_max():
    assert calculate_level(9999) == 5


def test_all_level_thresholds_covered():
    for level, threshold in LEVEL_THRESHOLDS.items():
        assert calculate_level(threshold) == level


# ─────────────────────────────────────────────
# Pontuação (D6)
# ─────────────────────────────────────────────

def test_first_attempt_points():
    assert POINTS_FIRST_ATTEMPT == 100


def test_reinforcement_points():
    assert POINTS_AFTER_REINFORCEMENT == 70


def test_onboarding_points():
    assert POINTS_ONBOARDING == 50


def test_reinforcement_less_than_first_attempt():
    assert POINTS_AFTER_REINFORCEMENT < POINTS_FIRST_ATTEMPT


# ─────────────────────────────────────────────
# Nomes de nível
# ─────────────────────────────────────────────

def test_level_names():
    assert _level_name(1) == "Iniciante"
    assert _level_name(2) == "Consciente"
    assert _level_name(3) == "Planejador"
    assert _level_name(4) == "Estrategista"
    assert _level_name(5) == "Autônomo"


def test_next_level_threshold_from_1():
    assert _next_level_threshold(1) == 300


def test_next_level_threshold_from_5_is_none():
    assert _next_level_threshold(5) is None


# ─────────────────────────────────────────────
# Pontuação máxima alcançável (18 missões + onboarding)
# ─────────────────────────────────────────────

def test_max_points_reaches_level_5():
    """Com 18 missões × 100 pts + 50 pts onboarding = 1850 pts → nível 5."""
    max_points = 18 * POINTS_FIRST_ATTEMPT + POINTS_ONBOARDING
    assert max_points >= 1800
    assert calculate_level(max_points) == 5
