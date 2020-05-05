# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""ProxyIDP Remote application CLI."""
import click
from flask.cli import with_appcontext
from invenio_accounts.models import User
from invenio_cesnet_proxyidp.utils import register_account
from invenio_db import db
from invenio_oauthclient.utils import oauth_get_user, oauth_link_external_id


@click.group()
def proxyidp():
    """ProxyIDP client CLI."""


@proxyidp.command()
@click.argument('external_id')
@click.argument('email')
@click.option('--username', help="Preferred account username")
@click.option('--dn', help="Account display name.")
@with_appcontext
def create_account(external_id, email, username=None, dn=''):
    """Create a user capable of logging in with ProxyIDP."""
    click.secho("Creating account for {}".format(external_id), fg="yellow")

    account_info = dict(
        user=dict(
            email=email,
            profile=dict(
                username=username or external_id.split('@')[0],
                displayname=dn,
                full_name=dn,
            )
        ),
        external_id=external_id,
        external_method='ProxyIDP'
    )

    user = oauth_get_user(
        client_id=None,
        account_info=account_info,
        access_token=None,
    )
    if user:
        click.secho("Account with this e-mail already exists", fg="red")
        return

    user: User = register_account(account_info)
    if user:
        db.session.commit()
        click.secho("Successfully created user {} (ID: {})".format(user.email, user.id), fg="green")
    else:
        click.secho("Failed to create user", fg="red")
