from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Any


CORPUS_PATH = Path(__file__).parent / "corpus" / "poi_corpus.jsonl"


def _load_corpus() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    if not CORPUS_PATH.exists():
        return items
    with CORPUS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def _detect_city_from_text(text: str) -> str:
    """Enhanced city detection from text with multiple language support."""
    text_lower = text.lower()
    
    # Turkish cities
    city_mappings = {
        "istanbul": ["istanbul", "constantinople", "konstantinopolis", "istanbul'da", "istanbul'da", "istanbul'u"],
        "ankara": ["ankara", "ankara'da", "ankara'da"],
        "izmir": ["izmir", "izmir'de", "izmir'de"],
        "antalya": ["antalya", "antalya'da", "antalya'da"],
        "bursa": ["bursa", "bursa'da", "bursa'da"],
        "trabzon": ["trabzon", "trabzon'da", "trabzon'da"],
    }
    
    # International cities
    city_mappings.update({
        "paris": ["paris", "pariş", "paris'te", "paris'te"],
        "rome": ["rome", "roma", "roma'da", "roma'da"],
        "london": ["london", "londra", "londra'da", "londra'da"],
        "new york": ["new york", "nyc", "manhattan", "brooklyn", "new york'ta"],
        "tokyo": ["tokyo", "tokyo'da", "tokyo'da"],
        "barcelona": ["barcelona", "barselona", "barselona'da"],
        "amsterdam": ["amsterdam", "amsterdam'da"],
        "prague": ["prague", "prag", "prag'da"],
        "vienna": ["vienna", "vienna'da", "vienna'da"],
        "budapest": ["budapest", "budapeşte", "budapeşte'de"],
    })
    
    for city, keywords in city_mappings.items():
        if any(keyword in text_lower for keyword in keywords):
            return city
    
    return ""


def simple_keyword_score(text: str, query: str) -> int:
    """Enhanced keyword scoring with partial matches and category boosts."""
    if not text or not query:
        return 0
    
    text_lower = text.lower()
    query_lower = query.lower()
    
    # Exact word matches
    text_tokens = set(text_lower.split())
    query_tokens = set(query_lower.split())
    exact_matches = sum(1 for t in query_tokens if t in text_tokens)
    
    # Partial matches (for longer words)
    partial_matches = 0
    for query_word in query_tokens:
        if len(query_word) > 3:  # Only check longer words
            for text_word in text_tokens:
                if query_word in text_word or text_word in query_word:
                    partial_matches += 0.5
    
    # Category-specific boosts
    category_boosts = 0
    if any(word in query_lower for word in ["müze", "museum", "sanat", "art", "galeri", "gallery"]):
        if any(word in text_lower for word in ["museum", "gallery", "müze", "galeri"]):
            category_boosts += 3
    
    if any(word in query_lower for word in ["yemek", "food", "restoran", "restaurant", "gastronomi"]):
        if any(word in text_lower for word in ["food", "restaurant", "yemek", "restoran"]):
            category_boosts += 3
    
    if any(word in query_lower for word in ["tarih", "historic", "tarihi", "ancient"]):
        if any(word in text_lower for word in ["historic", "ancient", "tarihi", "tarih"]):
            category_boosts += 2
    
    if any(word in query_lower for word in ["doğa", "nature", "park", "bahçe", "garden"]):
        if any(word in text_lower for word in ["park", "garden", "bahçe", "doğa", "nature"]):
            category_boosts += 2
    
    return exact_matches + partial_matches + category_boosts


def retrieve_pois(goal: str, profile_card: str | None = None, city_hint: str | None = None, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Enhanced POI retrieval using improved city detection and scoring.
    """
    corpus = _load_corpus()
    if not corpus:
        return []

    # Enhanced city detection
    target_city = (city_hint or "").strip().lower()
    if not target_city:
        target_city = _detect_city_from_text(goal)
    
    # If still no city found, try to infer from profile card
    if not target_city and profile_card:
        target_city = _detect_city_from_text(profile_card)
    
    # Score each POI
    enriched: List[Dict[str, Any]] = []
    for poi in corpus:
        city = str(poi.get("city", "")).lower()
        
        # Filter by city if we have a target
        if target_city and city != target_city:
            continue

        # Build searchable text
        searchable = " ".join(
            [
                poi.get("name", ""),
                poi.get("category", ""),
                poi.get("neighborhood", ""),
                " ".join(poi.get("tags", [])),
                poi.get("summary", ""),
                city,
            ]
        )
        
        # Calculate base score
        base_score = simple_keyword_score(searchable, goal)
        profile_score = simple_keyword_score(searchable, profile_card or "")
        
        # Additional scoring factors
        category_match = 0
        if profile_card:
            profile_lower = profile_card.lower()
            poi_category = poi.get("category", "").lower()
            
            # Museum/Art preferences
            if any(kw in profile_lower for kw in ["müze", "sanat", "museum", "art", "galeri", "gallery"]):
                if poi_category in ["museum", "gallery"]:
                    category_match += 3
            
            # Food preferences
            if any(kw in profile_lower for kw in ["yemek", "gastronomi", "food", "restoran", "restaurant"]):
                if poi_category in ["food-street", "restaurant"]:
                    category_match += 3
            
            # Historic preferences
            if any(kw in profile_lower for kw in ["tarih", "historic", "tarihi", "ancient"]):
                if poi_category in ["landmark", "museum"]:
                    category_match += 2
            
            # Nature preferences
            if any(kw in profile_lower for kw in ["doğa", "nature", "park", "bahçe", "garden"]):
                if poi_category in ["park", "garden"]:
                    category_match += 2
        
        # Final score
        final_score = base_score + profile_score + category_match
        
        # Add some randomness for variety when scores are similar
        import random
        final_score += random.uniform(0, 0.1)
        
        poi_copy = dict(poi)
        poi_copy["_score"] = final_score
        enriched.append(poi_copy)

    # Sort by score and return top results
    enriched.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return enriched[:top_k]


def get_available_cities() -> List[str]:
    """Get list of all available cities in the corpus."""
    corpus = _load_corpus()
    cities = set()
    for poi in corpus:
        if poi.get("city"):
            cities.add(poi.get("city"))
    return sorted(list(cities))


def get_city_stats(city: str) -> Dict[str, Any]:
    """Get statistics for a specific city."""
    corpus = _load_corpus()
    city_pois = [poi for poi in corpus if poi.get("city", "").lower() == city.lower()]
    
    if not city_pois:
        return {}
    
    categories = {}
    for poi in city_pois:
        cat = poi.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_pois": len(city_pois),
        "categories": categories,
        "avg_duration": sum(poi.get("avg_duration_min", 0) for poi in city_pois) / len(city_pois),
        "price_levels": list(set(poi.get("price_level", "") for poi in city_pois))
    }
