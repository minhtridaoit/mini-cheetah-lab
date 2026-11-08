# Third-party source and local changes

Mini Cheetah Lab integrates the following upstream projects. Their original
copyright notices and licenses remain in the source tree.

## MIT Cheetah-Software

- Upstream: https://github.com/mit-biomimetics/Cheetah-Software
- Copyright: MIT Biomimetic Robotics Lab, 2019.
- License: MIT, retained in `LICENSE`.
- Source: `common/`, `robot/`, `sim/`, `user/`, `resources/`, and related C++
  build/configuration files.
- Original setup instructions: `docs/CHEETAH_SOFTWARE.md`.

## MjLab

- Upstream: https://github.com/mujocolab/mjlab
- Imported revision: `dcdf6ce519abfd2ea45e9503ae6fb650b75bb869`.
- Package version at import: 1.6.0.
- License: Apache-2.0, retained in `mjlab/LICENSE`.
- Source: `mjlab/`; the Python package name remains `mjlab` for compatibility.
- Original project overview and citation metadata:
  `mjlab/docs/UPSTREAM_README.md` and `mjlab/docs/UPSTREAM_CITATION.cff`.

Local changes include the Mini Cheetah robot asset and velocity-task
registration, flat/rough environment and PPO settings, corrected hip mesh
transforms and standing pose, a local model viewer, and project documentation.
The MjLab runtime is included directly, rather than as a Git submodule.

## Bundled libraries

Dependencies under `third-party/` retain their original license files and
source notices. They remain separate from this project's original additions.
