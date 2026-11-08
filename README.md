# Mini Cheetah Lab

Dự án cá nhân để mô phỏng và huấn luyện robot Mini Cheetah bằng MuJoCo và
MjLab, đồng thời giữ lại bộ điều khiển C++ của Cheetah-Software để tham khảo
và phát triển tiếp.

Phần đang phát triển là hai bài toán bám vận tốc trên mặt phẳng và địa hình
gồ ghề. Mô hình đã được chỉnh lại cách lắp mesh hông và tư thế đứng ban đầu.

## Cấu trúc

| Thư mục | Nội dung |
| --- | --- |
| `mjlab/` | MjLab được tích hợp trực tiếp, gồm task và mô hình Mini Cheetah |
| `mjlab/src/mjlab/tasks/velocity/config/mini_cheetah/` | Cấu hình môi trường và PPO |
| `mjlab/src/mjlab/asset_zoo/robots/mini_cheetah/` | MJCF, mesh, actuator và tư thế ban đầu |
| `common/`, `robot/`, `user/` | Động lực học, giao tiếp robot và điều khiển C++ |
| `sim/` | Simulator Qt gốc |
| `resources/` | Mesh gốc của robot |
| `mujoco_env/`, `mjlab_mini_cheetah/` | Các bản thử nghiệm trước khi tích hợp MjLab |
| `docs/` | Hướng dẫn dự án và tài liệu Cheetah-Software gốc |

`build/` chỉ dành cho dữ liệu build trên máy. Mã nguồn MjLab chính nằm ở
`mjlab/`; không cần tải một repo MjLab khác để chạy dự án này.

## Cài đặt môi trường RL

Cần Python 3.11–3.14 và [uv](https://docs.astral.sh/uv/). Huấn luyện với
MuJoCo-Warp cần GPU NVIDIA; chọn bản CUDA phù hợp với driver trên máy.

```sh
cd mjlab
uv sync --locked --extra cu130 --group dev
```

Nếu máy dùng CUDA 12.6, thay `--extra cu130` bằng `--extra cu126`.
Để kiểm tra cấu hình và xem mô hình bằng CPU, dùng `--extra cpu`.

## Xem robot 3D

Chạy từ thư mục gốc dự án:

```sh
make view
```

Cửa sổ giữ robot ở tư thế đứng để kiểm tra hình dạng: kéo chuột trái để xoay,
cuộn để phóng to và kéo chuột phải để dịch chuyển góc nhìn. Đây là chế độ xem
mô hình, chưa chạy policy hay bước mô phỏng vật lý.

Kiểm tra model mà không mở cửa sổ:

```sh
cd mjlab
uv run python scripts/view_mini_cheetah.py --check
```

## Huấn luyện và chạy policy

```sh
cd mjlab
uv run train Mjlab-Velocity-Flat-MiniCheetah --env.scene.num-envs 4096
uv run train Mjlab-Velocity-Rough-MiniCheetah --env.scene.num-envs 4096
```

Giảm `--env.scene.num-envs` nếu GPU thiếu bộ nhớ. Sau khi có checkpoint:

```sh
uv run play Mjlab-Velocity-Flat-MiniCheetah \
  --checkpoint-file logs/rsl_rl/mini_cheetah_velocity/TEN_LAN_CHAY/model_1000.pt
```

Thay đường dẫn mẫu bằng checkpoint thực tế. Model mặc định có 12 khớp,
PD `kp=30`, `kd=0.8`, giới hạn mô-men `17 Nm`; tư thế đứng là
`hip=0`, `thigh=0.8`, `calf=-1.6` rad, thân cao `0.31 m`.

Các môi trường thử nghiệm trong `mujoco_env/` có observation và action scale
khác MjLab; cần đối chiếu trước khi chuyển policy giữa hai môi trường.

## Kiểm tra và đưa lên GitHub

```sh
make check
make test-config
```

Môi trường Python, log, checkpoint và file build được bỏ qua bởi Git.
Hướng dẫn tạo commit và đẩy lên repo của bạn nằm trong [docs/GITHUB.md](docs/GITHUB.md).
Hướng dẫn build bộ điều khiển C++ nằm trong
[docs/CHEETAH_SOFTWARE.md](docs/CHEETAH_SOFTWARE.md).

## Nguồn gốc

Dự án được phát triển từ MIT Cheetah-Software và MjLab. Phần tích hợp Mini
Cheetah và cấu hình môi trường được quản lý trong repo này. Giấy phép và ghi
công của mã nguồn gốc được giữ tại [LICENSE](LICENSE),
[mjlab/LICENSE](mjlab/LICENSE) và [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
