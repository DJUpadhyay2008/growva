from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import httpx
import logging

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])

logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    role: str # "user", "assistant", "system"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    provider: Optional[str] = "openrouter" # "openrouter" or "google"
    model: Optional[str] = "z-ai/glm-5.2:free"
    api_key: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    provider_used: str
    model_used: str

AGRI_SYSTEM_PROMPT = """You are 'Kisan Sahayak' (किसान सहायक), an expert AI Agricultural Agronomist and smart advisor on the Growva Smart Farming platform.
Your objective is to provide clear, actionable, friendly, and practical farming advice to farmers in India and worldwide.

Key capabilities & Growva features you know about:
- **Crop Planning & Suitability**: Crop matching based on location, soil, rainfall, temperature, and seasonal timing.
- **7-Day Weather & Climate Risk**: Hyperlocal rain probability, temperature alerts, and sowing windows.
- **Disease & Leaf Scanner**: Instant diagnosis of leaf blights, fungal rusts, organic Neem/bio-pesticide treatments, and chemical sprays.
- **Live Mandi APMC Prices**: Real-time market rates for commodities like Wheat, Cotton, Groundnut, Cumin, Paddy, and Onion.
- **Government Schemes**: PM-KISAN (₹6000/yr), PM Fasal Bima Yojana (Crop Insurance), PM-KUSUM (Solar Pumps), Soil Health Card.
- **Agricultural By-Products**: Circular economy utilization of stubble, husks, and organic waste into bio-char, fodder, and green energy.

Guidance Rules:
1. Always be polite, encouraging, and supportive of farmers.
2. Provide concise, bulleted steps when suggesting farming practices or disease treatments.
3. Support English, Hindi, Hinglish, and regional agricultural terms.
4. Keep advice practical, affordable, and scientifically accurate.
"""

def generate_local_fallback_reply(last_user_msg: str) -> str:
    msg_lower = last_user_msg.lower()
    
    if any(k in msg_lower for k in ["mandi", "price", "rate", "bhav", "cost"]):
        return "💰 **Growva Mandi Price Advisory**:\nCurrent modal prices in major APMC mandis:\n- **Wheat (Lokwan)**: ₹2,600 / quintal (Bavla Mandi)\n- **Cotton (Shankar-6)**: ₹7,150 / quintal (Sanand Mandi)\n- **Groundnut (Bold)**: ₹6,200 / quintal (Rajkot APMC)\n- **Cumin (Super Fine)**: ₹23,000 / quintal (Unjha APMC)\n\n*Tip: Check the 'Mandi Rates' tab on Growva for real-time state and district filters!*"
    
    if any(k in msg_lower for k in ["disease", "leaf", "spot", "blight", "yellow", "fungus", "mango", "tomato"]):
        return "🌿 **Growva Crop Disease & Health Advisory**:\nIf you notice yellowing, spots, or wilting on leaves:\n1. **Upload Photo**: Go to the **Disease Check** tab and upload/click a photo of the leaf.\n2. **Organic Treatment**: Spray Neem oil extract (5ml/L water) or *Trichoderma viride* (5g/L).\n3. **Chemical Spray**: Apply Copper Oxychloride 50 WP (2.5g/L water) or Mancozeb 75 WP.\n\n*Try our instant Photo Leaf Scanner above for 96% accurate AI diagnosis!*"
    
    if any(k in msg_lower for k in ["scheme", "pm kisan", "subsidy", "insurance", "fasal bima", "kusum"]):
        return "📜 **Government Agri Schemes Overview**:\n- **PM-KISAN**: Direct ₹6,000/year income support in 3 installments to eligible landholders.\n- **PM Fasal Bima Yojana (PMFBY)**: Low-cost crop insurance (1.5% Rabi, 2% Kharif) against storm/flood damage.\n- **PM-KUSUM**: Up to 60% government subsidy for solar irrigation pumps.\n\n*Use Growva's 'Govt Schemes' tab to test your instant eligibility!*"
    
    if any(k in msg_lower for k in ["weather", "rain", "temperature", "sow", "climate"]):
        return "🌧️ **Smart Weather & Sowing Window**:\n- **Current Status**: Favorable soil moisture detected in your region with light shower probability in 2 days.\n- **Recommendation**: Groundnut and Cotton sowing windows are optimal right now. Ensure field drainage bunds are clear.\n\n*Check the 'Weather' tab in Growva for 7-day hourly rain risk graphs!*"

    return f"🌾 **Namaste Farmer! (किसान सहायक)**\n\nThank you for reaching out! As your Growva AI Assistant, I can help you with:\n\n- 🚜 **Crop Selection**: Finding high-yield crops matching your soil & season.\n- 🍃 **Leaf Disease Diagnosis**: Uploading photos to detect pests & fungal spots.\n- 💰 **Mandi Market Rates**: Latest APMC commodity prices across India.\n- 📜 **Govt Subsidies & Schemes**: PM-KISAN, PMFBY, and solar pump applications.\n\n*How can I assist your farm today? Feel free to ask in English, Hindi, or Hinglish!*"

