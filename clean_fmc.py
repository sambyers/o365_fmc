#clean up script for FMC

from fireREST import FireREST

fmc = FireREST(fmc_server, username, password)

network_objs = fmc.get_objects('network')

print(type(network_objs))