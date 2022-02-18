from typing import List
from util import RandomTSPInstance, show_plot
from amplify.client import FixstarsClient
from amplify.constraint import equal_to
from amplify import (
    BinaryPoly,
    SymbolGenerator,
    sum_poly,
    Solver,
    decode_solution,
)
import os
import numpy as np
from dotenv import load_dotenv


def solve(instance: RandomTSPInstance, token: str) -> List[int]:
    ncity = instance.ncity
    gen = SymbolGenerator(BinaryPoly)
    q = gen.array((ncity, ncity))

    # travel cost
    cost = sum_poly(
        ncity,
        lambda n: sum_poly(
            ncity,
            lambda i: sum_poly(
                ncity, lambda j: instance.distances[i][j] *
                q[n][i] * q[(n + 1) % ncity][j]
            ),
        ),
    )

    # row and column constraints
    row_constraints = [
        equal_to(sum_poly([q[n][i] for i in range(ncity)]), 1) for n in range(ncity)
    ]
    col_constraints = [
        equal_to(sum_poly([q[n][i] for n in range(ncity)]), 1) for i in range(ncity)
    ]
    constraints = sum(row_constraints) + sum(col_constraints)
    constraints *= np.amax(instance.distances)
    model = cost + constraints

    # solve
    client = FixstarsClient()
    client.token = token
    client.parameters.timeout = 3000
    solver = Solver(client)

    result = solver.solve(model)
    if len(result) == 0:
        raise RuntimeError("Any one of constraints is not satisfied.")

    # energy, values = result[0].energy, result[0].values
    values = result[0].values
    q_values = decode_solution(q, values, 1)
    route = np.where(np.array(q_values) == 1)[1]
    return route


if __name__ == '__main__':
    load_dotenv(".env")
    token: str = os.environ.get("AMPLIFY_TOKEN")
    instance: RandomTSPInstance = RandomTSPInstance(ncity=15)
    route = solve(instance, token)
    print(route)
    show_plot(instance=instance, route=route, filename="tsp.png")
