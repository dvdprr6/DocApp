#
# Setup the dev environment
#

Exec { path => ["/bin/", "/sbin/", "/usr/bin", "/usr/sbin/" ] }

class doc-apt-webapp{

}

include doc-apt-webapp
include python3
include system-update