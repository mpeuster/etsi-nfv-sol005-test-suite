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
from sol005tests.adaptor import BaseAdaptor


LOG = logging.getLogger(os.path.basename(__file__))


OSM_MISSING = "Attention: 'osmclient' not installed on this system. \
The OsmAdaptor won't be able to work. \
Please install 'osmclient': https://osm.etsi.org/wikipub/index.php/OsmClient"


class OsmAdaptor(BaseAdaptor):
    """
    Adaptor uses osmclient to connect to OSM's NBI.
    """

    def __init__(self, *args, **kwargs):
        # initialize base adaptor
        super(OsmAdaptor, self).__init__(*args, **kwargs)
        # initialize OSM adaptor
        self.osmclient_cls = None
        if (not self._safe_import_osmclient()
                or self.osmclient_cls is None):
            exit(1)

    def _safe_import_osmclient(self):
        """
        We need the osmclient package on the system.
        """
        try:
            import osmclient
            LOG.debug("Found OSM client: {}".format(osmclient))
            from osmclient.sol005.client import Client as OsmSol005Client
            self.osmclient_cls = OsmSol005Client
            return True
        except BaseException as e:
            LOG.error(str(e))
            LOG.error(OSM_MISSING)
        return False

    def setUp(self):
        self.osm = self.osmclient_cls(self.env_conf.get("api_url"))

    def check_connection(self):
        # does a vnfd list to check connection
        return isinstance(self.osm.vnfd.list(), list)
