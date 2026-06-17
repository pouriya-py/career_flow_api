# tests/test_matching.py
from app.services.matching_service import calculate_match_score
from app import models

def test_matching_algorithm_perfect_match():
    """تست زمانی که همه مهارت‌ها و شرایط منطبق هستند"""
    user = models.UserProfile(
        name="Test User",
        skills=["Python", "FastAPI", "Docker"],
        target_market=models.MarketType.GLOBAL,
        experience_years=3
    )
    job = models.JobOpportunity(
        title="Senior Python Dev",
        company="Tech Corp",
        required_skills=["Python", "FastAPI", "Docker"],
        market_type=models.MarketType.GLOBAL,
        is_remote=True
    )
    
    score = calculate_match_score(user, job)
    assert score == 100, f"Expected 100, got {score}"

def test_matching_algorithm_partial_match():
    """تست زمانی که فقط برخی مهارت‌ها منطبق هستند"""
    user = models.UserProfile(
        name="Test User",
        skills=["Python", "Django"],
        target_market=models.MarketType.IRAN,
        experience_years=1
    )
    job = models.JobOpportunity(
        title="Python Dev",
        company="Startup",
        required_skills=["Python", "FastAPI", "React"],
        market_type=models.MarketType.IRAN,
        is_remote=False
    )
    
    score = calculate_match_score(user, job)
    # 1 مهارت مشترک از 2 مهارت کاربر = 35% + 15% بازار = 50%
    assert score == 50, f"Expected 50, got {score}"