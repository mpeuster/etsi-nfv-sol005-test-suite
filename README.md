# etsi-nfv-sol005-test-suite
Tests ETSI NFV SOL005 compatible APIs.

## Notes

* The test suite assumes to always use the same test service for everything: Ping-Pong service with two VNFs. Each adaptor has to come with the corresponding fixtures (e.g., VNFDs, NSDs) for its MANO system to be tested.

## Install

### Sol005 Test Suite

```sh
python3 setup.py install
```

### OSM Adaptor

If the OSM adaptor should be used, the `osmclient` package needs to be installed:

#### Ubuntu

```sh
# install missing packages
sudo apt install python3-dev
sudo pip uninstall backports.ssl-match-hostname
sudo apt-get install python-backports.ssl-match-hostname
sudo apt-get install libcurl4-openssl-dev
# (may be incomplete)
pip install git+https://osm.etsi.org/gerrit/osm/osmclient
```

#### OS X
```sh
brew install libmagic
pip uninstall pycurl
export PYCURL_SSL_LIBRARY=openssl
export LDFLAGS=-L/usr/local/opt/openssl/lib;export CPPFLAGS=-I/usr/local/opt/openssl/include;pip install pycurl --compile --no-cache-dir

pip install git+https://osm.etsi.org/gerrit/osm/osmclient
```


## Configure

```sh
# basic configuration
export TST_SOL005_ADAPTOR=osm
export TST_SOL005_API_URL=fgcn-osm1.cs.upb.de
# VIM configuration (needed if VIM tests should be executed)
export TST_SOL005_VIM_URL=http://$VIMEMU_HOSTNAME:6001/v2.0
export TST_SOL005_VIM_TYPE=openstack
export TST_SOL005_VIM_USER=username
export TST_SOL005_VIM_PASSWORD=password
export TST_SOL005_VIM_TENEANT=tenantName
```

## Run the test suite

```sh
# default
pytest

# enable logging output
pytest --log-cli-level DEBUG

# filter by markers (skip tests that deploy a NS):
pytest -m "not nsdeploy"

# filter by test name
pytest --log-cli-level DEBUG -k "test_ns_create"

# if you have version conflicts, try:
python3 -m pytest
```


## Manual style check
```sh
flake8 --exclude .eggs sol005tests
```
