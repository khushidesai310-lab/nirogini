"""
hospitals.py - Trusted hospital database for 5 Indian cities
Sorted by trust level and budget-friendliness.
Government hospitals listed first for budget-conscious users.
"""

HOSPITALS = {
    "mumbai": [
        {"name": "KEM Hospital", "type": "Government", "area": "Parel",
         "speciality": "General, Women's Health", "budget": "low",
         "phone": "022-24136051", "ayushman": True,
         "note": "One of Mumbai's most trusted government hospitals. Excellent gynaecology department."},
        {"name": "Nair Hospital", "type": "Government", "area": "Mumbai Central",
         "speciality": "General, Obstetrics", "budget": "low",
         "phone": "022-23027641", "ayushman": True,
         "note": "Reputed government hospital with affordable quality care."},
        {"name": "Tata Memorial Hospital", "type": "Government", "area": "Parel",
         "speciality": "Cancer Care", "budget": "low-medium",
         "phone": "022-24177000", "ayushman": True,
         "note": "India's top cancer hospital. Government rates available."},
        {"name": "Lilavati Hospital", "type": "Private", "area": "Bandra",
         "speciality": "General, Women's Health", "budget": "high",
         "phone": "022-26751000", "ayushman": False,
         "note": "Highly trusted private hospital with transparent billing."},
        {"name": "Kokilaben Dhirubhai Ambani Hospital", "type": "Private", "area": "Andheri",
         "speciality": "General, Cancer, Women's Health", "budget": "high",
         "phone": "022-30999999", "ayushman": False,
         "note": "Premium private hospital with excellent women's health centre."},
    ],
    "delhi": [
        {"name": "AIIMS Delhi", "type": "Government", "area": "Ansari Nagar",
         "speciality": "All specialities", "budget": "low",
         "phone": "011-26588500", "ayushman": True,
         "note": "India's premier medical institution. Highly subsidised rates."},
        {"name": "Safdarjung Hospital", "type": "Government", "area": "Ansari Nagar",
         "speciality": "General, Obstetrics", "budget": "low",
         "phone": "011-26165060", "ayushman": True,
         "note": "Large government hospital with excellent women's health services."},
        {"name": "Ram Manohar Lohia Hospital", "type": "Government", "area": "Connaught Place",
         "speciality": "General", "budget": "low",
         "phone": "011-23404380", "ayushman": True,
         "note": "Well-equipped government hospital in central Delhi."},
        {"name": "Apollo Hospital Delhi", "type": "Private", "area": "Sarita Vihar",
         "speciality": "All specialities", "budget": "high",
         "phone": "011-29871011", "ayushman": False,
         "note": "Trusted private hospital with transparent pricing."},
        {"name": "Fortis Escorts", "type": "Private", "area": "Okhla",
         "speciality": "Heart, General", "budget": "medium-high",
         "phone": "011-47135000", "ayushman": False,
         "note": "Reputed private hospital known for honest diagnostics."},
    ],
    "bangalore": [
        {"name": "Victoria Hospital", "type": "Government", "area": "City Market",
         "speciality": "General, Women's Health", "budget": "low",
         "phone": "080-26701150", "ayushman": True,
         "note": "Oldest and most trusted government hospital in Bangalore."},
        {"name": "Kidwai Memorial Cancer Institute", "type": "Government", "area": "Hosur Road",
         "speciality": "Cancer Care", "budget": "low",
         "phone": "080-26094000", "ayushman": True,
         "note": "Government cancer hospital with subsidised treatment."},
        {"name": "Manipal Hospital", "type": "Private", "area": "Old Airport Road",
         "speciality": "All specialities", "budget": "medium-high",
         "phone": "080-25024444", "ayushman": False,
         "note": "Well-regarded private hospital known for honest billing."},
        {"name": "St. John's Medical College Hospital", "type": "Private-Aided", "area": "Koramangala",
         "speciality": "General, Women's Health", "budget": "medium",
         "phone": "080-22065000", "ayushman": True,
         "note": "Affordable private hospital with good women's health department."},
        {"name": "Narayana Health", "type": "Private", "area": "Bommasandra",
         "speciality": "Heart, General", "budget": "medium",
         "phone": "080-71222222", "ayushman": True,
         "note": "Known for affordable quality care. Ayushman empanelled."},
    ],
    "ahmedabad": [
        {"name": "Civil Hospital Ahmedabad", "type": "Government", "area": "Asarwa",
         "speciality": "All specialities", "budget": "low",
         "phone": "079-22681100", "ayushman": True,
         "note": "Gujarat's largest government hospital. Excellent women's health facilities."},
        {"name": "SVP Hospital", "type": "Government", "area": "Ellisbridge",
         "speciality": "General", "budget": "low",
         "phone": "079-26578900", "ayushman": True,
         "note": "Trusted government hospital with affordable care."},
        {"name": "Apollo Hospitals Ahmedabad", "type": "Private", "area": "Bhat",
         "speciality": "All specialities", "budget": "high",
         "phone": "079-66701800", "ayushman": False,
         "note": "Trusted private hospital with transparent billing practices."},
        {"name": "HCG Cancer Centre", "type": "Private", "area": "Mithakhali",
         "speciality": "Cancer Care", "budget": "medium-high",
         "phone": "079-40019000", "ayushman": True,
         "note": "Specialised cancer centre with good patient reviews."},
        {"name": "Zydus Hospital", "type": "Private", "area": "SG Highway",
         "speciality": "General, Women's Health", "budget": "medium-high",
         "phone": "079-66190200", "ayushman": False,
         "note": "Well-regarded private hospital in Ahmedabad."},
    ],
    "kolkata": [
        {"name": "SSKM Hospital", "type": "Government", "area": "BBD Bagh",
         "speciality": "All specialities", "budget": "low",
         "phone": "033-22041400", "ayushman": True,
         "note": "West Bengal's premier government hospital. Highly subsidised."},
        {"name": "NRS Medical College", "type": "Government", "area": "Sealdah",
         "speciality": "General, Obstetrics", "budget": "low",
         "phone": "033-22651740", "ayushman": True,
         "note": "Trusted government hospital with good women's health services."},
        {"name": "Chittaranjan National Cancer Institute", "type": "Government", "area": "Park Circus",
         "speciality": "Cancer Care", "budget": "low",
         "phone": "033-24767832", "ayushman": True,
         "note": "Government cancer hospital with affordable treatment."},
        {"name": "Apollo Gleneagles", "type": "Private", "area": "Canal Circular Road",
         "speciality": "All specialities", "budget": "high",
         "phone": "033-23203040", "ayushman": False,
         "note": "Trusted private hospital known for honest diagnostics."},
        {"name": "Fortis Hospital Kolkata", "type": "Private", "area": "Anandapur",
         "speciality": "General, Women's Health", "budget": "medium-high",
         "phone": "033-66284444", "ayushman": False,
         "note": "Reputed private hospital with good women's health department."},
    ],
}

