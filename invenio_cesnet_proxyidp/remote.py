# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Remote application for enabling sign in/up with OpenID Connect. """

from invenio_openid_connect import InvenioAuthOpenIdRemote

from invenio_cesnet_proxyidp.models import UserInfo


class PerunAuthRemote(InvenioAuthOpenIdRemote):
    """ OArepo OpenID Connect Abstract Remote App """

    CONFIG_OPENID = 'PROXYIDP_CONFIG'
    CONFIG_OPENID_CREDENTIALS = 'PROXYIDP_CONFIG_CREDENTIALS'

    name = 'ProxyIDP'
    description = 'eduID Federated Login'
    icon = ''
    userinfo_cls = UserInfo
