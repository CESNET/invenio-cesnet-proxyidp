# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Remote application for enabling sign in/up with OpenID Connect. """
from flask_login import current_user
from invenio_openid_connect import InvenioAuthOpenIdRemote

from invenio_cesnet_proxyidp.models import UserInfo
from werkzeug.exceptions import abort
from werkzeug.utils import redirect


class ProxyIDPAuthRemote(InvenioAuthOpenIdRemote):
    """ OArepo OpenID Connect Abstract Remote App """

    CONFIG_OPENID = 'PROXYIDP_CONFIG'
    CONFIG_OPENID_CREDENTIALS = 'PROXYIDP_CONFIG_CREDENTIALS'

    name = 'ProxyIDP'
    description = 'eduID Federated Login'
    icon = ''
    userinfo_cls = UserInfo

    def remote_app(self) -> dict:
        ra = super(ProxyIDPAuthRemote, self).remote_app()
        ra['signup_handler']['view'] = self.block_signups
        return ra

    def block_signups(self, remote, *args, **kwargs):
        """Handler rejecting all signups."""

        # User already authenticated so move on
        if current_user.is_authenticated:
            return redirect('/')
        else:
            abort(403)

