# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Perun ProxyIDP OpenIDC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""
from cesnet_perun_proxyidp.remote import PerunAuthRemote

OAUTHCLIENT_REMOTE_APPS = dict(
    eduid=PerunAuthRemote().remote_app()
)
