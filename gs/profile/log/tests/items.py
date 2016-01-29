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
from __future__ import absolute_import, unicode_literals, print_function
from mock import MagicMock, patch
from unittest import TestCase
from gs.profile.log.items import AuditItems


class TestAuditItems(TestCase):
    'Checking the check_email function'

    def setUp(self):
        self.items = AuditItems(MagicMock(), MagicMock(), MagicMock)

    @patch('gs.profile.log.items.createObject')
    def test_get_userInfo_nocache(self, patched_createObject):
        'Test getting a user if he or she is absent from the cache'
        uid = 'example'
        r = self.items.get_userInfo(uid)

        self.assertEqual(r, self.items.users[uid])
        patched_createObject.assert_called_once_with(
            'groupserver.UserFromId', self.items.context, uid)

    @patch('gs.profile.log.items.createObject')
    def test_get_userInfo_cache(self, patched_createObject):
        'Test getting a user if he or she is present in the cache'
        uid = 'example'
        u = MagicMock()
        self.items.users[uid] = u
        r = self.items.get_userInfo(uid)

        self.assertEqual(r, u)
        self.assertEqual(0, patched_createObject.call_count)

    @patch('gs.profile.log.items.createObject')
    def test_get_groupInfo_nocache(self, patched_createObject):
        'Test getting a group if it is absent from the cache'
        gid = 'example_group'
        r = self.items.get_groupInfo(gid)

        self.assertEqual(r, self.items.groups[gid])
        patched_createObject.assert_called_once_with(
            'groupserver.GroupInfo', self.items.context, gid)

    @patch('gs.profile.log.items.createObject')
    def test_get_groupInfo_cache(self, patched_createObject):
        'Test getting a group if it is present in the cache'
        gid = 'example_group'
        g = MagicMock()
        self.items.groups[gid] = g
        r = self.items.get_groupInfo(gid)

        self.assertEqual(r, g)
        self.assertEqual(0, patched_createObject.call_count)

    @patch.object(AuditItems, 'get_userInfo')
    @patch.object(AuditItems, 'get_groupInfo')
    def test_marshall(self, g_gI, g_uI):
        'Test we marshall the data'
        d = {
            'user_id': 'anotherperson',
            'instance_user_id': 'person',
            'site_id': 'example_site',
            'group_id': 'example_group',
        }
        r = self.items.marshal_data(d)
        self.assertIn('userInfo', r)
        self.assertIn('instanceUserInfo', r)
        self.assertIn('siteInfo', r)
        self.assertIn('groupInfo', r)

        g_gI.assert_called_once_with('example_group')
        g_uI.assert_called_once_with('anotherperson')
