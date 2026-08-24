import React,{useMemo,useState,useEffect} from 'react';
import {createRoot} from 'react-dom/client';
import {motion,useMotionValue,useSpring,useTransform} from 'framer-motion';
import {ArrowRight,CalendarDays,CheckCircle2,CloudRain,Droplets,Globe2,Leaf,MapPin,Menu,Mic,Recycle,Search,ShieldCheck,Sprout,Sun,TrendingUp,Wind,X} from 'lucide-react';
import './styles.css';
import { fetchCropRecommendations } from './services/plannerApi';

import robot from './assets/robotic-farm.jpeg';
import vegetableGuide from './assets/indian-vegetables-guide.jpg';
import fruitGuide from './assets/fruit-guide.jpg';

const languages=[
['en','English'],['as','অসমীয়া'],['bn','বাংলা'],['brx','बड़ो'],['doi','डोगरी'],['gu','ગુજરાતી'],['hi','हिन्दी'],['kn','ಕನ್ನಡ'],['ks','कॉशुर'],['kok','कोंकणी'],['mai','मैथिली'],['ml','മലയാളം'],['mni','মৈতৈലोन্'],['mr','मराठी'],['ne','नेपाली'],['or','ଓଡ଼ିଆ'],['pa','ਪੰਜਾਬੀ'],['sa','संस्कृतम्'],['sat','ᱥᱟᱱᱛᱟᱲᱤ'],['sd','سنڌي'],['ta','தமிழ்'],['te','తెలుగు'],['ur','اُردُو']
];
const nav=['Dashboard','Planner','Weather','Crop Library','Schemes'];
const groups={
 Crops:['Wheat','Rice','Bajra','Maize','Barley','Jowar','Ragi','Oats','Sorghum','Quinoa','Buckwheat','Amaranth','Foxtail Millet','Little Millet','Kodo Millet','Barnyard Millet','Proso Millet','Sugarcane','Cotton','Jute','Tea','Coffee','Tobacco'],
 Pulses:['Chickpea','Pigeon Pea','Green Gram','Black Gram','Lentil','Field Pea','Cowpea','Horse Gram','Moth Bean','Soybean','Peanut','Rajma','Lima Bean'],
 Vegetables:['Tomato','Potato','Onion','Garlic','Carrot','Radish','Beetroot','Cabbage','Cauliflower','Broccoli','Spinach','Amaranth Leaves','Okra','Brinjal','Capsicum','Green Peas','Cucumber','Bottle Gourd','Bitter Gourd','Ridge Gourd','Pumpkin','Sweet Corn','French Bean','Drumstick','Turnip','Sweet Potato','Yam','Taro','Colocasia','Green Chilli','Lettuce','Celery','Mushroom','Zucchini','Cluster Bean','Ivy Gourd','Snake Gourd','Ash Gourd'],
 Fruits:['Mango','Banana','Apple','Orange','Guava','Papaya','Pomegranate','Grapes','Watermelon','Muskmelon','Pineapple','Litchi','Sapota','Jackfruit','Custard Apple','Strawberry','Strawberries','Kiwi','Peach','Plum','Pear','Fig','Dragon Fruit','Avocado','Coconut','Amla','Jamun','Karonda','Passion Fruit','Mosambi','Lemon','Chikoo','Apricot','Cherries','Blueberries','Melon','Lime','Raspberry','Dates','Blood Orange','Persimmon','Star Fruit','Cantaloupe'],
 Spices:['Turmeric','Ginger','Cumin','Coriander','Black Pepper','Cardamom','Clove','Cinnamon','Fenugreek','Mustard','Fennel','Ajwain','Chilli','Saffron','Nutmeg','Mace','Star Anise','Tamarind','Bay Leaf','Curry Leaf','Asafoetida','Poppy Seed','Sesame','Dill','Black Cumin']
};

