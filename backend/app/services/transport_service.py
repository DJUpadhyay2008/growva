from typing import Dict, Any

TRANSPORT_CONFIG = {
    "base_cost_per_km": 12.0,           # Dispatch & fuel base rate per km
    "weight_rate_per_quintal_km": 1.50, # Weight scaling rate per quintal per km
    "minimum_transport_cost": 250.0     # Minimum vehicle loading fee
}

def estimate_transport_cost(distance_km: float, quantity_quintals: float = 1.0) -> Dict[str, float]:
    """
    Calculates estimated logistics/transportation cost from farm to market.
    
    Formula:
    Transport Cost = max(minimum_cost, (distance_km * base_rate) + (distance_km * quantity * weight_rate))
    
    This reflects real-world Indian agricultural transport dynamics where distance and load volume
    jointly determine actual transport expenses.
    """
    if distance_km <= 0:
        return {
            "total_transport_cost": 0.0,
            "transport_cost_per_quintal": 0.0
        }

    base_dist_cost = distance_km * TRANSPORT_CONFIG["base_cost_per_km"]
    weight_dist_cost = distance_km * quantity_quintals * TRANSPORT_CONFIG["weight_rate_per_quintal_km"]
    
    raw_cost = base_dist_cost + weight_dist_cost
    total_cost = max(TRANSPORT_CONFIG["minimum_transport_cost"], raw_cost)
    cost_per_quintal = total_cost / max(1.0, quantity_quintals)

    return {
        "total_transport_cost": round(total_cost, 2),
        "transport_cost_per_quintal": round(cost_per_quintal, 2)
    }
