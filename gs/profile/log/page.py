# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2009, 2010, 2012, 2016 OnlineGroups.net and Contributors.
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
from gs.profile.base import ProfilePage
from Products.GSAuditTrail import AuditQuery


class AuditTrailView(ProfilePage):
    '''View the audit-trail for a user'''
    def __init__(self, context, request):
        super(AuditTrailView, self).__init__(context, request)
        self.users = {}

    @Lazy
    def queries(self):
        retval = AuditQuery()
        return retval

    @property
    def auditItems(self):
        rawItems = self.queries.get_instance_user_events(self.userInfo.id)
        for item in rawItems:
            if ((item['site_id'] == self.siteInfo.id) or (not item['site_id'])):
                newItem = self.marshal_data(item)
                event = createObject(newItem['subsystem'], self.context, **newItem)
                yield event

    def marshal_data(self, data):
        assert type(data) == dict
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
        retval = self.users.get(uid, createObject('groupserver.UserFromId', self.context, uid))
        self.users[uid] = retval
        return retval

    def get_groupInfo(self, gid):
        retval = None
        if gid:
            retval = createObject('groupserver.GroupInfo', self.userInfo.user, gid)
        return retval
