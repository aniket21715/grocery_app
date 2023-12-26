from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from web.model import Product ,Purchase

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/purchase_history')
@login_required
def get_purchase_history():
    try:
        purchases = Purchase.query.filter_by(customer=current_user.id).all()
        purchase_history = []

        for purchase in purchases:
            product = Product.query.get(purchase.product)
            purchase_data = {
                'product_id': purchase.product,
                'product_name': product.name,
                'count': purchase.count,
                'purchase_date': purchase.date_added.strftime('%Y-%m-%d ')
            }
            purchase_history.append(purchase_data)

        return jsonify({'purchase_history': purchase_history}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
