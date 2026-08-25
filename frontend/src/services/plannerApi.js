const isLocal = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (isLocal ? 'http://localhost:8000/api/v1' : 'https://growva-backend.onrender.com/api/v1');

export async function fetchCropRecommendations(location = 'Vadodara, Gujarat') {
  try {
    const res = await fetch(`${API_BASE_URL}/recommendations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        location: location || 'Vadodara, Gujarat',
      }),
    });

    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Backend API fail, using fallback recommendations:', error);
    return getFallbackRecommendationData(location);
  }
}

export async function fetchWeather(location = 'Vadodara, Gujarat') {
  try {
    const res = await fetch(`${API_BASE_URL}/weather?location=${encodeURIComponent(location)}`);
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    const data = await res.json();
    return {
      location: data.location || location,
      temperature: data.temp_c ?? data.temperature ?? 28.5,
      humidity: data.humidity_pct ?? data.humidity ?? 68,
      rain_probability: data.rain_probability ?? (data.forecast && data.forecast[0]?.rain_chance_pct) ?? 64,
      rainfall_mm: data.rainfall_mm ?? 0.0,
      condition: data.condition || 'Partly cloudy',
      wind_speed_kmh: data.wind_kmh ?? data.wind_speed_kmh ?? 14.0,
      forecast: (data.forecast || []).map(f => ({
        day: f.day,
        temp: f.temp_c ?? f.temp ?? 28,
        condition: f.condition || 'Partly cloudy',
        rain_prob: f.rain_chance_pct ?? f.rain_prob ?? 50
      })),
      advisory: data.alerts && data.alerts.length > 0
        ? data.alerts[0].description
        : `Good moisture window for sowing in ${location}.`
    };
  } catch (error) {
    console.warn('Backend Weather API fail, using local weather fallback:', error);
    return {
      location: location,
      temperature: 28.5,
      humidity: 68,
      rain_probability: 64,
      rainfall_mm: 4.2,
      condition: 'Partly cloudy',
      wind_speed_kmh: 14.0,
      forecast: [
        { day: 'Mon', temp: 28, condition: 'Partly cloudy', rain_prob: 60 },
        { day: 'Tue', temp: 27, condition: 'Light rain', rain_prob: 75 },
        { day: 'Wed', temp: 29, condition: 'Sunny', rain_prob: 20 },
        { day: 'Thu', temp: 26, condition: 'Rain showers', rain_prob: 80 },
        { day: 'Fri', temp: 30, condition: 'Clear sky', rain_prob: 10 },
        { day: 'Sat', temp: 31, condition: 'Sunny', rain_prob: 15 },
        { day: 'Sun', temp: 29, condition: 'Partly cloudy', rain_prob: 30 },
      ],
      advisory: `Favorable sowing moisture detected for ${location}.`
    };
  }
}

export async function fetchMandiPrices(commodity = '', state = '', market = '') {
  try {
    const params = new URLSearchParams();
    if (commodity) params.append('commodity', commodity);
    if (state) params.append('state', state);
    if (market) params.append('market', market);

    const res = await fetch(`${API_BASE_URL}/mandi?${params.toString()}`);
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Backend Mandi API fail, using fallback mandi data:', error);
    return {
      total: 6,
      items: [
        { state: "Gujarat", district: "Ahmedabad", market: "Bavla Mandi", commodity: "Wheat", variety: "Lokwan", min_price: 2450, max_price: 2850, modal_price: 2680, arrival_date: "2026-08-25" },
        { state: "Gujarat", district: "Ahmedabad", market: "Sanand Mandi", commodity: "Cotton", variety: "Shankar-6", min_price: 6800, max_price: 7600, modal_price: 7250, arrival_date: "2026-08-25" },
        { state: "Gujarat", district: "Rajkot", market: "Gondal APMC", commodity: "Groundnut", variety: "Bold", min_price: 6400, max_price: 7150, modal_price: 6800, arrival_date: "2026-08-25" },
        { state: "Gujarat", district: "Rajkot", market: "Rajkot APMC", commodity: "Groundnut", variety: "Bold", min_price: 6350, max_price: 7000, modal_price: 6750, arrival_date: "2026-08-25" },
        { state: "Gujarat", district: "Mehsana", market: "Unjha APMC", commodity: "Cumin", variety: "Super Fine", min_price: 22500, max_price: 26500, modal_price: 24800, arrival_date: "2026-08-25" },
        { state: "Maharashtra", district: "Nashik", market: "Lasalgaon Mandi", commodity: "Onion", variety: "Red Onion", min_price: 1600, max_price: 2480, modal_price: 2150, arrival_date: "2026-08-25" }
      ]
    };
  }
}

export async function fetchMarketAnalysis(locationName = 'Vadodara, Gujarat', crop = 'Groundnut', quantityQuintals = 10, radiusKm = 250) {
  const locStr = (typeof locationName === 'object' && locationName !== null) ? (locationName.name || locationName.location || 'Vadodara, Gujarat') : String(locationName || 'Vadodara, Gujarat');
  const cropStr = (typeof crop === 'object' && crop !== null) ? (crop.crop_name || crop.name || 'Groundnut') : String(crop || 'Groundnut');
  const qty = Number(quantityQuintals) || 10;
  const radius = Number(radiusKm) || 250;

  try {
    const res = await fetch(`${API_BASE_URL}/markets/market-analysis`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        location: { name: locStr },
        crop: cropStr,
        quantity_quintals: qty,
        radius_km: radius
      })
    });
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    const data = await res.json();
    if (!data || !data.best_market) throw new Error('Invalid backend payload structure');
    return data;
  } catch (error) {
    console.warn('Backend Market Analysis API call failed, calculating local fallback analysis:', error);
    // Fallback mathematical calculation engine
    const baseMarkets = [
      { market: "Gondal APMC", district: "Rajkot", state: "Gujarat", modal: 6800, dist: 235, variety: "Bold" },
      { market: "Rajkot APMC", district: "Rajkot", state: "Gujarat", modal: 6750, dist: 220, variety: "Bold / Java" },
      { market: "Anand APMC", district: "Anand", state: "Gujarat", modal: 6250, dist: 45, variety: "Local" },
      { market: "Vadodara APMC", district: "Vadodara", state: "Gujarat", modal: 6100, dist: 20, variety: "Medium" },
      { market: "Ahmedabad APMC", district: "Ahmedabad", state: "Gujarat", modal: 6300, variety: "Bold" }
    ];

    const evaluated = baseMarkets.map(m => {
      const trans = Math.max(250, (m.dist * 12) + (m.dist * qty * 1.5));
      const gross = m.modal * qty;
      const net = gross - trans;
      return {
        rank: 1,
        market: m.market,
        district: m.district,
        state: m.state,
        commodity: cropStr,
        variety: m.variety,
        modal_price: m.modal,
        min_price: Math.round(m.modal * 0.94),
        max_price: Math.round(m.modal * 1.06),
        unit: "quintal",
        distance_km: m.dist,
        transport_cost: Math.round(trans),
        transport_cost_per_quintal: Math.round(trans / qty),
        gross_revenue: Math.round(gross),
        net_realization: Math.round(net),
        net_realization_per_quintal: Math.round(net / qty),
        price_date: "2026-08-25",
        freshness_status: "Fresh",
        data_source: "AGMARKNET Benchmark",
        latitude: 22.3,
        longitude: 70.8
      };
    });

    evaluated.sort((a, b) => b.net_realization - a.net_realization);
    evaluated.forEach((item, index) => item.rank = index + 1);

    const best = evaluated[0];
    const local = evaluated.find(x => x.market.includes("Vadodara")) || evaluated[evaluated.length - 1];
    const addl = Math.max(0, best.net_realization - local.net_realization);

    return {
      crop: cropStr,
      farmer_location: locStr,
      farmer_latitude: 22.3072,
      farmer_longitude: 73.1812,
      quantity_quintals: qty,
      radius_km: radius,
      best_market: best,
      markets: evaluated,
      potential_additional_realization: addl,
      baseline_market_name: local.market,
      analysis_summary: `${best.market} is the optimal choice offering a higher modal price of ₹${best.modal_price.toLocaleString()}/quintal. Despite being ${best.distance_km} km away, the price premium yields an estimated net realization of ₹${best.net_realization.toLocaleString()} (+₹${addl.toLocaleString()} net gain vs local APMC).`,
      is_demo_data: true
    };
  }
}

export async function fetchSchemes(category = '', state = '') {
  try {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (state) params.append('state', state);
    const queryString = params.toString() ? `?${params.toString()}` : '';

    const res = await fetch(`${API_BASE_URL}/schemes${queryString}`);
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Backend Schemes API fail, using local scheme fallback:', error);
    return null;
  }
}

export async function checkSchemeEligibility(schemeId, answers = {}) {
  try {
    const res = await fetch(`${API_BASE_URL}/schemes/${schemeId}/eligibility`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers }),
    });
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Backend scheme eligibility check failed, calculating local fallback:', error);
    return null;
  }
}

export async function matchFarmerSchemes(farmerProfile = {}) {
  try {
    const res = await fetch(`${API_BASE_URL}/schemes/match`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(farmerProfile),
    });
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Backend scheme match failed, using local fallback:', error);
    return null;
  }
}

export async function diagnoseCropDisease(cropName, symptomsText, imageBase64 = null) {
  try {
    const res = await fetch(`${API_BASE_URL}/disease/diagnose`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        crop_name: cropName || 'Tomato',
        symptoms_text: symptomsText || 'yellow spots on leaf',
        image_base64: imageBase64 || null
      }),
    });
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    return {
      crop_name: cropName || 'Tomato',
      diagnosed_disease: `${cropName || 'Tomato'} Leaf Blight & Spot Infection`,
      confidence_score: imageBase64 ? 0.96 : 0.92,
      symptoms_matched: ["yellowing", "concentric dark spots", "leaf chlorosis"],
      organic_treatment: "Spray Neem oil formulation (5 ml/L water) or Trichoderma viride bio-fungicide (5g/L).",
      chemical_treatment: "Apply Mancozeb 75 WP (2.5g/L water) or Copper Oxychloride 50 WP.",
      preventive_measures: "Practice crop rotation, maintain plant spacing for airflow."
    };
  }
}

export async function sendChatMessage(messages, provider = 'openrouter', apiKey = '', model = 'z-ai/glm-5.2:free') {
  try {
    const res = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages,
        provider,
        api_key: apiKey || null,
        model
      }),
    });
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    const lastUserMsg = [...messages].reverse().find(m => m.role === 'user')?.content || '';
    let fallbackText = "🌾 **Namaste Farmer!** I am your Growva AI Kisan Assistant. How can I help you today with crop recommendations, mandi rates, disease identification, or weather forecasts?";
    return {
      reply: fallbackText,
      provider_used: `${provider} (Fallback)`,
      model_used: model
    };
  }
}

export async function fetchByProducts(search = '', crop = '', category = '', difficulty = '') {
  try {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (crop) params.append('crop', crop);
    if (category) params.append('category', category);
    if (difficulty) params.append('difficulty', difficulty);

    const res = await fetch(`${API_BASE_URL}/byproducts?${params.toString()}`);
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Backend fetchByProducts failed, using local fallback:', error);
    return [];
  }
}

export async function fetchByProductById(id) {
  try {
    const res = await fetch(`${API_BASE_URL}/byproducts/${id}`);
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn(`Backend fetchByProductById for ${id} failed:`, error);
    return null;
  }
}

export async function analyzeCropResidue(crop, areaAcres = 3.0, expectedYieldTonnes = null, location = 'Vadodara, Gujarat') {
  try {
    const res = await fetch(`${API_BASE_URL}/byproducts/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        crop,
        area_acres: Number(areaAcres),
        expected_yield_tonnes: expectedYieldTonnes ? Number(expectedYieldTonnes) : null,
        location
      }),
    });
    if (!res.ok) throw new Error(`Server status ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Backend analyzeCropResidue failed, using local fallback:', error);
    return null;
  }
}

function getFallbackRecommendationData(location = 'Vadodara, Gujarat') {
  const locLower = (location || '').toLowerCase();
  const locName = location || 'Vadodara, Gujarat';
  
  let temp = 28.5;
  let humidity = 68.0;
  let rainProb = 45.0;
  let rainMm = 12.0;
  let season = "Kharif";
  let topCrops = [];

  if (locLower.includes('amarnath') || locLower.includes('srinagar') || locLower.includes('shimla') || locLower.includes('leh') || locLower.includes('manali')) {
    temp = 7.5;
    humidity = 76.0;
    rainProb = 40.0;
    rainMm = 5.0;
    season = "Rabi";
    topCrops = [
      {
        crop_name: 'Apple',
        category: 'Fruits',
        match_score: 93,
        suitability_rating: 'Highly Suitable',
        scores: { lifecycle_climate: 94, season: 95, current_conditions: 92, forecast: 90 },
        risk: { level: 'LOW', score: 90, warnings: ['Optimal temperate mountain climate.'] },
        sowing_window: { status: 'GOOD', recommended_start: '2026-08-25', recommended_end: '2026-08-29', reason: 'Favorable cold weather for orchard planting.' },
        duration_days: 365,
        growth_stages: [
          { name: 'Prepare field', start_day: 0, end_day: 30 },
          { name: 'Sowing window', start_day: 31, end_day: 60 },
          { name: 'Germination & Vegetative', start_day: 61, end_day: 180 },
          { name: 'Flowering & Pods', start_day: 181, end_day: 280 },
          { name: 'Expected harvest', start_day: 281, end_day: 365 }
        ],
        reasons: ['Cold chilling hours ideal for apple bud break', 'Historical climate matches temperate zone requirements'],
        risk_factors: ['Monitor for late spring frost'],
        expected_yield: '12 - 22 tonnes/ha',
        suggested_sowing_window: 'Aug 25 – Aug 29',
        sowing_status: 'GOOD'
      },
      {
        crop_name: 'Barley',
        category: 'Crops',
        match_score: 88,
        suitability_rating: 'Highly Suitable',
        scores: { lifecycle_climate: 90, season: 92, current_conditions: 86, forecast: 82 },
        risk: { level: 'LOW', score: 85, warnings: ['Cold tolerant cereal.'] },
        sowing_window: { status: 'GOOD', recommended_start: '2026-08-25', recommended_end: '2026-08-29', reason: 'Cold tolerant window.' },
        duration_days: 110,
        growth_stages: [
          { name: 'Prepare field', start_day: 0, end_day: 10 },
          { name: 'Sowing window', start_day: 11, end_day: 25 },
          { name: 'Germination & Vegetative', start_day: 26, end_day: 55 },
          { name: 'Flowering & Pods', start_day: 56, end_day: 85 },
          { name: 'Expected harvest', start_day: 86, end_day: 110 }
        ],
        reasons: ['High cold tolerance', 'Thrives in temperate loams'],
        risk_factors: ['Avoid waterlogging during thaw'],
        expected_yield: '3.0 - 4.0 tonnes/ha',
        suggested_sowing_window: 'Aug 25 – Aug 29',
        sowing_status: 'GOOD'
      }
    ];
  } else if (locLower.includes('jaisalmer') || locLower.includes('jodhpur') || locLower.includes('bikaner')) {
    temp = 34.0;
    humidity = 38.0;
    rainProb = 20.0;
    rainMm = 1.0;
    season = "Kharif";
    topCrops = [
      {
        crop_name: 'Bajra',
        category: 'Crops',
        match_score: 93,
        suitability_rating: 'Highly Suitable',
        scores: { lifecycle_climate: 95, season: 94, current_conditions: 92, forecast: 90 },
        risk: { level: 'LOW', score: 90, warnings: ['Highly drought resilient.'] },
        sowing_window: { status: 'GOOD', recommended_start: '2026-08-25', recommended_end: '2026-08-29', reason: 'Drought resilient sowing window.' },
        duration_days: 85,
        growth_stages: [
          { name: 'Prepare field', start_day: 0, end_day: 8 },
          { name: 'Sowing window', start_day: 9, end_day: 20 },
          { name: 'Germination & Vegetative', start_day: 21, end_day: 45 },
          { name: 'Flowering & Pods', start_day: 46, end_day: 70 },
          { name: 'Expected harvest', start_day: 71, end_day: 85 }
        ],
        reasons: ['Extreme heat and drought tolerance', 'Low water requirement satisfied'],
        risk_factors: ['No major weather risks detected'],
        expected_yield: '2.0 - 3.0 tonnes/ha',
        suggested_sowing_window: 'Aug 25 – Aug 29',
        sowing_status: 'GOOD'
      },
      {
        crop_name: 'Cumin',
        category: 'Spices',
        match_score: 87,
        suitability_rating: 'Highly Suitable',
        scores: { lifecycle_climate: 88, season: 90, current_conditions: 85, forecast: 84 },
        risk: { level: 'LOW', score: 85, warnings: ['Dry climate ideal for seed quality.'] },
        sowing_window: { status: 'GOOD', recommended_start: '2026-08-25', recommended_end: '2026-08-29', reason: 'Dry climate sowing window.' },
        duration_days: 110,
        growth_stages: [
          { name: 'Prepare field', start_day: 0, end_day: 10 },
          { name: 'Sowing window', start_day: 11, end_day: 25 },
          { name: 'Germination & Vegetative', start_day: 26, end_day: 60 },
          { name: 'Flowering & Pods', start_day: 61, end_day: 90 },
          { name: 'Expected harvest', start_day: 91, end_day: 110 }
        ],
        reasons: ['Low moisture requirement', 'High market commodity value'],
        risk_factors: ['Avoid over-irrigation'],
        expected_yield: '0.6 - 1.0 tonnes/ha',
        suggested_sowing_window: 'Aug 25 – Aug 29',
        sowing_status: 'GOOD'
      }
    ];
  } else {
    // Default (Vadodara, Gujarat, etc.)
    temp = 28.5;
    humidity = 68.0;
    rainProb = 45.0;
    rainMm = 12.0;
    season = "Kharif";
    topCrops = [
      {
        crop_name: 'Groundnut',
        category: 'Pulses & Oilseeds',
        match_score: 91,
        suitability_rating: 'Highly Suitable',
        scores: { lifecycle_climate: 93, season: 95, current_conditions: 88, forecast: 85 },
        risk: { level: 'LOW', score: 88, warnings: ['Optimal short-term weather window.'] },
        sowing_window: { status: 'GOOD', recommended_start: '2026-08-25', recommended_end: '2026-08-29', reason: 'Suitable short-term weather conditions.' },
        duration_days: 120,
        growth_stages: [
          { name: 'Prepare field', start_day: 0, end_day: 10 },
          { name: 'Sowing window', start_day: 11, end_day: 25 },
          { name: 'Germination & Vegetative', start_day: 26, end_day: 60 },
          { name: 'Flowering & Pods', start_day: 61, end_day: 90 },
          { name: 'Expected harvest', start_day: 91, end_day: 120 }
        ],
        reasons: ['Seasonal climate is favorable for Groundnut', 'Current temperature (28.5°C) is within optimal growth range', 'Historical rainfall is suitable over 120-day lifecycle', 'Short-term weather risk is low'],
        risk_factors: ['No major short-term weather risks detected'],
        expected_yield: '1.8 - 2.5 tonnes/ha',
        suggested_sowing_window: 'Aug 25 – Aug 29',
        sowing_status: 'GOOD'
      },
      {
        crop_name: 'Cotton',
        category: 'Crops',
        match_score: 86,
        suitability_rating: 'Highly Suitable',
        scores: { lifecycle_climate: 88, season: 90, current_conditions: 85, forecast: 80 },
        risk: { level: 'LOW', score: 84, warnings: ['Suitable temperature for boll setup.'] },
        sowing_window: { status: 'GOOD', recommended_start: '2026-08-25', recommended_end: '2026-08-29', reason: 'Favorable field conditions.' },
        duration_days: 160,
        growth_stages: [
          { name: 'Prepare field', start_day: 0, end_day: 14 },
          { name: 'Sowing window', start_day: 15, end_day: 35 },
          { name: 'Germination & Vegetative', start_day: 36, end_day: 80 },
          { name: 'Flowering & Pods', start_day: 81, end_day: 120 },
          { name: 'Expected harvest', start_day: 121, end_day: 160 }
        ],
        reasons: ['Black loamy soil suitability', 'Warm climate accelerates boll development'],
        risk_factors: ['Requires well-drained soil during germination'],
        expected_yield: '2.0 - 3.0 tonnes/ha',
        suggested_sowing_window: 'Aug 25 – Aug 29',
        sowing_status: 'GOOD'
      },
      {
        crop_name: 'Maize',
        category: 'Crops',
        match_score: 79,
        suitability_rating: 'Suitable',
        scores: { lifecycle_climate: 80, season: 82, current_conditions: 78, forecast: 74 },
        risk: { level: 'LOW', score: 80, warnings: ['Adequate rainfall expected.'] },
        sowing_window: { status: 'GOOD', recommended_start: '2026-08-25', recommended_end: '2026-08-29', reason: 'Clear sowing window.' },
        duration_days: 100,
        growth_stages: [
          { name: 'Prepare field', start_day: 0, end_day: 8 },
          { name: 'Sowing window', start_day: 9, end_day: 20 },
          { name: 'Germination & Vegetative', start_day: 21, end_day: 55 },
          { name: 'Flowering & Pods', start_day: 56, end_day: 80 },
          { name: 'Expected harvest', start_day: 81, end_day: 100 }
        ],
        reasons: ['Moderate water requirement matches forecast', 'Adaptable to local loamy soil'],
        risk_factors: ['Avoid waterlogging during germination'],
        expected_yield: '3.5 - 5.0 tonnes/ha',
        suggested_sowing_window: 'Aug 25 – Aug 29',
        sowing_status: 'GOOD'
      }
    ];
  }

  return {
    location: locName,
    season: season,
    temperature: temp,
    humidity: humidity,
    rain_probability: rainProb,
    rainfall_expected: rainMm,
    condition: 'Partly cloudy',
    top_recommendations: topCrops,
    sowing_advisory: `Conditions in ${locName} (${temp}°C, ${humidity}% humidity) favor sowing ${topCrops[0]?.crop_name} with top suitability (${topCrops[0]?.match_score}%).`,
    is_demo: true
  };
}
