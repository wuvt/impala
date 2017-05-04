#!/usr/bin/env python3

from impala.catalog import models
from impala.api.v1 import bp
from flask_restful import Api, Resource, abort
from flask import make_response, json


class ApiVersionInfo(Resource):
    # No auth required for this endpoint
    def get(self):
        return {'stable': False}


class ImpalaResource(Resource):
    # TODO require auth
    pass


def all_fields(model):
    columns = [c.name for c in model.__table__.columns]
    return dict([(c, getattr(model, c)) for c in columns])


class Stack(ImpalaResource):
    def get(self, id):
        stack = models.Stack.query.get(id)
        if not stack:
            abort(404, success=False, message="Stack not found")
        return all_fields(stack)


class StackList(ImpalaResource):
    def get(self):
        stacks = models.Stack.query.all()
        return [all_fields(stack) for stack in stacks]


class Format(ImpalaResource):
    def get(self, id):
        format = models.Format.query.get(id)
        if not format:
            abort(404, success=False, message="Format not found")
        return all_fields(format)


class FormatList(ImpalaResource):
    def get(self):
        formats = models.Format.query.all()
        return [all_fields(format) for format in formats]


class HoldingGroup(ImpalaResource):
    def get(self, id):
        holding_group = models.HoldingGroup.query.get(id)
        if not holding_group:
            abort(404, success=False, message="HoldingGroup not found")
        return all_fields(holding_group)


class HoldingGroupList(ImpalaResource):
    def get(self):
        holding_groups = models.HoldingGroup.query.all()
        return [all_fields(holding_group) for holding_group in holding_groups]


class Holding(ImpalaResource):
    def get(self, id):
        holding = models.Holding.query.get(id)
        if not holding:
            abort(404, success=False, message="Holding not found")
        return all_fields(holding)


class HoldingList(ImpalaResource):
    def get(self):
        holdings = models.Holding.query.all()
        return [all_fields(holding) for holding in holdings]


class RotationRelease(ImpalaResource):
    def get(self, id):
        rotation_release = models.RotationRelease.query.get(id)
        if not rotation_release:
            abort(404, success=False, message="RotationRelease not found")
        return all_fields(rotation_release)


class RotationReleaseList(ImpalaResource):
    def get(self):
        rotation_releases = models.RotationRelease.query.all()
        return [all_fields(rotation_release) for rotation_release in rotation_releases]


class HoldingTag(ImpalaResource):
    def get(self, id):
        holding_tag = models.HoldingTag.query.get(id)
        if not holding_tag:
            abort(404, success=False, message="HoldingTag not found")
        return all_fields(holding_tag)


class HoldingTagList(ImpalaResource):
    def get(self):
        holding_tags = models.HoldingTag.query.all()
        return [all_fields(holding_tag) for holding_tag in holding_tags]


class HoldingComment(ImpalaResource):
    def get(self, id):
        holding_comment = models.HoldingComment.query.get(id)
        if not holding_comment:
            abort(404, success=False, message="HoldingComment not found")
        return all_fields(holding_comment)


class HoldingCommentList(ImpalaResource):
    def get(self):
        holding_comments = models.HoldingComment.query.all()
        return [all_fields(holding_comment) for holding_comment in holding_comments]


class Track(ImpalaResource):
    def get(self, id):
        track = models.Track.query.get(id)
        if not track:
            abort(404, success=False, message="Track not found")
        return all_fields(track)


class TrackList(ImpalaResource):
    def get(self):
        tracks = models.Track.query.all()
        return [all_fields(track) for track in tracks]


api = Api(bp)
api.add_resource(ApiVersionInfo, '/')
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


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
