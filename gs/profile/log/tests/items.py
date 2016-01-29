# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from mock import MagicMock, patch
from unittest import TestCase
from gs.profile.log.items import AuditItems


class TestAuditItems(TestCase):
    'Checking the check_email function'

    def setUp(self):
        self.items = AuditItems(MagicMock(), MagicMock(), MagicMock)

    @patch.object(AuditItems, 'get_userInfo')
    @patch.object(AuditItems, 'get_groupInfo')
    def test_marshall(self, g_gI, g_uI):
        'A simple email address'
        d = {
            'user_id': 'anotherperson',
            'instance_user_id': 'person',
            'site_id': 'example_site',
            'group_id': 'example_group',
        }
        r = self.items.marshal_data(d)
        self.assertTrue(r)
