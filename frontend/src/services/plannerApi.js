// API Service for Growva Crop Planning & Weather Intelligence

const API_BASE_URL = 'http://localhost:8000/api/v1';

export async function fetchCropRecommendations(location, soilType = 'Fertile loam') {
  try {
    const res = await fetch(`${API_BASE_URL}/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        location: location || 'Vadodara, Gujarat',
        soil_type: soilType,
      }),
    });

    if (!res.ok) {
      throw new Error(`Server returned status ${res.status}`);
    }

    const data = await res.json();
    return data;
  } catch (error) {
    console.warn('Backend API connection failed, using local intelligent fallback:', error);
    return getFallbackRecommendationData(location);
  }
}

// Fallback generator if backend server is unreachable
function getFallbackRecommendationData(location = 'Vadodara, Gujarat') {
  const isVadodara = location.toLowerCase().includes('vadodara');
  const locName = location || 'Vadodara, Gujarat';
  
  const temp = isVadodara ? 29.5 : 28.0;
  const humidity = isVadodara ? 74.0 : 68.0;
  const rainProb = isVadodara ? 64.0 : 45.0;
  const rainMm = isVadodara ? 62.0 : 15.0;

  const topCrops = [
    {
      crop_name: 'Groundnut',
      category: 'Pulses & Oilseeds',
      match_score: 91,
      suitability_rating: 'Highly Suitable',
      scores: { climate_suitability: 93, season_suitability: 95, current_conditions: 88, forecast_suitability: 85 },
      risk: { level: 'LOW', score: 85, warnings: ['Low weather risk detected for current sowing window.'] },
      duration_days: 120,
      growth_stages: [
        { name: 'Prepare field', start_day: 0, end_day: 10 },
        { name: 'Sowing window', start_day: 11, end_day: 25 },
        { name: 'Germination & Vegetative', start_day: 26, end_day: 60 },
        { name: 'Flowering & Pods', start_day: 61, end_day: 90 },
        { name: 'Expected harvest', start_day: 91, end_day: 120 }
      ],
      reasons: ['Climate suitability is high', 'Temperature is within preferred 20-35°C range', 'Water availability matches requirement'],
      risk_factors: ['No major weather risks detected'],
      expected_yield: '1.8 - 2.5 tonnes/ha',
      suggested_sowing_window: 'Sow within the next 3–5 days (Favorable weather window)',
      sowing_status: 'GOOD'
    },
    {
      crop_name: 'Cotton',
      category: 'Crops',
      match_score: 86,
      suitability_rating: 'Highly Suitable',
      scores: { climate_suitability: 88, season_suitability: 90, current_conditions: 85, forecast_suitability: 80 },
      risk: { level: 'LOW', score: 82, warnings: ['Monitor short-term moisture level.'] },
      duration_days: 160,
      growth_stages: [
        { name: 'Prepare field', start_day: 0, end_day: 14 },
        { name: 'Sowing window', start_day: 15, end_day: 35 },
        { name: 'Vegetative growth', start_day: 36, end_day: 80 },
        { name: 'Boll formation', start_day: 81, end_day: 120 },
        { name: 'Expected harvest', start_day: 121, end_day: 160 }
      ],
      reasons: ['Deep fertile soil is ideal for cotton', 'Warm climate accelerates boll development'],
      risk_factors: ['Requires well-drained soil during germination'],
      expected_yield: '2.0 - 3.0 tonnes/ha',
      suggested_sowing_window: 'Sow after soil preparation within 5 days',
      sowing_status: 'GOOD'
    },
    {
      crop_name: 'Maize',
      category: 'Crops',
      match_score: 79,
      suitability_rating: 'Suitable',
      scores: { climate_suitability: 80, season_suitability: 82, current_conditions: 78, forecast_suitability: 75 },
      risk: { level: 'MEDIUM', score: 68, warnings: ['Requires consistent nitrogen application.'] },
      duration_days: 100,
      growth_stages: [
        { name: 'Prepare field', start_day: 0, end_day: 8 },
        { name: 'Sowing window', start_day: 9, end_day: 20 },
        { name: 'Tasseling', start_day: 21, end_day: 55 },
        { name: 'Cob filling', start_day: 56, end_day: 80 },
        { name: 'Expected harvest', start_day: 81, end_day: 100 }
      ],
      reasons: ['Moderate water requirement', 'Adaptable to local soil'],
      risk_factors: ['Avoid waterlogging during early germination'],
      expected_yield: '3.5 - 5.0 tonnes/ha',
      suggested_sowing_window: 'Sow during clear rain window',
      sowing_status: 'GOOD'
    },
    {
      crop_name: 'Soybean',
      category: 'Pulses',
      match_score: 73,
      suitability_rating: 'Suitable',
      scores: { climate_suitability: 75, season_suitability: 76, current_conditions: 72, forecast_suitability: 70 },
      risk: { level: 'LOW', score: 80, warnings: ['Ensure adequate soil phosphorus.'] },
      duration_days: 105,
      growth_stages: [
        { name: 'Prepare field', start_day: 0, end_day: 8 },
        { name: 'Sowing window', start_day: 9, end_day: 22 },
        { name: 'Vegetative growth', start_day: 23, end_day: 55 },
        { name: 'Pod filling', start_day: 56, end_day: 85 },
        { name: 'Expected harvest', start_day: 86, end_day: 105 }
      ],
      reasons: ['Fixes nitrogen naturally in soil', 'Short growth duration'],
      risk_factors: ['Sensitive to early weed competition'],
      expected_yield: '1.5 - 2.2 tonnes/ha',
      suggested_sowing_window: 'Sow within 4 days',
      sowing_status: 'GOOD'
    }
  ];

  return {
    location: locName,
    temperature: temp,
    humidity: humidity,
    rain_probability: rainProb,
    rainfall_expected: rainMm,
    condition: 'Partly cloudy',
    soil_type: 'Fertile loam',
    top_recommendations: topCrops,
    sowing_advisory: `Conditions are favorable for groundnut in ${locName}. The next 7 days show manageable rainfall risk, making this a suitable sowing window.`,
    is_demo: true
  };
}
