About the repository structure
==============================

This repository follows the [python3-pip-skeleton]
(https://diamondlightsource.github.io/python3-pip-skeleton/main/index.html)
repository structure, with a conventional pyproject.toml to describe the
package requirements and all code belonging under ``src/lunchbox``.

All code for the raspberry pi pico is stored in src/lunchbox/pico, such that
the Pico-W-Go vscode extension can be setup to sync with this folder. In this
way a user can develop both the micropython code for the pico as well as python
code for the ophyd devices and bluesky plans.
