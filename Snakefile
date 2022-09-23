configfile: "config.yaml"

wildcard_constraints:
  clusters="[0-9]+",
  opts="[-+a-zA-Z0-9\.]*",
  country="[A-Z]+",
  year="[0-9]+",

include: "subconfigs/subSnakefile"

rule solve_all_networks:
    input: expand("results/networks/elec_s_{clusters}_ec_lcopt_{opts}_c{country}_y{year}.nc", **config["scenarios"])

rule process_all_solved_networks:
    input: expand("results/summaries/elec_s_{clusters}_ec_lcopt_{opts}_c{country}_y{year}_capacity.csv", **config["scenarios"])

def memory(w):
    factor = 3.
    for o in w.opts.split('-'):
        m = re.match(r'^(\d+)h$', o, re.IGNORECASE)
        if m is not None:
            factor /= int(m.group(1))
            break
    return int(factor * (10000 + 195 * int(w.clusters)))

rule solve_network:
    input: "networks/elec_s_{clusters}_ec_lcopt_{opts}_c{country}_y{year}.nc"
    output: "results/networks/elec_s_{clusters}_ec_lcopt_{opts}_c{country}_y{year}.nc"
    threads: 4
    resources: mem=memory
    script: "scripts/solve_network.py"

rule process_solved_network:
    input: "results/networks/elec_s_{clusters}_ec_lcopt_{opts}_c{country}_y{year}.nc"
    output:
        capacities="results/summaries/elec_s_{clusters}_ec_lcopt_{opts}_c{country}_y{year}_capacity.csv",
        timeseries="results/summaries/elec_s_{clusters}_ec_lcopt_{opts}_c{country}_y{year}_time.csv",
        plot="results/summaries/elec_s_{clusters}_ec_lcopt_{opts}_c{country}_y{year}_plot.pdf"
    script: "scripts/process_solved_network.py"
