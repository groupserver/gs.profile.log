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
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSAuditTrail import AuditQuery


class AuditItems(object):
    def __init__(self, context, siteInfo, userInfo):
        self.context = context
        self.siteInfo = siteInfo
        self.userInfo = userInfo
        self.users = {}
        self.groups = {}

    @Lazy
    def queries(self):
        retval = AuditQuery()
        return retval

    @property
    def auditItems(self):
        '''Generator for the audit-event items'''
        rawItems = self.queries.get_instance_user_events(self.userInfo.id, limit=255)
        for item in rawItems:
            if ((item['site_id'] == self.siteInfo.id) or (not item['site_id'])):
                newItem = self.marshal_data(item)
                event = createObject(newItem['subsystem'], self.context, **newItem)
                yield event

    def marshal_data(self, data):
        if (type(data) != dict):
            raise TypeError('Expected dict, got {}'.format(type(data)))
        retval = data
        retval.pop('instance_user_id')
        retval['instanceUserInfo'] = self.userInfo

        retval.pop('site_id')
        retval['siteInfo'] = self.siteInfo

        uid = retval.pop('user_id')
        retval['userInfo'] = self.get_userInfo(uid)

        gid = retval.pop('group_id')
        retval['groupInfo'] = self.get_groupInfo(gid)
        assert type(retval) == dict
        return retval

    def get_userInfo(self, uid):
        # Cache, as we deal with so many user-infos.
        if uid in self.users:
            retval = self.users[uid]
        else:
            retval = createObject('groupserver.UserFromId', self.context, uid)
            self.users[uid] = retval
        return retval

    def get_groupInfo(self, gid):
        retval = None
        if (gid and (gid in self.groups)):
            retval = self.groups[gid]
        elif gid:
            retval = createObject('groupserver.GroupInfo', self.context, gid)
            self.groups[gid] = retval
        return retval