// Stable, real-photo URLs. Wikimedia Commons is used for representative agricultural photos; cards can fall back to a real Unsplash farm photo.
const photo={
Wheat:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Wheat%20field.jpg',Rice:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Rice%20paddy%20field%20in%20India.jpg',Maize:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Maize%20field.jpg',Barley:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Barley%20field.jpg',Jowar:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sorghum%20field.jpg',Ragi:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Finger%20millet.jpg',Oats:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Oat%20field.jpg',Sugarcane:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sugarcane%20field.jpg',Cotton:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cotton%20plant.jpg',Tea:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Tea%20plantation.jpg',Coffee:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Coffee%20plantation.jpg',Tomato:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Tomatoes%20on%20plant.jpg',Potato:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Potatoes.jpg',Onion:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Onions.jpg',Garlic:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Garlic.jpg',Carrot:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Carrots.jpg',Cabbage:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cabbage.jpg',Cauliflower:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cauliflower.jpg',Broccoli:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Broccoli.jpg',Spinach:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Spinach.jpg',Okra:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Okra.jpg',Brinjal:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Solanum%20melongena%20fruit.jpg',Capsicum:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Capsicum%20annuum%20fruits%20IMGP0044.jpg',Cucumber:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cucumis%20sativus%20fruit.jpg',Pumpkin:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pumpkins.jpg',Mango:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Mangoes.jpg',Banana:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Banana.jpg',Apple:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Apples.jpg',Orange:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Orange.jpg',Guava:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Guava.jpg',Papaya:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Papaya.jpg',Pomegranate:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pomegranate%20fruit.jpg',Grapes:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Grapes.jpg',Watermelon:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Watermelon.jpg',Pineapple:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pineapple.jpg',Litchi:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Lychee.jpg',Strawberry:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Strawberries.jpg',DragonFruit:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pitaya%20fruit.jpg',Coconut:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Coconuts.jpg',Amla:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Phyllanthus%20emblica%20fruit.jpg',Turmeric:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Turmeric%20plant.jpg',Ginger:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Ginger%20plant.jpg',Cumin:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cumin%20seeds.jpg',Coriander:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Coriander%20seeds.jpg',BlackPepper:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Black%20Pepper%20(Piper%20nigrum)%20fruits.jpg',Cardamom:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cardamom.jpg',Clove:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cloves.jpg',Cinnamon:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cinnamon.jpg',Fenugreek:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Fenugreek%20seeds.jpg',Chilli:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Red%20Chili%20Pepper.jpg',Saffron:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Saffron%20croccus.jpg',
Sorghum:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Ohavi%20Sorghum.jpg',Quinoa:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Quinoa.jpg',Buckwheat:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Buckwheat%20Flour%20%284107890675%29.jpg',Amaranth:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Amaranthus%20cruentus002.jpg',FoxtailMillet:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Foxtail%20millet.jpg',LittleMillet:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Little%20Millet.jpg',KodoMillet:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Kodo%20Millet.jpg',BarnyardMillet:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Brniyard%20Millet.jpg',ProsoMillet:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Proso%20Millet.jpg',Jute:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Jute%20plant.jpg',Tobacco:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Tobacco%20leaves.jpg',
Chickpea:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Chickpeas.jpg',PigeonPea:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pigeon%20pea.jpg',GreenGram:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Green%20Mung%20Dal.jpg',BlackGram:'https://commons.wikimedia.org/wiki/Special:Redirect/file/White%20urand%20dal.jpg',Lentil:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Lentils.jpg',FieldPea:'https://commons.wikimedia.org/wiki/Special:Redirect/file/White%20peas.jpg',Cowpea:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cowpea.jpg',HorseGram:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Horse%20Gram.jpg',MothBean:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Moth%20bean.jpg',Soybean:'https://commons.wikimedia.org/wiki/Special:Redirect/file/White%20soya.jpg',Peanut:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Ground%20nut%201.jpg',Rajma:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Rajma%20Dal.jpg',LimaBean:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Lima%20Beans%201.jpg',
AmaranthLeaves:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Amaranth%20leaves.jpg',SweetCorn:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sweet%20corn.jpg',Turnip:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Turnips.jpg',SweetPotato:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sweet%20potatoes.jpg',Yam:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Yams.jpg',Lettuce:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Lettuce.jpg',Celery:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Celery.jpg',Mushroom:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Agaricus%20bisporus.jpg',Zucchini:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Zucchini.jpg',ClusterBean:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Cluster%20beans.jpg',IvyGourd:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Ivy%20gourd.jpg',SnakeGourd:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Snake%20gourd.jpg',AshGourd:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Ash%20gourd.jpg',Drumstick:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Drumsticks%20or%20Moringa.jpg',
Muskmelon:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Muskmelon.jpg',Sapota:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sapodilla%20fruits.jpg',Jackfruit:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Jackfruit.jpg',CustardApple:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Custard%20apple.jpg',Pear:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Pears.jpg',Jamun:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Jamun%20fruit.jpg',Karonda:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Karonda%20fruit.jpg',PassionFruit:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Passion%20fruit.jpg',Mosambi:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Mosambi%20fruit.jpg',Chikoo:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sapodilla%20whole%20and%20halved.jpg',
Mustard:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Mustard%20seeds.jpg',Fennel:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Fennel%20seeds.jpg',Ajwain:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Ajwain%20seeds.jpg',Nutmeg:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Nutmeg.jpg',Mace:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Mace%20%28spice%29.jpg',StarAnise:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Star%20anise.jpg',Tamarind:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Tamarind.jpg',BayLeaf:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Bay%20leaves.jpg',CurryLeaf:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Curry%20leaves.jpg',Asafoetida:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Asafoetida.jpg',PoppySeed:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Poppy%20seeds.jpg',Sesame:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sesame%20seeds.jpg',Dill:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Dill.jpg',BlackCumin:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Black%20cumin.jpg'
};
const userProvidedPhoto={
  Oats:'/crops/user-provided/oats.jpeg',
  Turnip:'/crops/user-provided/turnip.jpeg',
  SweetPotato:'/crops/user-provided/sweet-potato.jpeg',
  Yam:'/crops/user-provided/yam.jpeg',
  Taro:'/crops/user-provided/taro.jpeg',
  Colocasia:'/crops/user-provided/colocasia.jpeg',
  Lettuce:'/crops/user-provided/lettuce.jpeg',
  Celery:'/crops/user-provided/celery.jpeg',
  Mushroom:'/crops/user-provided/mushroom.jpeg',
  Zucchini:'/crops/user-provided/zucchini.jpeg',
  ClusterBean:'/crops/user-provided/cluster-bean.jpeg',
  IvyGourd:'/crops/user-provided/ivy-gourd.jpeg',
  SnakeGourd:'/crops/user-provided/snake-gourd.jpeg',
  AshGourd:'/crops/user-provided/ash-gourd.jpeg',
  Banana:'/crops/user-provided/banana.jpeg',
  Amla:'/crops/user-provided/amla.jpeg',
  Mosambi:'/crops/user-provided/mosambi.jpeg',
  Chikoo:'/crops/user-provided/chikoo.jpeg',
  Cumin:'/crops/user-provided/cumin.jpeg',
  Mustard:'/crops/user-provided/mustard.jpeg',
  Ajwain:'/crops/user-provided/ajwain.jpeg',
  Saffron:'/crops/user-provided/saffron.jpeg',
  Sesame:'/crops/user-provided/sesame.jpeg'
};
const localPhoto={
  Bajra:'/crops/Bajra.jpeg',
  Tomato:'/crops/tomato.jpg',Okra:'/crops/okra.jpg',Brinjal:'/crops/brinjal.jpg',Potato:'/crops/potato.jpg',
  Cauliflower:'/crops/cauliflower.jpg',Cabbage:'/crops/cabbage.jpg',Cucumber:'/crops/cucumber.jpg',Radish:'/crops/radish.jpg',
  Carrot:'/crops/carrot.jpg','French Bean':'/crops/french-bean.jpg','Green Peas':'/crops/green-peas.jpg',Capsicum:'/crops/capsicum.jpg',
  'Bitter Gourd':'/crops/bitter-gourd.jpg',Pumpkin:'/crops/pumpkin.jpg','Bottle Gourd':'/crops/bottle-gourd.jpg','Ridge Gourd':'/crops/ridge-gourd.jpg',
  Spinach:'/crops/spinach.jpg','Fenugreek Leaves':'/crops/fenugreek-leaves.jpg',Taro:'/crops/taro.jpg',
  Corn:'/crops/corn.jpg',Beetroot:'/crops/beetroot.jpg',Colocasia:'/crops/colocasia.jpg','Green Chilli':'/crops/green-chilli.jpg',
  Apple:'/crops/apple.jpg',Orange:'/crops/orange.jpg',Banana:'/crops/banana.jpg',Apricot:'/crops/apricot.jpg',Plum:'/crops/plum.jpg',
  Lemon:'/crops/lemon.jpg',Peach:'/crops/peach.jpg',Cherries:'/crops/cherries.jpg',Kiwi:'/crops/kiwi.jpg',Grapes:'/crops/grapes.jpg',
  Watermelon:'/crops/watermelon.jpg',Strawberries:'/crops/strawberries.jpg',Blueberries:'/crops/blueberries.jpg','Dragon Fruit':'/crops/dragon-fruit.jpg',Melon:'/crops/melon.jpg',
  Pomegranate:'/crops/pomegranate.jpg',Pineapple:'/crops/pineapple.jpg',Lime:'/crops/lime.jpg',Raspberry:'/crops/raspberry.jpg',Mango:'/crops/mango.jpg',
  Fig:'/crops/fig.jpg',Coconut:'/crops/coconut.jpg',Avocado:'/crops/avocado.jpg',Dates:'/crops/dates.jpg','Blood Orange':'/crops/blood-orange.jpg',
  Persimmon:'/crops/persimmon.jpg','Star Fruit':'/crops/star-fruit.jpg',Papaya:'/crops/papaya.jpg',Guava:'/crops/guava.jpg',Cantaloupe:'/crops/cantaloupe.jpg'
};

