import pypsa
import pandas as pd

import matplotlib.pyplot as plt

plt.style.use("bmh")


def plot(load, resload, ylim=None, fn=None):
    fig, ax = plt.subplots(figsize=(16, 3))
    load.plot(label="load MW")
    resload.plot(label="residual load MW")
    plt.legend()

    if ylim is not None:
        plt.ylim(ylim)

    if fn is not None:
        plt.savefig(fn, bbox_inches="tight")


if __name__ == "__main__":

    n = pypsa.Network(snakemake.input[0])

    # TIME SERIES

    gen = n.generators_t.p.groupby(n.generators.carrier, axis=1).sum()

    sto = n.storage_units_t.p.groupby(n.storage_units.carrier, axis=1).sum()

    dem = n.loads_t.p.sum(axis=1)
    dem.name = "demand"

    avail = (
        n.generators_t.p_max_pu.multiply(n.generators.p_nom_opt)
        .groupby(n.generators.carrier, axis=1)
        .sum()
        .filter(regex="wind|ror|solar", axis=1)
    )
    gen_vres = gen.filter(regex="wind|ror|solar", axis=1)
    curt = avail - gen_vres
    curt.columns = [f"curtailment-{c}" for c in curt.columns]

    pd.concat([gen, sto, dem, curt], axis=1).div(1e3).to_csv(
        snakemake.output.timeseries, float_format="%.3f"
    )  # GW

    # CAPACITIES

    gen_cap = n.generators.groupby("carrier").p_nom_opt.sum()
    sto_cap = n.storage_units.groupby("carrier").p_nom_opt.sum()

    pd.concat([gen_cap, sto_cap]).div(1e3).to_csv(
        snakemake.output.capacities, float_format="%.3f", header="capacity"
    )  # GW

    # PLOT

    load = n.loads_t.p.sum(axis=1)
    vres = n.generators_t.p.filter(regex="ror|wind|solar", axis=1).sum(axis=1)
    plot(load, load - vres, fn=snakemake.output.plot)
