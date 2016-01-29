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
from gs.profile.base import ProfilePage
from .items import AuditItems


class AuditTrailView(ProfilePage):
    '''View the audit-trail for a user'''
    def __init__(self, context, request):
        super(AuditTrailView, self).__init__(context, request)

    @property
    def auditItems(self):
        '''Generator for the audit-event items'''
        items = AuditItems(self.context, self.siteInfo, self.userInfo)
        return items.auditItems
