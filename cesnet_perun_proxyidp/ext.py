# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Perun ProxyIDP OpenIDC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for Perun ProxyIDP OpenIDC."""

from __future__ import absolute_import, print_function

from . import config


class PerunProxyIDPOpenIDC(object):
    """Perun ProxyIDP OpenIDC extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['cesnet-perun-proxyidp'] = self

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
