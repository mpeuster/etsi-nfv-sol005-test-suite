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
import time
import subprocess
from sol005tests.adaptor import BaseAdaptor
from sol005tests import fixtures


LOG = logging.getLogger(os.path.basename(__file__))


OSM_MISSING = "Attention: 'osmclient' not installed on this system. \
The OsmAdaptor won't be able to work. \
Please install 'osmclient': https://osm.etsi.org/wikipub/index.php/OsmClient"


# fixtures: OSM test packages
TST_PACKAGE_NSD = fixtures.get_file("osm_pingpong_nsd.tar.gz")
TST_PACKAGE_VNF_PING = fixtures.get_file("osm_ping.tar.gz")
TST_PACKAGE_VNF_PONG = fixtures.get_file("osm_pong.tar.gz")

# global OSM-specific constants
OSM_PINGPONG_NSD_NAME = "pingpong"
OSM_PING_VNFD_NAME = "ping"
OSM_PONG_VNFD_NAME = "pong"


class OsmTimeoutException(BaseException):
    pass


class OsmDeploymentException(BaseException):
    pass


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

    def tearDown(self):
        """
        Clean up the catalog etc. after every test.
        """
        # delete all NSs
        for ns in self.osm.ns.list():
            self.ns_delete(ns.get("name"))
            self._wait_for_item_absent(self.osm.ns.list, ns.get("name"))
        # delete all NSDs
        for nsd in self.osm.nsd.list():
            self.nsd_delete(nsd.get("name"))
            self._wait_for_item_absent(self.osm.nsd.list, nsd.get("name"))
        # delete all VNFDs
        for vnfd in self.osm.vnfd.list():
            self.vnfd_delete(vnfd.get("name"))
            self._wait_for_item_absent(self.osm.vnfd.list, vnfd.get("name"))
        # delete all VIMs
        for vim in self.osm.vim.list():
            self.vim_delete(vim.get("name"))
            self._wait_for_item_absent(self.osm.vim.list, vim.get("name"))

    def check_connection(self):
        # does a vnfd list to check connection
        return isinstance(self.osm.vnfd.list(), list)

    def vim_create(self, name):
        """
        Example for vim_access dict:
        {'config': None,
         'vim-url': 'http://10.0.0.117:6001/v2.0',
         'description': 'no description',
         'vim-tenant-name': 'tenantName',
         'vim-type': 'openstack',
         'vim-password': 'password',
         'vim-username': 'username'}
        """
        vim_access = {"vim-type": self.env_conf.get("vim_type"),
                      "vim-url": self.env_conf.get("vim_url"),
                      "vim-tenant-name": self.env_conf.get("vim_tenant"),
                      "vim-username": self.env_conf.get("vim_user"),
                      "vim-password": self.env_conf.get("vim_password"),
                      "config": None,
                      "description": "etsi-sol005-test-suite-vim"}
        r = self.osm.vim.create(name, vim_access)
        self._wait_for_item(self.osm.vim.list, name)
        LOG.info("OSM created VIM: {} using {}".format(name, vim_access))
        return (name, r is None)

    def vim_list(self):
        return [vim.get("name") for vim in self.osm.vim.list()]

    def vim_show(self, name):
        r = self.osm.vim.get(name)
        return r

    def vim_delete(self, name):
        LOG.info("OSM deleting VIM '{}'".format(name))
        r = self.osm.vim.delete(name)
        return r is None

    def nsd_create(self):
        # osm requires to first create the constituent VNFs
        name = OSM_PINGPONG_NSD_NAME
        self.vnfd_create()
        self.vnfd_create(name="pong")
        r = self.osm.nsd.create(
            filename=TST_PACKAGE_NSD, overwrite=True)
        self._wait_for_item(self.osm.nsd.list, name)
        LOG.info("OSM created NSD: {}".format(name))
        return (name, r is None)

    def nsd_list(self):
        return [nsd.get("name") for nsd in self.osm.nsd.list()]

    def nsd_show(self, name):
        r = self.osm.nsd.get(name)
        return r

    def nsd_delete(self, name):
        LOG.info("OSM deleting NSD '{}'".format(name))
        r = self.osm.nsd.delete(name)
        return r is None

    def vnfd_create(self, name="ping"):
        if name == "ping":
            r = self.osm.vnfd.create(
                   filename=TST_PACKAGE_VNF_PING, overwrite=True)
        else:
            r = self.osm.vnfd.create(
                    filename=TST_PACKAGE_VNF_PONG, overwrite=True)
        self._wait_for_item(self.osm.vnfd.list, name)
        LOG.info("OSM created VNFD: {}".format(name))
        return (name, r is None)

    def vnfd_list(self):
        return [vnfd.get("name") for vnfd in self.osm.vnfd.list()]

    def vnfd_show(self, name):
        r = self.osm.vnfd.get(name)
        return r

    def vnfd_delete(self, name):
        LOG.info("OSM deleting VNFD '{}'".format(name))
        r = self.osm.vnfd.delete(name)
        return r is None

    def _ns_create(self, name, nsd, vim):
        """
        Workaround, because the method:
        self.osm.ns.create(OSM_PINGPONG_NSD_NAME, name, vim)
        does not seem to work.
        """
        cmd = ("osm ns-create --ns_name {} --nsd_name {} --vim_account {}"
               .format(name, nsd, vim))
        LOG.debug("executing: {}".format(cmd))
        subprocess.check_call(cmd, shell=True)

    def ns_create(self, name):
        LOG.info("OSM creating NS: {}".format(name))
        # 1. create a vim
        vim, _ = self.vim_create("testvim")
        # 2. on-board VNFDs and NSD
        nsd, _ = self.nsd_create()
        # 4. instantiate the service
        self._ns_create(name, nsd, vim)
        # 5. wait for instantiation  # TODO status
        self._wait_for_item(self.osm.ns.list, name, status="running")
        # 6. return result
        return (name, True)

    def ns_list(self):
        return [ns.get("name") for ns in self.osm.ns.list()]

    def ns_show(self, name):
        pass

    def ns_delete(self, name):
        LOG.info("OSM deleting NS instance '{}'".format(name))
        r = self.osm.ns.delete(name)
        return r is None

    def vnf_list(self):
        pass

    def vnf_show(self, name):
        pass

    def _wait_for_item(self, func_list, item_name,
                       status=None, status_field="operational-status",
                       timeout=30, wait=0.5, negate=False):
        """
        Sync. helper method that polls func_list(),e.g., vim-list on the OSM
        API until item_name is found or timeout (s) is reached.
        """
        start = time.time()
        while(time.time() - start < timeout):
            LOG.debug("Waiting for item: {} since {:4.2f}s"
                      .format(item_name, time.time() - start))
            if negate:
                # check if item is gone
                if item_name not in [it.get("name")
                                     for it in func_list()]:
                    return item_name
            else:
                for it in func_list():
                    if "name" in it:
                        if item_name in it.get("name"):
                            # found: stop and return
                            LOG.debug("Found item: {}".format(it.get("name")))
                            if status is not None:
                                LOG.debug("Field '{}' is '{}' should '{}'"
                                          .format(status_field,
                                                  it.get(status_field),
                                                  status))
                                # also check status
                                if status in it.get(status_field):
                                    return it.get("name")
                                if "fail" in it.get(status_field):
                                    raise OsmDeploymentException(
                                        "{} failed".format(item_name))
                            else:
                                return it.get("name")
            time.sleep(wait)
        raise OsmTimeoutException("Item '{}' was not found in time"
                                  .format(item_name))

    def _wait_for_item_absent(self, func_list, item_name,
                              status=None, status_field="operational-status",
                              timeout=30, wait=0.5):
        self._wait_for_item(func_list, item_name,
                            status, status_field,
                            timeout, wait, negate=True)
