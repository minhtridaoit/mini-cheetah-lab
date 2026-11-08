# Đưa Mini Cheetah Lab lên GitHub

Chạy các lệnh Git từ thư mục gốc chứa `README.md` và `mjlab/`.
Dự án đã có Git cục bộ, nhánh `main`, chưa gắn remote và chưa tạo commit.

## 1. Kiểm tra mã nguồn

```sh
git status
make check
make test-config
```

Git bỏ qua `build/`, `.venv/`, log, checkpoint và thư mục sao lưu
`.git-backups/`. Mã nguồn MjLab phải xuất hiện dưới `mjlab/`.

Nếu Git chưa biết tên/email của bạn, đặt cấu hình riêng cho repo:

```sh
git config user.name "TEN_CUA_BAN"
git config user.email "EMAIL_GITHUB_CUA_BAN"
```

## 2. Tạo commit đầu tiên

```sh
git add .
git commit -m "Initialize Mini Cheetah Lab"
```

## 3. Tạo repository trống trên GitHub

Trong GitHub, chọn **New repository**, đặt tên, ví dụ `mini-cheetah-lab`,
và chọn chế độ public/private theo ý bạn. Để repo trống: không tạo sẵn README,
license hoặc `.gitignore`, vì dự án đã có các file này.

## 4. Gắn remote và push

Thay `YOUR_USERNAME` và `YOUR_REPOSITORY` bằng tài khoản và tên repo vừa tạo:

```sh
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Đăng nhập GitHub khi công cụ Git yêu cầu. Sau lần đầu, bạn có thể dùng
**Commit** và **Sync Changes** trong VS Code.

## Bản sao trên máy hiện tại

Lịch sử Git của MjLab trước khi tích hợp được giữ trong
`.git-backups/mjlab.git`; cấu hình bot và quy trình phát hành upstream nằm ở
`.git-backups/upstream-scaffolding/`. Các bản sao này không được push.

Đường dẫn cũ `build/mjlab` là liên kết cục bộ đến `mjlab/`, giúp môi trường
Python hiện có tiếp tục chạy. Khi clone repo trên máy khác, tạo môi trường
mới trong `mjlab/` theo README; không cần liên kết này.
