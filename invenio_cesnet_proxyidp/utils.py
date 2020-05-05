# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""ProxyIDP Remote application utility functions."""
from invenio_oauthclient.utils import fill_form, create_csrf_disabled_registrationform, oauth_register, \
    create_registrationform


def register_account(account_info):
    """"Try to register a new OAuth account.

        :param :account_info account data
        :returns A :class:`invenio_accounts.models.User` of created user.
    """

    form = create_csrf_disabled_registrationform()
    form = fill_form(
        form,
        account_info['user']
    )
    if form.validate():
        # Register user
        return oauth_register(form)
