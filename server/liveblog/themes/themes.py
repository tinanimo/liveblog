# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from superdesk.resource import Resource
from superdesk.services import BaseService


class ThemesResource(Resource):

    schema = {
        'name': {
            'type': 'string'
        },
        'version': {
            'type': 'string'
        },
        'angularModule': {
            'type': 'string'
        },
        'styles': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'scripts': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        }
    }
    datasource = {
        'source': 'themes',
        'default_sort': [('_updated', -1)]
    }
    ITEM_METHODS = ['GET', 'POST', 'DELETE']
    privileges = {'GET': 'global_preferences', 'POST': 'global_preferences',
                  'PATCH': 'global_preferences', 'DELETE': 'global_preferences'}


class ThemesService(BaseService):
    pass
