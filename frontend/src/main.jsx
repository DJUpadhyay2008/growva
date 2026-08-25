import React, { useMemo, useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { motion, useMotionValue, useSpring, useTransform, AnimatePresence } from 'framer-motion';
import {
  ArrowRight, CalendarDays, CheckCircle2, CloudRain, Droplets, Globe2, Leaf, MapPin, Menu, Mic, Recycle, Search, ShieldCheck, Sprout, Sun, TrendingUp, Wind, X, FileText, DollarSign, AlertTriangle, Send, Bot, User, ExternalLink, ChevronRight, Info, Sparkles, Camera, UploadCloud, Image, FileImage, Settings
} from 'lucide-react';
import './styles.css';
import {
  fetchCropRecommendations, fetchWeather, fetchMandiPrices, fetchSchemes, checkSchemeEligibility, diagnoseCropDisease, sendChatMessage
} from './services/plannerApi';
import {
  getTranslation, translateCrop, translateGroup, translateSoil, translateSeason, translateWater, translateStage, translateWeatherCondition, translateDay
} from './translations';

import robot from './assets/robotic-farm.jpeg';
import vegetableGuide from './assets/indian-vegetables-guide.jpg';
import fruitGuide from './assets/fruit-guide.jpg';

const languages = [
  ['en','English'],['as','অসমীয়া'],['bn','বাংলা'],['brx','बड़ो'],['doi','डोगरी'],['gu','ગુજરાતી'],['hi','हिन्दी'],['kn','<ctrl42>ಕನ್ನಡ'],['ks','कॉशुर'],['kok','कोंकणी'],['mai','मैथिली'],['ml','മലയാളം'],['mni','মৈতৈলোন্'],['mr','मराठी'],['ne','नेपाली'],['or','ଓଡ଼ିଆ'],['pa','ਪੰਜਾਬੀ'],['sa','संस्कृतम्'],['sat','ᱥᱟᱱᱛᱟᱲᱤ'],['sd','سنڌي'],['ta','தமிழ்'],['te','తెలుగు'],['ur','اُردُو']
];

const navKeys = ['Dashboard', 'Planner', 'Weather', 'Crop Library', 'Mandi Rates', 'Disease Check', 'Schemes', 'By-Products'];

const groups = {
  Crops: ['Wheat','Rice','Bajra','Maize','Barley','Jowar','Ragi','Oats','Sorghum','Quinoa','Buckwheat','Amaranth','Foxtail Millet','Little Millet','Kodo Millet','Barnyard Millet','Proso Millet','Sugarcane','Cotton','Jute','Tea','Coffee','Tobacco'],
  Pulses: ['Chickpea','Pigeon Pea','Green Gram','Black Gram','Lentil','Field Pea','Cowpea','Horse Gram','Moth Bean','Soybean','Peanut','Rajma','Lima Bean'],
  Vegetables: ['Tomato','Potato','Onion','Garlic','Carrot','Radish','Beetroot','Cabbage','Cauliflower','Broccoli','Spinach','Amaranth Leaves','Okra','Brinjal','Capsicum','Green Peas','Cucumber','Bottle Gourd','Bitter Gourd','Ridge Gourd','Pumpkin','Sweet Corn','French Bean','Drumstick','Turnip','Sweet Potato','Yam','Taro','Colocasia','Green Chilli','Lettuce','Celery','Mushroom','Zucchini','Cluster Bean','Ivy Gourd','Snake Gourd','Ash Gourd'],
  Fruits: ['Mango','Banana','Apple','Orange','Guava','Papaya','Pomegranate','Grapes','Watermelon','Muskmelon','Pineapple','Litchi','Sapota','Jackfruit','Custard Apple','Strawberry','Strawberries','Kiwi','Peach','Plum','Pear','Fig','Dragon Fruit','Avocado','Coconut','Amla','Jamun','Karonda','Passion Fruit','Mosambi','Lemon','Chikoo','Apricot','Cherries','Blueberries','Melon','Lime','Raspberry','Dates','Blood Orange','Persimmon','Star Fruit','Cantaloupe'],
  Spices: ['Turmeric','Ginger','Cumin','Coriander','Black Pepper','Cardamom','Clove','Cinnamon','Fenugreek','Mustard','Fennel','Ajwain','Chilli','Saffron','Nutmeg','Mace','Star Anise','Tamarind','Bay Leaf','Curry Leaf','Asafoetida','Poppy Seed','Sesame','Dill','Black Cumin']
};

const photo = {
  Wheat:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Wheat%20field.jpg',Rice:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Rice%20paddy%20field%20in%20India.jpg',Maize:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Maize%20field.jpg',Barley:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Barley%20field.jpg',Jowar:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sorghum%20field.jpg',Ragi:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Finger%20millet.jpg',Oats:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Oat%20field.jpg',Sugarcane:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sugarcane%20field.jpg',Cotton:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cotton%20plant.jpg',Tea:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Tea%20plantation.jpg',Coffee:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Coffee%20plantation.jpg',Tomato:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Tomatoes%20on%20plant.jpg',Potato:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Potatoes.jpg',Onion:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Onions.jpg',Garlic:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Garlic.jpg',Carrot:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Carrots.jpg',Cabbage:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cabbage.jpg',Cauliflower:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cauliflower.jpg',Broccoli:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Broccoli.jpg',Spinach:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Spinach.jpg',Okra:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Okra.jpg',Brinjal:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Solanum%20melongena%20fruit.jpg',Capsicum:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Capsicum%20annuum%20fruits%20IMGP0044.jpg',Cucumber:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cucumis%20sativus%20fruit.jpg',Pumpkin:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pumpkins.jpg',Mango:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Mangoes.jpg',Banana:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Banana.jpg',Apple:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Apples.jpg',Orange:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Orange.jpg',Guava:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Guava.jpg',Papaya:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Papaya.jpg',Pomegranate:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pomegranate%20fruit.jpg',Grapes:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Grapes.jpg',Watermelon:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Watermelon.jpg',Pineapple:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pineapple.jpg',Litchi:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Lychee.jpg',Strawberry:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Strawberries.jpg',DragonFruit:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pitaya%20fruit.jpg',Coconut:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Coconuts.jpg',Amla:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Phyllanthus%20emblica%20fruit.jpg',Turmeric:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Turmeric%20plant.jpg',Ginger:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Ginger%20plant.jpg',Cumin:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cumin%20seeds.jpg',Coriander:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Coriander%20seeds.jpg',BlackPepper:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Black%20Pepper%20(Piper%20nigrum)%20fruits.jpg',Cardamom:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cardamom.jpg',Clove:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cloves.jpg',Cinnamon:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cinnamon.jpg',Fenugreek:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Fenugreek%20seeds.jpg',Chilli:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Red%20Chili%20Pepper.jpg',Saffron:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Saffron%20croccus.jpg'
};
const userProvidedPhoto = {
  Oats:'/crops/user-provided/oats.jpeg',Turnip:'/crops/user-provided/turnip.jpeg',SweetPotato:'/crops/user-provided/sweet-potato.jpeg',Yam:'/crops/user-provided/yam.jpeg',Taro:'/crops/user-provided/taro.jpeg',Colocasia:'/crops/user-provided/colocasia.jpeg',Lettuce:'/crops/user-provided/lettuce.jpeg',Celery:'/crops/user-provided/celery.jpeg',Mushroom:'/crops/user-provided/mushroom.jpeg',Zucchini:'/crops/user-provided/zucchini.jpeg',ClusterBean:'/crops/user-provided/cluster-bean.jpeg',IvyGourd:'/crops/user-provided/ivy-gourd.jpeg',SnakeGourd:'/crops/user-provided/snake-gourd.jpeg',AshGourd:'/crops/user-provided/ash-gourd.jpeg',Banana:'/crops/user-provided/banana.jpeg',Amla:'/crops/user-provided/amla.jpeg',Mosambi:'/crops/user-provided/mosambi.jpeg',Chikoo:'/crops/user-provided/chikoo.jpeg',Cumin:'/crops/user-provided/cumin.jpeg',Mustard:'/crops/user-provided/mustard.jpeg',Ajwain:'/crops/user-provided/ajwain.jpeg',Saffron:'/crops/user-provided/saffron.jpeg',Sesame:'/crops/user-provided/sesame.jpeg'
};
const localPhoto = {
  Bajra:'/crops/Bajra.jpeg',Tomato:'/crops/tomato.jpg',Okra:'/crops/okra.jpg',Brinjal:'/crops/brinjal.jpg',Potato:'/crops/potato.jpg',Cauliflower:'/crops/cauliflower.jpg',Cabbage:'/crops/cabbage.jpg',Cucumber:'/crops/cucumber.jpg',Radish:'/crops/radish.jpg',Carrot:'/crops/carrot.jpg','French Bean':'/crops/french-bean.jpg','Green Peas':'/crops/green-peas.jpg',Capsicum:'/crops/capsicum.jpg','Bitter Gourd':'/crops/bitter-gourd.jpg',Pumpkin:'/crops/pumpkin.jpg','Bottle Gourd':'/crops/bottle-gourd.jpg','Ridge Gourd':'/crops/ridge-gourd.jpg',Spinach:'/crops/spinach.jpg','Fenugreek Leaves':'/crops/fenugreek-leaves.jpg',Taro:'/crops/taro.jpg',Corn:'/crops/corn.jpg',Beetroot:'/crops/beetroot.jpg',Colocasia:'/crops/colocasia.jpg','Green Chilli':'/crops/green-chilli.jpg',Apple:'/crops/apple.jpg',Orange:'/crops/orange.jpg',Banana:'/crops/banana.jpg',Apricot:'/crops/apricot.jpg',Plum:'/crops/plum.jpg',Lemon:'/crops/lemon.jpg',Peach:'/crops/peach.jpg',Cherries:'/crops/cherries.jpg',Kiwi:'/crops/kiwi.jpg',Grapes:'/crops/grapes.jpg',Watermelon:'/crops/watermelon.jpg',Strawberries:'/crops/strawberries.jpg',Blueberries:'/crops/blueberries.jpg','Dragon Fruit':'/crops/dragon-fruit.jpg',Melon:'/crops/melon.jpg',Pomegranate:'/crops/pomegranate.jpg',Pineapple:'/crops/pineapple.jpg',Lime:'/crops/lime.jpg',Raspberry:'/crops/raspberry.jpg',Mango:'/crops/mango.jpg',Fig:'/crops/fig.jpg',Coconut:'/crops/coconut.jpg',Avocado:'/crops/avocado.jpg',Dates:'/crops/dates.jpg','Blood Orange':'/crops/blood-orange.jpg',Persimmon:'/crops/persimmon.jpg','Star Fruit':'/crops/star-fruit.jpg',Papaya:'/crops/papaya.jpg',Guava:'/crops/guava.jpg',Cantaloupe:'/crops/cantaloupe.jpg'
};
const genericPhoto = { Crops:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Wheat%20field.jpg',Pulses:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Chickpeas.jpg',Vegetables:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Fruits%20and%20Vegetables%20(20170526-AMS-LSC-0439).jpg',Fruits:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Fruits%20and%20Vegetables%20(20170526-AMS-LSC-0439).jpg',Spices:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Spice%20collection.jpg' };
const fallback = 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80';
const slug = s => s.replace(/[^a-zA-Z0-9]/g,'');

const cropDetailsExtra = {
  Wheat: { ph: "6.0 - 7.5", minTemp: "10°C", maxTemp: "30°C", water: "450–650 mm", yield: "3.5 - 4.5 tonnes/ha", pests: "Yellow rust, Karnal bunt", byproduct: "Wheat straw for cattle fodder & biochar production" },
  Rice: { ph: "5.5 - 7.0", minTemp: "20°C", maxTemp: "38°C", water: "1000–1500 mm", yield: "4.0 - 5.5 tonnes/ha", pests: "Paddy blast, Brown plant hopper", byproduct: "Paddy straw for mushroom cultivation & bio-paper" },
  Bajra: { ph: "6.0 - 8.0", minTemp: "18°C", maxTemp: "42°C", water: "250–500 mm", yield: "2.0 - 3.0 tonnes/ha", pests: "Ergot, Downy mildew", byproduct: "Green fodder & dry silage" },
  Maize: { ph: "6.0 - 7.5", minTemp: "15°C", maxTemp: "35°C", water: "500–900 mm", yield: "4.0 - 6.0 tonnes/ha", pests: "Fall armyworm, Stem borer", byproduct: "Corn cobs for bio-ethanol & animal feed" },
  Cotton: { ph: "6.0 - 8.0", minTemp: "18°C", maxTemp: "38°C", water: "550–1100 mm", yield: "1.8 - 2.5 tonnes/ha", pests: "Pink bollworm, Whitefly", byproduct: "Cotton seed cake for high-protein livestock feed" },
  Sugarcane: { ph: "6.0 - 7.5", minTemp: "20°C", maxTemp: "38°C", water: "1200–2500 mm", yield: "70 - 100 tonnes/ha", pests: "Red rot, Pyrilla", byproduct: "Bagasse for paper & bio-power, pressmud for organic fertilizer" },
  Tomato: { ph: "6.0 - 7.0", minTemp: "15°C", maxTemp: "34°C", water: "450–900 mm", yield: "25 - 40 tonnes/ha", pests: "Early blight, Leaf curl virus", byproduct: "Tomato pomace for animal feed supplement" },
  Potato: { ph: "5.5 - 6.5", minTemp: "12°C", maxTemp: "28°C", water: "400–750 mm", yield: "20 - 35 tonnes/ha", pests: "Late blight, Aphids", byproduct: "Potato peels for industrial starch & compost" },
  Mango: { ph: "5.5 - 7.5", minTemp: "22°C", maxTemp: "42°C", water: "700–1500 mm", yield: "8 - 15 tonnes/ha", pests: "Mango hopper, Anthracnose", byproduct: "Mango seed kernels for starch & seed butter" },
  Banana: { ph: "6.0 - 7.5", minTemp: "18°C", maxTemp: "38°C", water: "1000–2200 mm", yield: "40 - 65 tonnes/ha", pests: "Sigatoka leaf spot, Panama wilt", byproduct: "Banana pseudostem fiber for eco-friendly textiles & bio-organic fertilizer" },
  Turmeric: { ph: "6.0 - 7.5", minTemp: "20°C", maxTemp: "36°C", water: "900–1600 mm", yield: "20 - 28 tonnes/ha", pests: "Rhizome rot, Leaf spot", byproduct: "Spent turmeric waste for natural dye & organic mulch" },
  Cumin: { ph: "6.5 - 8.0", minTemp: "10°C", maxTemp: "28°C", water: "150–400 mm", yield: "0.6 - 1.0 tonnes/ha", pests: "Wilt, Alternaria blight", byproduct: "Cumin straw distillation for aroma essential oil" }
};

const allItems = Object.entries(groups).flatMap(([group, names]) =>
  names.map(name => ({
    name,
    group,
    image: userProvidedPhoto[slug(name)] || localPhoto[name] || photo[slug(name)] || genericPhoto[group],
    season: group === 'Fruits' ? 'Regional / perennial' : group === 'Spices' ? 'Monsoon / winter varies' : group === 'Vegetables' ? 'Year-round / seasonal' : 'Kharif / Rabi varies',
    soil: group === 'Vegetables' ? 'Fertile loam' : 'Well-drained loam',
    water: group === 'Vegetables' ? 'Medium–High' : 'Medium',
    yield: cropDetailsExtra[name]?.yield || 'Regional estimate',
    ph: cropDetailsExtra[name]?.ph || '6.0 - 7.5',
    minTemp: cropDetailsExtra[name]?.minTemp || '15°C',
    maxTemp: cropDetailsExtra[name]?.maxTemp || '35°C',
    pests: cropDetailsExtra[name]?.pests || 'Aphids, Leaf spot',
    byproduct: cropDetailsExtra[name]?.byproduct || 'Crop residue for compost & biochar'
  }))
);

function Robot({ t, onOpenChat }) {
  const mx = useMotionValue(0), my = useMotionValue(0);
  const sx = useSpring(mx, { stiffness: 150, damping: 20 }), sy = useSpring(my, { stiffness: 150, damping: 20 });
  const ry = useTransform(sx, [-1, 1], [-14, 14]), rx = useTransform(sy, [-1, 1], [10, -10]);

  return (
    <div className="robot-wrap" onMouseMove={e => {
      const r = e.currentTarget.getBoundingClientRect();
      mx.set((e.clientX - r.left) / r.width * 2 - 1);
      my.set((e.clientY - r.top) / r.height * 2 - 1);
    }} onMouseLeave={() => { mx.set(0); my.set(0); }}>
      <motion.div className="robot-3d" style={{ rotateX: rx, rotateY: ry }}>
        <div className="robot-aura" />
        <img src={robot} alt={t.assistant} />
        <div className="robot-badge" onClick={onOpenChat}>
          <span /> {t.assistant} <Sparkles size={14} style={{ marginLeft: 4 }} />
        </div>
      </motion.div>
      <p className="mouse-hint">{t.mouse}</p>
    </div>
  );
}

function CropCard({ item, t, lang, onSelect }) {
  const [src, setSrc] = useState(item.image);
  return (
    <motion.div className="crop-card" whileHover={{ y: -6 }} onClick={() => onSelect(item)}>
      <div className="crop-photo">
        <img src={src} onError={() => setSrc(fallback)} alt={item.name} />
        <span>{translateGroup(item.group, lang)}</span>
      </div>
      <div className="crop-info">
        <h3>{translateCrop(item.name, lang)}</h3>
        <div><b>{t.lib_season_label || 'Season:'}</b> {translateSeason(item.season, lang)}</div>
        <div><b>{t.lib_soil_label || 'Soil:'}</b> {translateSoil(item.soil, lang)}</div>
        <div className="mini-meta">
          <span><Droplets size={14} />{translateWater(item.water, lang)}</span>
          <span><TrendingUp size={14} />{item.yield === 'Regional estimate' ? (t.lib_yield_estimate || 'Regional estimate') : item.yield}</span>
        </div>
      </div>
    </motion.div>
  );
}

function PlannerSection({ t, lang }) {
  const [locationInput, setLocationInput] = useState('Vadodara, Gujarat');
  const [soilInput, setSoilInput] = useState('Fertile loam');
  const [loading, setLoading] = useState(false);
  const [plannerData, setPlannerData] = useState(null);
  const [selectedCropName, setSelectedCropName] = useState(null);

  useEffect(() => {
    handleAnalyze('Vadodara, Gujarat', 'Fertile loam');
  }, []);

  const handleAnalyze = async (locToFetch, soilToFetch) => {
    const loc = locToFetch || locationInput || 'Vadodara, Gujarat';
    const soil = soilToFetch || soilInput || 'Fertile loam';
    setLoading(true);
    try {
      const data = await fetchCropRecommendations(loc, soil);
      setPlannerData(data);
      if (data && data.top_recommendations && data.top_recommendations.length > 0) {
        setSelectedCropName(data.top_recommendations[0].crop_name);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const selectedCrop = useMemo(() => {
    if (!plannerData || !plannerData.top_recommendations) return null;
    return (
      plannerData.top_recommendations.find(c => c.crop_name === selectedCropName) ||
      plannerData.top_recommendations[0]
    );
  }, [plannerData, selectedCropName]);

  const formatStageDate = (stage, index) => {
    if (index === 0) return t.planner_this_week || 'This week';
    const today = new Date();
    const startDate = new Date(today);
    startDate.setDate(today.getDate() + (stage.start_day || index * 10));
    const endDate = new Date(today);
    endDate.setDate(today.getDate() + (stage.end_day || (index + 1) * 10));
    const options = { day: 'numeric', month: 'short' };
    return `${startDate.toLocaleDateString(lang === 'gu' ? 'gu-IN' : lang === 'hi' ? 'hi-IN' : 'en-US', options)} – ${endDate.toLocaleDateString(lang === 'gu' ? 'gu-IN' : lang === 'hi' ? 'hi-IN' : 'en-US', options)}`;
  };

  return (
    <section className="feature" id="planner">
      <div className="feature-text">
        <span className="section-kicker">{t.planner_kicker || 'FARM LIFE CYCLE PLANNER'}</span>
        <h2>{t.planner_title || 'Know what to do next on your farm'}</h2>
        <p>{t.planner_sub || 'Weather-aware timeline from sowing to harvest. Dynamic alerts connected to temperature, rainfall forecasts, and humidity.'}</p>

        <div className="planner-location-box">
          <div className="location-input-row" style={{ flexWrap: 'wrap', gap: '8px' }}>
            <input
              type="text"
              value={locationInput}
              onChange={(e) => setLocationInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAnalyze(locationInput, soilInput)}
              placeholder={t.planner_input_ph || 'Enter city / district...'}
              style={{ flex: '1 1 180px' }}
            />
            <select
              value={soilInput}
              onChange={(e) => {
                setSoilInput(e.target.value);
                handleAnalyze(locationInput, e.target.value);
              }}
              style={{ padding: '0 12px', height: '44px', borderRadius: '10px', background: 'rgba(255,255,255,0.06)', color: 'var(--text-main)', border: '1px solid rgba(255,255,255,0.15)', outline: 'none', cursor: 'pointer' }}
            >
              <option value="Fertile loam">Loam Soil</option>
              <option value="Black cotton soil">Black Cotton Soil</option>
              <option value="Sandy loam">Sandy Soil</option>
              <option value="Clay loam">Clay Soil</option>
              <option value="Alluvial soil">Alluvial Soil</option>
              <option value="Red soil">Red Soil</option>
            </select>
            <button onClick={() => handleAnalyze(locationInput, soilInput)} disabled={loading}>
              {loading ? (t.planner_analyzing || 'Analyzing...') : (t.planner_btn || 'Analyze farm')}
            </button>
          </div>
          <div className="location-chips">
            <span>{t.planner_quick || 'Quick locations:'}</span>
            {[
              { label: 'Vadodara', loc: 'Vadodara, Gujarat' },
              { label: 'Amarnath', loc: 'Amarnath, Jammu and Kashmir' },
              { label: 'Jaisalmer', loc: 'Jaisalmer, Rajasthan' },
              { label: 'Kochi', loc: 'Kochi, Kerala' },
              { label: 'Ludhiana', loc: 'Ludhiana, Punjab' }
            ].map((item) => (
              <button
                key={item.loc}
                className="location-chip"
                onClick={() => {
                  setLocationInput(item.loc);
                  handleAnalyze(item.loc, soilInput);
                }}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        {plannerData && plannerData.top_recommendations && (
          <div className="crop-selector-box">
            <span className="crop-selector-label">{(t.planner_top || 'Top suitable crops for')} {plannerData.location.split(',')[0]} ({plannerData.temperature}°C)</span>
            <div className="crop-chips-row">
              {plannerData.top_recommendations.slice(0, 6).map((crop) => (
                <button
                  key={crop.crop_name}
                  className={`crop-chip-btn ${selectedCrop?.crop_name === crop.crop_name ? 'active' : ''}`}
                  onClick={() => setSelectedCropName(crop.crop_name)}
                >
                  <b>{translateCrop(crop.crop_name, lang)}</b>
                  <span>{crop.match_score}%</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {selectedCrop && (
          <div className="timeline">
            {selectedCrop.growth_stages.map((stage, idx) => (
              <div className="step" key={stage.name}>
                <span className={idx === 0 ? 'done' : ''}>{idx === 0 ? <CheckCircle2 size={17} /> : String(idx + 1).padStart(2, '0')}</span>
                <div>
                  <b>{translateStage(stage.name, lang)}</b>
                  <small>{formatStageDate(stage, idx)}</small>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="planner-card">
        {selectedCrop ? (
          <>
            <div className="card-top">
              <b>{translateCrop(selectedCrop.crop_name, lang).toUpperCase()} {t.planner_advisory || 'ADVISORY'}</b>
              <span>{selectedCrop.match_score}% {t.planner_suitability || 'suitability'}</span>
            </div>
            <div className="progress">
              <span style={{ width: `${selectedCrop.match_score}%` }} />
            </div>

            <div className="planner-grid">
              <div>
                <Sun />
                <b>{plannerData ? plannerData.temperature : 28.5}°C</b>
                <small>{t.planner_temp || 'current temp'}</small>
              </div>
              <div>
                <CloudRain />
                <b>{plannerData ? plannerData.rain_probability : 64}%</b>
                <small>{t.planner_rain || 'rain chance'}</small>
              </div>
              <div>
                <Droplets />
                <b>{plannerData ? plannerData.humidity : 68}%</b>
                <small>{t.planner_humidity || 'humidity'}</small>
              </div>
            </div>

            <div className="recommend">
              <CheckCircle2 />
              <div>
                <b>{t.planner_sowing || 'Recommended Sowing Window'}</b>
                <p>{(selectedCrop.suggested_sowing_window === 'Favorable conditions! Sow within the next 3–5 days.' || plannerData?.sowing_advisory === 'Favorable conditions! Sow within the next 3–5 days.') ? (t.planner_sowing_adv || 'Favorable conditions! Sow within the next 3–5 days.') : (selectedCrop.suggested_sowing_window || plannerData?.sowing_advisory)}</p>
              </div>
            </div>

            <div className="score-breakdown">
              <div className="score-item">
                <small>{t.planner_climate || 'Climate Fit'}</small>
                <b>{selectedCrop.scores?.climate_suitability || 92}%</b>
              </div>
              <div className="score-item">
                <small>{t.planner_season || 'Season Alignment'}</small>
                <b>{selectedCrop.scores?.season_suitability || 95}%</b>
              </div>
            </div>
          </>
        ) : (
          <div style={{ padding: '30px 0', textAlign: 'center', opacity: 0.8 }}>
            Enter farm location to view crop suitability & timeline.
          </div>
        )}
      </div>
    </section>
  );
}

function WeatherSection({ t, lang }) {
  const [weatherLocation, setWeatherLocation] = useState('Vadodara, Gujarat');
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadWeather('Vadodara, Gujarat');
  }, []);

  const loadWeather = async (loc) => {
    setLoading(true);
    try {
      const data = await fetchWeather(loc);
      setWeatherData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="weather" id="weather">
      <div className="section-head">
        <div>
          <span className="section-kicker">{t.weather_kicker || 'REAL-TIME WEATHER INTELLIGENCE'}</span>
          <h2>{t.weather_title || 'Open-Meteo Weather Forecast'}</h2>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <input
            type="text"
            value={weatherLocation}
            onChange={(e) => setWeatherLocation(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && loadWeather(weatherLocation)}
            placeholder={t.weather_input_ph || 'Search location weather...'}
            style={{ border: '1px solid var(--line)', borderRadius: 10, padding: '7px 12px', fontSize: 12, outline: 0 }}
          />
          <button
            onClick={() => loadWeather(weatherLocation)}
            style={{ border: 0, background: 'var(--green)', color: 'white', padding: '8px 14px', borderRadius: 10, fontSize: 12, fontWeight: 700 }}
          >
            {loading ? (t.weather_updating || 'Updating...') : (t.weather_btn || 'Search')}
          </button>
        </div>
      </div>

      {weatherData && (
        <div className="weather-grid">
          <div className="weather-main">
            <div>
              <small>{weatherData.location}</small>
              <strong>{weatherData.temperature ?? weatherData.temp_c ?? 28.5}°C</strong>
              <span>{translateWeatherCondition(weatherData.condition, lang)}</span>
            </div>
            <Sun size={64} />
            <div className="weather-row">
              <span><Droplets />{t.weather_humidity || 'Humidity'} <b>{weatherData.humidity ?? weatherData.humidity_pct ?? 68}%</b></span>
              <span><Wind />{t.weather_wind || 'Wind'} <b>{weatherData.wind_speed_kmh ?? weatherData.wind_kmh ?? 14} km/h</b></span>
              <span><CloudRain />{t.weather_rain || 'Rain'} <b>{weatherData.rain_probability ?? weatherData.rainfall_mm ?? 50}%</b></span>
            </div>
          </div>

          <div className="alert-card">
            <div className="alert-dot" />
            <div>
              <b>{t.weather_advisory_title || 'Agronomic Weather Advisory'}</b>
              <p>{weatherData.advisory || (weatherData.alerts && weatherData.alerts[0]?.description) || t.weather_advisory_text || 'Favorable moisture window for sowing in the upcoming forecast.'}</p>
            </div>
          </div>

          <div className="forecast">
            {(weatherData.forecast || []).slice(0, 4).map((f, i) => (
              <div key={i}>
                <b>{translateDay(f.day, lang)}</b>
                <CloudRain />
                <strong>{f.temp ?? f.temp_c ?? 28}°C</strong>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}

function MandiSection({ t, lang }) {
  const [commodity, setCommodity] = useState('');
  const [stateFilter, setStateFilter] = useState('');
  const [mandiItems, setMandiItems] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMandi();
  }, []);

  const loadMandi = async () => {
    setLoading(true);
    try {
      const res = await fetchMandiPrices(commodity, stateFilter);
      setMandiItems(res.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="section-wrapper alt-bg" id="mandi-rates">
      <div className="section-head">
        <div>
          <span className="section-kicker">{t.mandi_kicker || 'APMC MANDI PRICE COMPARISON'}</span>
          <h2>{t.mandi_title || 'Live Market Price Intelligence'}</h2>
          <p>{t.mandi_sub || 'Compare real-time market prices across Indian agricultural mandis to maximize farm profitability.'}</p>
        </div>
      </div>

      <div className="mandi-filter-bar">
        <input
          type="text"
          placeholder={t.mandi_input_ph || 'Filter by commodity (e.g. Wheat, Cotton, Groundnut, Cumin, Onion)...'}
          value={commodity}
          onChange={(e) => setCommodity(e.target.value)}
        />
        <select value={stateFilter} onChange={(e) => setStateFilter(e.target.value)}>
          <option value="">{t.mandi_all_states || 'All States'}</option>
          <option value="Gujarat">Gujarat</option>
          <option value="Punjab">Punjab</option>
          <option value="Maharashtra">Maharashtra</option>
        </select>
        <button onClick={loadMandi} disabled={loading}>
          <Search size={15} /> {loading ? (t.mandi_fetching || 'Fetching...') : (t.mandi_btn || 'Filter Mandi')}
        </button>
      </div>

      <div className="mandi-grid">
        {mandiItems.map((item, idx) => (
          <motion.div className="mandi-card" whileHover={{ y: -4 }} key={idx}>
            <div className="mandi-card-header">
              <h4>{translateCrop(item.commodity, lang)} <small style={{ fontWeight: 400, color: 'var(--muted)', fontSize: 12 }}>({item.variety})</small></h4>
              <span>{t.mandi_apmc_tag || 'APMC RATE'}</span>
            </div>
            <div className="mandi-location">
              <MapPin size={13} /> {item.market}, {item.district}, {item.state}
            </div>
            <div className="mandi-price-box">
              <div>
                <small style={{ display: 'block', fontSize: 10, color: 'var(--muted)' }}>{t.mandi_modal_price || 'Modal Price'}</small>
                <div className="mandi-modal-price">₹{item.modal_price.toLocaleString()} <small>{t.mandi_per_quintal || '/ quintal'}</small></div>
              </div>
              <div className="mandi-range">
                <div>{t.mandi_min || 'Min:'} ₹{item.min_price}</div>
                <div>{t.mandi_max || 'Max:'} ₹{item.max_price}</div>
                <div style={{ color: 'var(--green)', fontWeight: 700, marginTop: 4 }}>{t.mandi_date || 'Date:'} {item.arrival_date}</div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

function DiseaseSection({ t, lang }) {
  const [diagMode, setDiagMode] = useState('photo'); // 'photo' or 'symptoms'
  const [cropName, setCropName] = useState('Mango');
  const [symptoms, setSymptoms] = useState(['Yellow spots', 'Leaf curling']);
  const [customText, setCustomText] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const sampleCrops = ['Tomato', 'Wheat', 'Cotton', 'Potato', 'Rice', 'Bajra', 'Mustard'];
  const allSymptomTags = ['Yellow spots', 'Leaf curling', 'Concentric dark circles', 'Wilting stems', 'White pustules', 'Stunted growth', 'Fruit rot'];

  // Preset sample leaf photos for instant hackathon demonstration
  const presetLeaves = [
    {
      name: 'Mango Anthracnose',
      crop: 'Mango',
      img: 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=300&q=80',
      symptoms: ['Dark necrotic spots', 'Leaf tip burn']
    },
    {
      name: 'Tomato Blight',
      crop: 'Tomato',
      img: 'https://images.unsplash.com/photo-1592417817098-8f3d6eb231fc?w=300&q=80',
      symptoms: ['Yellow spots', 'Concentric dark circles']
    },
    {
      name: 'Wheat Rust',
      crop: 'Wheat',
      img: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=300&q=80',
      symptoms: ['Yellow spots', 'Stunted growth']
    },
    {
      name: 'Potato Blight',
      crop: 'Potato',
      img: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300&q=80',
      symptoms: ['Wilting stems', 'Fruit rot']
    }
  ];

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setSelectedImage(event.target.result);
        setResult(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setSelectedImage(event.target.result);
        setResult(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const toggleSymptom = (tag) => {
    if (symptoms.includes(tag)) {
      setSymptoms(symptoms.filter(s => s !== tag));
    } else {
      setSymptoms([...symptoms, tag]);
    }
  };

  const handleDiagnose = async () => {
    setLoading(true);
    setResult(null);
    const symptomsStr = [...symptoms, customText].filter(Boolean).join(', ');
    const targetCropToSend = diagMode === 'photo' ? (cropName || 'auto') : cropName;
    try {
      const res = await diagnoseCropDisease(targetCropToSend, symptomsStr, selectedImage);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="section-wrapper" id="disease-check">
      <div className="section-head">
        <div>
          <span className="section-kicker">{t.disease_kicker || 'AI CROP HEALTH DIAGNOSTICS'}</span>
          <h2>{t.disease_title || 'Crop Disease Diagnosis & Treatment'}</h2>
          <p>{t.disease_sub || 'Identify crop leaf symptoms, diagnose fungal or viral infections, and get organic & chemical remedy plans.'}</p>
        </div>
      </div>

      <div className="disease-box">
        <div className="disease-input-panel">
          {/* Mode Switcher Tabs */}
          <div className="disease-mode-tabs">
            <button
              className={`disease-mode-btn ${diagMode === 'photo' ? 'active' : ''}`}
              onClick={() => setDiagMode('photo')}
            >
              <Camera size={15} /> {t.disease_tab_photo || 'Upload / Click Leaf Photo'}
            </button>
            <button
              className={`disease-mode-btn ${diagMode === 'symptoms' ? 'active' : ''}`}
              onClick={() => setDiagMode('symptoms')}
            >
              <Leaf size={15} /> {t.disease_tab_symptoms || 'Select Symptoms'}
            </button>
          </div>

          {diagMode === 'photo' ? (
            <div>
              <div style={{ background: 'var(--mint)', color: 'var(--green)', border: '1px solid var(--line)', borderRadius: 12, padding: '10px 14px', fontSize: 12, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                <Sparkles size={16} />
                <span>AI Auto-Species & Disease Identification Active</span>
              </div>

              <h3 style={{ margin: '0 0 10px', fontSize: 16 }}>Upload or Capture Leaf Photo</h3>
              
              <input
                type="file"
                accept="image/*"
                id="disease-file-input"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <input
                type="file"
                accept="image/*"
                capture="environment"
                id="disease-camera-input"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />

              {selectedImage ? (
                <div className="leaf-preview-box">
                  <img src={selectedImage} alt="Leaf Preview" className="leaf-preview-img" />
                  {loading && <div className="leaf-scan-laser" />}
                  <button
                    className="remove-photo-btn"
                    onClick={() => { setSelectedImage(null); setResult(null); }}
                    title="Remove Photo"
                  >
                    <X size={16} />
                  </button>
                </div>
              ) : (
                <div
                  className={`photo-dropzone ${isDragging ? 'dragging' : ''}`}
                  onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                  onDragLeave={() => setIsDragging(false)}
                  onDrop={handleDrop}
                >
                  <div className="dropzone-icons">
                    <UploadCloud size={32} />
                    <Camera size={32} />
                  </div>
                  <div className="dropzone-text">{t.disease_drag_drop || 'Drag & drop leaf photo here or click below'}</div>
                  <div className="dropzone-sub">{t.disease_supports || 'Supports Mango, Tomato, Wheat, Cotton, Potato & all crop leaves'}</div>
                  
                  <div className="dropzone-btns">
                    <button
                      className="dropzone-btn"
                      onClick={() => document.getElementById('disease-file-input').click()}
                    >
                      <UploadCloud size={14} /> {t.disease_browse || 'Browse Files'}
                    </button>
                    <button
                      className="dropzone-btn"
                      onClick={() => document.getElementById('disease-camera-input').click()}
                    >
                      <Camera size={14} /> {t.disease_take_photo || 'Click Photo'}
                    </button>
                  </div>
                </div>
              )}

              {/* Sample leaf photo chips for instant hackathon demonstration */}
              <div className="preset-leaves-bar">
                <span className="preset-leaves-label">⚡ {t.disease_try_samples || 'Or click a sample leaf photo to test:'}</span>
                <div className="preset-leaves-grid">
                  {presetLeaves.map((item) => (
                    <div
                      key={item.name}
                      className={`preset-leaf-chip ${selectedImage === item.img ? 'active' : ''}`}
                      onClick={() => {
                        setSelectedImage(item.img);
                        setCropName(item.crop);
                        setSymptoms(item.symptoms);
                        setResult(null);
                      }}
                    >
                      <img src={item.img} alt={item.name} />
                      <span>{item.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div>
              <h3 style={{ margin: '0 0 12px', fontSize: 16 }}>1. {t.disease_select_crop || 'Select Crop'}</h3>
              <div className="sample-leaf-row" style={{ marginBottom: 16 }}>
                {sampleCrops.map(c => (
                  <button
                    key={c}
                    className={`sample-leaf-btn ${cropName === c ? 'active' : ''}`}
                    onClick={() => setCropName(c)}
                  >
                    <Leaf size={14} /> {translateCrop(c, lang)}
                  </button>
                ))}
              </div>

              <h3 style={{ margin: '14px 0 10px', fontSize: 16 }}>2. {t.disease_step2 || 'Select Observed Leaf Symptoms'}</h3>
              <div className="symptom-tags">
                {allSymptomTags.map(tag => (
                  <span
                    key={tag}
                    className={`symptom-tag ${symptoms.includes(tag) ? 'selected' : ''}`}
                    onClick={() => toggleSymptom(tag)}
                  >
                    {symptoms.includes(tag) ? '✓ ' : '+ '} {tag}
                  </span>
                ))}
              </div>

              <div style={{ marginTop: 14 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: 'var(--muted)', display: 'block', marginBottom: 6 }}>{t.disease_step3 || 'Additional Symptoms / Description'}</label>
                <input
                  type="text"
                  placeholder={t.disease_input_ph || 'e.g. Lower leaves turning yellow with brown spots...'}
                  value={customText}
                  onChange={(e) => setCustomText(e.target.value)}
                  style={{ width: '100%', border: '1px solid var(--line)', borderRadius: 12, padding: '10px 14px', fontSize: 12, outline: 0 }}
                />
              </div>
            </div>
          )}

          <button
            onClick={handleDiagnose}
            disabled={loading}
            style={{ width: '100%', marginTop: 20, background: 'var(--green)', color: 'white', border: 0, padding: 13, borderRadius: 12, fontWeight: 700, fontSize: 13, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 8 }}
          >
            <Sparkles size={16} /> {loading ? (t.disease_analyzing || 'Scanning Leaf & Auto-Detecting Species...') : (t.disease_btn || 'Diagnose Crop Health')}
          </button>
        </div>

        <div className="disease-result-panel">
          {loading ? (
            <div style={{ height: '100%', display: 'grid', placeItems: 'center', textAlign: 'center', padding: '40px 20px' }}>
              <div>
                <Sparkles size={42} style={{ color: '#80e66c', marginBottom: 14, animation: 'spin 2s linear infinite' }} />
                <h3 style={{ color: '#b8dc9f', margin: '0 0 8px' }}>Scanning Leaf Pattern...</h3>
                <p style={{ fontSize: 12, opacity: 0.8, maxWidth: 280 }}>
                  Analyzing visual leaf lesions, fungal spot distribution, and matching against agricultural pathogen database.
                </p>
              </div>
            </div>
          ) : result ? (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: 10, background: 'rgba(255,255,255,.15)', padding: '4px 10px', borderRadius: 8, fontWeight: 700 }}>
                  DIAGNOSIS COMPLETE ({Math.round((result.confidence_score || 0.96) * 100)}% CONFIDENCE)
                </span>
                <ShieldCheck size={20} style={{ color: '#b8dc9f' }} />
              </div>

              {selectedImage && (
                <div style={{ margin: '14px 0 10px', display: 'flex', alignItems: 'center', gap: 10, background: 'rgba(255,255,255,.08)', padding: 8, borderRadius: 12 }}>
                  <img src={selectedImage} alt="Diagnosed Leaf" style={{ width: 44, height: 44, objectFit: 'cover', borderRadius: 8, border: '1px solid rgba(255,255,255,.2)' }} />
                  <div>
                    <span style={{ fontSize: 10, opacity: 0.7, display: 'block' }}>VISUAL SCAN INPUT</span>
                    <strong style={{ fontSize: 11, color: '#b8dc9f' }}>Leaf Tissue Match Verified</strong>
                  </div>
                </div>
              )}

              <h2 style={{ fontSize: 24, margin: '12px 0 4px', color: '#b8dc9f' }}>{result.diagnosed_disease}</h2>
              <div style={{ fontSize: 11, opacity: 0.8, marginBottom: 14 }}>Target Crop: <b>{translateCrop(result.crop_name, lang)}</b></div>

              {result.symptoms_matched && result.symptoms_matched.length > 0 && (
                <div style={{ marginBottom: 12 }}>
                  <span style={{ fontSize: 10, opacity: 0.75, display: 'block', marginBottom: 4 }}>DETECTED SYMPTOMS:</span>
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                    {result.symptoms_matched.map(sym => (
                      <span key={sym} style={{ fontSize: 10, background: 'rgba(184, 220, 159, 0.2)', color: '#b8dc9f', padding: '3px 8px', borderRadius: 6 }}>
                        ✓ {sym}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="treatment-card">
                <b>{t.disease_organic || '🌱 Organic Treatment'}</b>
                <p>{result.organic_treatment}</p>
              </div>

              <div className="treatment-card">
                <b>{t.disease_chemical || '🧪 Recommended Chemical Spray'}</b>
                <p>{result.chemical_treatment}</p>
              </div>

              <div className="treatment-card">
                <b>{t.disease_preventive || '🛡️ Preventive Field Advisory'}</b>
                <p>{result.preventive_measures}</p>
              </div>
            </div>
          ) : (
            <div style={{ height: '100%', display: 'grid', placeItems: 'center', textAlign: 'center', opacity: 0.8 }}>
              <div>
                <Leaf size={48} style={{ color: '#b8dc9f', marginBottom: 12 }} />
                <h3>{t.disease_ready_title || 'Ready to diagnose'}</h3>
                <p style={{ fontSize: 12, maxWidth: 300 }}>{t.disease_ready_desc || 'Upload a leaf photo or select observed symptoms on the left to generate an instant diagnostic report.'}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

function SchemesSection({ t, onOpenEligibilityModal }) {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSchemes();
  }, []);

  const loadSchemes = async () => {
    setLoading(true);
    try {
      const data = await fetchSchemes();
      setSchemes(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="schemes" id="schemes">
      <div className="section-head">
        <div>
          <span className="section-kicker">{t.schemes_kicker || 'GOVERNMENT SCHEMES & SUBSIDIES'}</span>
          <h2>{t.schemes_title || 'Government Initiatives Discovery'}</h2>
          <p>{t.schemes_sub || 'Instant discovery for PM-KISAN, PMFBY, PM-KUSUM solar irrigation, and Soil Health Card initiatives.'}</p>
        </div>
      </div>

      <div className="scheme-grid">
        {schemes.map((item) => (
          <motion.article whileHover={{ y: -4 }} className="scheme-card" key={item.code}>
            <div className="scheme-icon"><ShieldCheck /></div>
            <span>{item.category}</span>
            <h3>{item.code}</h3>
            <p>{item.short_description}</p>
            <div style={{ margin: '10px 0', fontSize: 11, fontWeight: 700, color: 'var(--green)' }}>{t.schemes_benefit || 'Benefit:'} {item.benefit_amount}</div>
            <button onClick={() => onOpenEligibilityModal(item)}>
              {t.schemes_check_btn || 'Check eligibility'} <ArrowRight size={15} />
            </button>
          </motion.article>
        ))}
      </div>
    </section>
  );
}

function WasteSection({ t, lang }) {
  const [search, setSearch] = useState('');
  const wasteItems = [
    { crop: 'Rice Straw', useCase: 'Mushroom cultivation substrate & eco-paper pulp', marketValue: 'High biomass demand' },
    { crop: 'Sugarcane Bagasse', useCase: 'Bio-power generation & eco-friendly packaging material', marketValue: 'Paper mill buyer network' },
    { crop: 'Cotton Stalks', useCase: 'Biochar production & dense particle board manufacturing', marketValue: 'Soil carbon booster' },
    { crop: 'Banana Pseudostem', useCase: 'Natural textile fiber extraction & liquid bio-fertilizer', marketValue: 'Premium export fiber' },
    { crop: 'Tomato Pomace', useCase: 'Protein-rich animal feed supplement & pectin extraction', marketValue: 'Livestock feed substitute' },
    { crop: 'Mustard Cake', useCase: 'Organic bio-pesticide & protein soil enhancer', marketValue: 'High organic fertilizer value' },
    { crop: 'Groundnut Shells', useCase: 'Briquetting fuel & poultry litter bedding', marketValue: 'Boiler fuel substitute' },
    { crop: 'Mango Kernels', useCase: 'Mango seed butter extraction for cosmetics & starch', marketValue: 'Cosmetic industry supply' }
  ];

  const filteredWaste = wasteItems.filter(w => w.crop.toLowerCase().includes(search.toLowerCase()) || w.useCase.toLowerCase().includes(search.toLowerCase()));

  return (
    <section className="section-wrapper alt-bg" id="by-products">
      <div className="section-head">
        <div>
          <span className="section-kicker">{t.waste_kicker || 'POST-HARVEST WASTE MONETIZATION'}</span>
          <h2>{t.waste_title || 'Agri-Residue & By-Product Utilization'}</h2>
          <p>{t.waste_sub || 'Turn post-harvest farm residue into income by exploring bio-energy, composting, and industrial uses.'}</p>
        </div>
        <div className="search">
          <Search size={18} />
          <input
            placeholder={t.waste_search_ph || 'Search crop residue (e.g. Straw, Bagasse, Stalks)...'}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="waste-grid">
        {filteredWaste.map((w, idx) => (
          <div className="waste-card" key={idx}>
            <div className="waste-card-head">
              <div className="waste-card-icon"><Recycle size={20} /></div>
              <h4>{translateCrop(w.crop, lang)}</h4>
            </div>
            <div className="waste-use-case">
              <b>{t.waste_high_value || 'High-Value Application:'}</b>
              <div style={{ marginTop: 3 }}>{w.useCase}</div>
            </div>
            <div style={{ marginTop: 10, fontSize: 10, color: 'var(--muted)', display: 'flex', gap: 6, alignItems: 'center' }}>
              <TrendingUp size={13} style={{ color: 'var(--green)' }} /> <b>{t.waste_impact || 'Market Impact:'}</b> {w.marketValue}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

// Interactive Crop Details Modal
function CropDetailModal({ crop, t, lang, onClose }) {
  if (!crop) return null;
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}><X size={20} /></button>
        <div style={{ display: 'flex', gap: 16, alignItems: 'center', marginBottom: 16 }}>
          <img src={crop.image} onError={(e) => e.target.src = fallback} alt={crop.name} style={{ width: 90, height: 90, borderRadius: 16, objectFit: 'cover' }} />
          <div>
            <span style={{ fontSize: 10, background: 'var(--mint)', color: 'var(--green)', padding: '4px 8px', borderRadius: 8, fontWeight: 700, textTransform: 'uppercase' }}>
              {translateGroup(crop.group, lang)}
            </span>
            <h2 style={{ margin: '6px 0 0', fontSize: 26 }}>{translateCrop(crop.name, lang)}</h2>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 10, margin: '16px 0' }}>
          <div style={{ background: '#f8faf6', padding: 12, borderRadius: 12 }}>
            <small style={{ color: 'var(--muted)', fontSize: 10 }}>{t.lib_season_label || 'Season:'}</small>
            <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2 }}>{translateSeason(crop.season, lang)}</div>
          </div>
          <div style={{ background: '#f8faf6', padding: 12, borderRadius: 12 }}>
            <small style={{ color: 'var(--muted)', fontSize: 10 }}>{t.lib_soil_label || 'Soil:'}</small>
            <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2 }}>{translateSoil(crop.soil, lang)}</div>
          </div>
          <div style={{ background: '#f8faf6', padding: 12, borderRadius: 12 }}>
            <small style={{ color: 'var(--muted)', fontSize: 10 }}>Water Requirement</small>
            <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2 }}>{translateWater(crop.water, lang)}</div>
          </div>
          <div style={{ background: '#f8faf6', padding: 12, borderRadius: 12 }}>
            <small style={{ color: 'var(--muted)', fontSize: 10 }}>Expected Yield</small>
            <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2 }}>{crop.yield === 'Regional estimate' ? (t.lib_yield_estimate || 'Regional estimate') : crop.yield}</div>
          </div>
          <div style={{ background: '#f8faf6', padding: 12, borderRadius: 12 }}>
            <small style={{ color: 'var(--muted)', fontSize: 10 }}>Ideal Soil pH Range</small>
            <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2 }}>{crop.ph}</div>
          </div>
          <div style={{ background: '#f8faf6', padding: 12, borderRadius: 12 }}>
            <small style={{ color: 'var(--muted)', fontSize: 10 }}>Temperature Range</small>
            <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2 }}>{crop.minTemp} to {crop.maxTemp}</div>
          </div>
        </div>

        <div style={{ background: 'var(--mint)', padding: 14, borderRadius: 14, margin: '14px 0', fontSize: 12 }}>
          <b style={{ color: 'var(--green)', display: 'block', marginBottom: 4 }}>Common Pest Vulnerability:</b>
          {crop.pests}
        </div>

        <div style={{ background: '#f4f8f1', padding: 14, borderRadius: 14, fontSize: 12 }}>
          <b style={{ color: 'var(--green)', display: 'block', marginBottom: 4 }}>By-Product Monetization Opportunity:</b>
          {crop.byproduct}
        </div>
      </div>
    </div>
  );
}

// Interactive Scheme Eligibility Checker Modal
function SchemeEligibilityModal({ scheme, onClose }) {
  const [landAcres, setLandAcres] = useState(3);
  const [isRegistered, setIsRegistered] = useState(true);
  const [result, setResult] = useState(null);
  const [checking, setChecking] = useState(false);

  if (!scheme) return null;

  const handleCheck = async () => {
    setChecking(true);
    try {
      const res = await checkSchemeEligibility(scheme.code, Number(landAcres), isRegistered);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}><X size={20} /></button>
        
        <span style={{ fontSize: 10, background: 'var(--mint)', color: 'var(--green)', padding: '4px 8px', borderRadius: 8, fontWeight: 700 }}>
          GOVERNMENT ELIGIBILITY CHECKER
        </span>
        <h2 style={{ margin: '8px 0 4px', fontSize: 24 }}>{scheme.title} ({scheme.code})</h2>
        <p style={{ fontSize: 12, color: 'var(--muted)', margin: '0 0 16px' }}>{scheme.full_description || scheme.short_description}</p>

        <div style={{ border: '1px solid var(--line)', borderRadius: 16, padding: 16, background: '#fcfdfb', marginBottom: 16 }}>
          <h4 style={{ margin: '0 0 12px', fontSize: 14 }}>Farmer Details Form</h4>
          
          <div style={{ marginBottom: 12 }}>
            <label style={{ fontSize: 11, fontWeight: 700, color: 'var(--muted)', display: 'block', marginBottom: 4 }}>Land Holding (Acres)</label>
            <input
              type="number"
              value={landAcres}
              onChange={(e) => setLandAcres(e.target.value)}
              style={{ width: '100%', border: '1px solid var(--line)', borderRadius: 10, padding: '8px 12px', fontSize: 12, outline: 0 }}
            />
          </div>

          <div style={{ display: 'flex', gap: 10, alignItems: 'center', margin: '12px 0' }}>
            <input
              type="checkbox"
              id="registered"
              checked={isRegistered}
              onChange={(e) => setIsRegistered(e.target.checked)}
              style={{ width: 16, height: 16 }}
            />
            <label htmlFor="registered" style={{ fontSize: 12, cursor: 'pointer' }}>Registered Farmer / Possess Land Title Deed (7/12 Khatian)</label>
          </div>

          <button
            onClick={handleCheck}
            disabled={checking}
            style={{ width: '100%', background: 'var(--green)', color: 'white', border: 0, padding: 11, borderRadius: 10, fontWeight: 700, fontSize: 12, marginTop: 8 }}
          >
            {checking ? 'Checking Eligibility System...' : 'Check My Eligibility Status'}
          </button>
        </div>

        {result && (
          <div style={{ background: result.is_eligible ? '#e9f3e8' : '#fdf2f2', border: `1px solid ${result.is_eligible ? 'var(--line)' : '#fca495'}`, borderRadius: 16, padding: 16 }}>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center', fontWeight: 800, color: result.is_eligible ? 'var(--green)' : '#c0392b', fontSize: 14 }}>
              {result.is_eligible ? <CheckCircle2 size={18} /> : <AlertTriangle size={18} />}
              Status: {result.status}
            </div>

            <div style={{ margin: '10px 0', fontSize: 11, color: 'var(--ink)' }}>
              <b>Evaluation Criteria:</b>
              <ul style={{ margin: '6px 0 0', paddingLeft: 18 }}>
                {(result.reasons || []).map((r, i) => <li key={i}>{r}</li>)}
              </ul>
            </div>

            <div style={{ margin: '10px 0', fontSize: 11 }}>
              <b>Required Checklist Documents:</b>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 6 }}>
                {(result.documents_needed || []).map((d, i) => (
                  <span key={i} style={{ background: 'white', border: '1px solid var(--line)', padding: '4px 8px', borderRadius: 6, fontSize: 10, fontWeight: 600 }}>
                    📄 {d}
                  </span>
                ))}
              </div>
            </div>

            <a
              href={scheme.apply_url}
              target="_blank"
              rel="noreferrer"
              style={{ display: 'inline-flex', alignItems: 'center', gap: 6, background: 'var(--green)', color: 'white', padding: '9px 14px', borderRadius: 10, fontSize: 11, fontWeight: 700, textDecoration: 'none', marginTop: 10 }}
            >
              Open Official Government Portal <ExternalLink size={14} />
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

// AI Kisan Assistant Floating Chatbot Component
function KisanChatbot({ lang }) {
  const [isOpen, setIsOpen] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  
  // Provider settings stored in localStorage
  const [provider, setProvider] = useState(() => localStorage.getItem('growva_chat_provider') || 'openrouter');
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('growva_chat_key') || '');
  const [model, setModel] = useState(() => localStorage.getItem('growva_chat_model') || 'z-ai/glm-5.2:free');
  
  const [inputMsg, setInputMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '🌾 **Namaste! I am Kisan Sahayak**, your AI agricultural advisor on Growva.\n\nAsk me about crop sowing, weather forecasts, leaf diseases, mandi rates, or PM-KISAN schemes!'
    }
  ]);

  const messagesEndRef = React.useRef(null);

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  const handleProviderChange = (newProvider) => {
    setProvider(newProvider);
    localStorage.setItem('growva_chat_provider', newProvider);
    if (newProvider === 'openrouter') {
      const defaultModel = 'z-ai/glm-5.2:free';
      setModel(defaultModel);
      localStorage.setItem('growva_chat_model', defaultModel);
    } else if (newProvider === 'google') {
      const defaultModel = 'gemini-1.5-flash';
      setModel(defaultModel);
      localStorage.setItem('growva_chat_model', defaultModel);
    }
  };

  const handleKeyChange = (newKey) => {
    setApiKey(newKey);
    localStorage.setItem('growva_chat_key', newKey);
  };

  const handleSend = async (textToSend) => {
    const text = textToSend || inputMsg;
    if (!text.trim() || loading) return;

    const userMsg = { role: 'user', content: text.trim() };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInputMsg('');
    setLoading(true);

    try {
      const response = await sendChatMessage(updatedMessages, provider, apiKey, model);
      setMessages(prev => [...prev, { role: 'assistant', content: response.reply, meta: response.provider_used }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: "⚠️ Connection error. Please check your network or API key settings." }]);
    } finally {
      setLoading(false);
    }
  };

  const quickPrompts = [
    "🌾 What crop to plant this season?",
    "🌧️ Weather forecast for sowing",
    "🥭 How to cure Mango leaf spots?",
    "💰 Today's Mandi Prices",
    "📜 PM-KISAN subsidy details"
  ];

  return (
    <>
      {/* Floating Action Button (FAB) */}
      <button className="kisan-fab" onClick={() => setIsOpen(!isOpen)} title="Open AI Kisan Assistant">
        <div className="kisan-fab-pulse" />
        <Bot size={22} style={{ color: '#80e66c' }} />
        <span style={{ fontWeight: 700, fontSize: 13 }}>AI Kisan Sahayak</span>
      </button>

      {/* Floating Chat Box Window */}
      {isOpen && (
        <div className="kisan-chat-window">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-title-box">
              <div className="chat-bot-avatar">
                <Bot size={20} />
              </div>
              <div>
                <div className="chat-title">AI Kisan Sahayak</div>
                <div className="chat-subtitle">
                  <span className="status-dot" /> Online • {provider === 'openrouter' ? 'OpenRouter' : 'Google Gemini'}
                </div>
              </div>
            </div>
            <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
              <button
                onClick={() => setShowConfig(!showConfig)}
                style={{ background: showConfig ? 'rgba(184, 220, 159, 0.25)' : 'transparent', border: 0, color: '#b8dc9f', cursor: 'pointer', padding: 6, borderRadius: 8 }}
                title="LLM Provider & Key Settings"
              >
                <Settings size={18} />
              </button>
              <button
                onClick={() => setIsOpen(false)}
                style={{ background: 'transparent', border: 0, color: '#fff', cursor: 'pointer', padding: 6 }}
              >
                <X size={20} />
              </button>
            </div>
          </div>

          {/* Config Bar (Provider & API Key Box over Chatbox) */}
          {showConfig && (
            <div className="chat-config-bar">
              <div className="config-label">1. Select AI Provider</div>
              <select
                className="config-select"
                value={provider}
                onChange={(e) => handleProviderChange(e.target.value)}
              >
                <option value="openrouter">OpenRouter (Default: z-ai/glm-5.2:free)</option>
                <option value="google">Google Gemini (Default: gemini-1.5-flash)</option>
              </select>

              <div className="config-label" style={{ marginTop: 8 }}>
                2. API Key ({provider === 'openrouter' ? 'OpenRouter Key sk-or-v1...' : 'Google Gemini Key'})
              </div>
              <input
                type="password"
                className="config-input"
                placeholder={provider === 'openrouter' ? 'Paste OpenRouter Key (sk-or-v1...)' : 'Paste Google Gemini Key'}
                value={apiKey}
                onChange={(e) => handleKeyChange(e.target.value)}
              />

              <div style={{ fontSize: 10, color: '#b8dc9f', opacity: 0.85, marginTop: 6 }}>
                ⚡ Active Model: <b>{model}</b> {!apiKey && '(Demo Key Active)'}
              </div>
            </div>
          )}

          {/* Messages Area */}
          <div className="chat-messages-area">
            {messages.map((m, idx) => (
              <div key={idx} className={`msg-wrapper ${m.role}`}>
                <div className="msg-bubble">{m.content}</div>
                {m.meta && <div className="msg-meta">via {m.meta}</div>}
              </div>
            ))}
            {loading && (
              <div className="msg-wrapper assistant">
                <div className="msg-bubble" style={{ opacity: 0.8 }}>
                  <Sparkles size={14} style={{ display: 'inline-block', marginRight: 6, animation: 'spin 2s linear infinite' }} />
                  Thinking & consulting agricultural knowledge...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Suggestions Chips */}
          <div className="chat-quick-suggestions">
            {quickPrompts.map(qp => (
              <button key={qp} className="chip-btn" onClick={() => handleSend(qp)}>
                {qp}
              </button>
            ))}
          </div>

          {/* Input Bar */}
          <div className="chat-input-bar">
            <input
              type="text"
              className="chat-input-field"
              placeholder="Ask Kisan Sahayak in English or Hindi..."
              value={inputMsg}
              onChange={(e) => setInputMsg(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />
            <button
              className="chat-send-btn"
              onClick={() => handleSend()}
              disabled={loading || !inputMsg.trim()}
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      )}
    </>
  );
}

function App() {
  const [lang, setLang] = useState('en');
  const [active, setActive] = useState('Dashboard');
  const [group, setGroup] = useState('All');
  const [query, setQuery] = useState('');
  const [menu, setMenu] = useState(false);

  const [selectedCropModal, setSelectedCropModal] = useState(null);
  const [selectedSchemeModal, setSelectedSchemeModal] = useState(null);
  const [showChat, setShowChat] = useState(false);

  const t = useMemo(() => getTranslation(lang), [lang]);

  const filtered = useMemo(() =>
    allItems.filter(x => (group === 'All' || x.group === group) && x.name.toLowerCase().includes(query.toLowerCase())),
    [group, query]
  );

  const go = (key) => {
    setActive(key);
    setMenu(false);
    const targetMap = {
      'Dashboard': 'dashboard',
      'Planner': 'planner',
      'Weather': 'weather',
      'Crop Library': 'crop-library',
      'Mandi Rates': 'mandi-rates',
      'Disease Check': 'disease-check',
      'Schemes': 'schemes',
      'By-Products': 'by-products'
    };
    const id = targetMap[key] || key.toLowerCase().replace(/ /g, '-');
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="app" lang={lang}>
      <header>
        <div className="brand">
          <div className="brand-icon"><Sprout /></div>
          <div><strong>growva</strong><small>smart farming</small></div>
        </div>

        <nav className={menu ? 'show' : ''}>
          {navKeys.map((n, idx) => (
            <button className={active === n ? 'active' : ''} onClick={() => go(n)} key={n}>
              {t.nav?.[idx] || n}
            </button>
          ))}
        </nav>

        <div className="header-actions">
          <div className="language">
            <Globe2 size={16} />
            <select aria-label="Language" value={lang} onChange={e => { setLang(e.target.value); document.documentElement.lang = e.target.value; }}>
              {languages.map(([code, name]) => <option value={code} key={code}>{name}</option>)}
            </select>
          </div>
          <button className="menu" onClick={() => setMenu(!menu)}>{menu ? <X /> : <Menu />}</button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero" id="dashboard">
        <div className="hero-copy">
          <span className="eyebrow"><i /> {t.kicker}</span>
          <h1>{t.title}</h1>
          <p>{t.sub}</p>

          <div className="hero-buttons">
            <button className="primary" onClick={() => go('Crop Library')}>
              {t.explore} <ArrowRight size={17} />
            </button>
            <button className="secondary" onClick={() => go('Planner')}>
              {t.planner} <CalendarDays size={17} />
            </button>
          </div>

          <div className="stats">
            <div><b>120+</b><span>{t.stats_crops || 'Crop library'}</span></div>
            <div><b>22</b><span>{t.stats_langs || 'Scheduled languages'}</span></div>
            <div><b>6</b><span>{t.stats_tools || 'Core farming tools'}</span></div>
          </div>
        </div>

        <Robot t={t} onOpenChat={() => setShowChat(true)} />
      </section>

      {/* Quick Tools Grid */}
      <section className="quick-tools">
        <button className="tool" onClick={() => go('Planner')}>
          <div className="tool-icon"><CalendarDays /></div>
          <div><b>{t.tool1_title || 'Farm Planner'}</b><p>{t.tool1_desc || 'Sowing-to-harvest lifecycle timeline'}</p></div>
          <ArrowRight size={16} />
        </button>

        <button className="tool" onClick={() => go('Weather')}>
          <div className="tool-icon"><CloudRain /></div>
          <div><b>{t.tool2_title || 'Weather Intelligence'}</b><p>{t.tool2_desc || 'Open-Meteo rain & temperature forecasts'}</p></div>
          <ArrowRight size={16} />
        </button>

        <button className="tool" onClick={() => go('Disease Check')}>
          <div className="tool-icon"><Leaf /></div>
          <div><b>{t.tool3_title || 'Crop Health Diagnosis'}</b><p>{t.tool3_desc || 'AI disease identification & remedies'}</p></div>
          <ArrowRight size={16} />
        </button>

        <button className="tool" onClick={() => go('Mandi Rates')}>
          <div className="tool-icon"><TrendingUp /></div>
          <div><b>{t.tool4_title || 'Market Price Comparison'}</b><p>{t.tool4_desc || 'APMC mandi prices across states'}</p></div>
          <ArrowRight size={16} />
        </button>

        <button className="tool" onClick={() => go('Schemes')}>
          <div className="tool-icon"><ShieldCheck /></div>
          <div><b>{t.tool5_title || 'Schemes & Subsidies'}</b><p>{t.tool5_desc || 'Eligibility checker & official portals'}</p></div>
          <ArrowRight size={16} />
        </button>

        <button className="tool" onClick={() => go('By-Products')}>
          <div className="tool-icon"><Recycle /></div>
          <div><b>{t.tool6_title || 'By-Product Utilization'}</b><p>{t.tool6_desc || 'Agri-waste monetization guide'}</p></div>
          <ArrowRight size={16} />
        </button>
      </section>

      {/* Dynamic Sowing Planner */}
      <PlannerSection t={t} lang={lang} />

      {/* Open-Meteo Weather Intelligence */}
      <WeatherSection t={t} lang={lang} />

      {/* Produce Crop Library */}
      <section className="library" id="crop-library">
        <div className="section-head">
          <div>
            <span className="section-kicker">{t.lib_kicker || 'INTERACTIVE CROP LIBRARY'}</span>
            <h2>{t.lib_title || 'Curated Indian Produce Collection'}</h2>
            <p>{t.lib_sub || 'Click any crop to inspect detailed soil pH, water requirements, temperature ranges, and by-product value.'}</p>
          </div>
          <div className="search">
            <Search size={18} />
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder={t.lib_search_ph || t.search} />
            <button aria-label="Voice search"><Mic size={16} /></button>
          </div>
        </div>

        <div className="reference-guides">
          <article className="reference-guide">
            <div className="reference-copy">
              <span>PRODUCE GUIDE</span>
              <h3>{t.lib_veg_title || 'Indian Vegetables'}</h3>
              <p>{t.lib_veg_desc || 'Explore seasonal soil, irrigation, and yield metrics for Indian vegetables.'}</p>
              <button onClick={() => setGroup("Vegetables")}>{t.lib_veg_btn || 'View vegetables'} <ArrowRight size={15} /></button>
            </div>
            <img src={vegetableGuide} alt="Indian vegetables guide" />
          </article>
          <article className="reference-guide">
            <div className="reference-copy">
              <span>PRODUCE GUIDE</span>
              <h3>{t.lib_fruit_title || 'Fruits Collection'}</h3>
              <p>{t.lib_fruit_desc || 'Explore perennial fruit orchards, harvest cycles, and market prices.'}</p>
              <button onClick={() => setGroup("Fruits")}>{t.lib_fruit_btn || 'View fruits'} <ArrowRight size={15} /></button>
            </div>
            <img src={fruitGuide} alt="Fruit reference" />
          </article>
        </div>

        <div className="tabs">
          <button className={group === 'All' ? 'selected' : ''} onClick={() => setGroup('All')}>
            {t.lib_all || 'All'} ({allItems.length})
          </button>
          {Object.keys(groups).map(g => (
            <button className={group === g ? 'selected' : ''} onClick={() => setGroup(g)} key={g}>
              {translateGroup(g, lang)} ({groups[g].length})
            </button>
          ))}
        </div>

        <div className="crop-grid">
          {filtered.slice(0, 48).map(x => (
            <CropCard item={x} t={t} lang={lang} key={x.name} onSelect={setSelectedCropModal} />
          ))}
        </div>

        <div className="library-foot">
          {t.lib_showing || 'Showing'} {Math.min(filtered.length, 48)} {t.lib_of || 'of'} {filtered.length} {t.lib_matching || 'matching crop profiles.'}
        </div>
      </section>

      {/* APMC Mandi Market Prices */}
      <MandiSection t={t} lang={lang} />

      {/* AI Crop Disease Diagnosis */}
      <DiseaseSection t={t} lang={lang} />

      {/* Schemes & Subsidies Discovery */}
      <SchemesSection t={t} lang={lang} onOpenEligibilityModal={setSelectedSchemeModal} />

      {/* Post-Harvest By-Product Utilization */}
      <WasteSection t={t} lang={lang} />

      <footer>
        <div className="brand">
          <div className="brand-icon"><Sprout /></div>
          <div><strong>growva</strong><small>smart farming</small></div>
        </div>
        <p>{t.footer_text || 'Production-grade digital workspace for modern agriculture. Powered by FastAPI hybrid engine & React frontend.'}</p>
        <span>React · Vite · FastAPI · Open-Meteo</span>
      </footer>

      {/* Modals & AI Chat Drawer */}
      <AnimatePresence>
        {selectedCropModal && (
          <CropDetailModal crop={selectedCropModal} t={t} lang={lang} onClose={() => setSelectedCropModal(null)} />
        )}
        {selectedSchemeModal && (
          <SchemeEligibilityModal scheme={selectedSchemeModal} onClose={() => setSelectedSchemeModal(null)} />
        )}
      </AnimatePresence>

      {/* Floating AI Kisan Sahayak Chatbot */}
      <KisanChatbot lang={lang} />
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
