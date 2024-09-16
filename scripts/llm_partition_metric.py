import difflib
import re
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dtw import dtw
from scipy.stats import wasserstein_distance


def split_on_partitions(code: str) -> list[str]:
    code = re.sub(r"^<JANUS_PARTITION>\s*", "", code)
    code = re.sub(r"\s*<JANUS_PARTITION>\s*$", "", code)
    code = code.strip("\n")
    return re.split(r"\n\s*<JANUS_PARTITION>\s*\n", code)


def get_partition_bitvec(chunks: list[str]) -> np.ndarray:
    # Split each chunk into lines
    chunk_lines = [chunk.strip().split("\n") for chunk in chunks]
    chunk_lens = list(map(len, chunk_lines))

    # Get line index of each partition
    partition_indices = np.cumsum([0] + chunk_lens)

    # Get a bitvector where there is a bit for each line of the original input,
    #  with 1s at locations corresponding to the last line of partitions
    bitvec = np.zeros(sum(chunk_lens) + 1, dtype=bool)
    bitvec[partition_indices] = True

    return bitvec


@np.vectorize(signature="(n),(n)->()")
def emd(a: np.ndarray, b: np.ndarray) -> float:
    """Earth mover's distance (EMD) between two bit vectors"""
    support = np.arange(len(a))
    return wasserstein_distance(support, support, a, b)


def manhattan(a: np.ndarray, b: np.ndarray) -> float:
    return np.linalg.norm(a.astype(float) - b.astype(float), ord=1, axis=-1)


def euclidean(a: np.ndarray, b: np.ndarray) -> float:
    return np.linalg.norm(a.astype(float) - b.astype(float), axis=-1)


@np.vectorize(signature="(n),(n)->()")
def dynamic_time_warp(a: np.ndarray, b: np.ndarray) -> float:
    return dtw(a, b).normalizedDistance


def f1(a: np.ndarray, b: np.ndarray) -> float:
    tp = np.bitwise_and(a, b).sum(axis=-1)
    fp = np.bitwise_and(np.bitwise_not(a), b).sum(axis=-1)
    fn = np.bitwise_and(a, np.bitwise_not(b)).sum(axis=-1)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * (precision * recall) / (precision + recall)


def check_files(a: str, b: str) -> None:
    a_chunks = split_on_partitions(a)
    b_chunks = split_on_partitions(b)

    # Check that the strings are equal when partitions have been removed
    a = "\n".join(a_chunks)
    b = "\n".join(b_chunks)
    a_lines = a.split("\n")
    b_lines = b.split("\n")
    if a != b:
        diff = "\n".join(difflib.unified_diff(a_lines, b_lines))
        raise Exception(f"Departitioned strings don't match. Diff: \n{diff}")

    av = get_partition_bitvec(a_chunks)
    bv = get_partition_bitvec(b_chunks)
    if len(av) != len(bv):
        raise Exception(
            f"Bitvecs don't match: \n{get_bitstring(av)}\n{get_bitstring(bv)}"
        )


def experimental_mean_dist(
    bitvec: np.ndarray,
    metric: Callable[[np.ndarray, np.ndarray], float] = emd,
    density: float | None = None,
    n: int = 1000,
) -> tuple[float, float]:
    """Construct n random partitionings with the given density, and calculate
    the mean/stddev EMD from the given bit vector.
    """
    m = len(bitvec)
    if density is None:
        density = bitvec[1:-1].mean()
        if density == 0:
            density = 1 / m
    samples = np.random.binomial(n=1, p=density, size=(n, m))
    samples[:, [0, -1]] = 1
    dists = metric(bitvec, samples)
    return dists.mean(), dists.std()


def density_normalized_metric(
    metric: Callable[[np.ndarray, np.ndarray], float],
    density: float | None = None,
    n: int = 1000,
) -> Callable[[np.ndarray, np.ndarray], float]:
    def func(a: np.ndarray, b: np.ndarray) -> float:
        dist = metric(a, b)
        mean, std = experimental_mean_dist(a, metric, density, n)
        return (dist - mean) / std

    return func


def get_paths(dir: Path, glob="**/*.m") -> dict[str, Path]:
    return {str(p.relative_to(dir)): p for p in dir.rglob(glob)}


def get_bitstring(bitvec: np.ndarray, chars=(" ", "|")) -> str:
    return "[" + "".join(np.array(chars)[bitvec.astype(int)]) + "]"


