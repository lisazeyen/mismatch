import logging

logger = logging.getLogger(__name__)

import pypsa

import sys
import os

# Add pypsa-eur scripts to path for import
sys.path.insert(0, os.getcwd() + "/submodules/pypsa-eur-DE-2013/scripts")

from solve_network import solve_network, prepare_network

if __name__ == "__main__":

    opts = snakemake.wildcards.opts.split("-")
    solve_opts = snakemake.config["solving"]["options"]

    n = pypsa.Network(snakemake.input[0])
    n = prepare_network(n, solve_opts)
    n = solve_network(n, config=snakemake.config, opts=opts)
    n.export_to_netcdf(snakemake.output[0])
