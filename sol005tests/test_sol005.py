#  Copyright (c) 2018 Manuel Peuster, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).

#
# This module implements tests for the interfaces that are officially
# part of the ETSI SOL005 specification. Each high-level interface is
# encapsulated in its own BaseTest class.
#
import logging
import os
from sol005tests import BaseTest


LOG = logging.getLogger(os.path.basename(__file__))


class Sol005_BaiscTest(BaseTest):

    def test_connection(self):
        self.assertTrue(self.adaptor.check_connection())


class Sol005_NsdManagementInterface(BaseTest):

    def test_nsd_create(self):
        name, passed = self.adaptor.nsd_create()
        self.assertTrue(passed)

    def test_nsd_list(self):
        # 0
        r = self.adaptor.nsd_list()
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 0)
        # 1
        self.adaptor.nsd_create()
        r = self.adaptor.nsd_list()
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 1)

    def test_nsd_show(self):
        name, _ = self.adaptor.nsd_create()
        r = self.adaptor.nsd_show(name)
        self.assertIsNotNone(r)
        self.assertTrue(isinstance(r, dict))
        self.assertNotEqual(len(r), 0)

    def test_nsd_delete(self):
        name, _ = self.adaptor.nsd_create()
        r = self.adaptor.nsd_delete(name)
        self.assertTrue(r)


class Sol005_VnfPackageManagementInterface(BaseTest):

    def test_vnfd_create(self):
        name, passed = self.adaptor.vnfd_create()
        self.assertTrue(passed)
        return name

    def test_vnfd_list(self):
        # 0
        r = self.adaptor.vnfd_list()
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 0)
        # 1
        self.adaptor.vnfd_create()
        r = self.adaptor.vnfd_list()
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 1)
        # 2
        self.adaptor.vnfd_create(which="pong")
        r = self.adaptor.vnfd_list()
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 2)

    def test_vnfd_show(self):
        name, _ = self.adaptor.vnfd_create()
        r = self.adaptor.vnfd_show(name)
        self.assertIsNotNone(r)
        self.assertTrue(isinstance(r, dict))
        self.assertNotEqual(len(r), 0)

    def test_vnfd_delete(self):
        name, _ = self.adaptor.vnfd_create()
        r = self.adaptor.vnfd_delete(name)
        self.assertTrue(r)


class Sol005_NsLifecycleManagementInterface(BaseTest):
    pass


class Sol005_NsPerformanceManagementInterface(BaseTest):
    """
    Not yet implemented.
    """
    pass


class Sol005_NsFaultManagementInterface(BaseTest):
    """
    Not yet implemented.
    """
    pass
