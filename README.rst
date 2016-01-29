==================
``gs.profile.log``
==================
---------------------------
Profile log for GroupServer
---------------------------

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2016-01-29
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

GroupServer records events in the ``audit_event`` table
[#audit]_. This product provides the page ``log.html`` in the
*profile* context that provides a view of these events for a
person.

Resources
=========


- Translations:
  https://www.transifex.com/projects/p/gs-profile-log/
- Code repository: https://github.com/groupserver/gs.profile.log
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

.. [#audit] See
            <https://github.com/groupserver/Products.GSAuditTrail>
