# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""Embed module"""
import superdesk
from flask import render_template, request, current_app as app
from superdesk import get_resource_service
import tinys3
import io


ASSETS_DIR = 'embed_assets'
bp = superdesk.Blueprint('embed_liveblog', __name__, template_folder='templates', static_folder=ASSETS_DIR)


class AmazonAccessKeyUnknownException(Exception):
    pass


def is_relative_to_current_folder(url):
    return not (url.startswith('/') or url.startswith('http://') or url.startswith('https://'))


@bp.route('/embed/<blog_id>')
def embed(blog_id, api_host=None):
    api_host = api_host or request.url_root
    blog = get_resource_service('client_blogs').find_one(req=None, _id=blog_id)
    if not blog:
        return 'blog not found', 404
    theme_root = blog['theme']['name']
    # complete the urls from `scripts` and `styles` fields when it's relative
    for asset_type in ('scripts', 'styles'):
        blog['theme'][asset_type] = list(
            map(lambda url: '%s/%s' % (theme_root, url) if is_relative_to_current_folder(url) else url,
                blog['theme'].get(asset_type) or list())
        )
    scope = {
        'blog': blog,
        'api_host': api_host,
        'assets_root': '/%s/%s/' % (ASSETS_DIR, theme_root)
    }
    return render_template('embed.html', **scope)


def publish_embed(blog_id, api_host=None):
    html = embed(blog_id, api_host)
    if not app.config['AMAZON_ACCESS_KEY_ID']:
        raise AmazonAccessKeyUnknownException()
    s3 = tinys3.Connection(
        app.config['AMAZON_ACCESS_KEY_ID'],
        app.config['AWS_SECRET_ACCESS_KEY'],
        default_bucket=app.config['AMAZON_CONTAINER_NAME'])
    # Uploading a single file
    response = s3.upload('%s/index.html' % (blog_id), io.BytesIO(bytes(html, 'utf-8')))
    return response.url.replace('s3.amazonaws.com/%s' % (app.config['AMAZON_CONTAINER_NAME']),
                                '%s.s3.amazonaws.com' % (app.config['AMAZON_CONTAINER_NAME']))


@bp.app_template_filter('is_relative_to_current_folder')
def is_relative_to_current_folder_filter(s):
    return is_relative_to_current_folder(s)

# EOF
