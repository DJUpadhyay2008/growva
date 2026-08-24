import sys
import os
from sqlalchemy.orm import Session
from app.database.database import engine, Base, SessionLocal
from app.database.models import (
    CropModel, WeatherLogModel, PlannerTaskModel,
    MandiPriceModel, GovernmentSchemeModel, DiseaseRecordModel
)

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if already seeded
        if db.query(CropModel).count() > 0:
            print("Database already contains crop records. Skipping seed.")
            return

        print("Seeding database with comprehensive agricultural dataset...")

        crops_data = [
            # Crops / Cereals
            ("Wheat", "गेहूँ", "ઘઉં", "Crops", "Rabi (Winter)", "Fertile well-drained clay loam", "Medium (450–650 mm)", 120, 10, 30, 400, 700, 6.0, 7.5, "3.5 - 4.5 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Wheat%20field.jpg", "Stubble for fodder & biochar", "Rust, Karnal bunt"),
            ("Rice", "चावल", "ચોખા", "Crops", "Kharif (Monsoon)", "Clayey loam, alluvial", "High (1000–1500 mm)", 130, 20, 38, 900, 1800, 5.5, 7.0, "4.0 - 5.5 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Rice%20paddy%20field%20in%20India.jpg", "Paddy straw for mushroom cultivation", "Blast, Brown plant hopper"),
            ("Bajra", "बाजरा", "બાજરી", "Crops", "Kharif (Monsoon)", "Sandy loam, arid soil", "Low (250–500 mm)", 85, 18, 42, 250, 600, 6.0, 8.0, "2.0 - 3.0 tonnes/ha", "/crops/Bajra.jpeg", "Green fodder & silage", "Ergot, Downy mildew"),
            ("Maize", "मक्का", "મકાઈ", "Crops", "Kharif / Rabi", "Deep fertile loamy soil", "Medium (500–800 mm)", 100, 15, 35, 500, 900, 6.0, 7.5, "4.0 - 6.0 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Maize%20field.jpg", "Corn cobs for bio-ethanol", "Fall armyworm"),
            ("Barley", "जौ", "જવ", "Crops", "Rabi (Winter)", "Well-drained loamy soil", "Low–Medium (350–500 mm)", 110, 8, 28, 300, 600, 6.5, 7.8, "3.0 - 4.0 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Barley%20field.jpg", "Malt production waste as animal feed", "Powdery mildew"),
            ("Jowar", "ज्वार", "જુવાર", "Crops", "Kharif / Rabi", "Clay loam & black soil", "Low–Medium (400–600 mm)", 105, 18, 40, 350, 700, 6.0, 8.5, "2.5 - 3.5 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Sorghum%20field.jpg", "Sorghum stalks for bio-energy", "Shoot fly"),
            ("Ragi", "रागी", "રાગી", "Crops", "Kharif (Monsoon)", "Red, lateritic, loamy soil", "Medium (400–750 mm)", 115, 15, 34, 400, 800, 5.0, 7.0, "2.0 - 2.8 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Finger%20millet.jpg", "Straw for cattle feed", "Blast disease"),
            ("Oats", "जई", "ઓટ્સ", "Crops", "Rabi (Winter)", "Loam to heavy clay", "Medium (400–600 mm)", 95, 10, 26, 350, 650, 5.5, 7.0, "2.5 - 3.5 tonnes/ha", "/crops/user-provided/oats.jpeg", "Green forage", "Crown rust"),
            ("Sugarcane", "गन्ना", "શેરડી", "Crops", "Perennial / Annual", "Deep rich loamy soil", "Very High (1500–2500 mm)", 360, 20, 38, 1200, 2500, 6.0, 7.5, "70 - 100 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Sugarcane%20field.jpg", "Bagasse for paper & bio-power, pressmud for organic fertilizer", "Red rot, Pyrilla"),
            ("Cotton", "कपास", "કપાસ", "Crops", "Kharif (Monsoon)", "Deep black cotton soil (Vertisols)", "Medium (600–1000 mm)", 160, 18, 38, 550, 1100, 6.0, 8.0, "1.8 - 2.5 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Cotton%20plant.jpg", "Cotton seed cake for feed", "Pink bollworm"),

            # Pulses
            ("Chickpea", "चना", "ચણા", "Pulses", "Rabi (Winter)", "Well-drained clay loam", "Low (300–450 mm)", 110, 10, 30, 250, 500, 6.0, 8.0, "1.5 - 2.2 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Chickpeas.jpg", "Husk for cattle feed", "Wilt, Pod borer"),
            ("Pigeon Pea", "अरहर / तुअर", "તુવેર", "Pulses", "Kharif (Monsoon)", "Deep loamy to clay soil", "Medium (600–900 mm)", 180, 18, 35, 500, 1000, 6.5, 7.5, "1.2 - 2.0 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Pigeon%20pea.jpg", "Stalks for fuel & fencing", "Sterility mosaic"),
            ("Green Gram", "मूंग", "મગ", "Pulses", "Kharif / Summer", "Well-drained loamy soil", "Low (350–500 mm)", 70, 20, 38, 300, 600, 6.2, 7.2, "1.0 - 1.5 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Green%20Mung%20Dal.jpg", "Green manure incorporation", "Yellow mosaic virus"),
            ("Black Gram", "उड़द", "અડદ", "Pulses", "Kharif / Rabi", "Loam to heavy clay", "Low–Medium (400–600 mm)", 80, 20, 36, 350, 650, 6.0, 7.5, "1.0 - 1.4 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/White%20urand%20dal.jpg", "Husk & green residue", "Powdery mildew"),
            ("Lentil", "मसूर", "મસૂર", "Pulses", "Rabi (Winter)", "Loam to clay loam", "Low (300–450 mm)", 105, 8, 28, 250, 500, 6.0, 7.5, "1.2 - 1.8 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Lentils.jpg", "Straw for livestock", "Rust"),
            ("Soybean", "सोयाबीन", "સોયાબીન", "Pulses", "Kharif (Monsoon)", "Well-drained fertile loam", "Medium (600–900 mm)", 100, 18, 35, 550, 1000, 6.0, 7.5, "2.0 - 2.8 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/White%20soya.jpg", "Soy meal for protein feed", "Girdle beetle"),

            # Vegetables
            ("Tomato", "टमाटर", "ટમેટા", "Vegetables", "Year-round / Seasonal", "Rich fertile loam", "Medium (500–800 mm)", 90, 15, 34, 450, 900, 6.0, 7.0, "25 - 40 tonnes/ha", "/crops/tomato.jpg", "Tomato pomace for animal feed", "Early blight, Leaf curl"),
            ("Potato", "आलू", "બટાટા", "Vegetables", "Rabi (Winter)", "Loose friable sandy loam", "Medium (500–700 mm)", 100, 12, 28, 400, 750, 5.5, 6.5, "20 - 35 tonnes/ha", "/crops/potato.jpg", "Peels for compost & starch", "Late blight"),
            ("Onion", "प्याज़", "ડુંગળી", "Vegetables", "Kharif / Rabi", "Deep rich friable loam", "Medium (450–650 mm)", 120, 12, 32, 350, 700, 6.0, 7.0, "18 - 30 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Onions.jpg", "Outer skins for natural dye", "Purple blotch"),
            ("Garlic", "लहसुन", "લસણ", "Vegetables", "Rabi (Winter)", "Rich well-drained loam", "Medium (400–600 mm)", 135, 10, 28, 300, 600, 6.0, 7.0, "6 - 10 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Garlic.jpg", "Garlic husk for bio-pesticide", "Thrips"),
            ("Carrot", "गाजर", "ગાજર", "Vegetables", "Rabi (Winter)", "Deep loose sandy loam", "Medium (400–600 mm)", 85, 10, 25, 350, 600, 6.0, 7.0, "15 - 25 tonnes/ha", "/crops/carrot.jpg", "Carrot tops for greens", "Alternaria leaf blight"),
            ("Cabbage", "पत्तागोभी", "કોબીજ", "Vegetables", "Rabi (Winter)", "Moist fertile loam", "Medium (450–700 mm)", 80, 10, 26, 400, 700, 6.0, 7.2, "25 - 35 tonnes/ha", "/crops/cabbage.jpg", "Outer leaves for compost", "Black rot"),
            ("Cauliflower", "फूलगोभी", "ફૂલકોબી", "Vegetables", "Rabi (Winter)", "Rich well-drained clay loam", "Medium (450–700 mm)", 85, 12, 26, 400, 750, 6.0, 7.0, "20 - 30 tonnes/ha", "/crops/cauliflower.jpg", "Leaves & stalk for cattle fodder", "Downy mildew"),
            ("Spinach", "पालक", "પાલક", "Vegetables", "Year-round / Winter", "Fertile moist loam", "Medium (350–550 mm)", 45, 10, 28, 300, 600, 6.5, 7.5, "10 - 15 tonnes/ha", "/crops/spinach.jpg", "Residue for green compost", "Damping off"),
            ("Okra", "भिंडी", "ભીંડા", "Vegetables", "Summer / Kharif", "Warm well-drained sandy loam", "Medium (400–650 mm)", 65, 20, 38, 350, 700, 6.0, 7.0, "10 - 16 tonnes/ha", "/crops/okra.jpg", "Stalks for jaggery clarification", "Yellow vein mosaic"),
            ("Brinjal", "बैंगन", "રીંગણ", "Vegetables", "Year-round", "Rich silt to clay loam", "Medium (450–700 mm)", 100, 18, 35, 400, 800, 5.5, 6.8, "20 - 30 tonnes/ha", "/crops/brinjal.jpg", "Plant waste for vermicompost", "Fruit and shoot borer"),
            ("Capsicum", "शिमला मिर्च", "કેપ્સિકમ", "Vegetables", "Winter / Spring", "Well-drained sandy loam", "Medium (450–700 mm)", 90, 15, 30, 400, 700, 6.0, 7.0, "15 - 25 tonnes/ha", "/crops/capsicum.jpg", "Trimmings for compost", "Anthracnose"),
            ("Cucumber", "खीरा", "કાંકડી", "Vegetables", "Summer / Kharif", "Loamy fertile soil", "Medium (400–600 mm)", 55, 18, 36, 350, 600, 6.0, 7.0, "12 - 20 tonnes/ha", "/crops/cucumber.jpg", "Vines for green manure", "Powdery mildew"),

            # Fruits
            ("Mango", "आम", "કેરી", "Fruits", "Perennial (Summer)", "Deep well-drained alluvial / red loam", "Medium (750–1200 mm)", 365, 22, 42, 700, 1500, 5.5, 7.5, "8 - 15 tonnes/ha", "/crops/mango.jpg", "Mango seed kernels for starch & oil", "Mango hopper, Anthracnose"),
            ("Banana", "केला", "કેળા", "Fruits", "Perennial / Year-round", "Rich fertile alluvial soil", "High (1200–2000 mm)", 365, 18, 38, 1000, 2200, 6.0, 7.5, "40 - 65 tonnes/ha", "/crops/user-provided/banana.jpeg", "Banana pseudostem fiber for textiles & paper", "Sigatoka leaf spot"),
            ("Apple", "सेब", "સફરજન", "Fruits", "Perennial (Temperate)", "Deep well-drained loamy soil", "Medium (800–1200 mm)", 365, 2, 24, 700, 1400, 5.5, 6.8, "12 - 22 tonnes/ha", "/crops/apple.jpg", "Apple pomace for pectin extraction", "Apple scab"),
            ("Orange", "संतरा", "સંતરા", "Fruits", "Perennial", "Well-drained deep loamy soil", "Medium (750–1100 mm)", 365, 12, 35, 600, 1200, 6.0, 7.5, "15 - 25 tonnes/ha", "/crops/orange.jpg", "Peel essential oil extraction", "Citrus dieback"),
            ("Guava", "अमरूद", "જામફળ", "Fruits", "Perennial", "Adaptable to sandy loam & clay", "Medium (500–1000 mm)", 365, 15, 40, 450, 1200, 5.0, 8.0, "15 - 25 tonnes/ha", "/crops/guava.jpg", "Pruned wood for biochar", "Guava wilt"),
            ("Papaya", "पपीता", "પપૈયા", "Fruits", "Perennial", "Rich well-drained loamy soil", "Medium (800–1400 mm)", 300, 20, 38, 700, 1500, 6.0, 7.0, "40 - 70 tonnes/ha", "/crops/papaya.jpg", "Papain enzyme from latex", "Papaya ring spot virus"),
            ("Pomegranate", "अनार", "દાડમ", "Fruits", "Perennial", "Well-drained loamy to light soil", "Low–Medium (400–700 mm)", 365, 15, 42, 300, 800, 6.5, 8.0, "10 - 18 tonnes/ha", "/crops/pomegranate.jpg", "Rind extract for tannin & medicine", "Bacterial blight"),
            ("Grapes", "अंगूर", "દ્રાક્ષ", "Fruits", "Perennial", "Deep well-drained sandy loam", "Medium (500–800 mm)", 365, 12, 36, 400, 900, 6.5, 7.5, "20 - 35 tonnes/ha", "/crops/grapes.jpg", "Grape seed oil & pomace compost", "Downy mildew"),

            # Spices
            ("Turmeric", "हल्दी", "હળદર", "Spices", "Monsoon / Kharif", "Well-drained sandy / clay loam", "High (1000–1500 mm)", 240, 20, 36, 900, 1600, 6.0, 7.5, "20 - 28 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Turmeric%20plant.jpg", "Turmeric spent waste for organic mulch", "Rhizome rot"),
            ("Ginger", "अदरक", "આદુ", "Spices", "Monsoon / Kharif", "Rich friable humus loam", "High (1200–1800 mm)", 240, 18, 35, 1000, 1800, 5.5, 6.5, "15 - 22 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Ginger%20plant.jpg", "Ginger residue for essential oil distillation", "Soft rot"),
            ("Cumin", "जीरा", "જીરું", "Spices", "Rabi (Winter)", "Well-drained loamy soil", "Low (200–350 mm)", 110, 10, 28, 150, 400, 6.5, 8.0, "0.6 - 1.0 tonnes/ha", "/crops/user-provided/cumin.jpeg", "Cumin straw for aroma oil", "Wilt, Alternaria blight"),
            ("Coriander", "धनिया", "ધાણા", "Spices", "Rabi / Winter", "Deep fertile loamy soil", "Low–Medium (300–500 mm)", 90, 10, 30, 250, 550, 6.0, 7.5, "1.0 - 1.5 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Coriander%20seeds.jpg", "Herbal waste for compost", "Powdery mildew"),
            ("Black Pepper", "काली मिर्च", "મરી", "Spices", "Perennial", "Red laterite / clay loam rich in humus", "Very High (1500–2500 mm)", 365, 18, 35, 1400, 3000, 5.5, 6.5, "1.5 - 2.5 tonnes/ha", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Black%20Pepper%20(Piper%20nigrum)%20fruits.jpg", "Pepper husks for oleoresin", "Quick wilt"),
            ("Mustard", "सरसों", "રાઈ", "Spices", "Rabi (Winter)", "Light to medium loam", "Low (250–450 mm)", 105, 10, 28, 200, 500, 6.0, 7.5, "1.2 - 2.0 tonnes/ha", "/crops/user-provided/mustard.jpeg", "Mustard cake for organic fertilizer & animal feed", "White rust, Aphids")
        ]

        for item in crops_data:
            crop = CropModel(
                name=item[0],
                hindi_name=item[1],
                gujarati_name=item[2],
                category=item[3],
                season=item[4],
                soil_type=item[5],
                water_req=item[6],
                duration_days=item[7],
                min_temp=item[8],
                max_temp=item[9],
                min_rainfall=item[10],
                max_rainfall=item[11],
                ideal_ph_min=item[12],
                ideal_ph_max=item[13],
                expected_yield=item[14],
                image_url=item[15],
                byproducts=item[16],
                common_pests=item[17]
            )
            db.add(crop)

        # Seed Planner Tasks
        tasks_data = [
            ("Field A", "Wheat", "28 Aug", "15 Dec", "Sowing window", 25, 35, "Rain window detected", "Based on rainfall forecast, consider sowing pearl millet or wheat after the next suitable rain window."),
            ("Field B", "Tomato", "10 Aug", "25 Nov", "First irrigation", 58, 42, "No rain expected next 3 days", "Apply 15mm drip irrigation tomorrow morning."),
            ("Field C", "Cotton", "01 Jun", "30 Oct", "Boll Formation", 70, 50, "Pest alert in district", "Inspect lower leaves for pink bollworm larvae."),
        ]
        for t in tasks_data:
            task = PlannerTaskModel(
                field_name=t[0],
                crop_name=t[1],
                sowing_date=t[2],
                expected_harvest=t[3],
                stage_name=t[4],
                progress_pct=t[5],
                soil_moisture_pct=t[6],
                weather_alert=t[7],
                daily_recommendation=t[8]
            )
            db.add(task)

        # Seed Mandi Prices
        mandi_data = [
            ("Gujarat", "Ahmedabad", "Bavla Mandi", "Wheat", "Lokwan", 2400.0, 2750.0, 2600.0, "2026-08-24"),
            ("Gujarat", "Ahmedabad", "Sanand Mandi", "Cotton", "Shankar-6", 6800.0, 7400.0, 7150.0, "2026-08-24"),
            ("Gujarat", "Rajkot", "Rajkot APMC", "Groundnut", "Bold", 5800.0, 6500.0, 6200.0, "2026-08-24"),
            ("Gujarat", "Mehsana", "Unjha APMC", "Cumin", "Super Fine", 21000.0, 24500.0, 23000.0, "2026-08-24"),
            ("Punjab", "Ludhiana", "Ludhiana APMC", "Paddy", "Basmati 1121", 3800.0, 4400.0, 4150.0, "2026-08-24"),
            ("Maharashtra", "Nashik", "Lasalgaon Mandi", "Onion", "Red Onion", 1400.0, 2100.0, 1850.0, "2026-08-24"),
        ]
        for m in mandi_data:
            mandi = MandiPriceModel(
                state=m[0], district=m[1], market=m[2],
                commodity=m[3], variety=m[4],
                min_price=m[5], max_price=m[6], modal_price=m[7],
                arrival_date=m[8]
            )
            db.add(mandi)

        # Seed Government Schemes
        schemes_data = [
            (
                "PM-KISAN",
                "Pradhan Mantri Kisan Samman Nidhi",
                "Income support",
                "Direct income support of ₹6,000 per year in three equal installments to eligible landholding farmer families.",
                "Direct benefit transfer of ₹6,000/year to bank account via Aadhaar-linked account.",
                "₹6,000 / year",
                "All landholding farmers with cultivable land up to standard limits, subject to exclusion criteria for high income tax payers.",
                "Aadhaar Card, Land Ownership Document (Khatian/7-12 extract), Bank Account Passbook",
                "https://pmkisan.gov.in/"
            ),
            (
                "PMFBY",
                "Pradhan Mantri Fasal Bima Yojana",
                "Crop insurance",
                "Comprehensive crop insurance coverage against non-preventable natural risks from pre-sowing to post-harvest.",
                "Low premium rate (1.5% for Rabi, 2% for Kharif, 5% for commercial crops) with full claim payout for yield losses.",
                "Up to 100% Crop Value Compensation",
                "All farmers including sharecroppers and tenant farmers growing notified crops in notified areas.",
                "Aadhaar Card, Land Sowing Certificate, Bank Passbook, Land Record Document",
                "https://pmfby.gov.in/"
            ),
            (
                "PM-KUSUM",
                "PM Kisan Urja Suraksha evam Utthaan Mahabhiyan",
                "Solar irrigation",
                "Subsidy up to 60% for installing standalone solar agriculture pumps and solarizing grid-connected agriculture pumps.",
                "Subsidized solar pump sets (3 HP to 10 HP) and extra income by selling surplus solar power back to the grid.",
                "60% Government Subsidy",
                "Individual farmers, water user associations, cooperatives, and panchayats having valid agricultural land.",
                "Aadhaar, Land Registry Document, Electricity Connection Bill (if applicable), Bank Details",
                "https://pmkusum.mnre.gov.in/"
            ),
            (
                "SOIL-HEALTH",
                "Soil Health Card Scheme",
                "Soil testing",
                "Biennial soil testing to provide customized nutrient recommendations (N, P, K, micro-nutrients) for optimal fertilizer use.",
                "Free soil testing report card with customized fertilizer dose recommendation for target yield.",
                "Free Soil Nutrient Analysis",
                "All farmers across India possessing agricultural land holdings.",
                "Aadhaar Card, Field Location Coordinates / Khasra Number",
                "https://soilhealth.dac.gov.in/"
            )
        ]
        for s in schemes_data:
            scheme = GovernmentSchemeModel(
                code=s[0], title=s[1], category=s[2],
                short_description=s[3], full_description=s[4],
                benefit_amount=s[5], eligibility_criteria=s[6],
                required_documents=s[7], apply_url=s[8]
            )
            db.add(scheme)

        # Seed Disease Records
        disease_data = [
            (
                "Wheat", "Yellow Rust (Puccinia striiformis)",
                "Yellow pustules arranged in linear stripes on leaves.",
                "Fungal pathogen Puccinia striiformis",
                "Spray neem oil formulation (5 ml/L) or garlic extract spray.",
                "Apply Propiconazole 25 EC (1 ml/L) or Tebuconazole 250 EC.",
                "Plant resistant varieties like HD 2967 or PBW 550, follow recommended crop rotation."
            ),
            (
                "Tomato", "Early Blight (Alternaria solani)",
                "Concentric dark spots ('target spots') on lower leaves leading to yellowing.",
                "Fungal pathogen Alternaria solani",
                "Spray Trichoderma viride formulation (5g/L) or copper sulfate solution.",
                "Apply Mancozeb 75 WP (2.5g/L) or Chlorothalonil 75 WP.",
                "Mulch soil around plants, practice crop rotation, avoid overhead watering."
            ),
            (
                "Cotton", "Pink Bollworm (Pectinophora gossypiella)",
                "Rosetted flowers, lint staining, and internal boll destruction.",
                "Lepidopteran pest Pectinophora gossypiella",
                "Install Pheromone traps (5 traps/acre) and release Trichogramma egg parasitoids.",
                "Spray Emamectin benzoate 5 SG (0.5g/L) or Spinetoram 11.7 SC.",
                "Maintain closed season, destroy crop residue post-harvest, use Bt cotton hybrids."
            )
        ]
        for d in disease_data:
            record = DiseaseRecordModel(
                crop_name=d[0], disease_name=d[1], symptoms=d[2],
                cause=d[3], organic_treatment=d[4],
                chemical_treatment=d[5], preventive_measures=d[6]
            )
            db.add(record)

        db.commit()
        print("Database successfully seeded!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