if __name__ == "__main__":
    # path = Path("~/llm-data/vista_irt-mumps/00-inputs/processed_inputs").expanduser()
    # file_glob = "**/*.m"
    path = Path("~/llm-data/walmart-alc/00-inputs/processed_inputs").expanduser()
    file_glob = "**/*.asm"
    outpath = Path("~/janus/scripts/plots").expanduser()
    outpath.mkdir(parents=True, exist_ok=True)

    human_paths = get_paths(path / "human-partitioned", file_glob)
    gen_paths = get_paths(path / "llm-partitioned", file_glob)
    gen_paths.update(get_paths(path / "alg-partitioned", file_glob))

    # Check Files
    failed = False
    for filename, p in gen_paths.items():
        a = (path / "human-partitioned" / p.name).read_text()
        b = p.read_text()
        # b = b + "\n" + a.rsplit("\n", 1)[-1]
        # p.write_text(b)
        try:
            check_files(a, b)
        except Exception as e:
            print(f"{filename}: {e}")
            failed = True
    if failed:
        raise Exception()

    # TODO: Issue is that ast-strict chunking does not retain
    # code outside of CSECTS/DSECTS

    human_bitvecs = {
        k: get_partition_bitvec(split_on_partitions(p.read_text().strip()))
        for k, p in human_paths.items()
    }
    human_bitstrs = {k: get_bitstring(v) for k, v in human_bitvecs.items()}

    human_partition_densities = [v[1:-1].mean() for v in human_bitvecs.values()]
    mean_human_partition_density = float(np.mean(human_partition_densities))

    gen_bitvecs = {
        k: get_partition_bitvec(split_on_partitions(p.read_text().strip()))
        for k, p in gen_paths.items()
    }
    gen_bitstrs = {k: get_bitstring(v) for k, v in gen_bitvecs.items()}

    metrics = dict(
        F1=f1,
        DTW=dynamic_time_warp,
        EMD=emd,
        L2=euclidean,
        # norm_dtw=density_normalized_metric(
        #   dynamic_time_warp,
        #   density=mean_human_partition_density),
        # norm_emd=density_normalized_metric(
        #   emd,
        #   density=mean_human_partition_density)
    )
    metric_names = list(metrics.keys())

    score_dict: dict[str, dict[str, float]] = {}
    for metric_name, metric in metrics.items():
        score_dict[metric_name] = {
            key: metric(human_bitvecs[Path(key).name], gen_bitvecs[key])
            for key in gen_bitvecs.keys()
            if Path(key).name in human_bitvecs
        }

    data = [
        (
            Path(key).name,
            len(human_bitvecs[Path(key).name]),
            human_bitvecs[Path(key).name][1:-1].mean(),
            Path(key).parts[0],
            Path(key).parts[1],
            gen_bitvecs[key][1:-1].mean(),
            *[score_dict[m][key] for m in metric_names],
            gen_bitstrs[key],
        )
        for key in gen_bitvecs.keys()
    ]
    df = pd.DataFrame(
        data=data,
        columns=[
            "file",
            "length",
            "human_density",
            "partitioner",
            "limit",
            "density",
            "F1",
            "DTW",
            "EMD",
            "L2",
            "partition_string",
        ],
    )
    df.set_index("file", inplace=True)

    df["emd_norm"] = df.EMD - df.EMD.min()
    df.emd_norm = df.emd_norm / df.emd_norm.max()

    df["dtw_norm"] = df.DTW - df.DTW.min()
    df.dtw_norm = df.dtw_norm / df.dtw_norm.max()

    print(df)
    g = df.groupby(["partitioner", "limit"])[metric_names]
    print(df.groupby(["partitioner", "limit"])[metric_names].mean())

    # df.reset_index().pivot(index="file", columns=["partitioner","limit"], values="F1")

    for name, group in df.groupby("partitioner"):
        print()
        print(name)
        print(group[["human_density", "length", "density", *metric_names]].corr())

    plt.clf()
    ax = sns.scatterplot(
        x="length",
        y="F1",
        hue="partitioner",
        data=df,
    )
    ax.legend(loc="upper right")
    ax.set(
        xlabel="File Length",
        ylabel="F1 Score",
        title="F1 Score vs File Length",
    )
    # ax.set(xscale="log", yscale="log")
    ax.set_ylim(0, 1)
    plt.tight_layout()
    ax.get_figure().savefig(outpath / "f1_length.png")

    plt.clf()
    ax = sns.scatterplot(
        x="F1",
        y="emd_norm",
        hue="partitioner",
        data=df,
    )
    ax.legend(loc="upper right")
    ax.set(
        xlabel="F1 Score",
        ylabel="Normalized Earth Mover's Distance",
        title="EMD vs F1",
    )
    # ax.set(xscale="log", yscale="log")
    # ax.set_ylim(0, 1)
    plt.tight_layout()
    ax.get_figure().savefig(outpath / "emd_f1.png")

    plt.clf()
    ax = sns.scatterplot(
        x="F1",
        y="dtw_norm",
        hue="partitioner",
        data=df,
    )
    ax.legend(loc="upper right")
    ax.set(
        xlabel="F1 Score",
        ylabel="Normalized Dynamic Time Warping Distance",
        title="DTW vs F1",
    )
    # ax.set(xscale="log", yscale="log")
    # ax.set_ylim(0, 1)
    plt.tight_layout()
    ax.get_figure().savefig(outpath / "dtw_f1.png")

    plt.clf()
    ax = sns.scatterplot(
        x="emd_norm",
        y="dtw_norm",
        hue="partitioner",
        data=df,
    )
    ax.legend(loc="upper right")
    ax.set(
        xlabel="Normalized Earth Mover's Distance",
        ylabel="Normalized Dynamic Time Warping Distance",
        title="DTW vs EMD",
    )
    # ax.set(xscale="log", yscale="log")
    # ax.set_ylim(0, 1)
    plt.tight_layout()
    ax.get_figure().savefig(outpath / "dtw_emd.png")

    pivoted = df.reset_index().pivot(
        index=["file", "limit"], columns=["partitioner"], values="F1"
    )

    plt.clf()
    ax = sns.scatterplot(
        x="ast-strict",
        y="gpt-4o",
        hue="limit",
        data=pivoted,
    )
    ax.legend(loc="upper right")
    ax.set(
        xlabel="AST Strict F1",
        ylabel="GPT-4o F1",
        title="AST Chunking vs LLM chunking",
    )
    # ax.set(xscale="log", yscale="log")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    plt.tight_layout()
    ax.get_figure().savefig(outpath / "gpt-4o_ast-strict.png")

    # # Make sure we have the same files in each set
    # assert(not set.symmetric_difference(
    #     set(llm_bitvecs.keys()),
    #     set(human_bitvecs.keys())
    # ))

    # # metric = emd
    # # metric = dynamic_time_warp
    # metric = f1
    # # metric = euclidean
    # # metric = density_normalized_metric(emd)
    # # metric = density_normalized_metric(emd, density=mean_human_partition_density)

    # scores = {
    #     key: metric(human_bitvecs[key], llm_bitvecs[key])
    #     for key in human_bitvecs.keys()
    # }

    # for key in sorted(scores, key=scores.get): # type: ignore
    #     human_bitvec = human_bitvecs[key]
    #     llm_bitvec = llm_bitvecs[key]

    #     human_bitstring = "".join(map(str, human_bitvec.astype(int).tolist()))
    #     llm_bitstring = "".join(map(str, llm_bitvec.astype(int).tolist()))

    #     chars = np.array([" ", "|"])
    #     human_bitstring = "[" + "".join(chars[human_bitvec.astype(int)]) + "]"
    #     llm_bitstring = "[" + "".join(chars[llm_bitvec.astype(int)]) + "]"

    #     # cd_mean, cd_std = human_density_stats[key]
    #     # ad_mean, ad_std = mean_human_density_stats[key]
    #     # ld_mean, ld_std = llm_density_stats[key]

    #     print(f"{key}: {scores[key]:.3f}")
    #     # print(f"  Distance: {distances[key]:.5f}")
    #     # print(f"  Mean distance with correct density: {cd_mean:.3f} ({cd_std:.3f})")
    #     # print(f"  Mean distance with average density: {ad_mean:.3f} ({ad_std:.3f})")
    #     # print(f"  Mean distance with LLM density:     {ld_mean:.3f} ({ld_std:.3f})")
    #     print(f"SME: {human_bitstring}")
    #     print(f"LLM: {llm_bitstring}\n")