const genericPhoto={Crops:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Wheat%20field.jpg',Pulses:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Chickpeas.jpg',Vegetables:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Fruits%20and%20Vegetables%20(20170526-AMS-LSC-0439).jpg',Fruits:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Fruits%20and%20Vegetables%20(20170526-AMS-LSC-0439).jpg',Spices:'https://commons.wikimedia.org/wiki/Special:Redirect/file/Spice%20collection.jpg'};
const fallback='https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80';
const slug=s=>s.replace(/[^a-zA-Z0-9]/g,'');
const allItems=Object.entries(groups).flatMap(([group,names])=>names.map(name=>({name,group,image:userProvidedPhoto[slug(name)]||localPhoto[name]||photo[slug(name)]||genericPhoto[group],season:group==='Fruits'?'Regional / perennial':group==='Spices'?'Monsoon / winter varies':group==='Vegetables'?'Year-round / seasonal':'Kharif / Rabi varies',soil:group==='Vegetables'?'Fertile loam':'Well-drained loam',water:group==='Vegetables'?'Medium–High':'Medium',yield:'Regional estimate'})));

const T={
 en:{nav:['Dashboard','Planner','Weather','Crop Library','Schemes'],all:'All',kicker:'SMART AGRICULTURE PLATFORM',title:'Grow smarter. Harvest better.',sub:'A single digital workspace for farmers to plan crops, read weather, manage irrigation, find schemes, compare mandi prices and reduce post-harvest waste.',explore:'Explore crop library',planner:'Open planner',dashboard:'Farmer dashboard',weather:'Weather intelligence',library:'Crop library',schemes:'Schemes & subsidies',market:'Market price comparison',shelf:'Harvest & shelf-life',waste:'By-product utilization',photo:'Crop health from photo',search:'Search crops, vegetables, fruits and spices…',today:'Today’s recommendation',sow:'Based on rainfall forecast, consider sowing pearl millet after the next suitable rain window.',plannerTitle:'Know what to do next on the farm.',plannerText:'Plan every stage from sowing to harvest. Reminders can be connected to rainfall, crop age and irrigation needs.',weatherTitle:'Weather-aware farming decisions',libraryTitle:'Real produce library',libraryText:'Explore crops, vegetables, fruits, spices and pulses with season, soil, water and yield guidance.',schemesTitle:'Schemes & subsidy discovery',schemesText:'Design-ready cards for scheme eligibility, document checklist and official application links.',showing:'Showing',of:'of',matches:'matching profiles.',season:'Season',soil:'Soil',income:'Income support',insurance:'Crop insurance',solar:'Solar irrigation',soiltest:'Soil testing',eligibility:'Check eligibility',rain:'Rain window detected',rainText:'Good opportunity for sowing moisture-loving crops after rainfall.',mouse:'Move your mouse around the robot',assistant:'AI field assistant',location:'Ahmedabad, Gujarat',prepare:'Prepare soil',sowing:'Sowing window',irrigation:'First irrigation',harvest:'Expected harvest',week:'This week',regional:'Regional estimate'},
 hi:{nav:['डैशबोर्ड','प्लानर','मौसम','फसल लाइब्रेरी','योजनाएँ'],all:'सभी',kicker:'स्मार्ट कृषि प्लेटफ़ॉर्म',title:'स्मार्ट खेती करें। बेहतर उपज पाएँ।',sub:'फसल योजना, मौसम, सिंचाई, सरकारी योजनाएँ, मंडी भाव और कटाई के बाद की जानकारी एक ही प्लेटफ़ॉर्म पर।',explore:'फसल लाइब्रेरी देखें',planner:'प्लानर खोलें',dashboard:'किसान डैशबोर्ड',weather:'मौसम जानकारी',library:'फसल लाइब्रेरी',schemes:'योजनाएँ और सब्सिडी',market:'बाज़ार भाव तुलना',shelf:'कटाई और शेल्फ-लाइफ़',waste:'उप-उत्पाद उपयोग',photo:'फोटो से फसल स्वास्थ्य',search:'फसल, सब्ज़ी, फल और मसाले खोजें…',today:'आज की सलाह',sow:'बारिश के पूर्वानुमान के आधार पर अगली उपयुक्त बारिश के बाद बाजरा बोने पर विचार करें।',plannerTitle:'खेत में अगला काम जानें।',plannerText:'बुवाई से कटाई तक हर चरण की योजना बनाएँ।',weatherTitle:'मौसम के अनुसार खेती के निर्णय',libraryTitle:'वास्तविक कृषि उत्पाद लाइब्रेरी',libraryText:'फसल, सब्ज़ी, फल, मसाले और दालों की जानकारी देखें।',schemesTitle:'योजनाएँ और सब्सिडी खोजें',schemesText:'पात्रता और आवेदन की जानकारी देखें।',showing:'दिखाए जा रहे',of:'में से',matches:'मिलान प्रोफ़ाइल।',season:'मौसम',soil:'मिट्टी',income:'आय सहायता',insurance:'फसल बीमा',solar:'सौर सिंचाई',soiltest:'मृदा परीक्षण',eligibility:'पात्रता देखें',rain:'बारिश का अवसर',rainText:'बारिश के बाद नमी पसंद करने वाली फसल बोने का अच्छा समय।',mouse:'रोबोट के आसपास माउस घुमाएँ',assistant:'एआई खेत सहायक',location:'अहमदाबाद, गुजरात',prepare:'मिट्टी तैयार करें',sowing:'बुवाई का समय',irrigation:'पहली सिंचाई',harvest:'संभावित कटाई',week:'इस सप्ताह',regional:'क्षेत्रीय अनुमान'},
 gu:{nav:['ડેશબોર્ડ','પ્લાનર','હવામાન','પાક લાઇબ્રેરી','યોજનાઓ'],all:'બધા',kicker:'સ્માર્ટ કૃષિ પ્લેટફોર્મ',title:'સ્માર્ટ ખેતી. વધુ સારી ઉપજ.',sub:'પાક આયોજન, હવામાન, સિંચાઈ, સરકારી યોજનાઓ, બજાર ભાવ અને કાપણી પછીની માહિતી એક જ પ્લેટફોર્મમાં.',explore:'પાક લાઇબ્રેરી જુઓ',planner:'પ્લાનર ખોલો',dashboard:'ખેડૂત ડેશબોર્ડ',weather:'હવામાન માહિતી',library:'પાક લાઇબ્રેરી',schemes:'યોજનાઓ અને સબસિડી',market:'બજાર ભાવ સરખામણી',shelf:'કાપણી અને શેલ્ફ-લાઇફ',waste:'બાય-પ્રોડક્ટ ઉપયોગ',photo:'ફોટોથી પાક આરોગ્ય',search:'પાક, શાકભાજી, ફળ અને મસાલા શોધો…',today:'આજની સલાહ',sow:'વરસાદની આગાહી મુજબ આગામી યોગ્ય વરસાદ પછી બાજરી વાવવાનું વિચારો.',plannerTitle:'ખેતરમાં આગળ શું કરવું તે જાણો.',plannerText:'વાવણીથી કાપણી સુધી દરેક તબક્કાનું આયોજન કરો.',weatherTitle:'હવામાન આધારિત ખેતીના નિર્ણયો',libraryTitle:'વાસ્તવિક પાક લાઇબ્રેરી',libraryText:'પાક, શાકભાજી, ફળ, મસાલા અને કઠોળની માહિતી જુઓ.',schemesTitle:'યોજનાઓ અને સબસિડી શોધો',schemesText:'પાત્રતા અને અરજીની માહિતી જુઓ.',showing:'બતાવી રહ્યા છીએ',of:'માંથી',matches:'મેળ ખાતી પ્રોફાઇલ.',season:'મોસમ',soil:'માટી',income:'આવક સહાય',insurance:'પાક વીમો',solar:'સૌર સિંચાઈ',soiltest:'માટી પરીક્ષણ',eligibility:'પાત્રતા તપાસો',rain:'વરસાદની તક',rainText:'વરસાદ પછી ભેજવાળા પાક માટે સારો સમય.',mouse:'રોબોટની આસપાસ માઉસ ફેરવો',assistant:'AI ખેતર સહાયક',location:'અમદાવાદ, ગુજરાત',prepare:'માટી તૈયાર કરો',sowing:'વાવણી સમય',irrigation:'પ્રથમ સિંચાઈ',harvest:'અંદાજિત કાપણી',week:'આ અઠવાડિયે',regional:'પ્રાદેશિક અંદાજ'}
};
// For the remaining scheduled languages, core labels are localized while the detailed agricultural copy remains clear and can be extended without changing the app architecture.
const short={as:['ডেশব’ৰ্ড','প্লেনাৰ','বতৰ','শস্য লাইব্ৰেৰী','আঁচনি'],bn:['ড্যাশবোর্ড','পরিকল্পনা','আবহাওয়া','ফসল লাইব্রেরি','প্রকল্প'],brx:['डैसबोर्ड','प्लानार','हावायाव','फसल लाइब्रेरि','स्किम'],doi:['डैशबोर्ड','प्लैनर','मौसम','फसल लाइब्रेरी','योजनाएं'],kn:['ಡ್ಯಾಶ್‌ಬೋರ್ಡ್','ಪ್ಲಾನರ್','ಹವಾಮಾನ','ಬೆಳೆ ಗ್ರಂಥಾಲಯ','ಯೋಜನೆಗಳು'],ks:['ڈیش بورڈ','پلانر','موسم','فصل لائبریری','سکیم'],kok:['डॅशबोर्ड','प्लॅनर','हवामान','पीक लायब्ररी','योजना'],mai:['डैशबोर्ड','प्लानर','मौसम','फसल लाइब्रेरी','योजना'],ml:['ഡാഷ്ബോർഡ്','പ്ലാനർ','കാലാവസ്ഥ','വിള ലൈബ്രറി','പദ്ധതികൾ'],mni:['ꯗꯦꯁꯕꯣꯔꯗ','ꯄ꯭ꯂꯥꯅꯔ','ꯋꯥꯔꯤ','ꯀꯣꯄ ꯂꯥꯏꯕ꯭ꯔꯔꯤ','ꯁ꯭ꯀꯤꯝ'],mr:['डॅशबोर्ड','प्लॅनर','हवामान','पीक लायब्ररी','योजना'],ne:['ड्यासबोर्ड','योजना','मौसम','बाली पुस्तकालय','योजनाहरू'],or:['ଡ୍ୟାସବୋର୍ଡ','ଯୋଜନା','ପାଣିପାଗ','ଫସଲ ଲାଇବ୍ରେରୀ','ଯୋଜନା'],pa:['ਡੈਸ਼ਬੋਰਡ','ਪਲਾਨਰ','ਮੌਸਮ','ਫਸਲ ਲਾਇਬ੍ਰੇਰੀ','ਸਕੀਮਾਂ'],sa:['दर्शकफलकम्','योजनाकारः','वायुमानम्','सस्यग्रन्थालयः','योजनाः'],sat:['ᱰᱮᱥᱵᱚᱨᱰ','ᱯᱞᱟᱱᱟᱨ','ᱦᱟᱣᱟ','ᱠᱷᱮᱛ ᱞᱟᱭᱵᱨᱮᱨᱤ','ᱥᱠᱤᱢ'],sd:['ڊيش بورڊ','پلانر','موسم','فصل لائبريري','اسڪيمون'],ta:['டாஷ்போர்டு','திட்டமிடுபவர்','வானிலை','பயிர் நூலகம்','திட்டங்கள்'],te:['డ్యాష్‌బోర్డ్','ప్లానర్','వాతావరణం','పంట లైబ్రరీ','పథకాలు'],ur:['ڈیش بورڈ','پلانر','موسم','فصل لائبریری','اسکیمیں']};
for(const [code,navs] of Object.entries(short)){T[code]={...T.en,nav:navs};}

