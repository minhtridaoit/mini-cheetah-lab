"""Tests for command manager."""

from dataclasses import dataclass

import pytest
import torch
from conftest import get_test_device
from manager_test_env import make_manager_test_env_cfg

from mjlab.envs import ManagerBasedRlEnv
from mjlab.managers.command_manager import CommandTerm, CommandTermCfg


@pytest.fixture(scope="module")
def device():
  return get_test_device()


class CounterCommand(CommandTerm):
  """Stateful command term: a per-env counter ticked by _update_command."""

  def __init__(self, cfg, env):
    super().__init__(cfg, env)
    self.ticks = torch.zeros(self.num_envs, dtype=torch.long, device=self.device)

  @property
  def command(self) -> torch.Tensor:
    return self.ticks.unsqueeze(-1).float()

  def _update_metrics(self) -> None:
    pass

  def _resample_command(self, env_ids: torch.Tensor) -> None:
    self.ticks[env_ids] = 0

  def _update_command(self, env_ids: torch.Tensor | None = None) -> None:
    if env_ids is None:
      self.ticks += 1
    else:
      self.ticks[env_ids] += 1


@dataclass(kw_only=True)
class CounterCommandCfg(CommandTermCfg):
  resampling_time_range: tuple[float, float] = (1e9, 1e9)

  def build(self, env) -> CounterCommand:
    return CounterCommand(self, env)


@pytest.fixture
def counter_env(device):
  cfg = make_manager_test_env_cfg()
  cfg.scene.num_envs = 4
  cfg.commands = {"counter": CounterCommandCfg()}
  env = ManagerBasedRlEnv(cfg=cfg, device=device)
  yield env
  env.close()


def test_partial_reset_does_not_advance_other_envs(counter_env):
  env = counter_env
  term = env.command_manager.get_term("counter")
  assert isinstance(term, CounterCommand)

  # Full reset: every env is resampled (counter zeroed) then ticked once.
  env.reset()
  assert term.ticks.tolist() == [1, 1, 1, 1]

  action = torch.zeros((env.num_envs, 1), device=env.device)
  env.step(action)
  assert term.ticks.tolist() == [2, 2, 2, 2]

  # Partial reset: only env 1 is resampled and ticked. Before the fix for
  # issue #1138 the other envs advanced too (to 3).
  env.reset(env_ids=torch.tensor([1], dtype=torch.int64, device=env.device))
  assert term.ticks.tolist() == [2, 1, 2, 2]

  # The next step advances everyone by exactly one.
  env.step(action)
  assert term.ticks.tolist() == [3, 2, 3, 3]


def test_old_style_update_command_raises(counter_env):
  """Terms with the old zero-arg _update_command fail fast at construction."""

  class OldStyleCommand(CounterCommand):
    def _update_command(self) -> None:  # type: ignore[override]
      self.ticks += 1

  @dataclass(kw_only=True)
  class OldStyleCommandCfg(CounterCommandCfg):
    def build(self, env) -> "OldStyleCommand":
      return OldStyleCommand(self, env)

  with pytest.raises(TypeError, match="env_ids"):
    OldStyleCommandCfg().build(counter_env)
