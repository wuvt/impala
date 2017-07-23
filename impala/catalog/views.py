import datetime
from flask import render_template, make_response, redirect, url_for, request
import requests
from sqlalchemy import or_
from impala import app
from impala.catalog.models import Holding, HoldingGroup, Format

RESULTS_PER_PAGE = 25


@app.route('/')
def index():
    return redirect(url_for('list_holdings'))


@app.route('/holdings', defaults={'page': 1})
@app.route('/holdings/page/<int:page>')
def list_holdings(page):
    # TODO sort by newest
    pagination = HoldingGroup.query.join(Holding).join(Format).filter(Holding.active == True).paginate(page, per_page=RESULTS_PER_PAGE)

    holding_groups = pagination.items

    for hg in holding_groups:
        print(str(hg))
        for h in hg.holdings:
            print(str(h))

    now = datetime.datetime.now()
    return render_template("catalog/holding_list.html",
                           now=now, pagination=pagination,
                           holding_groups=holding_groups,
                           endpoint="list_holdings")


@app.route('/search', defaults={'page': 1})
@app.route('/search/page/<int:page>')
def search(page):
    # TODO sort by newest
    query = HoldingGroup.query.join(Holding)
    if 'any' in request.args:
        ilike = "%{}%".format(request.args['any'])
        query = query.filter(or_(HoldingGroup.album_title.ilike(ilike),
                                 HoldingGroup.album_artist.ilike(ilike)))
    if 'album_artist' in request.args:
        ilike = "%{}%".format(request.args['album_artist'])
        query = query.filter(HoldingGroup.album_artist.ilike(ilike))
    if 'album_title' in request.args:
        ilike = "%{}%".format(request.args['album_title'])
        query = query.filter(HoldingGroup.album_title.ilike(ilike))

    pagination = query.paginate(page, per_page=RESULTS_PER_PAGE)
    holding_groups = pagination.items
    now = datetime.datetime.now()

    return render_template("catalog/holding_list.html",
                           now=now, pagination=pagination,
                           holding_groups=holding_groups,
                           endpoint="search")


@app.route('/coverartarchive/<type>/<mbid>', defaults={'size': 0})
@app.route('/coverartarchive/<type>/<mbid>/<int:size>')
def mb_cover_art(type, mbid, size):
    if type not in ['release-group', 'release']:
        return None
    try:
        r = requests.get('https://coverartarchive.org/{}/{}/'.format(type, mbid))
        dict = r.json()
        for i in dict['images']:
            if not i['front']:
                continue
            if size == 250:
                url = i['thumbnails']['small']
            elif size == 500:
                url = i['thumbnails']['large']
            else:
                url = i['image']
        r = requests.get(url)
        resp = make_response(r.content)
        resp.headers['Content-Type'] = r.headers['Content-Type']
        return resp
    except:
        return None