const groupNames={en:{Crops:'Crops',Pulses:'Pulses',Vegetables:'Vegetables',Fruits:'Fruits',Spices:'Spices'},hi:{Crops:'फसलें',Pulses:'दालें',Vegetables:'सब्ज़ियाँ',Fruits:'फल',Spices:'मसाले'},gu:{Crops:'પાક',Pulses:'કઠોળ',Vegetables:'શાકભાજી',Fruits:'ફળ',Spices:'મસાલા'}};
const cropNames={hi:{Wheat:'गेहूँ',Rice:'चावल',Maize:'मक्का',Bajra:'बाजरा',Jowar:'ज्वार',Ragi:'रागी',Sugarcane:'गन्ना',Cotton:'कपास',Tomato:'टमाटर',Potato:'आलू',Onion:'प्याज़',Garlic:'लहसुन',Carrot:'गाजर',Cabbage:'पत्तागोभी',Cauliflower:'फूलगोभी',Broccoli:'ब्रोकोली',Spinach:'पालक',Okra:'भिंडी',Brinjal:'बैंगन',Capsicum:'शिमला मिर्च',Cucumber:'खीरा',Pumpkin:'कद्दू',Mango:'आम',Banana:'केला',Apple:'सेब',Orange:'संतरा',Guava:'अमरूद',Papaya:'पपीता',Pomegranate:'अनार',Grapes:'अंगूर',Watermelon:'तरबूज',Pineapple:'अनानास',Litchi:'लीची',Strawberry:'स्ट्रॉबेरी',Coconut:'नारियल',Amla:'आंवला',Turmeric:'हल्दी',Ginger:'अदरक',Cumin:'जीरा',Coriander:'धनिया',BlackPepper:'काली मिर्च',Cardamom:'इलायची',Clove:'लौंग',Cinnamon:'दालचीनी',Fenugreek:'मेथी',Chilli:'मिर्च',Saffron:'केसर'}};
const cropLabel=(name,lang)=>cropNames[lang]?.[name]||name;
const groupLabel=(name,lang)=>groupNames[lang]?.[name]||name;

