from models import Order, OrderProduct, Product, User, db
from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from sqlalchemy import func, extract, desc
from datetime import datetime, timedelta

analytics = Blueprint("analytics", __name__)
api = Api(analytics)


def success_response(data):
    return jsonify({"data": data})


def error_response(message, status_code=500):
    return jsonify({"message": message}), status_code


class TotalSales(Resource):
    def get(self):
        try:
            total_sales = db.session.query(func.sum(Order.total_price)).scalar() or 0
            return success_response({"total_sales": total_sales})
        except Exception as e:
            return error_response(f"Error retrieving total sales: {str(e)}")


class TotalOrders(Resource):
    def get(self):
        try:
            total_orders = db.session.query(func.count(Order.id)).scalar()
            return success_response({"total_orders": total_orders})
        except Exception as e:
            return error_response(f"Error retrieving total orders: {str(e)}")


class TotalCustomers(Resource):
    def get(self):
        try:
            total_customers = db.session.query(func.count(User.id)).scalar()
            return success_response({"total_customers": total_customers})
        except Exception as e:
            return error_response(f"Error retrieving total customers: {str(e)}")


class AverageOrderValue(Resource):
    def get(self):
        try:
            total_sales = db.session.query(func.sum(Order.total_price)).scalar() or 0
            total_orders = db.session.query(func.count(Order.id)).scalar() or 1
            avg_order_value = total_sales / total_orders
            return success_response({"avg_order_value": round(avg_order_value, 2)})
        except Exception as e:
            return error_response(f"Error calculating average order value: {str(e)}")


class MonthlySales(Resource):
    def get(self):
        try:
            monthly_sales = (
                db.session.query(
                    extract("month", Order.created_at).label("month"),
                    func.sum(Order.total_price).label("sales"),
                )
                .group_by("month")
                .order_by("month")
                .all()
            )
            data = [{"month": month, "sales": sales} for month, sales in monthly_sales]
            return success_response(data)
        except Exception as e:
            return error_response(f"Error retrieving monthly sales: {str(e)}")


class WeeklyVisitors(Resource):
    def get(self):
        try:
            start_date = datetime.now() - timedelta(days=7)
            weekly_visitors = (
                db.session.query(func.count(User.id))
                .filter(User.created_at >= start_date)
                .scalar()
            )
            return success_response({"weekly_visitors": weekly_visitors})
        except Exception as e:
            return error_response(f"Error retrieving weekly visitors: {str(e)}")


class TopSellingProducts(Resource):
    def get(self):
        try:
            top_products = (
                db.session.query(
                    Product.title, func.sum(OrderProduct.quantity).label("total_sold")
                )
                .join(OrderProduct, OrderProduct.product_id == Product.id)
                .group_by(Product.id)
                .order_by(desc("total_sold"))
                .limit(10)
                .all()
            )
            data = [
                {"title": title, "total_sold": total_sold}
                for title, total_sold in top_products
            ]
            return success_response(data)
        except Exception as e:
            return error_response(f"Error retrieving top-selling products: {str(e)}")


class SalesByCategory(Resource):
    def get(self):
        try:
            sales_by_category = (
                db.session.query(
                    Product.category_id,
                    func.sum(OrderProduct.quantity * Product.price).label(
                        "total_sales"
                    ),
                )
                .join(OrderProduct, OrderProduct.product_id == Product.id)
                .group_by(Product.category_id)
                .all()
            )
            data = [
                {"category_id": category_id, "total_sales": total_sales}
                for category_id, total_sales in sales_by_category
            ]
            return success_response(data)
        except Exception as e:
            return error_response(f"Error retrieving sales by category: {str(e)}")


class DailySales(Resource):
    def get(self):
        try:
            start_date = datetime.now() - timedelta(days=7)
            daily_sales = (
                db.session.query(
                    func.date(Order.created_at).label("date"),
                    func.sum(Order.total_price).label("sales"),
                )
                .filter(Order.created_at >= start_date)
                .group_by(func.date(Order.created_at))
                .order_by("date")
                .all()
            )
            data = [
                {"date": date.strftime("%Y-%m-%d"), "sales": sales}
                for date, sales in daily_sales
            ]
            return success_response(data)
        except Exception as e:
            return error_response(f"Error retrieving daily sales: {str(e)}")


class ProductInventory(Resource):
    def get(self):
        try:
            inventory = (
                db.session.query(Product.title, Product.quantity)
                .order_by(desc(Product.quantity))
                .all()
            )
            data = [
                {"title": title, "quantity": quantity} for title, quantity in inventory
            ]
            return success_response(data)
        except Exception as e:
            return error_response(f"Error retrieving product inventory: {str(e)}")


api.add_resource(TotalSales, "/total-sales")
api.add_resource(TotalOrders, "/total-orders")
api.add_resource(TotalCustomers, "/total-customers")
api.add_resource(AverageOrderValue, "/average-order-value")
api.add_resource(MonthlySales, "/monthly-sales")
api.add_resource(WeeklyVisitors, "/weekly-visitors")
api.add_resource(TopSellingProducts, "/top-selling-products")
api.add_resource(SalesByCategory, "/sales-by-category")
api.add_resource(DailySales, "/daily-sales")
api.add_resource(ProductInventory, "/product-inventory")