BUDGET_MAP = {
    "government": ["low"],
    "affordable": ["low", "medium"],
    "moderate": ["medium", "medium-high"],
    "flexible": ["medium", "medium-high", "high"],
    "private": ["medium", "medium-high", "high"],
    "any": ["low", "medium", "medium-high", "high"],
}


def get_hospitals(city, budget_preference="any", speciality=None):
    city_key = city.lower().strip()
    hospitals = HOSPITALS.get(city_key, [])
    if not hospitals:
        return []
    budget_levels = BUDGET_MAP.get(budget_preference, BUDGET_MAP["any"])
    filtered = [h for h in hospitals if any(b in h["budget"] for b in budget_levels)]
    if speciality:
        filtered = [h for h in filtered
                   if speciality.lower() in h["speciality"].lower()] or filtered
    return filtered


def get_budget_question(language="en"):
    if language == "hi":
        return {
            "question": "Hospital के लिए आप क्या prefer करती हैं?",
            "options": [
                {"value": "government", "label": "Government hospital — affordable और trusted"},
                {"value": "affordable", "label": "Affordable — government या low-cost private"},
                {"value": "moderate", "label": "Quality care — cost matter करती है पर quality ज्यादा"},
                {"value": "flexible", "label": "Best care — cost से ज्यादा quality important है"},
            ]
        }
    return {
        "question": "What type of hospital do you prefer?",
        "options": [
            {"value": "government", "label": "Government hospital — affordable and trusted"},
            {"value": "affordable", "label": "Affordable — government or low-cost private"},
            {"value": "moderate", "label": "Quality care — cost matters but quality is priority"},
            {"value": "flexible", "label": "Best available — quality over cost"},
        ]
    }
