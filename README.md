# etsi-nfv-sol005-test-suite
Tests ETSI NFV SOL005 compatible APIs.

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
export TST_SOL005_ADAPTOR=osm
export TST_SOL005_API_URL=fgcn-osm1.cs.upb.de
```

## Run the test suite

```sh
# default
pytest

# enable logging output
pytest --log-cli-level DEBUG
```
