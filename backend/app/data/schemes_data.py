"""
Verified Government Agricultural Schemes Database for Growva.
All scheme details, benefits, eligibility rules, and official links are sourced
from official Government of India and State Government portals.
Last Verified: August 2026
"""

SCHEMES_DATABASE = [
    {
        "id": "pm-kisan",
        "code": "PM-KISAN",
        "name": "Pradhan Mantri Kisan Samman Nidhi",
        "shortName": "PM-KISAN",
        "category": "income_support",
        "categoryLabel": "Income Support",
        "description": "Central Sector Scheme providing financial support to all landholding farmer families across India to supplement crop health and domestic requirements.",
        "benefits": [
            "₹6,000 per year transferred directly to bank account (DBT)",
            "Distributed in 3 equal installments of ₹2,000 every 4 months",
            "100% funding by Government of India"
        ],
        "targetBeneficiaries": ["Landholding farmer families", "Small & Marginal Farmers"],
        "states": ["All States & UTs"],
        "eligibilityQuestions": [
            {
                "id": "owns_land",
                "type": "boolean",
                "question": "Do you or your family own cultivable agricultural land registered in land records?",
                "options": []
            },
            {
                "id": "is_taxpayer",
                "type": "boolean",
                "question": "Did any family member pay Income Tax in the last assessment year?",
                "options": []
            },
            {
                "id": "is_govt_pensioner",
                "type": "boolean",
                "question": "Are you or any family member a retired/serving government employee with pension > ₹10,000/month?",
                "options": []
            },
            {
                "id": "is_institutional",
                "type": "boolean",
                "question": "Is the agricultural land registered under an institutional landholder (trust/company)?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "owns_land", "operator": "equals", "value": True, "failureReason": "Cultivable land ownership registered in official land records is mandatory for PM-KISAN."},
            {"field": "is_taxpayer", "operator": "equals", "value": False, "failureReason": "Income Tax payers in the previous assessment year are excluded from PM-KISAN benefits."},
            {"field": "is_govt_pensioner", "operator": "equals", "value": False, "failureReason": "Government retirees/employees receiving pension > ₹10,000/month are excluded."},
            {"field": "is_institutional", "operator": "equals", "value": False, "failureReason": "Institutional landholders (companies, trusts) are excluded from family benefit scheme."}
        ],
        "requiredDocuments": [
            "Aadhaar Card linked with Mobile Number",
            "Proof of Landholding (7/12, Khatauni or Jamabandi)",
            "Active Savings Bank Account details (Aadhaar Seeded / NPCI linked)",
            "e-KYC Completion Certificate via PM-KISAN portal/CSC"
        ],
        "applicationSteps": [
            "Visit the official PM-KISAN portal (pmkisan.gov.in) or your nearest Common Service Centre (CSC).",
            "Click on 'New Farmer Registration' and enter your Aadhaar number and state.",
            "Fill in land records details (Survey/Khasra number, District, Sub-district, Khatauni).",
            "Upload digital copies of land documents and submit the application.",
            "Complete mandatory face/OTP e-KYC on the portal."
        ],
        "officialWebsite": "https://pmkisan.gov.in",
        "officialSourceName": "Ministry of Agriculture & Farmers Welfare, Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "pmfby",
        "code": "PMFBY",
        "name": "Pradhan Mantri Fasal Bima Yojana",
        "shortName": "PMFBY",
        "category": "insurance",
        "categoryLabel": "Crop Insurance",
        "description": "Comprehensive yield-based crop insurance scheme covering non-preventable natural risks from pre-sowing to post-harvest for notified crops in notified areas.",
        "benefits": [
            "Comprehensive risk cover against Drought, Flood, Pest, Disease & Unseasonal Rain",
            "Low fixed farmer premium: 2% for Kharif crops, 1.5% for Rabi crops, 5% for Commercial/Horticultural crops",
            "Balance premium subsidized equally by Central and State Governments"
        ],
        "targetBeneficiaries": ["All Farmers", "Loanee Farmers", "Non-Loanee Farmers", "Sharecroppers & Tenant Farmers"],
        "states": ["Participating States & UTs"],
        "eligibilityQuestions": [
            {
                "id": "crop_notified",
                "type": "boolean",
                "question": "Is your crop cultivated in a notified area specified by your state government?",
                "options": []
            },
            {
                "id": "season",
                "type": "select",
                "question": "Which crop season are you applying for?",
                "options": ["Kharif", "Rabi", "Commercial / Horticultural"]
            },
            {
                "id": "has_insurable_interest",
                "type": "boolean",
                "question": "Are you cultivating the crop as land owner, tenant, or sharecropper with insurable interest?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "crop_notified", "operator": "equals", "value": True, "failureReason": "Crop insurance applies specifically to notified crops in notified insurance units/blocks."},
            {"field": "has_insurable_interest", "operator": "equals", "value": True, "failureReason": "Applicant must have insurable interest (actual cultivation as owner or documented tenant)."}
        ],
        "requiredDocuments": [
            "Aadhaar Card",
            "Land Possession Certificate / Sowing Certificate issued by Patwari/Talati",
            "Bank Passbook copy showing IFSC Code",
            "Tenant / Sharecropper agreement (if applicable)"
        ],
        "applicationSteps": [
            "Visit national crop insurance portal (pmfby.gov.in) or contact your bank branch / insurance intermediary.",
            "Select State, Season, Year, and Scheme name.",
            "Enter land details and crop sown in the current season.",
            "Pay the nominal farmer premium amount (1.5% - 5%) online or at CSC/Bank branch.",
            "Download and save the insurance policy receipt acknowledgement."
        ],
        "officialWebsite": "https://pmfby.gov.in",
        "officialSourceName": "Ministry of Agriculture & Farmers Welfare, Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "pm-kusum",
        "code": "PM-KUSUM",
        "name": "Pradhan Mantri Kisan Urja Suraksha evam Utthaan Mahabhiyan",
        "shortName": "PM-KUSUM",
        "category": "irrigation",
        "categoryLabel": "Solar Irrigation",
        "description": "Scheme to provide solar-powered irrigation pumps and grid-connected solar power plants to farmers for reliable daytime irrigation and extra income generation.",
        "benefits": [
            "Up to 60% total subsidy (30% Central + 30% State Govt) for standalone solar pumps",
            "Bank loan facility for up to 30% of project cost (farmer pays only 10% upfront)",
            "Uninterrupted daytime solar power for crop irrigation"
        ],
        "targetBeneficiaries": ["Individual Farmers", "Water User Associations", "Farmer Cooperatives", "Panchayats"],
        "states": ["All States"],
        "eligibilityQuestions": [
            {
                "id": "has_water_source",
                "type": "boolean",
                "question": "Do you have an accessible groundwater or surface water source on your agricultural land?",
                "options": []
            },
            {
                "id": "pump_requirement",
                "type": "select",
                "question": "What type of solar pump assistance do you require?",
                "options": ["Off-Grid Standalone Solar Pump", "Solarization of Existing Grid-Connected Pump", "Solar Power Plant on Barren/Fallow Land"]
            },
            {
                "id": "has_grid_connection",
                "type": "boolean",
                "question": "Does your farm location already have an electricity grid connection for irrigation?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "has_water_source", "operator": "equals", "value": True, "failureReason": "A verified groundwater/borewell or surface water source is required for solar pump installation."}
        ],
        "requiredDocuments": [
            "Aadhaar Card",
            "7/12 Land ownership records / Title deed",
            "Borewell / Water source verification certificate",
            "Bank Account Passbook",
            "Passport size photograph"
        ],
        "applicationSteps": [
            "Access the official state nodal renewable energy agency portal (e.g. GEDA in Gujarat, REDA in states) or PM-KUSUM portal (pmkusum.mnre.gov.in).",
            "Submit online application under Component B (Standalone Off-Grid Pump) or Component C (Solarization).",
            "Pay the 10% farmer share deposit after field survey verification.",
            "Nodal agency installs solar panels and pump set on farm location."
        ],
        "officialWebsite": "https://pmkusum.mnre.gov.in",
        "officialSourceName": "Ministry of New and Renewable Energy (MNRE), Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "soil-health-card",
        "code": "SHC",
        "name": "Soil Health Card Scheme",
        "shortName": "Soil Health Card",
        "category": "soil",
        "categoryLabel": "Soil Health",
        "description": "National scheme providing customized soil health status cards to farmers every 2 years, containing crop-wise fertilizer and micronutrient recommendations.",
        "benefits": [
            "Free comprehensive soil sample laboratory testing (12 essential soil parameters)",
            "Tailored nutrient recommendations (Macro: N, P, K; Micro: Zinc, Boron, Iron, Manganese, Copper)",
            "Reduces fertilizer costs by 15-20% through balanced fertilizer application"
        ],
        "targetBeneficiaries": ["All Farmers across India"],
        "states": ["All States & UTs"],
        "eligibilityQuestions": [
            {
                "id": "cultivates_land",
                "type": "boolean",
                "question": "Are you currently cultivating agricultural land?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "cultivates_land", "operator": "equals", "value": True, "failureReason": "Available to all active farmers cultivating agricultural land."}
        ],
        "requiredDocuments": [
            "Aadhaar Card / Farmer ID",
            "Farm Survey Number / Khasra details",
            "Contact Mobile Number"
        ],
        "applicationSteps": [
            "Contact your local Agriculture Officer, Gram Sevak, or Krishi Vigyan Kendra (KVK).",
            "Soil samples are collected by agriculture department officials from your field grid (2.5 ha irrigated / 10 ha rainfed).",
            "Lab analysis is performed at district soil testing laboratories.",
            "Download or collect your printed Soil Health Card from soilhealth.dac.gov.in or Gram Panchayat."
        ],
        "officialWebsite": "https://soilhealth.dac.gov.in",
        "officialSourceName": "Department of Agriculture & Farmers Welfare, Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "kcc",
        "code": "KCC",
        "name": "Kisan Credit Card Scheme",
        "shortName": "Kisan Credit Card",
        "category": "credit",
        "categoryLabel": "Agricultural Credit",
        "description": "Provides adequate and timely institutional credit from banks to farmers for crop cultivation, post-harvest expenses, maintenance of farm assets, and allied activities.",
        "benefits": [
            "Concessional interest rate of 7% per annum for crop loans up to ₹3 Lakh",
            "3% Interest Subvention for prompt repayment (effective net interest rate only 4%)",
            "Collateral-free agricultural loans up to ₹1.60 Lakh"
        ],
        "targetBeneficiaries": ["Owner Cultivators", "Tenant Farmers", "Sharecroppers", "Self Help Groups (SHGs)", "Animal Husbandry & Fishery Farmers"],
        "states": ["All States & UTs"],
        "eligibilityQuestions": [
            {
                "id": "farmer_category",
                "type": "select",
                "question": "Select your farming occupation category:",
                "options": ["Individual Land Owner", "Tenant Farmer / Sharecropper", "Joint Borrower Group", "Animal Husbandry / Fisheries Farmer"]
            },
            {
                "id": "has_existing_default",
                "type": "boolean",
                "question": "Do you have any active willful default on existing institutional bank loans?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "has_existing_default", "operator": "equals", "value": False, "failureReason": "Applicants with active bank defaults must clear outstanding dues prior to new KCC sanction."}
        ],
        "requiredDocuments": [
            "Duly filled KCC Application Form",
            "Aadhaar Card & PAN Card",
            "Land Holding Proof (7/12, Khatauni / Revenue documents)",
            "Crop Sowing Certificate / Cropping Pattern declaration",
            "No Dues Certificate from neighbouring bank branches (for fresh applicants)"
        ],
        "applicationSteps": [
            "Download KCC application form from bank portal or myscheme.gov.in or visit commercial bank/Cooperative bank/RRB branch.",
            "Fill in crop land details, proposed cropping schedule, and credit requirement.",
            "Attach land documents and Aadhaar copy.",
            "Bank verifies land records and sanctions KCC limit & issue Smart Card/Debit Card within 14 working days."
        ],
        "officialWebsite": "https://myscheme.gov.in/schemes/kcc",
        "officialSourceName": "Reserve Bank of India (RBI) & NABARD",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "e-nam",
        "code": "e-NAM",
        "name": "National Agriculture Market (e-NAM)",
        "shortName": "e-NAM",
        "category": "market",
        "categoryLabel": "Market Access",
        "description": "Pan-India electronic trading portal networking existing APMC mandis to create a unified national market for agricultural commodities with transparent online bidding.",
        "benefits": [
            "Direct access to nationwide buyers without middlemen interference",
            "Transparent electronic bidding and price discovery based on quality testing",
            "Direct Online Payment directly into farmer's bank account (DBT)"
        ],
        "targetBeneficiaries": ["All Farmers", "Traders", "Commission Agents", "Farmer Producer Organizations (FPOs)"],
        "states": ["23 States and 4 UTs integrated"],
        "eligibilityQuestions": [
            {
                "id": "has_apmc_mandi",
                "type": "boolean",
                "question": "Are you selling agricultural produce at an e-NAM integrated APMC Mandi?",
                "options": []
            },
            {
                "id": "has_bank_account",
                "type": "boolean",
                "question": "Do you have an active bank account linked with Aadhaar?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "has_bank_account", "operator": "equals", "value": True, "failureReason": "An active Aadhaar-linked bank account is necessary to receive direct e-NAM online sale proceeds."}
        ],
        "requiredDocuments": [
            "Aadhaar Card",
            "Bank Account Passbook (IFSC code)",
            "APMC Farmer Passbook / Registration ID",
            "Mobile Number for SMS transaction alerts"
        ],
        "applicationSteps": [
            "Register on e-NAM portal (enam.gov.in) or mobile app or at the e-NAM gate entry counter in your APMC mandi.",
            "Bring your harvested produce to the e-NAM Mandi for electronic assaying (quality testing).",
            "Lot details and quality parameters are uploaded for online bidding across national traders.",
            "Accept high bid price and receive direct online payment into your bank account."
        ],
        "officialWebsite": "https://enam.gov.in",
        "officialSourceName": "Small Farmers Agribusiness Consortium (SFAC), Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "pmksy-pdmc",
        "code": "PMKSY-PDMC",
        "name": "Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop",
        "shortName": "PMKSY Micro-Irrigation",
        "category": "irrigation",
        "categoryLabel": "Micro-Irrigation",
        "description": "Focuses on enhancing water use efficiency at farm level through micro-irrigation technologies (Drip and Sprinkler irrigation systems).",
        "benefits": [
            "55% subsidy for Small & Marginal Farmers (< 2 Ha landholding)",
            "45% subsidy for Other Category Farmers",
            "Saves up to 40-50% water while increasing crop productivity by 20-30%"
        ],
        "targetBeneficiaries": ["Small & Marginal Farmers", "All Landholding Farmers", "Members of Water User Associations"],
        "states": ["All States"],
        "eligibilityQuestions": [
            {
                "id": "owns_or_leases_land",
                "type": "boolean",
                "question": "Do you own or hold long-term lease land with an assured water source?",
                "options": []
            },
            {
                "id": "land_acres",
                "type": "number",
                "question": "What is your total land holding size in acres?",
                "unit": "acres"
            }
        ],
        "eligibilityRules": [
            {"field": "owns_or_leases_land", "operator": "equals", "value": True, "failureReason": "Assured land possession and water source (borewell, canal, pond) are required."}
        ],
        "requiredDocuments": [
            "7/12 Land extract & 8-A khatauni",
            "Aadhaar Card",
            "Water & Electricity source proof",
            "Soil & Water testing report",
            "Quotation from authorized Micro-Irrigation vendor"
        ],
        "applicationSteps": [
            "Apply online through state horticulture/agriculture department portal (e.g., Gujarat GGRC portal or state PMKSY portal).",
            "Select MI vendor and upload farm map and crop details.",
            "Field inspection is conducted by department officer.",
            "System installation completed; subsidy released directly to vendor/farmer."
        ],
        "officialWebsite": "https://pmksy.gov.in",
        "officialSourceName": "Department of Agriculture & Farmers Welfare, Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "pkvy",
        "code": "PKVY",
        "name": "Paramparagat Krishi Vikas Yojana",
        "shortName": "PKVY Organic",
        "category": "organic_farming",
        "categoryLabel": "Organic Farming",
        "description": "Promotes organic farming through adoption of organic village clusters and Participatory Guarantee System (PGS) organic certification.",
        "benefits": [
            "Financial assistance of ₹50,000 per hectare over 3 years",
            "₹31,000/ha incentive provided directly to farmer for organic inputs (seeds, bio-fertilizers, neem cake)",
            "Free PGS-India organic certification and value addition branding support"
        ],
        "targetBeneficiaries": ["Farmer Groups / Clusters", "Individual Organic Farmers"],
        "states": ["All States"],
        "eligibilityQuestions": [
            {
                "id": "willing_organic",
                "type": "boolean",
                "question": "Are you willing to adopt 100% chemical-free organic farming practices?",
                "options": []
            },
            {
                "id": "in_farmer_cluster",
                "type": "boolean",
                "question": "Are you part of or willing to join a local cluster of 20+ farmers (total min 20 ha land)?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "willing_organic", "operator": "equals", "value": True, "failureReason": "Applicant must commit to chemical-free organic farming standards."}
        ],
        "requiredDocuments": [
            "Aadhaar Card",
            "Land title proof",
            "Bank Passbook details",
            "Cluster Member Group Declaration Form"
        ],
        "applicationSteps": [
            "Contact District Agriculture Officer or Regional Executive Agency.",
            "Form a cluster of 20 or more farmers in a contiguous area.",
            "Register group on PGS-India portal (pgsindia-ncof.gov.in).",
            "Receive direct input assistance and organic conversion training."
        ],
        "officialWebsite": "https://pgsindia-ncof.gov.in",
        "officialSourceName": "National Centre of Organic Farming (NCOF), Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "aif",
        "code": "AIF",
        "name": "Agriculture Infrastructure Fund",
        "shortName": "Agri Infra Fund",
        "category": "infrastructure",
        "categoryLabel": "Infrastructure",
        "description": "Medium-to-long term debt financing facility for investment in viable post-harvest management infrastructure and community farming assets.",
        "benefits": [
            "3% per annum Interest Subvention on loans up to ₹2 Crore for up to 7 years",
            "Credit Guarantee coverage under CGTMSE scheme for loans up to ₹2 Crore",
            "Covers Warehouses, Cold Chains, Processing units, Assaying units & Packhouses"
        ],
        "targetBeneficiaries": ["Farmers", "Agri-Entrepreneurs", "Startups", "FPOs", "Primary Agricultural Credit Societies (PACS)"],
        "states": ["All States"],
        "eligibilityQuestions": [
            {
                "id": "project_type",
                "type": "select",
                "question": "Select proposed infrastructure project type:",
                "options": ["Warehouse / Cold Storage / Silo", "Sorting / Grading / Assaying Unit", "Solar Power / Custom Hiring Centre", "Primary Processing / Drying Unit"]
            },
            {
                "id": "has_dpr",
                "type": "boolean",
                "question": "Do you have a detailed project report (DPR) or bank loan proposal ready?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "has_dpr", "operator": "equals", "value": True, "failureReason": "A project proposal or DPR for post-harvest infrastructure is required for bank loan sanction."}
        ],
        "requiredDocuments": [
            "Aadhaar & PAN Card",
            "Detailed Project Report (DPR)",
            "Land Ownership / Lease Agreement (min 10 years)",
            "Bank Account Statement (last 6 months)",
            "Entity Registration / FPO Certificate (if applicable)"
        ],
        "applicationSteps": [
            "Register on AIF portal (agriinfra.gov.in).",
            "Upload project profile, DPR, and select preferred lending bank.",
            "Application is screened online and routed to selected bank for credit evaluation.",
            "Upon loan sanction, 3% interest subvention is automatically credited to loan account."
        ],
        "officialWebsite": "https://agriinfra.gov.in",
        "officialSourceName": "Ministry of Agriculture & Farmers Welfare, Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "smam",
        "code": "SMAM",
        "name": "Sub-Mission on Agricultural Mechanization",
        "shortName": "SMAM Mechanization",
        "category": "mechanization",
        "categoryLabel": "Mechanization",
        "description": "Promotes agricultural mechanization among small and marginal farmers through individual equipment subsidies and Custom Hiring Centres (CHCs).",
        "benefits": [
            "40% to 50% subsidy on individual farm machinery (Tractors, Rotavators, Harvesters, Tillers)",
            "Up to 80% financial assistance for setting up Custom Hiring Centres (CHCs)",
            "Special higher financial assistance for SC, ST, Small/Marginal, and Women farmers"
        ],
        "targetBeneficiaries": ["Small & Marginal Farmers", "Women Farmers", "SC/ST Farmers", "CHCs & Cooperative Societies"],
        "states": ["All States & UTs"],
        "eligibilityQuestions": [
            {
                "id": "machinery_type",
                "type": "select",
                "question": "Select equipment category requested:",
                "options": ["Tractor / Power Tiller", "Rotavator / Seed Drill / Cultivator", "Combine Harvester / Baler", "Custom Hiring Centre Establishment"]
            },
            {
                "id": "owns_land_mechanization",
                "type": "boolean",
                "question": "Do you hold registered agricultural land in land records?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "owns_land_mechanization", "operator": "equals", "value": True, "failureReason": "Land title proof in agricultural records is required for individual equipment subsidy."}
        ],
        "requiredDocuments": [
            "Aadhaar Card",
            "7/12 Land Record / Khatauni",
            "Caste Certificate (for SC/ST benefit enhancement)",
            "Bank Passbook copy",
            "Proforma Invoice / Quotation from registered machinery manufacturer/dealer"
        ],
        "applicationSteps": [
            "Register on Direct Benefit Transfer in Agricultural Mechanization portal (agrimachinery.nic.in).",
            "Select machine type, manufacturer, and authorized local dealer.",
            "Upload land records and proforma invoice.",
            "After district committee sanction and purchase verification, subsidy is credited to bank account."
        ],
        "officialWebsite": "https://agrimachinery.nic.in",
        "officialSourceName": "Department of Agriculture & Farmers Welfare, Govt of India",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "ikhedut-gujarat",
        "code": "IKHEDUT-GUJ",
        "name": "Gujarat i-Khedut Farm Subsidy Portal",
        "shortName": "i-Khedut Gujarat",
        "category": "mechanization",
        "categoryLabel": "State Subsidy",
        "description": "Single window online portal by Govt of Gujarat for farmers in Gujarat to apply for state agricultural schemes, implements, tractor subsidies, and pipe lines.",
        "benefits": [
            "Subsidies on farm implements (Rotavator, Thresher, Cultivator, Seed Drill)",
            "Financial aid for farm fencing (Barbed wire fencing assistance)",
            "Subsidies for water storage tanks, underground pipelines, and seed mini-kits"
        ],
        "targetBeneficiaries": ["Landholding Farmers in Gujarat", "Small & Marginal Farmers of Gujarat"],
        "states": ["Gujarat"],
        "eligibilityQuestions": [
            {
                "id": "is_gujarat_resident",
                "type": "boolean",
                "question": "Are you a resident farmer holding agricultural land in Gujarat?",
                "options": []
            },
            {
                "id": "has_712_8a",
                "type": "boolean",
                "question": "Do you have valid 7/12 and 8-A land record documents for your Gujarat farm?",
                "options": []
            }
        ],
        "eligibilityRules": [
            {"field": "is_gujarat_resident", "operator": "equals", "value": True, "failureReason": "i-Khedut schemes are strictly applicable to farmers owning agricultural land in Gujarat state."},
            {"field": "has_712_8a", "operator": "equals", "value": True, "failureReason": "Valid 7/12 & 8-A revenue records from Gujarat land portal are mandatory."}
        ],
        "requiredDocuments": [
            "Aadhaar Card",
            "Latest 7/12 and 8-A Land Extract (AnyRoR Gujarat)",
            "Bank Account Passbook (Gujarat Bank branch)",
            "Caste Certificate (if applying under SC/ST quota)"
        ],
        "applicationSteps": [
            "Visit Gujarat i-Khedut Portal (ikhedut.gujarat.gov.in).",
            "Select active agricultural / horticulture scheme from list.",
            "Fill in 7/12 survey details, Aadhaar number, and bank details.",
            "Submit application and print acknowledgement receipt.",
            "Submit physical copies to Gram Sevak / District Agriculture Officer."
        ],
        "officialWebsite": "https://ikhedut.gujarat.gov.in",
        "officialSourceName": "Department of Agriculture, Farmers Welfare & Co-operation, Govt of Gujarat",
        "sourceLastVerified": "Aug 2026",
        "active": True
    },
    {
        "id": "mmksy-gujarat",
        "code": "MMKSY-GUJ",
        "name": "Mukhya Mantri Kisan Sahay Yojana (Gujarat)",
        "shortName": "MMKSY Gujarat",
        "category": "insurance",
        "categoryLabel": "Crop Relief",
        "description": "State crop compensation scheme by Gujarat Government offering financial relief to farmers suffering crop loss due to drought, unseasonal rainfall, or heavy rains.",
        "benefits": [
            "Zero farmer premium required (100% state funded relief assistance)",
            "₹20,000 per hectare assistance for crop loss between 33% and 60% (max 4 hectares)",
            "₹25,000 per hectare assistance for crop loss above 60% (max 4 hectares)"
        ],
        "targetBeneficiaries": ["All Landholding Farmers in Gujarat"],
        "states": ["Gujarat"],
        "eligibilityQuestions": [
            {
                "id": "is_gujarat_farmer",
                "type": "boolean",
                "question": "Do you hold cultivable land in a Gujarat district affected by natural calamity?",
                "options": []
            },
            {
                "id": "crop_damage_pct",
                "type": "select",
                "question": "What is the estimated crop damage percentage in your field?",
                "options": ["Below 33%", "Between 33% and 60%", "Above 60%"]
            }
        ],
        "eligibilityRules": [
            {"field": "is_gujarat_farmer", "operator": "equals", "value": True, "failureReason": "Applicable to registered landholding farmers in calamity-declared talukas of Gujarat."},
            {"field": "crop_damage_pct", "operator": "not_equals", "value": "Below 33%", "failureReason": "Minimum 33% verified crop damage is required to trigger financial compensation."}
        ],
        "requiredDocuments": [
            "Aadhaar Card",
            "7/12 & 8-A Revenue Record",
            "Bank Account Passbook copy",
            "Crop Sowing / Loss Declaration Form verified by Talati"
        ],
        "applicationSteps": [
            "When calamity is declared, apply via i-Khedut portal or e-Gram Kendra in your village.",
            "Submit survey number and crop loss detail form.",
            "Joint survey team (Agriculture officer + Revenue Talati) inspects field.",
            "Approved assistance is directly transferred to bank account."
        ],
        "officialWebsite": "https://ikhedut.gujarat.gov.in",
        "officialSourceName": "Revenue Department & Agriculture Department, Govt of Gujarat",
        "sourceLastVerified": "Aug 2026",
        "active": True
    }
]
