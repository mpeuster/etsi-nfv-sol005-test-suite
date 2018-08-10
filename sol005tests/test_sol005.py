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
from sol005tests import fixtures


LOG = logging.getLogger(os.path.basename(__file__))


TST_PACKAGE_NSD = fixtures.get_file("pingpong_nsd.tar.gz")
TST_PACKAGE_VNF_PING = fixtures.get_file("ping.tar.gz")
TST_PACKAGE_VNF_PONG = fixtures.get_file("pong.tar.gz")


class Sol005_BaiscTest(BaseTest):

    def test_connection(self):
        self.assertTrue(self.adaptor.check_connection())


class Sol005_NsdManagementInterface(BaseTest):

    def test_nsd_create(self):
        LOG.debug(TST_PACKAGE_NSD)
        LOG.debug(TST_PACKAGE_VNF_PING)
        LOG.debug(TST_PACKAGE_VNF_PONG)


class Sol005_VnfPackageManagementInterface(BaseTest):
    pass


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
