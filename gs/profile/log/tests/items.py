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
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from zope.component import ComponentLookupError
from gs.profile.log.items import AuditItems


class TestAuditItems(TestCase):
    'Checking the check_email function'

    def setUp(self):
        self.items = AuditItems(MagicMock(), MagicMock(), MagicMock())

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

    @patch.object(AuditItems, 'queries', new_callable=PropertyMock)
    def test_auditItems_empty(self, m_queries):
        'Ensure we get no items if there are no items'
        m_queries().get_instance_user_events.return_value = []
        items = self.items.auditItems

        with self.assertRaises(StopIteration):
             items.next()

    @patch.object(AuditItems, 'queries', new_callable=PropertyMock)
    @patch.object(AuditItems, 'marshal_data')
    @patch('gs.profile.log.items.createObject')
    def test_auditItems(self, m_createObject, m_marshal_data, m_queries):
        'Ensure we get an items if there is an item'
        subsystem = 'ethel.the.frog'
        d = {'subsystem': subsystem, 'site_id': 'test'}
        m_queries().get_instance_user_events.return_value = [d, ]
        self.items.siteInfo.id = 'test'
        m_marshal_data.return_value = d
        m_createObject.return_value = 'Audit item'
        items = self.items.auditItems
        r = items.next()

        self.assertEqual('Audit item', r)  # Do we get an item returned
        m_createObject.assert_called_once_with(subsystem, self.items.context, subsystem=subsystem,
                                               site_id='test')

    @patch.object(AuditItems, 'queries', new_callable=PropertyMock)
    @patch.object(AuditItems, 'marshal_data')
    @patch('gs.profile.log.items.createObject')
    def test_auditItems_issue(self, m_createObject, m_marshal_data, m_queries):
        'Ensure we handle a lookup-error when generating the items'
        subsystem = 'ethel.the.frog'
        d = {'subsystem': subsystem, 'site_id': 'test'}
        m_queries().get_instance_user_events.return_value = [d, ]
        self.items.siteInfo.id = 'test'
        m_createObject.side_effect = ComponentLookupError
        items = self.items.auditItems

        with self.assertRaises(StopIteration):
             items.next()
        self.assertEqual(1, m_createObject.call_count)
