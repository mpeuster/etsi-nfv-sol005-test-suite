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
import logging
import os


LOG = logging.getLogger(os.path.basename(__file__))


class BaseAdaptor(object):

    def __init__(self, env_conf):
        self.env_conf = env_conf
        LOG.info("Initializing '{}' pointing to '{}'"
                 .format(self.__class__.__name__,
                         self.env_conf.get("api_url")))

    def setUp(self):
        pass

    def tearDown(self):
        """
        Important: Every adaptor should clean the catalog
        of its MANO solution on tearDown.
        """
        pass
