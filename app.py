from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Contoh data produk makanan sehat
foods = [
    {"id": "1", "name": "Salad Buah", "description": "Salad segar dengan buah-buahan pilihan", "price": 30000, "reviews": []},
    {"id": "2", "name": "Smoothie Hijau", "description": "Smoothie dari sayuran hijau organik", "price": 25000, "reviews": []},
]

class FoodList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(foods),
            "foods": foods
        }

class FoodDetail(Resource):
    def get(self, food_id):
        food = next((f for f in foods if f["id"] == food_id), None)
        if food:
            return {
                "error": False,
                "message": "success",
                "food": food
            }
        return {"error": True, "message": "Food not found"}, 404

class FoodSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [f for f in foods if query in f['name'].lower() or query in f['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "foods": result
        }

class AddReview(Resource):
    def post(self):
        data = request.get_json()
        food_id = data.get('id')
        name = data.get('name')
        review_text = data.get('review')
        
        food = next((f for f in foods if f["id"] == food_id), None)
        if food:
            new_review = {
                "name": name,
                "review": review_text,
                "date": datetime.now().strftime("%d %B %Y")
            }
            food['reviews'].append(new_review)
            return {
                "error": False,
                "message": "success",
                "reviews": food['reviews']
            }
        return {"error": True, "message": "Food not found"}, 404

class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        food_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        food = next((f for f in foods if f["id"] == food_id), None)
        if food:
            review = next((r for r in food['reviews'] if r['name'] == name), None)
            if review:
                review['review'] = new_review_text
                review['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "success",
                    "reviews": food['reviews']
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Food not found"}, 404

class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        food_id = data.get('id')
        name = data.get('name')
        
        food = next((f for f in foods if f["id"] == food_id), None)
        if food:
            review = next((r for r in food['reviews'] if r['name'] == name), None)
            if review:
                food['reviews'].remove(review)
                return {
                    "error": False,
                    "message": "success",
                    "reviews": food['reviews']
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Food not found"}, 404

# Menambahkan resource ke API
api.add_resource(FoodList, '/foods')
api.add_resource(FoodDetail, '/foods/<string:food_id>')
api.add_resource(FoodSearch, '/foods/search')
api.add_resource(AddReview, '/review')
api.add_resource(UpdateReview, '/review/update')
api.add_resource(DeleteReview, '/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