function Robot({t}){const mx=useMotionValue(0),my=useMotionValue(0),sx=useSpring(mx,{stiffness:150,damping:20}),sy=useSpring(my,{stiffness:150,damping:20});const ry=useTransform(sx,[-1,1],[-14,14]),rx=useTransform(sy,[-1,1],[10,-10]);return <div className="robot-wrap" onMouseMove={e=>{const r=e.currentTarget.getBoundingClientRect();mx.set((e.clientX-r.left)/r.width*2-1);my.set((e.clientY-r.top)/r.height*2-1)}} onMouseLeave={()=>{mx.set(0);my.set(0)}}><motion.div className="robot-3d" style={{rotateX:rx,rotateY:ry}}><div className="robot-aura"/><img src={robot} alt={t.assistant}/><div className="robot-badge"><span/>{t.assistant}</div></motion.div><p className="mouse-hint">{t.mouse}</p></div>}
function CropCard({item,t,lang}){const [src,setSrc]=useState(item.image);return <motion.div className="crop-card" whileHover={{y:-6}}><div className="crop-photo"><img src={src} onError={()=>setSrc(fallback)} alt={cropLabel(item.name,lang)}/><span>{groupLabel(item.group,lang)}</span></div><div className="crop-info"><h3>{cropLabel(item.name,lang)}</h3><div><b>{t.season}</b>{item.season}</div><div><b>{t.soil}</b>{item.soil}</div><div className="mini-meta"><span><Droplets size={14}/>{item.water}</span><span><TrendingUp size={14}/>{t.regional}</span></div></div></motion.div>}
function PlannerSection({ t, lang }) {
  const [locationInput, setLocationInput] = useState('Vadodara, Gujarat');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [plannerData, setPlannerData] = useState(null);
  const [selectedCropName, setSelectedCropName] = useState(null);

  useEffect(() => {
    handleAnalyze('Vadodara, Gujarat');
  }, []);

  const handleAnalyze = async (locToFetch) => {
    const loc = locToFetch || locationInput || 'Vadodara, Gujarat';
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCropRecommendations(loc);
      setPlannerData(data);
      if (data && data.top_recommendations && data.top_recommendations.length > 0) {
        setSelectedCropName(data.top_recommendations[0].crop_name);
      }
    } catch (err) {
      setError("We couldn't analyze this location right now.");
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
    if (index === 0) return 'This week';
    const today = new Date();
    const startDate = new Date(today);
    startDate.setDate(today.getDate() + (stage.start_day || index * 10));

    const endDate = new Date(today);
    endDate.setDate(today.getDate() + (stage.end_day || (index + 1) * 10));

    const options = { day: 'numeric', month: 'short' };
    const startStr = startDate.toLocaleDateString('en-US', options);
    const endStr = endDate.toLocaleDateString('en-US', options);

    if (stage.start_day === stage.end_day) return startStr;
    return `${startStr} – ${endStr}`;
  };

  return (
    <section className="feature" id="planner">
      <div className="feature-text">
        <span className="section-kicker">{t.planner}</span>
        <h2>{t.plannerTitle}</h2>
        <p>{t.plannerText}</p>

        <div className="planner-location-box">
          <div className="location-input-row">
            <input
              type="text"
              value={locationInput}
              onChange={(e) => setLocationInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAnalyze(locationInput)}
              placeholder="Search city / district / village (e.g. Vadodara)"
            />
            <button onClick={() => handleAnalyze(locationInput)} disabled={loading}>
              {loading ? 'Analyzing...' : 'Analyze farm'}
            </button>
          </div>
          <div className="location-chips">
            <span>Location:</span>
            {['Vadodara, Gujarat', 'Ahmedabad, Gujarat', 'Rajkot, Gujarat', 'Pune, Maharashtra', 'Ludhiana, Punjab'].map((loc) => (
              <button
                key={loc}
                className="location-chip"
                onClick={() => {
                  setLocationInput(loc);
                  handleAnalyze(loc);
                }}
              >
                {loc.split(',')[0]}
              </button>
            ))}
          </div>
        </div>

        {loading && (
          <div style={{ margin: '14px 0', color: 'var(--green)', fontSize: '12px', fontWeight: 600 }}>
            Analyzing local weather... Checking seasonal climate... Evaluating suitable crops...
          </div>
        )}

        {error && (
          <div style={{ margin: '12px 0', color: '#c0392b', fontSize: '12px' }}>
            {error}{' '}
            <button onClick={() => handleAnalyze(locationInput)} style={{ marginLeft: 6, textDecoration: 'underline' }}>
              Try again
            </button>
          </div>
        )}

        {plannerData && plannerData.top_recommendations && (
          <div className="crop-selector-box">
            <span className="crop-selector-label">Recommended for {plannerData.location.split(',')[0]}</span>
            <div className="crop-chips-row">
              {plannerData.top_recommendations.slice(0, 5).map((crop) => (
                <button
                  key={crop.crop_name}
                  className={`crop-chip-btn ${selectedCrop?.crop_name === crop.crop_name ? 'active' : ''}`}
                  onClick={() => setSelectedCropName(crop.crop_name)}
                >
                  <b>{crop.crop_name}</b>
                  <span>{crop.match_score}%</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {selectedCrop && (
          <div className="timeline">
            {selectedCrop.growth_stages.map((stage, idx) => (
              <Step
                key={stage.name}
                n={String(idx + 1).padStart(2, '0')}
                title={stage.name}
                date={formatStageDate(stage, idx)}
                done={idx === 0}
              />
            ))}
          </div>
        )}
      </div>

      <div className="planner-card">
        {selectedCrop ? (
          <>
            <div className="card-top">
              <b>{selectedCrop.crop_name.toUpperCase()}</b>
              <span>{selectedCrop.match_score}% suitability</span>
            </div>
            <div className="progress">
              <span style={{ width: `${selectedCrop.match_score}%` }} />
            </div>

            <div className="planner-grid">
              <div>
                <Sun />
                <b>{plannerData ? plannerData.temperature : 28}°C</b>
                <small>current temp</small>
              </div>
              <div>
                <CloudRain />
                <b>{plannerData ? plannerData.rain_probability : 64}%</b>
                <small>rain chance</small>
              </div>
              <div>
                <Droplets />
                <b>{plannerData ? plannerData.humidity : 68}%</b>
                <small>humidity</small>
              </div>
            </div>

            <div className="recommend">
              <CheckCircle2 />
              <div>
                <b>Today's recommendation</b>
                <p>{selectedCrop.suggested_sowing_window || plannerData?.sowing_advisory}</p>
              </div>
            </div>

            {selectedCrop.risk && selectedCrop.risk.warnings && (
              <div style={{ marginTop: 12, padding: '10px 12px', background: 'rgba(0,0,0,0.18)', borderRadius: 12, fontSize: 11, display: 'flex', gap: 8, alignItems: 'center' }}>
                <span className={`status-badge ${selectedCrop.sowing_status || 'GOOD'}`}>
                  SOWING: {selectedCrop.sowing_status || 'GOOD'}
                </span>
                <span style={{ opacity: 0.9, fontSize: 10 }}>
                  {selectedCrop.risk.warnings[0]}
                </span>
              </div>
            )}
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

function App(){const [lang,setLang]=useState('en'),[active,setActive]=useState('Dashboard'),[group,setGroup]=useState('All'),[query,setQuery]=useState(''),[menu,setMenu]=useState(false);const t=T[lang]||T.en;const navLabels=t.nav;const filtered=useMemo(()=>allItems.filter(x=>(group==='All'||x.group===group)&&x.name.toLowerCase().includes(query.toLowerCase())),[group,query]);const go=(key)=>{setActive(key);setMenu(false);document.getElementById(key.toLowerCase().replace(/ /g,'-'))?.scrollIntoView({behavior:'smooth'})};const navKeys=['Dashboard','Planner','Weather','Crop Library','Schemes'];const currentIndex=navKeys.indexOf(active);return <div className="app" lang={lang}>
<header><div className="brand"><div className="brand-icon"><Sprout/></div><div><strong>growva</strong><small>smart farming</small></div></div><nav className={menu?'show':''}>{navKeys.map((n,i)=><button className={active===n?'active':''} onClick={()=>go(n)} key={n}>{navLabels[i]}</button>)}</nav><div className="header-actions"><div className="language"><Globe2 size={16}/><select aria-label="Language" value={lang} onChange={e=>{setLang(e.target.value);document.documentElement.lang=e.target.value}}>{languages.map(([code,name])=><option value={code} key={code}>{name}</option>)}</select></div><button className="menu" onClick={()=>setMenu(!menu)}>{menu?<X/>:<Menu/>}</button></div></header>
<section className="hero" id="dashboard"><div className="hero-copy"><span className="eyebrow"><i/> {t.kicker}</span><h1>{t.title}</h1><p>{t.sub}</p><div className="hero-buttons"><button className="primary" onClick={()=>go('Crop Library')}>{t.explore}<ArrowRight size={17}/></button><button className="secondary" onClick={()=>go('Planner')}>{t.planner}<CalendarDays size={17}/></button></div><div className="stats"><div><b>120+</b><span>{t.library}</span></div><div><b>22</b><span>Indian scheduled languages</span></div><div><b>5</b><span>core farming tools</span></div></div></div><Robot t={t}/></section>
<section className="quick-tools"><Tool icon={<CalendarDays/>} title={t.planner} text={t.plannerText} onClick={()=>go('Planner')}/><Tool icon={<CloudRain/>} title={t.weather} text={t.weatherTitle} onClick={()=>go('Weather')}/><Tool icon={<Leaf/>} title={t.photo} text={t.libraryText}/><Tool icon={<TrendingUp/>} title={t.market} text={t.market}/><Tool icon={<ShieldCheck/>} title={t.schemes} text={t.schemesText} onClick={()=>go('Schemes')}/><Tool icon={<Recycle/>} title={t.waste} text={t.waste}/></section>
<PlannerSection t={t} lang={lang} />

<section className="weather" id="weather"><div className="section-head"><div><span className="section-kicker">{t.weather}</span><h2>{t.weatherTitle}</h2></div><span className="location"><MapPin size={15}/> {t.location}</span></div><div className="weather-grid"><div className="weather-main"><div><small>Today</small><strong>28°</strong><span>Partly cloudy</span></div><Sun size={64}/><div className="weather-row"><span><Droplets/>Humidity <b>68%</b></span><span><Wind/>Wind <b>14 km/h</b></span><span><CloudRain/>Rain <b>4.2 mm</b></span></div></div><div className="alert-card"><span className="alert-dot"/> <div><b>{t.rain}</b><p>{t.rainText}</p></div></div><div className="forecast"><div><b>Tue</b><CloudRain/><strong>27°</strong></div><div><b>Wed</b><Sun/><strong>29°</strong></div><div><b>Thu</b><CloudRain/><strong>26°</strong></div><div><b>Fri</b><Sun/><strong>30°</strong></div></div></div></section>
<section className="library" id="crop-library"><div className="section-head"><div><span className="section-kicker">{t.library}</span><h2>{t.libraryTitle}</h2><p>{t.libraryText}</p></div><div className="search"><Search size={18}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder={t.search}/><button aria-label="Voice search"><Mic size={16}/></button></div></div><div className="reference-guides"><article className="reference-guide"><div className="reference-copy"><span>YOUR REFERENCE</span><h3>Indian vegetables</h3><p>Real vegetable photos from the image you provided. Click the category to browse matching vegetable cards.</p><button onClick={()=>setGroup("Vegetables")}>View vegetables <ArrowRight size={15}/></button></div><img src={vegetableGuide} alt="Indian vegetables reference"/></article><article className="reference-guide"><div className="reference-copy"><span>YOUR REFERENCE</span><h3>Fruits collection</h3><p>Real fruit photos from your uploaded reference. The matching fruits are included in the library.</p><button onClick={()=>setGroup("Fruits")}>View fruits <ArrowRight size={15}/></button></div><img src={fruitGuide} alt="Fruit reference"/></article></div><div className="tabs"><button className={group==='All'?'selected':''} onClick={()=>setGroup('All')}>{t.all} ({allItems.length})</button>{Object.keys(groups).map(g=><button className={group===g?'selected':''} onClick={()=>setGroup(g)} key={g}>{groupLabel(g,lang)} ({groups[g].length})</button>)}</div><div className="crop-grid">{filtered.slice(0,48).map(x=><CropCard item={x} t={t} lang={lang} key={x.name}/>)}</div><div className="library-foot">{t.showing} {Math.min(filtered.length,48)} {t.of} {filtered.length} {t.matches}</div></section>
<section className="schemes" id="schemes"><div className="section-head"><div><span className="section-kicker">{t.schemes}</span><h2>{t.schemesTitle}</h2><p>{t.schemesText}</p></div></div><div className="scheme-grid"><Scheme title="PM-KISAN" tag={t.income} text={t.sow} t={t}/><Scheme title="PMFBY" tag={t.insurance} text={t.rainText} t={t}/><Scheme title="PM-KUSUM" tag={t.solar} text={t.plannerText} t={t}/><Scheme title="Soil Health Card" tag={t.soiltest} text={t.libraryText} t={t}/></div></section>
<footer><div className="brand"><div className="brand-icon"><Sprout/></div><div><strong>growva</strong><small>smart farming</small></div></div><p>{t.sub}</p><span>React · Vite · Framer Motion</span></footer>
</div>}
function Tool({icon,title,text,onClick}){return <button className="tool" onClick={onClick}><div className="tool-icon">{icon}</div><div><b>{title}</b><p>{text}</p></div><ArrowRight size={16}/></button>}
function Step({n,title,date,done}){return <div className="step"><span className={done?'done':''}>{done?<CheckCircle2 size={17}/>:n}</span><div><b>{title}</b><small>{date}</small></div></div>}
function Scheme({title,tag,text,t}){return <motion.article whileHover={{y:-4}} className="scheme-card"><div className="scheme-icon"><ShieldCheck/></div><span>{tag}</span><h3>{title}</h3><p>{text}</p><button>{t.eligibility} <ArrowRight size={15}/></button></motion.article>}
createRoot(document.getElementById('root')).render(<App/>);
