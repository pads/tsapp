"""
Push assets to the target server.
"""

from __future__ import absolute_import

import glob
import urllib2

from .http import http_write


def push_assets(server, bag, auth_token, tiddler=None, hard=False):
    """
    Push *.html in the local dir and everything in assets
    to server, into the named bag, using the provided
    auth_token (if any). If hard is True, delete the assets first.
    """
    if tiddler:
        sources = glob.glob('assets/%s' % tiddler) + glob.glob(tiddler)
    else:
        sources = glob.glob('*.html') + glob.glob('assets/*')

    for path in sources:
        target_name = path
        if target_name.endswith('.html') or target_name.endswith('.tid'):
            target_name = target_name.rsplit('.', 1)[0]
        if '/' in target_name:
            target_name = target_name.split('/')[-1]
        target_path = '/bags/%s/tiddlers/%s' % (urllib2.quote(bag),
                urllib2.quote(target_name))

        uri = server + target_path

        if hard:
            http_write(method='DELETE', uri=uri, auth_token=auth_token,
                    filename=path)
        http_write(method='PUT', uri=uri, auth_token=auth_token,
                filename=path)
