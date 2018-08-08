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
import unittest
import logging
import os


LOG = logging.getLogger(os.path.basename(__file__))


class BaseTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        # define global members
        self.adaptor = None
        # get configurations from environment
        self.env_adaptor = os.environ.get("TST_SOL005_ADAPTOR", "osm")
        self.env_api_url = os.environ.get("TST_SOL005_API_URL", "127.0.0.1")
        # initialize test adaptor
        self._init_adaptor()
        # logging
        LOG.info("Initialized '{}'".format(self.__class__.__name__))

    def _init_adaptor(self):
        if self.env_adaptor == "osm":
            from sol005tests.adaptor.osm import OsmAdaptor
            self.adaptor = OsmAdaptor(self.env_api_url)
            return
        LOG.error("TST_SOL005_ADAPTOR={} not implemented. Abort.")
        exit(1)

    def setUp(self):
        self.adaptor.setUp()

    def tearDown(self):
        self.adaptor.tearDown()
