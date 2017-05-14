#!/usr/bin/env python3

from datetime import datetime
from impala.catalog import models
from impala import db
from impala.api.v1 import bp
from flask_restful import Api, Resource, abort, reqparse
from flask import make_response, json, current_app, request, session
from passlib.hash import pbkdf2_sha256
import sqlalchemy
from uuid import uuid4


class ApiVersionInfo(Resource):
    # No auth required for this endpoint
    def get(self):
        return {'stable': False}


def all_fields(model):
    columns = [c.name for c in model.__table__.columns]
    return dict([(c, getattr(model, c)) for c in columns])


class LoginResource(Resource):
    def get(self):
        auth = request.authorization
        if auth:
            user = current_app.config['M2M_USERS'].get(auth.username, {})
            password_hash = user.get('password_hash', None)

            if password_hash is not None and \
                    pbkdf2_sha256.verify(auth.password, password_hash):
                session['username'] = auth.username
                session['access'] = user.get('access', [])
                return {'message': "Logged in"}, 200
            else:
                abort(401, message="Invalid username or password")
        else:
            return {'message': "Authentication required"}, 401, \
                    {'WWW-Authenticate': 'Basic realm="impala"'}


class LogoutResource(Resource):
    def post(self):
        session.pop('username', None)
        session.pop('access', [])
        return {'message': "Logged out"}, 200


class ImpalaResource(Resource):
    def get(self, model, id=None):
        if id:
            item = model.query.get(id)
            if not item:
                abort(404, success=False, message="Item not found")
            return all_fields(item)
        else:
            items = model.query.all()
            return [all_fields(item) for item in items]

    def put(self, model, added_by="Unknown"):
        post_parser = reqparse.RequestParser()

        for c in model.__table__.columns:
            name = c.name
            required = not c.nullable
            if name not in ['id', 'added_at', 'added_by']:
                if str(c.type) == 'INTEGER':
                    post_parser.add_argument(name, dest=name, type=int,
                                             required=required)
                else:
                    post_parser.add_argument(name, dest=name, required=required)
            else:
                post_parser.add_argument(name, dest=name, required=False)

        args = post_parser.parse_args()
        if not args['id']:
            args['id'] = uuid4().__str__()

        args['added_by'] = added_by
        args['added_at'] = datetime.now()

        del_list = []
        for k, v in args.items():
            if not v:
                del_list.append(k)
        for k in del_list:
            args.pop(k)

        item = model(**args)
        try:
            db.session.add(item)
            db.session.commit()
            return {'message': "Item added", 'id': args['id']}, 201

        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            abort(409, success=False, message="Item already exists or foreign key constraint not met")
        except sqlalchemy.exc.StatementError:
            db.session.rollback()
            abort(400, success=False, message="Invalid parameter syntax")
        except:
            db.session.rollback()
            abort(500, success=False, message="Something broke during the query")

    def patch(self, model, id):
        post_parser = reqparse.RequestParser()

        for c in model.__table__.columns:
            name = c.name
            if name not in ['id', 'added_at', 'added_by']:
                if str(c.type) == 'INTEGER':
                    post_parser.add_argument(name, dest=name, type=int,
                                             required=False)
                else:
                    post_parser.add_argument(name, dest=name, required=False)

        args = post_parser.parse_args()

        del_list = []
        for k, v in args.items():
            if not v:
                del_list.append(k)
        for k in del_list:
            args.pop(k)

        try:
            model.query.filter_by(id=id).update(args)
            db.session.commit()
            return {'message': "Item updated", 'id': id}, 200

        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            abort(409, success=False, message="Invalid change")
        except sqlalchemy.exc.StatementError:
            db.session.rollback()
            abort(400, success=False, message="Invalid parameter syntax")
        except:
            db.session.rollback()
            abort(500, success=False, message="Something broke during the query")


class LibrarianResource(ImpalaResource):
    """
    Any authenticated user may do a GET. Only users with the "librarian" role
    may perform PATCH or PUT operations.
    """
    def get(self, model, id=None):
        if 'username' in session:
            return super().get(model, id)
        else:
            abort(403, success=False, message="Unauthorized")

    def patch(self, model, id=None):
        if 'librarian' in session.get('access', []):
            return super().patch(model, id)
        else:
            abort(403, success=False, message="Unauthorized")

    def put(self, model):
        if 'librarian' in session.get('access', []):
            return super().put(model)
        else:
            abort(403, success=False, message="Unauthorized")


