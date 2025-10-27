from datetime import date
from typing import List, Optional, Tuple

from flask_login import current_user
from app.extensions import db
from app.models import UserInventory, Ingredient


def get_user_inventory(user_id: int) -> List[UserInventory]:
    """Return all inventory items for the given user, ordered by expiry_date (soonest first)."""
    # Order by expiry date (soonest first), then by created_at; place NULL expiry at the end
    # Use a portable pattern for SQLite (which lacks NULLS LAST): order by (expiry_date IS NULL), then expiry_date
    return (
        UserInventory.query.filter_by(user_id=user_id)
        .order_by(UserInventory.expiry_date.is_(None), UserInventory.expiry_date.asc(), UserInventory.created_at.asc())
        .all()
    )


def get_expiring_items(user_id: int, days: int = 7) -> List[UserInventory]:
    """Return items expiring within the next N days."""
    today = date.today()
    cutoff = date.fromordinal(today.toordinal() + days)
    return (
        UserInventory.query.filter(
            UserInventory.user_id == user_id,
            UserInventory.expiry_date != None,  # noqa: E711
            UserInventory.expiry_date <= cutoff,
        )
        .order_by(UserInventory.expiry_date.asc())
        .all()
    )


def add_inventory_item(
    user_id: int,
    ingredient_id: int,
    quantity: float,
    unit: Optional[str] = None,
    expiry_date: Optional[date] = None,
) -> UserInventory:
    """Create a new inventory item for the user.

    Note: In later iterations we may merge with existing rows of the same ingredient.
    """
    item = UserInventory(
        user_id=user_id,
        ingredient_id=ingredient_id,
        quantity=quantity,
        unit=unit,
        expiry_date=expiry_date,
    )
    db.session.add(item)
    db.session.commit()
    return item


def delete_inventory_item(user_id: int, item_id: int) -> bool:
    """Delete a user's inventory item by id. Returns True if deleted."""
    item = UserInventory.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return False
    db.session.delete(item)
    db.session.commit()
    return True


def find_or_create_ingredient(name: str, default_unit: str) -> Ingredient:
    """Utility: case-insensitive ingredient lookup; create if not found.
    Requires a default_unit when creating a new ingredient, because Ingredient.unit is non-nullable.
    """
    ing = Ingredient.query.filter(Ingredient.name.ilike(name)).first()
    if ing:
        return ing
    ing = Ingredient(name=name.strip(), unit=default_unit)
    db.session.add(ing)
    db.session.commit()
    return ing
