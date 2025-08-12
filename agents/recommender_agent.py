from __future__ import annotations

from typing import List, Dict, Any

from rag.retriever import retrieve_pois


def build_profile_card_from_answers(goal: str, answers: List[int] | None) -> str:
    """
    Build a very lightweight profile card text using answer indices.
    This is a placeholder until a richer analysis is added.
    """
    if not answers:
        return "Genel tempo, dengeli aktiviteler, orta bütçe, yerel yemeklere açık."

    # Very naive mapping by first few answers if present
    tempo_map = {
        0: "yoğun tempo",
        1: "orta tempo",
        2: "rahat tempo",
        3: "esnek tempo",
    }
    tempo = tempo_map.get(answers[0], "orta tempo")

    interest_hint = "müze ve sanat"
    if len(answers) > 1:
        if answers[1] == 0:
            interest_hint = "müzeler ve tarihi yerler"
        elif answers[1] == 1:
            interest_hint = "yerel kültür ve gelenekler"
        elif answers[1] == 2:
            interest_hint = "mimari ve sanat"
        else:
            interest_hint = "dengeli aktiviteler"

    budget_hint = "orta bütçe"
    if len(answers) > 2:
        budget_map = {0: "yüksek bütçe", 1: "orta bütçe", 2: "düşük bütçe", 3: "karışık bütçe"}
        budget_hint = budget_map.get(answers[2], "orta bütçe")

    return f"{tempo}, {interest_hint}, {budget_hint}."


def recommend_pois(goal: str, answers: List[int] | None, city_hint: str | None = None, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Recommend POIs for a goal using simple RAG retrieval and a short reason per item.
    Returns a list of POIs with a 'reason' field.
    """
    profile_card = build_profile_card_from_answers(goal, answers)
    pois = retrieve_pois(goal=goal, profile_card=profile_card, city_hint=city_hint, top_k=top_k)

    results: List[Dict[str, Any]] = []
    for poi in pois:
        reason = f"{profile_card.split('.')[0].capitalize()} ile uyumlu; {poi.get('avg_duration_min', 90)} dk ayırabilirsiniz."
        item = {
            "poi_id": poi.get("id"),
            "name": poi.get("name"),
            "category": poi.get("category"),
            "neighborhood": poi.get("neighborhood"),
            "avg_duration_min": poi.get("avg_duration_min"),
            "price_level": poi.get("price_level"),
            "reason": reason,
        }
        results.append(item)

    return results


