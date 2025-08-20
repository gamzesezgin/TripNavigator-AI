import streamlit as st
import requests
import json

def get_fallback_attractions(city_or_goal):
    """
    Fallback turistik yerler
    """
    fallback_attractions = {
        "istanbul": [
            {"name": "Ayasofya", "rating": 4.5, "reviews": 25000, "description": "Tarihi cami ve müze"},
            {"name": "Topkapı Sarayı", "rating": 4.4, "reviews": 18000, "description": "Osmanlı sarayı"},
            {"name": "Kapalı Çarşı", "rating": 4.2, "reviews": 15000, "description": "Tarihi alışveriş merkezi"},
            {"name": "Sultanahmet Camii", "rating": 4.6, "reviews": 22000, "description": "Mavi Cami"},
            {"name": "Galata Kulesi", "rating": 4.3, "reviews": 12000, "description": "Tarihi kule"},
            {"name": "Dolmabahçe Sarayı", "rating": 4.4, "reviews": 8000, "description": "Neo-klasik saray"},
            {"name": "Yerebatan Sarnıcı", "rating": 4.3, "reviews": 9000, "description": "Bizans sarnıcı"},
            {"name": "Ortaköy Camii", "rating": 4.2, "reviews": 6000, "description": "Boğaz manzaralı cami"}
        ],
        "ankara": [
            {"name": "Anıtkabir", "rating": 4.7, "reviews": 35000, "description": "Atatürk'ün anıt mezarı"},
            {"name": "Kızılay Meydanı", "rating": 4.1, "reviews": 8000, "description": "Şehir merkezi"},
            {"name": "Ankara Kalesi", "rating": 4.3, "reviews": 12000, "description": "Tarihi kale"},
            {"name": "Atakule", "rating": 4.0, "reviews": 5000, "description": "Gözlem kulesi"},
            {"name": "Kurtuluş Savaşı Müzesi", "rating": 4.4, "reviews": 6000, "description": "Tarihi müze"},
            {"name": "Hacı Bayram-ı Veli Camii", "rating": 4.2, "reviews": 4000, "description": "Tarihi cami"}
        ],
        "izmir": [
            {"name": "Kemeraltı Çarşısı", "rating": 4.3, "reviews": 15000, "description": "Tarihi çarşı"},
            {"name": "Konak Meydanı", "rating": 4.2, "reviews": 10000, "description": "Şehir merkezi"},
            {"name": "Saat Kulesi", "rating": 4.1, "reviews": 8000, "description": "Tarihi saat kulesi"},
            {"name": "Kadifekale", "rating": 4.0, "reviews": 6000, "description": "Tarihi kale"},
            {"name": "Alsancak Mahallesi", "rating": 4.4, "reviews": 12000, "description": "Modern mahalle"}
        ]
    }
    
    # Şehir adını küçük harfe çevir
    city_lower = city_or_goal.lower()
    
    # Eşleşen şehir varsa döndür
    if city_lower in fallback_attractions:
        return fallback_attractions[city_lower]
    
    # Genel fallback
    return [
        {"name": "Şehir Merkezi", "rating": 4.0, "reviews": 5000, "description": "Ana şehir merkezi"},
        {"name": "Tarihi Bölge", "rating": 4.2, "reviews": 3000, "description": "Tarihi yerler"},
        {"name": "Park ve Bahçeler", "rating": 4.1, "reviews": 2000, "description": "Yeşil alanlar"},
        {"name": "Müzeler", "rating": 4.3, "reviews": 1500, "description": "Kültürel mekanlar"}
    ]

def get_fallback_restaurants(city_or_goal, cuisine="genel"):
    """
    Fallback restoranlar
    """
    fallback_restaurants = {
        "istanbul": [
            {"name": "Mikla Restaurant", "rating": 4.6, "reviews": 2500, "cuisine": "Modern Türk", "price": "$$$"},
            {"name": "Çiya Sofrası", "rating": 4.5, "reviews": 3200, "cuisine": "Geleneksel", "price": "$$"},
            {"name": "Pandeli", "rating": 4.4, "reviews": 1800, "cuisine": "Osmanlı", "price": "$$$"},
            {"name": "Balıkçı Lokantası", "rating": 4.3, "reviews": 2100, "cuisine": "Deniz Ürünleri", "price": "$$"},
            {"name": "Kebapçı", "rating": 4.2, "reviews": 1500, "cuisine": "Kebap", "price": "$"},
            {"name": "Pide Salonu", "rating": 4.1, "reviews": 1200, "cuisine": "Pide", "price": "$"}
        ],
        "ankara": [
            {"name": "Kebapçı Selim Usta", "rating": 4.4, "reviews": 1800, "cuisine": "Kebap", "price": "$$"},
            {"name": "Çiğköfte Salonu", "rating": 4.2, "reviews": 1200, "cuisine": "Çiğköfte", "price": "$"},
            {"name": "Dönerci", "rating": 4.1, "reviews": 900, "cuisine": "Döner", "price": "$"},
            {"name": "Pide Salonu", "rating": 4.0, "reviews": 800, "cuisine": "Pide", "price": "$"}
        ],
        "izmir": [
            {"name": "Deniz Ürünleri Restoranı", "rating": 4.5, "reviews": 2200, "cuisine": "Deniz Ürünleri", "price": "$$"},
            {"name": "Boyoz Salonu", "rating": 4.3, "reviews": 1500, "cuisine": "Boyoz", "price": "$"},
            {"name": "Kumru Salonu", "rating": 4.2, "reviews": 1200, "cuisine": "Kumru", "price": "$"},
            {"name": "Çiğdem Pastanesi", "rating": 4.1, "reviews": 1000, "cuisine": "Tatlı", "price": "$"}
        ]
    }
    
    # Şehir adını küçük harfe çevir
    city_lower = city_or_goal.lower()
    
    # Eşleşen şehir varsa döndür
    if city_lower in fallback_restaurants:
        return fallback_restaurants[city_lower]
    
    # Genel fallback
    return [
        {"name": "Yerel Restoran", "rating": 4.0, "reviews": 500, "cuisine": "Yerel Mutfak", "price": "$$"},
        {"name": "Kebap Salonu", "rating": 4.1, "reviews": 300, "cuisine": "Kebap", "price": "$"},
        {"name": "Pide Salonu", "rating": 4.0, "reviews": 250, "cuisine": "Pide", "price": "$"},
        {"name": "Çay Salonu", "rating": 3.9, "reviews": 200, "cuisine": "Çay & Kahve", "price": "$"}
    ]

def recommend_pois(city_or_goal, top_k=8):
    """
    Place of Interest önerileri için temel fonksiyon
    """
    return get_fallback_attractions(city_or_goal)

def get_popular_attractions(city_or_goal, top_k=8):
    """
    Popüler turistik yerleri getirir
    """
    return get_fallback_attractions(city_or_goal)

def get_food_recommendations(city_or_goal, cuisine, top_k=6):
    """
    Yemek mekanı önerileri getirir
    """
    return get_fallback_restaurants(city_or_goal, cuisine)
