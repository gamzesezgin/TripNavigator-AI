"""
Gemini Handler Modülü
AI destekli seyahat planlama ve öneri sistemi
"""

# Ana fonksiyonları import et
from .question_generator import (
    generate_goal_specific_questions,
    generate_learning_style_questions
)

from .personality_analyzer import (
    analyze_learning_style,
    analyze_personality_from_answers,
    analyze_culture_travel_personality,
    analyze_adventure_travel_personality,
    analyze_city_travel_personality,
    analyze_relaxation_travel_personality,
    analyze_food_travel_personality,
    analyze_general_travel_personality
)

from .recommendation_generator import (
    generate_culture_recommendations,
    generate_adventure_recommendations,
    generate_city_recommendations,
    generate_relaxation_recommendations,
    generate_food_recommendations,
    generate_general_recommendations
)

from .ai_destination_recommender import (
    generate_ai_destination_recommendation,
    generate_fallback_destinations,
    generate_recommendation_reasoning
)

from .plan_generator import generate_plan_with_gemini, generate_fallback_plan, generate_hardcoded_fallback_plan

# Tüm fonksiyonları dışa aktar
__all__ = [
    # Question Generator
    'generate_goal_specific_questions',
    'generate_learning_style_questions',
    
    # Personality Analyzer
    'analyze_learning_style',
    'analyze_personality_from_answers',
    'analyze_culture_travel_personality',
    'analyze_adventure_travel_personality',
    'analyze_city_travel_personality',
    'analyze_relaxation_travel_personality',
    'analyze_food_travel_personality',
    'analyze_general_travel_personality',
    
    # Recommendation Generator
    'generate_culture_recommendations',
    'generate_adventure_recommendations',
    'generate_city_recommendations',
    'generate_relaxation_recommendations',
    'generate_food_recommendations',
    'generate_general_recommendations',
    
    # AI Destination Recommender
    'generate_ai_destination_recommendation',
    'generate_fallback_destinations',
    'generate_recommendation_reasoning',
    
    # Plan Generator
    'generate_plan_with_gemini',
    'generate_fallback_plan',
    'generate_hardcoded_fallback_plan'
]
