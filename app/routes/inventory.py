from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
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
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        quantity = request.form.get('quantity', '').strip()
        unit = request.form.get('unit', '').strip()
        expiry_raw = request.form.get('expiry_date', '').strip()

        if not name or not quantity or not unit:
            flash('Name, quantity, and unit are required.', 'error')
            return redirect(url_for('inventory.add'))

        try:
            qty = float(quantity)
            if qty <= 0:
                raise ValueError
        except ValueError:
            flash('Quantity must be a positive number.', 'error')
            return redirect(url_for('inventory.add'))

        expiry_date = None
        if expiry_raw:
            try:
                # Expecting HTML date input format YYYY-MM-DD
                expiry_date = datetime.strptime(expiry_raw, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid expiry date format.', 'error')
                return redirect(url_for('inventory.add'))

        ingredient = find_or_create_ingredient(name=name, default_unit=unit)
        add_inventory_item(
            user_id=current_user.id,
            ingredient_id=ingredient.id,
            quantity=qty,
            unit=unit,
            expiry_date=expiry_date,
        )
        flash('Inventory item added.', 'success')
        return redirect(url_for('inventory.index'))

    return render_template('inventory/add.html')


@bp.route('/<int:item_id>/delete', methods=['POST'])
@login_required
def delete(item_id: int):
    if delete_inventory_item(current_user.id, item_id):
        flash('Item deleted from inventory.', 'success')
    else:
        flash('Item not found or not yours.', 'error')
    return redirect(url_for('inventory.index'))
