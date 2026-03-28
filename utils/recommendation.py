def get_recommendations(crop, disease):
    
    recommendations = {
        "rice": {
            "fertilizer": "Use urea and DAP",
            "water": "Maintain flooded conditions",
            "pest": "Use neem oil for pest control"
        },
        "wheat": {
            "fertilizer": "Use nitrogen-rich fertilizer",
            "water": "Irrigate every 10-15 days",
            "pest": "Use insecticides for aphids"
        },
        "maize": {
            "fertilizer": "Use NPK fertilizer",
            "water": "Moderate irrigation required",
            "pest": "Use biological pest control"
        }
    }

    crop = crop.lower()

    if crop in recommendations:
        return recommendations[crop]
    else:
        return {
            "fertilizer": "General fertilizer recommended",
            "water": "Regular watering",
            "pest": "General pest control"
        }