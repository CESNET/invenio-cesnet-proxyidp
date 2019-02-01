# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

""" Models used by the ProxyIDP Remote application """

class UserInfo(object):
    sub: str = None
    name: str = None
    preferred_username: str = None
    given_name: str = None
    family_name: str = None
    zoneinfo: str = None
    locale: str = None
    email: str = None
    groupNames: list = []

    def __init__(self, userinfo: dict):
        for k, v in userinfo.items():
            setattr(self, k, v)

    @property
    def username(self):
        if self.preferred_username:
            return self.preferred_username
        elif self.email:
            return self.email

        return self.sub
