# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Remote application for enabling sign in/up with OpenID Connect. """
from flask import session, url_for, current_app
from flask_login import current_user
from invenio_cesnet_proxyidp.utils import register_account
from invenio_db import db
from invenio_oauthclient import current_oauthclient
from invenio_oauthclient.errors import OAuthError
from invenio_oauthclient.handlers import oauth_error_handler, token_session_key, response_token_setter, token_getter, \
    get_session_next_url
from invenio_oauthclient.models import UserIdentity
from invenio_oauthclient.signals import account_info_received, account_setup_received, account_setup_committed
from invenio_oauthclient.utils import oauth_get_user, create_csrf_disabled_registrationform, fill_form, oauth_register, \
    oauth_authenticate, _get_external_id
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
        ra['authorized_handler'] = self.handle_authorized
        return ra

    def handle_authorized(self, resp, remote, *args, **kwargs):
        """Callback for handling user authorization."""
        return self.authorized_handler(resp, remote, *args, **kwargs)

    @oauth_error_handler
    def authorized_handler(self, resp, remote, *args, **kwargs):
        """Handle sign-in functionality.

        :param remote: The remote application.
        :param resp: The response.
        :returns: Redirect response.
        """
        # Remove any previously stored auto register session key
        session.pop(token_session_key(remote.name) + '_autoregister', None)

        # Store token in session
        # ----------------------
        # Set token in session - token object only returned if
        # current_user.is_autenticated().
        token = response_token_setter(remote, resp)
        handlers = current_oauthclient.signup_handlers[remote.name]

        # Sign-in user
        # ---------------
        if not current_user.is_authenticated:
            account_info = handlers['info'](resp)
            account_info_received.send(
                remote, token=token, response=resp, account_info=account_info
            )

            user = oauth_get_user(
                remote.consumer_key,
                account_info=account_info,
                access_token=token_getter(remote)[0],
            )

            # Make sure that external identity either matches
            # or is not yet created (gets created on first oidc login)
            extid = _get_external_id(account_info)
            user_identity: UserIdentity = UserIdentity.query.filter_by(
                id=extid['id'], method=extid['method']).first()
            if user_identity and user_identity.id != extid['id']:
                abort(401)

            if user is None:
                abort(403)

            # Authenticate user
            if not oauth_authenticate(remote.consumer_key, user,
                                      require_existing_link=False):
                return current_app.login_manager.unauthorized()

            # Link account
            # ------------
            # Need to store token in database instead of only the session when
            # called first time.
            token = response_token_setter(remote, resp)

        # Setup account
        # -------------
        if not token.remote_account.extra_data:
            account_setup = handlers['setup'](token, resp)
            account_setup_received.send(
                remote, token=token, response=resp, account_setup=account_setup
            )
            db.session.commit()
            account_setup_committed.send(remote, token=token)
        else:
            db.session.commit()

        # Redirect to next
        next_url = get_session_next_url(remote.name)
        if next_url:
            return redirect(next_url)
        return redirect(url_for('invenio_oauthclient_settings.index'))

    def block_signups(self, remote, *args, **kwargs):
        """Handler rejecting all signups."""

        # User already authenticated so move on
        if current_user.is_authenticated:
            return redirect('/')
        else:
            abort(403)

