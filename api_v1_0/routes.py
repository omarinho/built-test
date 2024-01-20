from flask import request, jsonify
from models import db, BlogPost, Category
from app import app


@app.route("/posts/", methods=["GET"])
def get_all_posts():
    try:
        posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
        if not posts:
            return jsonify({"message": "No posts found"}), 404
        serialized_posts = [
            {
                "id": post.id,
                "title": post.title,
                "contents": post.contents,
                "timestamp": post.timestamp.isoformat(),
                "categoryId": post.category_id,
            }
            for post in posts
        ]
        return jsonify(serialized_posts), 200
    except Exception as e:
        print(f"Error in get_all_posts: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    try:
        if not isinstance(id, int) or id <= 0:
            return jsonify({"error": "Invalid post ID"}), 400
        post = BlogPost.query.get(id)
        if not post:
            return jsonify({"message": "Post not found"}), 404
        serialized_post = {
            "id": post.id,
            "title": post.title,
            "contents": post.contents,
            "timestamp": post.timestamp.isoformat(),
            "categoryId": post.category_id,
        }
        return jsonify(serialized_post), 200
    except Exception as e:
        print(f"Error in get_post: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/categories/", methods=["GET"])
def get_categories():
    try:
        categories = Category.query.all()
        if not categories:
            return jsonify({"message": "No categories found"}), 404
        serialized_categories = [
            {"id": category.id, "name": category.name}
            for category in categories
        ]
        return jsonify(serialized_categories), 200
    except Exception as e:
        print(f"Error in get_categories: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/posts/", methods=["POST"])
def create_post():
    try:
        required_fields = ["title", "contents", "categoryId"]
        if not request.json or not all(
            field in request.json for field in required_fields
        ):
            return jsonify({"error": "Missing required fields"}), 400
        title = request.json["title"]
        contents = request.json["contents"]
        category_id = request.json["categoryId"]
        if not isinstance(category_id, int) or category_id <= 0:
            return jsonify({"error": "Invalid category ID"}), 400
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        new_post = BlogPost(
            title=title, contents=contents, category_id=category_id
        )
        db.session.add(new_post)
        db.session.commit()
        serialized_post = {
            "id": new_post.id,
            "title": new_post.title,
            "contents": new_post.contents,
            "timestamp": new_post.timestamp.isoformat(),
            "categoryId": new_post.category_id,
        }
        return jsonify(serialized_post), 201
    except Exception as e:
        print(f"Error in create_post: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.session.close()


@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    try:
        if not isinstance(id, int) or id <= 0:
            return jsonify({"error": "Invalid post ID"}), 400
        required_fields = ["title", "contents", "categoryId"]
        if not request.json or not all(
            field in request.json for field in required_fields
        ):
            return jsonify({"error": "Missing required fields"}), 400
        title = request.json["title"]
        contents = request.json["contents"]
        category_id = request.json["categoryId"]
        if not isinstance(category_id, int) or category_id <= 0:
            return jsonify({"error": "Invalid category ID"}), 400
        post = BlogPost.query.get(id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        post.title = title
        post.contents = contents
        post.category_id = category_id
        db.session.commit()
        serialized_post = {
            "id": post.id,
            "title": post.title,
            "contents": post.contents,
            "timestamp": post.timestamp.isoformat(),
            "categoryId": post.category_id,
        }
        return jsonify(serialized_post), 200
    except Exception as e:
        print(f"Error in update_post: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.session.close()


@app.route("/posts/", methods=["DELETE"])
def delete_all_posts():
    try:
        BlogPost.query.delete()
        db.session.commit()
        return jsonify({"message": "All posts deleted successfully"}), 200
    except Exception as e:
        print(f"Error in delete_all_posts: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.session.close()


@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    try:
        if not isinstance(id, int) or id <= 0:
            return jsonify({"error": "Invalid post ID"}), 400
        post = BlogPost.query.get(id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        db.session.delete(post)
        db.session.commit()
        return (
            jsonify({"message": f"Post with ID {id} deleted successfully"}),
            200,
        )
    except Exception as e:
        print(f"Error in delete_post: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.session.close()
