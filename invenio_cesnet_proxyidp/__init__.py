# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Perun ProxyIDP OpenIDC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""CESNET Perun ProxyIDP OpenIDC auth backend"""

from __future__ import absolute_import, print_function

from .ext import InvenioCesnetProxyIDP
from .version import __version__

__all__ = ('__version__', 'InvenioCesnetProxyIDP')
