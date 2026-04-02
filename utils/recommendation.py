def get_recommendations(crop, disease):

    crop = crop.lower().strip()
    disease = disease.lower().strip()

    print("DEBUG → Crop:", crop)
    print("DEBUG → Disease:", disease)

    crop_data = {
        "rice": {
            "fertilizer": "Use urea and DAP",
            "water": "Maintain flooded conditions",
            "pest": "Use neem oil or biological pest control"
        },
        "maize": {
            "fertilizer": "Use NPK fertilizer",
            "water": "Moderate irrigation required",
            "pest": "Use insecticides for corn pests"
        },
        "corn": {
            "fertilizer": "Apply nitrogen-rich fertilizer",
            "water": "Keep soil moist but not waterlogged",
            "pest": "Use pest-resistant hybrids or pesticides"
        },
        "potato": {
            "fertilizer": "Use potassium-rich fertilizer",
            "water": "Regular watering but avoid overwatering",
            "pest": "Control beetles and aphids"
        },
        "tomato": {
            "fertilizer": "Use balanced NPK fertilizer",
            "water": "Consistent watering required",
            "pest": "Use neem oil or organic pesticides"
        },
        "pepper": {
            "fertilizer": "Use phosphorus-rich fertilizer",
            "water": "Moderate watering",
            "pest": "Control mites and aphids"
        },
        "jute": {
            "fertilizer": "Use nitrogen-rich fertilizer",
            "water": "Warm and humid conditions required",
            "pest": "Monitor for stem rot and insects"
        }
    }

    disease_data = {
        "early_blight": "Apply fungicides like chlorothalonil",
        "late_blight": "Use copper-based fungicides immediately",
        "bacterial_spot": "Remove infected leaves and use copper spray",
        "leaf_mold": "Improve ventilation and reduce humidity",
        "septoria": "Apply fungicide and remove infected leaves",
        "target_spot": "Use fungicide and avoid overhead watering",
        "mosaic": "Remove infected plants and control insects",
        "yellow": "Control whiteflies and use resistant varieties",
        "rust": "Apply sulfur-based fungicides",
        "gray_leaf_spot": "Use resistant varieties and fungicides",
        "healthy": "No disease detected, maintain good practices"
    }

    # DEFAULT
    fertilizer = "General fertilizer recommended"
    water = "Regular watering"
    pest = "General pest control"
    disease_advice = "Monitor plant regularly"

    # EXACT MATCH FIRST
    if crop in crop_data:
        fertilizer = crop_data[crop]["fertilizer"]
        water = crop_data[crop]["water"]
        pest = crop_data[crop]["pest"]
    else:
        # FALLBACK PARTIAL MATCH
        for key in crop_data:
            if key in crop:
                fertilizer = crop_data[key]["fertilizer"]
                water = crop_data[key]["water"]
                pest = crop_data[key]["pest"]

    # DISEASE MATCH
    for key in disease_data:
        if key in disease:
            disease_advice = disease_data[key]

    return {
        "fertilizer": fertilizer,
        "water": water,
        "pest": pest,
        "disease_advice": disease_advice
    }