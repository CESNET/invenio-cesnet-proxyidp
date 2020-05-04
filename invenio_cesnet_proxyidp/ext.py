# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Perun ProxyIDP OpenIDC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for Perun ProxyIDP OpenIDC."""

from __future__ import absolute_import, print_function
from . import config


class InvenioCesnetProxyIDP(object):
    """ProxyIDP OpenIDC extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_config(self, app):
        """Extension configuration."""
        for k in dir(config):
            if k.startswith('INVENIO_CESNET_PROXYIDP_'):
                app.config.setdefault(k, getattr(config, k))

    def init_app(self, app):
        """Flask application initialization."""

