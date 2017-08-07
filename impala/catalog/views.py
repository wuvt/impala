import datetime
from pprint import pprint
from flask import render_template, make_response, redirect, url_for, request, session
from flask import copy_current_request_context
import requests
from sqlalchemy import or_
from impala import app
from impala.api.v1.views import HoldingSearchList
from impala.catalog.models import Holding, HoldingGroup, Format

RESULTS_PER_PAGE = 25

TOP_NAV = [('/holdings', 'Holdings'),
           ('/collages', 'Collages'),
           ('/requests', 'Requests'),
           ('/charts', 'Charts'),
           ('/help', 'Help')]

@app.route('/')
def index():
    return redirect(url_for('list_holdings'))


@app.route('/holdings', defaults={'page': 1})
@app.route('/holdings/page/<int:page>')
def list_holdings(page):
    # TODO sort by newest
    if 'username' in session:
        user = session['username']
    else:
        user = None

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
                           user=user, endpoint="list_holdings",
                           top_nav=TOP_NAV, curpage="Holdings")


@app.route('/search', defaults={'page': 1})
@app.route('/search/page/<int:page>')
def search(page):
    # TODO a lot of this is duplicated from the API and can be factored into a
    # helper function
    if 'username' in session:
        user = session['username']
    else:
        user = None
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
                           user=user, endpoint="search",
                           top_nav=TOP_NAV, curpage=None)


@app.route('/coverartarchive/<type>/<mbid>', defaults={'size': 0})
@app.route('/coverartarchive/<type>/<mbid>/<int:size>')
def mb_cover_art(type, mbid, size):
    # TODO cache this at the load balancer level
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
#        return redirect(url)
        r = requests.get(url)
        resp = make_response(r.content)
        resp.headers['Content-Type'] = r.headers['Content-Type']
        return resp
    except:
        return None
