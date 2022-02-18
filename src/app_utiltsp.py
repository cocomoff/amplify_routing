import os
import streamlit as st
from src.util_tsp.solver_amplify import solve
from src.util import RandomTSPInstance
from dotenv import load_dotenv
import matplotlib.pyplot as plt

slider = st.slider("ncity", min_value=5, max_value=20, value=10)
coeff = st.slider("weight", min_value=1, max_value=10, value=3)
instance: RandomTSPInstance = RandomTSPInstance(ncity=slider, utility=True)
st.write(f"Set to the # of city = {slider}, weight {coeff}")

load_dotenv(".env")
token: str = os.environ.get("AMPLIFY_TOKEN")

with st.spinner("computation..."):
    route = solve(instance, token, A=coeff)

    # build f
    f = plt.figure(figsize=(3, 3))
    plt.xlabel("x")
    plt.ylabel("y")

    # draw route
    if len(route) > 0:
        ncity = len(route)
        path_length = sum(
            [instance.distances[route[i]]
                [route[(i + 1) % ncity]] for i in range(ncity)]
        )
        get_util = sum(instance.utilities[j] for j in route)
        plt.title(f"path length: {path_length:>.3f}, util: {get_util}")

        x = [i[0] for i in instance.locations]
        y = [i[1] for i in instance.locations]
        for i in range(ncity):
            r = route[i]
            n = route[(i + 1) % ncity]
            plt.plot([x[r], x[n]], [y[r], y[n]], "b--", alpha=0.5)

    plt.scatter(*zip(*instance.locations))
    plt.tight_layout()
    st.pyplot(f)
