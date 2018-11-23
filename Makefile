#######################################################################
#
# CHALLENGER MAKEFILE
#
#	This Makefile exposes various targets related to the compiling
#	and building of the `challenger` application.
#
#######################################################################


clean:
	rm -rf var
	rm -rf .coverage.*
	rm -rf .coverage

env:
	virtualenv env