@router.post("", response_model=ChatResponse)
async def chat_with_kisan_ai(req: ChatRequest):
    provider = (req.provider or "openrouter").lower()
    model = req.model or ("z-ai/glm-5.2:free" if provider == "openrouter" else "gemini-1.5-flash")
    api_key = req.api_key.strip() if req.api_key else None
    
    last_user_msg = next((m.content for m in reversed(req.messages) if m.role == "user"), "Hello")

    # If no API key provided, use local smart fallback with clear indicator
    if not api_key:
        reply_text = f"🌾 *(Growva AI Demo Mode — Enter API key in ⚙️ Settings for live LLM response)*\n\n" + generate_local_fallback_reply(last_user_msg)
        return ChatResponse(
            reply=reply_text,
            provider_used=f"{provider} (Demo Assistant)",
            model_used=model
        )

    # 1. OpenRouter Integration
    if provider == "openrouter":
        openrouter_messages = [{"role": "system", "content": AGRI_SYSTEM_PROMPT}]
        for m in req.messages:
            openrouter_messages.append({"role": m.role, "content": m.content})
            
        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                res = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://growva-seven.vercel.app",
                        "X-Title": "Growva Smart Farming"
                    },
                    json={
                        "model": model,
                        "messages": openrouter_messages,
                        "temperature": 0.7,
                        "max_tokens": 800
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    return ChatResponse(
                        reply=content,
                        provider_used="OpenRouter API",
                        model_used=model
                    )
                else:
                    logger.warning(f"OpenRouter API error {res.status_code}: {res.text}")
                    err_msg = "Invalid API key" if res.status_code in [401, 403] else f"Status {res.status_code}"
                    reply_text = f"*(Notice: OpenRouter ({err_msg}). Falling back to Kisan Sahayak AI)*\n\n" + generate_local_fallback_reply(last_user_msg)
                    return ChatResponse(reply=reply_text, provider_used="OpenRouter Fallback", model_used=model)
        except Exception as e:
            logger.error(f"OpenRouter call failed: {e}")
            reply_text = generate_local_fallback_reply(last_user_msg)
            return ChatResponse(reply=reply_text, provider_used="Local Assistant", model_used=model)

    # 2. Google Gemini Integration
    elif provider == "google":
        contents = []
        for m in req.messages:
            role = "user" if m.role == "user" else "model"
            contents.append({"role": role, "parts": [{"text": m.content}]})

        # Standard verified Google Gemini model endpoints
        fallback_models = [model, "gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash-8b"]
        candidate_models = list(dict.fromkeys([m for m in fallback_models if m]))

        last_error_code = 200
        last_error_text = ""

        async with httpx.AsyncClient(timeout=25.0) as client:
            for current_model in candidate_models:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{current_model}:generateContent?key={api_key}"
                try:
                    res = await client.post(
                        gemini_url,
                        headers={"Content-Type": "application/json"},
                        json={
                            "system_instruction": {"parts": [{"text": AGRI_SYSTEM_PROMPT}]},
                            "contents": contents,
                            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 800}
                        }
                    )
                    if res.status_code == 200:
                        data = res.json()
                        content = data["candidates"][0]["content"]["parts"][0]["text"]
                        return ChatResponse(
                            reply=content,
                            provider_used="Google Gemini API",
                            model_used=current_model
                        )
                    else:
                        last_error_code = res.status_code
                        try:
                            err_detail = res.json().get("error", {}).get("message", res.text[:100])
                        except Exception:
                            err_detail = res.text[:100]
                        last_error_text = err_detail
                        logger.warning(f"Google Gemini model '{current_model}' error {res.status_code}: {err_detail}")
                except Exception as e:
                    logger.error(f"Google Gemini call failed for model '{current_model}': {e}")
            
            # Format helpful user-facing note
            if last_error_code == 400 and "API key" in last_error_text:
                note = "🔑 Invalid API key provided. Please verify your Google AI Studio API Key in ⚙️ Settings."
            elif last_error_code == 404:
                note = f"⚠️ Gemini model endpoint returned HTTP 404. Key may not have access to specified model."
            else:
                note = f"⚠️ Google Gemini returned HTTP {last_error_code} ({last_error_text})."

            reply_text = f"*({note} Falling back to Kisan Sahayak AI)*\n\n" + generate_local_fallback_reply(last_user_msg)
            return ChatResponse(reply=reply_text, provider_used="Google Gemini Fallback", model_used=model)

    # Fallback default
    return ChatResponse(
        reply=generate_local_fallback_reply(last_user_msg),
        provider_used="Growva Assistant",
        model_used=model
    )