class UserResource(ImpalaResource):
    """
    Any authenticated user may do a GET. Users with the "librarian" role may
    perform arbitrary PATCH or PUT operations. All users may perform PUT
    operations. All users may perform PATCH operations on resources where the
    "added_by" field corresponds to their username.
    """
    def get(self, model, id=None):
        if 'username' in session:
            return super().get(model, id)
        else:
            abort(403, success=False, message="Unauthorized")

    def patch(self, model, id=None):
        data = super().get(model, id)
        if 'librarian' in session.get('access', []) or \
                data['added_by'] == session['username']:
            return super().patch(model, id)
        else:
            abort(403, success=False, message="Unauthorized")

    def put(self, model):
        if 'username' in session:
            return super().put(model, session['username'])
        else:
            abort(403, success=False, message="Unauthorized")


class Stack(LibrarianResource):
    def get(self, id):
        return super().get(models.Stack, id)

    def patch(self, id):
        return super().patch(models.Stack, id)


class StackList(LibrarianResource):
    def get(self):
        return super().get(models.Stack)

    def put(self):
        return super().put(models.Stack)


class Format(LibrarianResource):
    def get(self, id):
        return super().get(models.Format, id)

    def patch(self, id):
        return super().patch(models.Format, id)


class FormatList(LibrarianResource):
    def get(self):
        return super().get(models.Format)

    def put(self):
        return super().put(models.Format)


class HoldingGroup(LibrarianResource):
    def get(self, id):
        return super().get(models.HoldingGroup, id)

    def patch(self, id):
        return super().patch(models.HoldingGroup, id)


class HoldingGroupList(LibrarianResource):
    def get(self):
        return super().get(models.HoldingGroup)

    def put(self):
        return super().put(models.HoldingGroup)


class Holding(LibrarianResource):
    def get(self, id):
        return super().get(models.Holding, id)

    def patch(self, id):
        return super().patch(models.Holding, id)


class HoldingList(LibrarianResource):
    def get(self):
        return super().get(models.Holding)

    def put(self):
        return super().put(models.Holding)


class RotationRelease(LibrarianResource):
    def get(self, id):
        return super().get(models.RotationRelease, id)

    def patch(self, id):
        return super().patch(models.RotationRelease, id)


class RotationReleaseList(LibrarianResource):
    def get(self):
        return super().get(models.RotationRelease)

    def put(self):
        return super().put(models.RotationRelease)


class HoldingTag(UserResource):
    def get(self, id):
        return super().get(models.HoldingTag, id)

    def patch(self, id):
        return super().patch(models.HoldingTag, id)


class HoldingTagList(UserResource):
    def get(self):
        return super().get(models.HoldingTag)

    def put(self):
        return super().put(models.HoldingTag)


class HoldingComment(UserResource):
    def get(self, id):
        return super().get(models.HoldingComment, id)

    def patch(self, id):
        return super().patch(models.HoldingComment, id)


class HoldingCommentList(UserResource):
    def get(self):
        return super().get(models.HoldingComment)

    def put(self):
        return super().put(models.HoldingComment)


class Track(LibrarianResource):
    def get(self, id):
        return super().get(models.Track, id)

    def patch(self, id):
        return super().patch(models.Track, id)


class TrackList(LibrarianResource):
    def get(self):
        return super().get(models.Track)

    def put(self):
        return super().put(models.Track)


class TrackMetadata(LibrarianResource):
    def get(self, id):
        return super().get(models.TrackMetadata, id)

    def patch(self, id):
        return super().patch(models.Track, id)


class TrackMetadataList(LibrarianResource):
    def get(self):
        return super().get(models.TrackMetadata)

    def put(self):
        return super().put(models.TrackMetadata)


api = Api(bp)
api.add_resource(ApiVersionInfo, '/')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(Stack, '/stacks/<string:id>')
api.add_resource(StackList, '/stacks')
api.add_resource(Format, '/formats/<string:id>')
api.add_resource(FormatList, '/formats')
api.add_resource(HoldingGroup, '/holding_groups/<string:id>')
api.add_resource(HoldingGroupList, '/holding_groups')
api.add_resource(Holding, '/holdings/<string:id>')
api.add_resource(HoldingList, '/holdings')
api.add_resource(RotationRelease, '/rotation_releases/<string:id>')
api.add_resource(RotationReleaseList, '/rotation_releases')
api.add_resource(HoldingTag, '/holding_tags/<string:id>')
api.add_resource(HoldingTagList, '/holding_tags')
api.add_resource(HoldingComment, '/holding_comments/<string:id>')
api.add_resource(HoldingCommentList, '/holding_comments')
api.add_resource(Track, '/tracks/<string:id>')
api.add_resource(TrackList, '/tracks')
api.add_resource(TrackMetadata, '/track_metadata/<string:id>')
api.add_resource(TrackMetadataList, '/track_metadata')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
