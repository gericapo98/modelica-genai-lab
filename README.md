# Modelica GenAI Lab

Experimental sandbox for automated Modelica model generation, compilation, and verification using GenAI-assisted workflows.

Goal: evaluate LLM-generated Modelica models against reference implementations via reproducible simulation pipelines.

Stack: OpenModelica (CLI via Docker), OMPython, FMU (FMPy), RTAMT (STL checks), NumPy/Pandas.

Process: text/prompt → Modelica model (.mo) → compiled/simulated (OMC) → outputs compared numerically (RMSE, tolerance) → optional STL property verification → report deviation.

Scope: pipeline robustness, semantic correctness, and behavioral equivalence testing for GenAI-produced models.

Focus: automation, reproducibility, differential testing, and expressiveness of generative modeling.

