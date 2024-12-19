import streamlit as st
from amplpy import AMPL, modules
import os


def run_ampl(nqueens):
    ampl = AMPL()
    ampl.read("./ampl_model.txt")
    ampl.option["solver"] = "highs"
    ampl.option["highs_options"] = "outlev=2"
    ampl.param["n"] = nqueens
    output = ampl.get_output("solve;")
    solution = ampl.get_data("Row").to_dict()
    st.write(solution)
    return output, solution


def show_problem_definition():
    st.subheader("Problem definition", divider="blue")
    st.markdown(":red[How can $N$ queens be placed on an $N \\times N$ chessboard so that no two of them attack each other?]")


def get_ampl_license():
    uuid = os.environ.get("AMPLKEY_UUID")  # Use a free https://ampl.com/ce license
    if uuid is not None:
        modules.activate(uuid)  # activate your license


def show_solution(n, solution):
    st.subheader("Solution", divider="blue")
    queens = set((int(r) - 1, int(c) - 1) for c, r in solution.items())
    solution = "#" + " # " * (n) + "#\n"
    for r in range(n):
        row = "".join([" Q " if (r, c) in queens else " + " for c in range(n)])
        solution += "#" + row + "#\n"
    solution += "#" + " # " * (n) + "#\n"
    st.code(solution, language=None)


def provide_input_parameters():
    st.subheader("Provide input parameters", divider="blue")
    nqueens = st.slider("How many queens?", 2, 25, 8)
    return nqueens


def show_highs_output(output, n):
    st.subheader(f"HiGHS output for {n}", divider="blue")
    st.code(output)


def main():
    st.title("N-Queens")
    get_ampl_license()
    show_problem_definition()
    n = provide_input_parameters()
    output, solution = run_ampl(n)
    show_solution(n, solution)
    show_highs_output(output, n)




if __name__ == "__main__":
    main()
