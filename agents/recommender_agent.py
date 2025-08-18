import streamlit as st
import requests
import json
from agents.tripadvisor_handler import (
    get_attractions_by_city,
    get_restaurants_by_city,
    get_fallback_attractions,
    get_fallback_restaurants
)

def recommend_pois(city_or_goal, top_k=8):
    """
    Place of Interest önerileri için temel fonksiyon
    """
    try:
        # Önce TripAdvisor'dan dene
        places = get_attractions_by_city(city_or_goal, top_k)
        if places:
            return places
    except Exception as e:
        st.warning(f"⚠️ TripAdvisor API hatası: {e}")
    
    # Fallback kullan
    return get_fallback_attractions(city_or_goal)

def get_popular_attractions(city_or_goal, top_k=8):
    """
    Popüler turistik yerleri getirir
    """
    try:
        # Önce TripAdvisor'dan dene
        places = get_attractions_by_city(city_or_goal, top_k)
        if places:
            return places
    except Exception as e:
        st.warning(f"⚠️ TripAdvisor API hatası: {e}")
    
    # Fallback kullan
    return get_fallback_attractions(city_or_goal)

def get_food_recommendations(city_or_goal, cuisine, top_k=6):
    """
    Yemek mekanı önerileri getirir
    """
    try:
        # Önce TripAdvisor'dan dene
        restaurants = get_restaurants_by_city(city_or_goal, cuisine, top_k)
        if restaurants:
            return restaurants
    except Exception as e:
        st.warning(f"⚠️ TripAdvisor API hatası: {e}")
    
    # Fallback kullan
    return get_fallback_restaurants(city_or_goal, cuisine)
