import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 1. CẤU HÌNH TRANG WEB
# =========================
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng theo dõi điểm học tập của 10 sinh viên.")

# =========================
# 2. DỮ LIỆU SINH VIÊN
# =========================
data = {
    "Họ tên": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Lê Văn Cường",
        "Phạm Thị Dung",
        "Hà Danh Bảo",
        "Vũ Thị Hương",
        "Đặng Văn Khoa",
        "Bùi Thị Lan",
        "Ngô Văn Minh",
        "Đỗ Thị Ngọc"
    ],
    "Chuyên cần": [9, 8, 10, 7, 9, 8, 10, 9, 7, 8],
    "Giữa kỳ":    [8, 7, 9, 6, 8, 7, 9, 8, 6, 7],
    "Cuối kỳ":    [9, 8, 10, 7, 9, 8, 9, 9, 7, 8]
}

df = pd.DataFrame(data)

# Công thức điểm tổng kết: 20% chuyên cần + 30% giữa kỳ + 50% cuối kỳ
df["Tổng kết"] = (
    0.2 * df["Chuyên cần"]
    + 0.3 * df["Giữa kỳ"]
    + 0.5 * df["Cuối kỳ"]
).round(2)


def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Không đạt"


df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# =========================
# 3. BẢNG ĐIỂM
# =========================
st.header("📋 Bảng điểm của 10 sinh viên")
st.dataframe(df, use_container_width=True, hide_index=True)

# =========================
# 4. THỐNG KÊ TỔNG QUAN
# =========================
diem_tb = df["Tổng kết"].mean()
sv_cao_nhat = df.loc[df["Tổng kết"].idxmax()]
sv_thap_nhat = df.loc[df["Tổng kết"].idxmin()]
so_sv_dat = int((df["Tổng kết"] >= 5).sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
col2.metric("Điểm cao nhất", f'{sv_cao_nhat["Tổng kết"]:.2f}')
col3.metric("Điểm thấp nhất", f'{sv_thap_nhat["Tổng kết"]:.2f}')
col4.metric("Số sinh viên đạt", f"{so_sv_dat}/10")

st.write(
    f'**Sinh viên cao nhất:** {sv_cao_nhat["Họ tên"]} '
    f'({sv_cao_nhat["Tổng kết"]:.2f} điểm)'
)
st.write(
    f'**Sinh viên thấp nhất:** {sv_thap_nhat["Họ tên"]} '
    f'({sv_thap_nhat["Tổng kết"]:.2f} điểm)'
)

# =========================
# 5. CHỌN SINH VIÊN XEM ĐIỂM
# =========================
st.header("🔎 Tra cứu điểm theo sinh viên")
ten_sv = st.selectbox("Chọn một sinh viên:", df["Họ tên"].tolist())
sv = df.loc[df["Họ tên"] == ten_sv].iloc[0]

st.subheader(f'Thông tin điểm: {sv["Họ tên"]}')
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", f'{sv["Chuyên cần"]:.1f}')
c2.metric("Giữa kỳ", f'{sv["Giữa kỳ"]:.1f}')
c3.metric("Cuối kỳ", f'{sv["Cuối kỳ"]:.1f}')
c4.metric("Tổng kết", f'{sv["Tổng kết"]:.2f}')
c5.metric("Xếp loại", sv["Xếp loại"])

# =========================
# 6. BIỂU ĐỒ CỘT
# =========================
st.header("📊 Biểu đồ điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(df["Họ tên"], df["Tổng kết"])
ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", rotation=40)
ax.bar_label(bars, fmt="%.2f", padding=3)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# =========================
# 7. THÔNG TIN NGƯỜI TẠO
# =========================
st.divider()
st.caption("Người tạo ứng dụng: Hà Danh Bảo | MSSV: 040208015960")
