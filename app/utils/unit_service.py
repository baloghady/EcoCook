from typing import Optional

MASS_UNITS = {
    'g': 1.0,
    'kg': 1000.0,
}

VOLUME_UNITS = {
    'ml': 1.0,
    'l': 1000.0,
    'tbsp': 15.0,
    'tsp': 5.0,
}

COUNT_UNITS = {
    'piece': 1.0,
    'pieces': 1.0,
}

UNIT_CATEGORIES = {
    **{u: 'mass' for u in MASS_UNITS.keys()},
    **{u: 'volume' for u in VOLUME_UNITS.keys()},
    **{u: 'count' for u in COUNT_UNITS.keys()},
}


def normalize_unit_string(unit: Optional[str]) -> Optional[str]:
    if unit is None:
        return None
    return unit.strip().lower()


def convert_quantity(quantity: float, from_unit: str, to_unit: str) -> Optional[float]:
    """Convert between supported units. Returns None if incompatible categories."""
    from_unit = normalize_unit_string(from_unit)
    to_unit = normalize_unit_string(to_unit)
    if from_unit == to_unit:
        return quantity

    from_cat = UNIT_CATEGORIES.get(from_unit)
    to_cat = UNIT_CATEGORIES.get(to_unit)
    if not from_cat or not to_cat or from_cat != to_cat:
        return None

    if from_cat == 'mass':
        return quantity * (MASS_UNITS[from_unit] / MASS_UNITS[to_unit])
    if from_cat == 'volume':
        return quantity * (VOLUME_UNITS[from_unit] / VOLUME_UNITS[to_unit])
    if from_cat == 'count':
        return quantity * (COUNT_UNITS[from_unit] / COUNT_UNITS[to_unit])
    return None


def convert_recipe_to_ingredient_unit(recipe_qty: float, recipe_unit: str, ingredient_unit_value: str) -> Optional[float]:
    """Convert a recipe ingredient quantity (unit string) into the ingredient's canonical unit (enum .value)."""
    return convert_quantity(recipe_qty, recipe_unit, ingredient_unit_value)
