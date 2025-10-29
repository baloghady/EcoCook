from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import IngredientForm
from app.utils.inventory_service import (
    get_user_inventory,
    get_expiring_items,
    add_inventory_item,
    find_or_create_ingredient,
    delete_inventory_item,
)

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@bp.route('/')
@login_required
def index():
    q = request.args.get('q', '').strip().lower()
    items = get_user_inventory(current_user.id)
    if q:
        items = [i for i in items if q in i.ingredient.name.lower()]
    expiring = get_expiring_items(current_user.id, days=7)
    return render_template('inventory/index.html', items=items, expiring=expiring, q=q)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = IngredientForm()

    if form.validate_on_submit():
        ingredient = find_or_create_ingredient(
            name=form.name.data,
            default_unit=form.unit.data
        )
        add_inventory_item(
            user_id=current_user.id,
            ingredient_id=ingredient.id,
            quantity=float(form.quantity.data),
            unit=form.unit.data,
            expiry_date=form.expiry_date.data,
        )
        flash('Inventory item added successfully!', 'success')
        return redirect(url_for('inventory.index'))

    return render_template('inventory/add.html', form=form)


@bp.route('/<int:item_id>/delete', methods=['POST'])
@login_required
def delete(item_id: int):
    if delete_inventory_item(current_user.id, item_id):
        flash('Item deleted from inventory.', 'success')
    else:
        flash('Item not found or not yours.', 'error')
    return redirect(url_for('inventory.index'))
