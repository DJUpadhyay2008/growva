from app.schemas.byproduct import ByProduct, Application, ScoreFactors, ValueRange

BYPRODUCTS_DATABASE = [
    ByProduct(
        id="rice_straw",
        sourceCrop="Rice",
        residueName="Rice Straw",
        description="Abundant post-harvest paddy straw rich in lignocellulose and silica, ideal for mushroom cultivation, bioenergy, and eco-packaging.",
        residueFactor=1.40,
        residueFactorSource="ICAR - Indian Agricultural Research Institute (IARI) Residue Ratios 2024",
        processingDifficulty="medium",
        requiredProcessing=["Collection & Baling", "Sun Drying", "Chopping / Shredding", "Substrate Pasteurization"],
        demandLevel="high",
        opportunityScore=84,
        scoreFactors=ScoreFactors(
            availability=95,
            demand=85,
            processingEffort=72,
            localSuitability=84
        ),
        valueRange=ValueRange(min=1200, max=2500, unit="₹ / tonne"),
        valueSource="Regional Biomass Aggregators & Mushroom Farm Procurement Data",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Paddy Straw Mushroom Substrate",
                category="Mushroom Cultivation",
                description="Paddy straw is the premier substrate for growing Volvariella volvacea (paddy straw mushroom) and Pleurotus (oyster mushroom), generating high-value edible yields.",
                processingSteps=[
                    "Harvest straw and dry to under 12% moisture content.",
                    "Chop straw into 3-5 cm pieces and soak in water for 12 hours.",
                    "Pasteurize with hot water (65°C) or chemical treatment for 4 hours.",
                    "Spawn with mushroom culture and incubate in dark humid room.",
                    "Harvest fresh mushrooms within 14-21 days."
                ],
                equipment=["Mechanical Straw Chopper", "Soaking Drums / Pasteurization Tank", "Spawn Trays"],
                marketChannel="Local Mushroom Growers, Agro-Processing Enterprises & Supermarkets",
                source="ICAR Directorate of Mushroom Research (DMR Solan)"
            ),
            Application(
                name="Biomass Fuel Pellets & Briquettes",
                category="Biomass",
                description="Densified paddy straw briquettes serve as green fuel for industrial boilers, brick kilns, and thermal power plants replacing coal.",
                processingSteps=[
                    "Collect field straw using tractor-mounted balers.",
                    "Shred straw to fine powder using hammer mill.",
                    "Compress under high pressure in mechanical briquetting press without chemical binders.",
                    "Cool and pack high-density briquettes."
                ],
                equipment=["Baler", "Hammer Mill", "Briquetting / Pelletizing Machine"],
                marketChannel="Industrial Boilers, Textile Units, Brick Kilns & Power Plants",
                source="Ministry of New and Renewable Energy (MNRE) Biomass Policy"
            ),
            Application(
                name="Organic Mulching & Farm Composting",
                category="Composting",
                description="Decomposed paddy straw enriched with fungal inoculants returns nitrogen, potassium, and organic carbon back into soil.",
                processingSteps=[
                    "Spread straw over farm beds or stack in 1.5m compost heaps.",
                    "Inoculate with Pusa Decomposer bio-fungal microbial solution.",
                    "Maintain 60% moisture and turn heap twice over 25 days.",
                    "Apply rich organic humus directly to crops."
                ],
                equipment=["Water Sprinklers", "Pusa Decomposer Microbial Packs"],
                marketChannel="On-Farm Soil Health & Local Organic Farmers",
                source="ICAR-IARI Pusa Decomposer Guidelines"
            ),
            Application(
                name="Eco-Friendly Molded Paper Packaging",
                category="Industrial Material",
                description="Pulp extracted from rice straw replaces tree wood pulp for manufacturing egg trays, fruit boxes, and biodegradable carry bags.",
                processingSteps=[
                    "Soda pulping of chopped straw to breakdown silica and lignin.",
                    "Bleaching and mechanical refining.",
                    "Thermoforming into molded bio-packaging products."
                ],
                equipment=["Paper Pulp Digester", "Hydrapulper", "Thermoforming Molding Dies"],
                marketChannel="Paper Mills & Sustainable Packaging Manufacturers",
                source="Central Pulp and Paper Research Institute (CPPRI)"
            )
        ]
    ),
    ByProduct(
        id="sugarcane_bagasse",
        sourceCrop="Sugarcane",
        residueName="Sugarcane Bagasse",
        description="Fibrous residue remaining after crushing sugarcane stalks. High energy content suitable for co-generation bio-power and eco-tableware.",
        residueFactor=0.33,
        residueFactorSource="Indian Sugar Mills Association (ISMA) Technical Digest",
        processingDifficulty="medium",
        requiredProcessing=["Drying", "Depithing", "Baling / Compaction", "Pulping"],
        demandLevel="high",
        opportunityScore=88,
        scoreFactors=ScoreFactors(
            availability=90,
            demand=92,
            processingEffort=78,
            localSuitability=92
        ),
        valueRange=ValueRange(min=1800, max=3200, unit="₹ / tonne"),
        valueSource="Sugar Mill Co-generation & Paper Industry Procurement",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Co-generation Bio-Power Generation",
                category="Biomass",
                description="High-calorific bagasse is burned in high-pressure boilers to generate steam and renewable electricity for captive use and grid export.",
                processingSteps=[
                    "Depith bagasse to separate high-density fiber from pith.",
                    "Dry bagasse to reduce moisture below 45%.",
                    "Feed directly into co-generation boiler combustion chamber."
                ],
                equipment=["Bagasse Depither", "Rotary Dryer", "High-Pressure Boiler Turbines"],
                marketChannel="Sugar Mills & State Electricity Grids",
                source="National Federation of Cooperative Sugar Factories"
            ),
            Application(
                name="Molded Biodegradable Tableware",
                category="Bio-Based Products",
                description="Chemical-free bagasse pulp is thermoformed into biodegradable plates, bowls, cups, and takeaway containers replacing single-use plastics.",
                processingSteps=[
                    "Refine bagasse fiber into eco-pulp.",
                    "Wash and dewater pulp slurry.",
                    "Hot-press mold into disposable tableware items."
                ],
                equipment=["Pulp Washing Plant", "Hydrapulper", "Automatic Molding Machines"],
                marketChannel="Food Packaging Companies & Export Distributors",
                source="CIPET Bio-Plastics Research Center"
            ),
            Application(
                name="Craft Paper & Corrugated Boxes",
                category="Industrial Material",
                description="Long bagasse fibers provide excellent tensile strength for manufacturing eco-paper, cardboard, and shipping cartons.",
                processingSteps=[
                    "Digestion of fibers with caustic soda.",
                    "Refining and web formation on Fourdrinier paper machine."
                ],
                equipment=["Chemical Digester", "Paper Making Machine"],
                marketChannel="Paper Mills & Packaging Box Units",
                source="Central Pulp and Paper Research Institute (CPPRI)"
            )
        ]
    ),
    ByProduct(
        id="cotton_stalks",
        sourceCrop="Cotton",
        residueName="Cotton Stalks",
        description="Woody, hard agricultural residue generated after cotton picking. Outstanding raw material for particleboards, biochar, and briquettes.",
        residueFactor=2.50,
        residueFactorSource="ICAR-Central Institute for Research on Cotton Technology (CIRCOT)",
        processingDifficulty="high",
        requiredProcessing=["Field Uprooting", "Chipping / Grinding", "Drying", "Pyrolysis / Compaction"],
        demandLevel="medium",
        opportunityScore=79,
        scoreFactors=ScoreFactors(
            availability=88,
            demand=76,
            processingEffort=65,
            localSuitability=87
        ),
        valueRange=ValueRange(min=1500, max=2800, unit="₹ / tonne"),
        valueSource="CIRCOT Industrial Demonstration Units",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Compressed Particleboard & Furniture Wood",
                category="Industrial Material",
                description="Cotton stalk chips bound with eco-resins produce high-density particleboards replacing natural timber in furniture manufacturing.",
                processingSteps=[
                    "Uproot cotton stalks and chip into uniform wood flakes.",
                    "Dry chips to 4% moisture content.",
                    "Mix with urea-formaldehyde resin and hot-press under 200°C."
                ],
                equipment=["Stalk Chipper", "Flash Dryer", "Hydraulic Hot Press"],
                marketChannel="Particleboard Manufacturers & Furniture Industries",
                source="ICAR-CIRCOT Mumbai Technical Manual"
            ),
            Application(
                name="Soil Carbon Biochar Production",
                category="Soil Amendment",
                description="Pyrolyzed cotton stalks produce porous biochar that increases soil water holding capacity and sequesters carbon for decades.",
                processingSteps=[
                    "Chop stalks into 5cm pieces.",
                    "Thermal pyrolysis in low-oxygen biochar kiln at 450°C.",
                    "Crush biochar and mix with farm compost before soil application."
                ],
                equipment=["Biochar Pyrolysis Kiln", "Grinder"],
                marketChannel="Soil Health Schemes & Organic Farming Cooperatives",
                source="ICAR-CRIDA Hyderabad Biochar Guidelines"
            )
        ]
    ),
    ByProduct(
        id="banana_pseudostem",
        sourceCrop="Banana",
        residueName="Banana Pseudostem",
        description="Moist, fibrous stem harvested after banana bunch cutting. Excellent source of high-tensile natural fiber, organic liquid fertilizer, and handcrafted paper.",
        residueFactor=1.80,
        residueFactorSource="ICAR-National Research Centre for Banana (NRCB Trichy)",
        processingDifficulty="medium",
        requiredProcessing=["Stem Splitting", "Mechanical Raspador Extraction", "Sap Pressing", "Fiber Washing & Drying"],
        demandLevel="high",
        opportunityScore=86,
        scoreFactors=ScoreFactors(
            availability=85,
            demand=90,
            processingEffort=78,
            localSuitability=91
        ),
        valueRange=ValueRange(min=3500, max=8000, unit="₹ / tonne (Fiber)"),
        valueSource="Navsari Agricultural University (NAU) Commercialization Cell",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Premium Textile & Handicraft Fiber",
                category="Bio-Based Products",
                description="Silky, strong natural plant fiber extracted from pseudostem sheaths used for weaving eco-textiles, rugs, ropes, and luxury handicrafts.",
                processingSteps=[
                    "Split harvested pseudostems longitudinally into sheaths.",
                    "Feed sheaths into mechanical raspador machine to scrape pulp away from fiber.",
                    "Wash extracted fiber in clean water and sun-dry.",
                    "Comb and spin into textile yarn."
                ],
                equipment=["Raspador Extraction Machine", "Fiber Washing Tank", "Comb & Spinning Wheel"],
                marketChannel="Textile Mills, Handicraft Exporters & Paper Craft Units",
                source="Navsari Agricultural University (NAU Gujarat)"
            ),
            Application(
                name="Enriched Organic Liquid Bio-Fertilizer (Sap)",
                category="Soil Amendment",
                description="Nutrient-dense sap squeezed during fiber extraction is rich in Potassium (K), Cytokinins, and micronutrients.",
                processingSteps=[
                    "Collect squeezed sap during sheath pressing.",
                    "Filter out coarse suspended particles.",
                    "Enrich with beneficial azotobacter and PSB bio-fertilizers.",
                    "Bottle for foliar spray on crops."
                ],
                equipment=["Screw Press Sap Extractor", "Filtering Tanks", "Bottling Line"],
                marketChannel="Horticulture Farmers, Nurseries & Agro-Inputs Stores",
                source="ICAR-NRCB Bio-Input Technology"
            )
        ]
    ),
    ByProduct(
        id="groundnut_shells",
        sourceCrop="Groundnut",
        residueName="Groundnut Shells",
        description="Dry, rigid pods remaining after peanut decortication. Excellent calorific value for industrial boiler fuel and poultry litter bedding.",
        residueFactor=0.30,
        residueFactorSource="ICAR-Directorate of Groundnut Research (DGR Junagadh)",
        processingDifficulty="low",
        requiredProcessing=["Screening", "Crushing / Briquetting", "Bagging"],
        demandLevel="high",
        opportunityScore=85,
        scoreFactors=ScoreFactors(
            availability=88,
            demand=88,
            processingEffort=90,
            localSuitability=84
        ),
        valueRange=ValueRange(min=2000, max=3500, unit="₹ / tonne"),
        valueSource="Oil Mill Decortication & Industrial Boiler Fuel Buyers",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Boiler Fuel Briquettes & Pellets",
                category="Biomass",
                description="Groundnut shells possess high calorific value (~4000 kcal/kg) and low ash content, making them ideal industrial boiler fuel.",
                processingSteps=[
                    "Screen shells to remove dirt and extraneous matter.",
                    "Compress in hydraulic briquetting press.",
                    "Package high-density briquettes for dispatch."
                ],
                equipment=["Vibrating Screen", "Briquetting Machine"],
                marketChannel="Industrial Boilers, Textile Processing & Chemical Units",
                source="Sardar Krushinagar Dantiwada Agricultural University"
            ),
            Application(
                name="Absorbent Poultry Litter Bedding",
                category="Animal Feed",
                description="Coarsely crushed shells absorb moisture efficiently, keeping poultry farm floors dry and hygienic.",
                processingSteps=[
                    "Crush shells into 5-10 mm particles.",
                    "Dust removal via cyclone separator.",
                    "Bag for poultry farm distribution."
                ],
                equipment=["Crusher", "Dust Extractor", "Bagging Machine"],
                marketChannel="Commercial Poultry Farms & Layer Hatcheries",
                source="ICAR-DGR Junagadh Advisory"
            )
        ]
    ),
    ByProduct(
        id="mustard_cake",
        sourceCrop="Mustard",
        residueName="Mustard Cake",
        description="Nutrient-dense press cake left after mustard seed oil extraction. Packed with nitrogen, glucosinolates, and organic proteins.",
        residueFactor=0.60,
        residueFactorSource="Oil Technological Association of India (OTAI)",
        processingDifficulty="low",
        requiredProcessing=["Oil Pressing Extraction", "Pulverizing", "Packaging"],
        demandLevel="high",
        opportunityScore=91,
        scoreFactors=ScoreFactors(
            availability=92,
            demand=95,
            processingEffort=92,
            localSuitability=85
        ),
        valueRange=ValueRange(min=18000, max=24000, unit="₹ / tonne"),
        valueSource="Mandi Mustard Oil Mill By-Product Quotations",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Organic Bio-Pesticide & Nematicide Soil Treatment",
                category="Soil Amendment",
                description="Glucosinolates in mustard cake break down into natural isothiocyanates in moist soil, suppressing soil-borne nematodes, fungi, and termites.",
                processingSteps=[
                    "Grind mustard cake into fine meal powder.",
                    "Incorporate 100 kg/acre into soil during land preparation 15 days before sowing.",
                    "Irrigate lightly to trigger natural bio-fumigation."
                ],
                equipment=["Cake Pulverizer / Grinder"],
                marketChannel="Organic Vegetable Growers & Horticulture Orchards",
                source="ICAR-Directorate of Rapeseed-Mustard Research (DRMR Bharatpur)"
            ),
            Application(
                name="Protein Enriched Cattle Feed Supplement",
                category="Animal Feed",
                description="Mustard cake contains 35-38% crude protein and essential amino acids for dairy cattle nutrition.",
                processingSteps=[
                    "Debittering / heat treatment to lower allylisothiocyanate content.",
                    "Mix with cereal grains and mineral mixture into feed pellets."
                ],
                equipment=["Feed Pelletizer", "Mixer"],
                marketChannel="Dairy Cooperatives & Feed Compounders",
                source="National Dairy Development Board (NDDB)"
            )
        ]
    ),
    ByProduct(
        id="wheat_straw",
        sourceCrop="Wheat",
        residueName="Wheat Straw",
        description="Soft cereal residue remaining after wheat grain threshing. Premier dry fodder for Indian cattle and raw material for straw pellets.",
        residueFactor=1.30,
        residueFactorSource="ICAR - Indian Institute of Wheat and Barley Research (IIWBR)",
        processingDifficulty="low",
        requiredProcessing=["Reaper Baling", "Chopping (Tukda)", "Storage"],
        demandLevel="high",
        opportunityScore=89,
        scoreFactors=ScoreFactors(
            availability=95,
            demand=94,
            processingEffort=88,
            localSuitability=80
        ),
        valueRange=ValueRange(min=4000, max=7500, unit="₹ / tonne (Dry Fodder)"),
        valueSource="North India Fodder Mandi Quotations",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Dry Cattle Fodder (Bhusa / Turi)",
                category="Animal Feed",
                description="Finely chopped wheat straw is the primary roughage fodder fed to dairy cows and buffaloes across India.",
                processingSteps=[
                    "Operate straw reaper behind combine harvester.",
                    "Chop straw into fine 1-2 cm pieces (Bhusa).",
                    "Store under dry covered sheds to prevent mold."
                ],
                equipment=["Straw Reaper Machine", "Baler"],
                marketChannel="Dairy Farmers, Gaushalas & Fodder Traders",
                source="ICAR-IIWBR Karnal Guidelines"
            )
        ]
    ),
    ByProduct(
        id="tomato_pomace",
        sourceCrop="Tomato",
        residueName="Tomato Pomace",
        description="Wet residue consisting of tomato skins, seeds, and pulp leftover from ketchup and sauce processing plants.",
        residueFactor=0.05,
        residueFactorSource="ICAR - Indian Institute of Horticultural Research (IIHR)",
        processingDifficulty="medium",
        requiredProcessing=["Drying", "Seed-Skin Separation", "Solvent Extraction"],
        demandLevel="medium",
        opportunityScore=78,
        scoreFactors=ScoreFactors(
            availability=70,
            demand=82,
            processingEffort=74,
            localSuitability=86
        ),
        valueRange=ValueRange(min=1500, max=3000, unit="₹ / tonne"),
        valueSource="Food Processing Waste Procurement",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Lycopene Antioxidant Extraction",
                category="Bio-Based Products",
                description="Tomato skins are packed with natural lycopene, a high-value antioxidant used in nutraceuticals and food colorants.",
                processingSteps=[
                    "Solar dry pomace to below 8% moisture.",
                    "Separate tomato skins from seeds using air classifier.",
                    "Supercritical CO2 extraction of lycopene pigment."
                ],
                equipment=["Rotary Solar Dryer", "Air Classifier", "Extraction Reactor"],
                marketChannel="Pharma & Food Colorant Manufacturers",
                source="ICAR-IIHR Bengaluru Technical Report"
            ),
            Application(
                name="Protein-Rich Livestock Feed Supplement",
                category="Animal Feed",
                description="Tomato seeds contain 20-22% crude fat and 28% protein suitable for poultry and ruminant nutrition.",
                processingSteps=[
                    "Dry pomace and mix with rice bran.",
                    "Incorporate 5-10% into daily cattle ration."
                ],
                equipment=["Feed Mixer"],
                marketChannel="Livestock Farms & Feed Mills",
                source="Indian Veterinary Research Institute (IVRI)"
            )
        ]
    ),
    ByProduct(
        id="mango_kernels",
        sourceCrop="Mango",
        residueName="Mango Kernels & Peels",
        description="Solid seed stone and peels remaining after mango pulp processing. Rich source of vegetable fat (Mango Butter) and pectin.",
        residueFactor=0.18,
        residueFactorSource="ICAR - Central Institute for Subtropical Horticulture (CISH Lucknow)",
        processingDifficulty="medium",
        requiredProcessing=["Washing & Decortication", "Kernel Drying", "Solvent Fat Extraction"],
        demandLevel="high",
        opportunityScore=87,
        scoreFactors=ScoreFactors(
            availability=80,
            demand=92,
            processingEffort=85,
            localSuitability=91
        ),
        valueRange=ValueRange(min=5000, max=12000, unit="₹ / tonne (Kernels)"),
        valueSource="Cosmetic Fat Processors & Extraction Exporters",
        lastVerified="Aug 2026",
        applications=[
            Application(
                name="Cosmetic Grade Mango Seed Butter",
                category="Bio-Based Products",
                description="Extracted mango kernel fat resembles cocoa butter and is highly sought after by global cosmetic industries for lip balms and skin creams.",
                processingSteps=[
                    "Decorticate hard mango stones to release inner soft kernel.",
                    "Sun-dry kernels to 8% moisture content.",
                    "Expeller pressing and solvent extraction of mango butter.",
                    "Refine, bleach, and deodorize (RBD) natural butter."
                ],
                equipment=["Kernel Decorticator", "Mechanical Expeller Press", "Refining Plant"],
                marketChannel="Cosmetic Manufacturers & Cocoa Butter Substitute Exporters",
                source="ICAR-CISH Lucknow By-Product Technology"
            )
        ]
    )
]

# Quick lookup index by crop name
CROP_TO_BYPRODUCT_MAP = {
    "rice": "rice_straw",
    "paddy": "rice_straw",
    "sugarcane": "sugarcane_bagasse",
    "cotton": "cotton_stalks",
    "banana": "banana_pseudostem",
    "groundnut": "groundnut_shells",
    "peanut": "groundnut_shells",
    "mustard": "mustard_cake",
    "wheat": "wheat_straw",
    "tomato": "tomato_pomace",
    "mango": "mango_kernels"
}
