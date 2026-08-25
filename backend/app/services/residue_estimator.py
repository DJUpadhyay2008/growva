from typing import Dict, Tuple

AVERAGE_CROP_YIELDS_PER_ACRE: Dict[str, Tuple[float, str]] = {
    "rice": (2.5, "ICAR National Average Paddy Yield (2.5 tonnes / acre)"),
    "paddy": (2.5, "ICAR National Average Paddy Yield (2.5 tonnes / acre)"),
    "wheat": (2.2, "ICAR-IIWBR Average Wheat Yield (2.2 tonnes / acre)"),
    "sugarcane": (30.0, "Indian Sugar Mills Assoc Average Sugarcane Yield (30 tonnes / acre)"),
    "cotton": (1.2, "CIRCOT Average Seed Cotton Yield (1.2 tonnes / acre)"),
    "banana": (15.0, "ICAR-NRCB Average Banana Bunch Yield (15 tonnes / acre)"),
    "groundnut": (1.0, "ICAR-DGR Average Pod Yield (1.0 tonnes / acre)"),
    "mustard": (0.8, "DRMR Average Mustard Seed Yield (0.8 tonnes / acre)"),
    "tomato": (12.0, "IIHR Average Tomato Fruit Yield (12 tonnes / acre)"),
    "mango": (4.0, "ICAR-CISH Average Mango Fruit Yield (4.0 tonnes / acre)")
}

def estimate_crop_residue(
    crop_name: str,
    area_acres: float,
    user_expected_yield: float = None,
    residue_factor: float = 1.4,
    residue_factor_source: str = "ICAR Residue Dataset"
) -> Dict:
    c_lower = crop_name.lower().strip()
    
    if user_expected_yield and user_expected_yield > 0:
        prod_tonnes = float(user_expected_yield)
        yield_source = "User Provided Farm Yield Estimate"
    else:
        avg_yield, source_text = AVERAGE_CROP_YIELDS_PER_ACRE.get(c_lower, (2.0, "Agronomic Regional Baseline Estimate"))
        prod_tonnes = round(avg_yield * area_acres, 2)
        yield_source = f"{source_text} × {area_acres} Acres"

    est_residue = round(prod_tonnes * residue_factor, 2)

    return {
        "farm_area_acres": area_acres,
        "estimated_production_tonnes": prod_tonnes,
        "yield_source": yield_source,
        "residue_factor": residue_factor,
        "residue_factor_source": residue_factor_source,
        "estimated_residue_tonnes": est_residue
    }
