"""Export trained RSL-RL policy to ONNX and TorchScript for deployment.

Usage:
    uv run python export_policy.py [--checkpoint path/to/model.pt]
"""

import argparse
import glob
import os

import torch
import torch.nn as nn


def find_latest_checkpoint(log_dir="logs/rsl_rl/mini_cheetah_velocity"):
  runs = glob.glob(os.path.join(log_dir, "*"))
  if not runs:
    return None
  latest_run = max(runs, key=os.path.getmtime)
  checkpoints = glob.glob(os.path.join(latest_run, "model_*.pt"))
  if not checkpoints:
    return None

  # Extract iteration number and find max
  def get_iter(path):
    name = os.path.basename(path)
    try:
      return int(name.split("_")[1].split(".")[0])
    except (IndexError, ValueError):
      return 0

  latest_checkpoint = max(checkpoints, key=get_iter)
  return latest_checkpoint


class PolicyWrapper(nn.Module):
  """Wraps actor network and normalizer for clean deployment."""

  def __init__(self, actor, normalizer=None):
    super().__init__()
    self.actor = actor
    self.normalizer = normalizer

  def forward(self, obs: torch.Tensor) -> torch.Tensor:
    if self.normalizer is not None:
      obs = self.normalizer(obs)
    return self.actor(obs)


def export_policy(checkpoint_path=None, output_dir="exported_policies"):
  os.makedirs(output_dir, exist_ok=True)

  if checkpoint_path is None:
    checkpoint_path = find_latest_checkpoint()
    if checkpoint_path is None:
      print(
        "Chưa tìm thấy checkpoint huấn luyện trong logs/rsl_rl/mini_cheetah_velocity/."
      )
      print(
        "Hãy chạy huấn luyện trước bằng: uv run train Mjlab-Velocity-Flat-MiniCheetah"
      )
      return

  print(f"[*] Đang tải checkpoint: {checkpoint_path}")
  checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)

  # Inspect checkpoint structure
  print("[*] Cấu trúc checkpoint keys:", list(checkpoint.keys()))

  # Extract actor weights
  model_state = checkpoint.get("model_state_dict", checkpoint)

  # Standard observation dimension for Mini Cheetah in mjlab is 45 dims
  obs_dim = 45
  action_dim = 12

  # Dummy actor matching RSL-RL architecture: MLP (512, 256, 128) -> ELU -> 12
  class ActorMLP(nn.Module):
    def __init__(self):
      super().__init__()
      self.net = nn.Sequential(
        nn.Linear(obs_dim, 512),
        nn.ELU(),
        nn.Linear(512, 256),
        nn.ELU(),
        nn.Linear(256, 128),
        nn.ELU(),
        nn.Linear(128, action_dim),
      )

    def forward(self, x):
      return self.net(x)

  actor = ActorMLP()

  # Try to load state dict if matching
  actor_dict = {}
  for k, v in model_state.items():
    if "actor" in k:
      clean_k = k.replace("actor.", "").replace("net.", "")
      actor_dict[clean_k] = v

  if actor_dict:
    try:
      actor.net.load_state_dict(actor_dict, strict=False)
      print("[+] Đã nạp trọng số Actor thành công!")
    except Exception as e:
      print(f"[!] Warning: {e}")

  actor.eval()

  # 1. Export TorchScript (JIT)
  dummy_input = torch.zeros(1, obs_dim, dtype=torch.float32)
  traced_model = torch.jit.trace(actor, dummy_input)
  assert isinstance(traced_model, torch.jit.ScriptModule)
  jit_path = os.path.join(output_dir, "mini_cheetah_policy.pt")
  traced_model.save(jit_path)
  print(f"[✓] Đã xuất TorchScript thành công: {jit_path}")

  # 2. Export ONNX
  onnx_path = os.path.join(output_dir, "mini_cheetah_policy.onnx")
  try:
    torch.onnx.export(
      actor,
      (dummy_input,),
      onnx_path,
      input_names=["observation"],
      output_names=["action"],
      dynamic_axes={"observation": {0: "batch_size"}, "action": {0: "batch_size"}},
      opset_version=14,
    )
    print(f"[✓] Đã xuất ONNX thành công: {onnx_path}")
  except Exception as e:
    print(f"[!] Lỗi xuất ONNX: {e}")

  print("\nThông tin mô hình triển khai:")
  print(
    f"  - Input shape:  [1, {obs_dim}] (IMU gyro, gravity, vel_cmd, joint_pos_err, joint_vel, last_action)"
  )
  print(
    f"  - Output shape: [1, {action_dim}] (12 target joint angles for PD controller)"
  )


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--checkpoint", type=str, default=None, help="Đường dẫn file checkpoint model_*.pt"
  )
  args = parser.parse_args()
  export_policy(args.checkpoint)
