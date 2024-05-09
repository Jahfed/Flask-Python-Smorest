from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel,StoreModel, ItemModel
from schemas import TagSchema,TagUpdateSchema, TagAndItemSchema

blp = Blueprint("Tags",__name__,description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self,tag_data,store_id):
        if TagModel.query.filter(TagModel.store_id==store_id,TagModel.name==tag_data["name"]).first():
            abort(400,message="Tag already exists...")

        tag = TagModel(**tag_data,store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema)
    def post(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Something went wrong in the form of an Error.")
        
        return tag
    
    @jwt_required()
    @blp.response(200,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Something went wrong in the form of an Error.")
        
        return {"message":"Item removed from Tag","item":item,"tag":tag}
    

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        return tag
    
    @jwt_required()
    @blp.response(202,description="Deletes a tag if not item is attached.",example="message")
    @blp.alt_response(404,description="Tag not founded.")
    @blp.alt_response(400,description="Returned if tag is assigned to one or more items. So no deletion.")
    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted"}
        abort(400,message="Could not delete tag, remove associated items first.")