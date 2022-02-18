import os
import streamlit as st
from solver_amplify import solve
from util import RandomTSPInstance
from dotenv import load_dotenv
import matplotlib.pyplot as plt

slider = st.slider("ncity", min_value=5, max_value=20, value=10)
instance: RandomTSPInstance = RandomTSPInstance(ncity=slider)
st.write(f"Set to the # of city = {slider}")

load_dotenv(".env")
token: str = os.environ.get("AMPLIFY_TOKEN")

with st.spinner("computation..."):
    route = solve(instance, token)

    # build f
    f = plt.figure(figsize=(3, 3))
    plt.xlabel("x")
    plt.ylabel("y")

    # draw route
    if len(route) > 0:
        ncity = instance.ncity
        path_length = sum(
            [instance.distances[route[i]]
                [route[(i + 1) % ncity]] for i in range(ncity)]
        )
        plt.title(f"path length: {path_length}")

        x = [i[0] for i in instance.locations]
        y = [i[1] for i in instance.locations]
        for i in range(ncity):
            r = route[i]
            n = route[(i + 1) % ncity]
            plt.plot([x[r], x[n]], [y[r], y[n]], "b--", alpha=0.5)

    plt.scatter(*zip(*instance.locations))
    plt.tight_layout()
    st.pyplot(f)
