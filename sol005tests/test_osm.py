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
# This module implements OSM specific tests that are not part
# of the official ETSI SOL004.
#
import logging
import os
import pytest
from sol005tests import BaseTest


LOG = logging.getLogger(os.path.basename(__file__))


class Osm_BaiscTest(BaseTest):

    def test_connection(self):
        self.assertTrue(self.adaptor.check_connection())


class OsmVimManagementInterface(BaseTest):

    def test_vim_create(self):
        name, passed = self.adaptor.vim_create("test_vim_create")
        self.assertTrue(passed)

    def test_vim_list(self):
        # 0
        r = self.adaptor.vim_list()
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 0)
        # 1
        self.adaptor.vim_create("test_vim_list_1")
        r = self.adaptor.vim_list()
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 1)
        # 2
        self.adaptor.vim_create("test_vim_list_2")
        r = self.adaptor.vim_list()
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 2)

    def test_vim_show(self):
        name, _ = self.adaptor.vim_create("test_vim_show")
        r = self.adaptor.vim_show(name)
        self.assertIsNotNone(r)
        self.assertTrue(isinstance(r, dict))
        self.assertNotEqual(len(r), 0)

    def test_vim_delete(self):
        name, _ = self.adaptor.vim_create("test_vim_delete")
        r = self.adaptor.vim_delete(name)
        self.assertTrue(r)


class OsmVnfManagementInterface(BaseTest):

    @pytest.mark.nsdeploy
    def test_vnf_list(self):
        pass

    @pytest.mark.nsdeploy
    def test_vnf_show(self):
        pass
