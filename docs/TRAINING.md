# Huấn luyện Mini Cheetah

Chạy các lệnh dưới đây trong `mjlab/` và dùng môi trường Python đã cài theo
README. Huấn luyện dùng GPU; lần đầu MuJoCo-Warp cần biên dịch kernel CUDA,
nên khởi động có thể lâu hơn các lần sau.

## Chạy thử trước khi huấn luyện dài

```sh
uv run train Mjlab-Velocity-Flat-MiniCheetah \
  --env.scene.num-envs 16 --agent.max-iterations 2
```

Lệnh phải hoàn tất mà không có traceback, tạo checkpoint và log. Chạy thử
ngắn chỉ xác nhận pipeline mô phỏng, PPO và lưu model hoạt động; không đánh
giá được khả năng đi của robot.

## Bắt đầu trên mặt phẳng

```sh
uv run train Mjlab-Velocity-Flat-MiniCheetah \
  --env.scene.num-envs 256 --agent.max-iterations 1000
```

256 môi trường là mức khởi đầu đã chạy thử trên RTX 3050 Laptop 6 GB của máy
hiện tại. Tăng số môi trường sau khi theo dõi VRAM và tốc độ; giảm xuống 128
hoặc 64 nếu thiếu bộ nhớ. `max-iterations` là số vòng cập nhật PPO, mỗi vòng
thu 24 bước cho mỗi môi trường; không phải số episode.

Nên kiểm tra dáng đi bằng checkpoint trước khi chuyển sang địa hình gồ ghề.
Task rough có thể khởi chạy riêng với số môi trường nhỏ:

```sh
uv run train Mjlab-Velocity-Rough-MiniCheetah \
  --env.scene.num-envs 16 --agent.max-iterations 1000
```

Đây là một lần huấn luyện mới, không tự nạp policy flat. Hai task có observation
khác nhau vì rough có thêm height scan; không nạp trực tiếp checkpoint flat
vào rough nếu chưa xử lý sự khác biệt này.

## Theo dõi và xem policy

Mặc định task Mini Cheetah dùng TensorBoard, không cần đăng nhập W&B:

```sh
uv run tensorboard --logdir logs/rsl_rl
```

Mở `http://localhost:6006`. Theo dõi reward, độ dài episode, lỗi bám vận tốc,
và các lần kết thúc vì ngã. Đánh giá bằng nhiều lần chạy và xem chuyển động
thực tế trong simulator thay vì chỉ nhìn reward.

Log và checkpoint được ghi tại:

```text
logs/rsl_rl/mini_cheetah_velocity/TEN_LAN_CHAY/
```

Runner lưu checkpoint mỗi 50 iterations và khi kết thúc, đồng thời xuất ONNX.
Thay đường dẫn mẫu sau bằng checkpoint có thật:

```sh
uv run play Mjlab-Velocity-Flat-MiniCheetah \
  --num-envs 1 --viewer native \
  --checkpoint-file logs/rsl_rl/mini_cheetah_velocity/TEN_LAN_CHAY/model_999.pt
```

Để tiếp tục một lần huấn luyện flat đã có, dùng đúng task và cấu hình mạng:

```sh
uv run train Mjlab-Velocity-Flat-MiniCheetah \
  --env.scene.num-envs 256 --agent.resume \
  --agent.load-run TEN_LAN_CHAY --agent.load-checkpoint model_999.pt
```

## Observation và triển khai sau huấn luyện

Policy flat hiện nhận observation 48 chiều, critic nhận 72 chiều, action có
12 chiều. Các con số này đã được xác nhận khi khởi tạo runner; chúng khác
observation 45 chiều của môi trường Gymnasium thử nghiệm.

Runner tự xuất ONNX phù hợp với policy đang huấn luyện. Script
`mjlab/export_policy.py` là bản thử nghiệm cũ với input cố định 45 chiều,
không dùng script đó cho policy MjLab mới. Việc chạy trên robot thật còn cần
đối chiếu thứ tự observation, chuẩn hóa, thứ tự/trục khớp và cách áp dụng
action với bộ điều khiển phần cứng.
