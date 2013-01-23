# Watson, a Python 3 web framework

> It's elementary my dear Watson

Watson is an easy to use framework designed to get out of your way and let you code your application rather than wrangle with the framework.

#### Build Status

Branch | Status
------------ | -------------
Master | ![Build Status](https://api.travis-ci.org/simoncoulton/watson.png?branch=master)
Develop | ![Build Status](https://api.travis-ci.org/simoncoulton/watson.png?branch=develop)


### Dependencies

Watson currently requires the following modules to work out of box:

* Jinja2

These can be installed by running `pip install -r requirements.txt`

#### Optional Dependencies

##### Memcached

Add python3-memcached to your applications `requirements.txt` file or `pip install python3-memcached`
This is currently maintained [here][1].

### Running the tests

1. Setup a virtualenv for Python 3.3
2. Install Fabric `pip install fabric` 
3. Install Nose `pip install nose`
3. Run `fab test clean`

Results from the tests can be found in `docs/tests/`

### Supported Versions
Currently Watson has been tested on the following Python versions:

* 3.2
* 3.3

[1]: http://pypi.python.org/pypi/python3-memcached/

