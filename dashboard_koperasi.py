import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Dashboard Koperasi",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS + ANIMASI
# ============================================================
st.markdown("""
<style>
    /* --- ANIMASI DASAR --- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }

    /* --- HEADER ANIMASI --- */
    .main-header {
        background: linear-gradient(270deg, #1e88e5, #42a5f5, #1565c0, #64b5f6);
        background-size: 400% 400%;
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: gradientMove 8s ease infinite, fadeIn 1s ease-out;
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.8rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* --- KARTU KPI (Base Style) --- */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #1e88e5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: fadeIn 0.8s ease-out forwards, float 4s ease-in-out infinite;
        height: 100%;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 900;
        color: #1e88e5;
        margin-top: 5px;
    }

    .metric-label {
        font-size: 14px;
        font-weight: 600;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* --- JUDUL SUBHEADER & FOOTER --- */
    h3 {
        border-bottom: 3px solid #1e88e5;
        padding-bottom: 8px;
        display: inline-block;
        color: #1565c0;
    }
    
    .footer {
        text-align: center; 
        color: #888; 
        padding: 20px;
        border-top: 1px solid #ddd;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER (Sudah dihilangkan nama Annisa)
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🏪 Dashboard Koperasi</h1>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KOMPONEN KPI DENGAN ANIMASI MENGIKUTI KURSOR (JAVASCRIPT)
# ============================================================
# Menggunakan HTML/JS via components.html agar bisa membaca posisi mouse
kpi_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    .kpi-container {
        display: flex;
        gap: 15px;
        perspective: 1000px; /* Penting untuk efek 3D */
        margin-bottom: 20px;
    }
    .kpi-card {
        flex: 1;
        background: #ffffff;
        border-radius: 15px;
        border-left: 6px solid #1e88e5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 20px;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        transform-style: preserve-3d;
        cursor: pointer;
        animation: float 4s ease-in-out infinite;
    }
    /* Warna khusus pulse untuk Total Penjualan */
    .kpi-card.pulse-card {
        border-left: 6px solid #ff9800;
    }
    
    .metric-label {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        transform: translateZ(20px); /* Efek 3D text */
    }
    .metric-value {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 28px;
        font-weight: 900;
        color: #1e88e5;
        margin-top: 5px;
        transform: translateZ(30px); /* Efek 3D text */
    }
    .kpi-card.pulse-card .metric-value { color: #ff9800; }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
</style>
</head>
<body style="margin: 0; padding: 0; overflow: hidden;">
    <!-- BARIS 1 -->
    <div class="kpi-container">
        <div class="kpi-card" onmousemove="tilt(event, this)" onmouseleave="reset(this)">
            <div class="metric-label">Kartu KIP</div>
            <div class="metric-value">4</div>
        </div>
        <div class="kpi-card pulse-card" onmousemove="tilt(event, this)" onmouseleave="reset(this)">
            <div class="metric-label">Total Penjualan</div>
            <div class="metric-value">Rp 2 Jt</div>
        </div>
        <div class="kpi-card" onmousemove="tilt(event, this)" onmouseleave="reset(this)">
            <div class="metric-label">Margin Kotor</div>
            <div class="metric-value">Rp 773 Rb</div>
        </div>
        <div class="kpi-card" onmousemove="tilt(event, this)" onmouseleave="reset(this)">
            <div class="metric-label">Jumlah Transaksi</div>
            <div class="metric-value">16</div>
        </div>
    </div>

    <!-- BARIS 2 -->
    <div class="kpi-container" style="margin-top: 15px;">
        <div class="kpi-card" style="flex: 1;" onmousemove="tilt(event, this)" onmouseleave="reset(this)">
            <div class="metric-label">Margin Kotor Persen</div>
            <div class="metric-value">44.00%</div>
        </div>
        <div class="kpi-card" style="flex: 1;" onmousemove="tilt(event, this)" onmouseleave="reset(this)">
            <div class="metric-label">Rata-rata Margin per Transaksi</div>
            <div class="metric-value">Rp 48.3 Rb</div>
        </div>
    </div>

<script>
    function tilt(event, element) {
        const rect = element.getBoundingClientRect();
        const x = event.clientX - rect.left; // x position within the element.
        const y = event.clientY - rect.top;  // y position within the element.

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        // Menghitung derajat kemiringan (semakin besar angkanya semakin miring)
        const rotateX = ((y - centerY) / centerY) * -15; 
        const rotateY = ((x - centerX) / centerX) * 15;

        // Hapus animasi float sementara saat di-hover agar tidak bentrok
        element.style.animation = "none";
        element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
        element.style.boxShadow = "0 15px 30px rgba(30, 136, 229, 0.4)";
    }

    function reset(element) {
        // Mengembalikan ke posisi semula dan memunculkan kembali animasi float
        element.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        element.style.boxShadow = "0 4px 6px rgba(0,0,0,0.05)";
        element.style.animation = "float 4s ease-in-out infinite";
    }
</script>
</body>
</html>
"""

# Render HTML di Streamlit (Tinggi diatur agar pas untuk 2 baris kartu)
components.html(kpi_html, height=220)

st.divider()

# ============================================================
# DATA PENJUALAN BULANAN
# ============================================================
bulan_data = {
    "Bulan": ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
    "Total Penjualan (Juta)": [0.21, 0.40, 0.63, 0.55, 0.42, 0.28,
                                0.14, 0.06, 0.10, 0.14, 0.20, 0.21]
}
df_bulanan = pd.DataFrame(bulan_data)

# ============================================================
# DATA PENJUALAN PER KECAMATAN
# ============================================================
kecamatan_data = {
    "Kecamatan": ["Jatigede", "Darmaraja", "Pamulihan", "Ganeas",
                  "Cimalaka", "Situraja", "Jatinunggal", "Buahdua",
                  "Jatinangor", "Rancakalong", "Paseh", "Cimanggung",
                  "Cibugel", "Conggeang", "Cisitu", "Cisarua"],
    "Total Penjualan": [
        127203500, 116925000, 101665000, 101680000,
        150440000, 128545000, 78020000, 83710000,
        90155000, 88705000, 83985000, 79655000,
        96465000, 98640000, 12224000, 3876000
    ]
}
df_kecamatan = pd.DataFrame(kecamatan_data).sort_values("Total Penjualan", ascending=True)

# ============================================================
# GRAFIK 1: TREN PENJUALAN BULANAN
# ============================================================
st.subheader("📈 Total Penjualan oleh Bulan")

fig_tren = go.Figure()
fig_tren.add_trace(go.Scatter(
    x=df_bulanan["Bulan"],
    y=df_bulanan["Total Penjualan (Juta)"],
    mode="lines+markers",
    line=dict(color="#1e88e5", width=3, shape="spline"),
    marker=dict(size=8, color="#1e88e5"),
    fill="tozeroy",
    fillcolor="rgba(30, 136, 229, 0.15)",
    hovertemplate="<b>%{x}</b><br>Penjualan: Rp %{y:.2f} Juta<extra></extra>"
))
fig_tren.update_layout(
    xaxis_title="Bulan",
    yaxis_title="Total Penjualan (Juta Rp)",
    hovermode="x unified",
    height=450,
    template="plotly_white"
)
st.plotly_chart(fig_tren, use_container_width=True)

st.caption("💡 Grafik garis (tren) menunjukkan pola musiman dengan sangat baik — puncak penjualan terjadi di bulan Maret.")

# ============================================================
# GRAFIK 2: PERINGKAT PENJUALAN PER KECAMATAN
# ============================================================
st.subheader("📊 Total Penjualan oleh Kecamatan")

fig_bar = px.bar(
    df_kecamatan,
    x="Total Penjualan",
    y="Kecamatan",
    orientation="h",
    text="Total Penjualan",
    color="Total Penjualan",
    color_continuous_scale="Blues",
    labels={"Total Penjualan": "Total Penjualan (Rp)"}
)
fig_bar.update_traces(
    texttemplate="Rp %{text:,.0f}",
    textposition="outside"
)
fig_bar.update_layout(
    height=600,
    template="plotly_white",
    coloraxis_showscale=False,
    xaxis_title="Total Penjualan (Rp)",
    yaxis_title=""
)
st.plotly_chart(fig_bar, use_container_width=True)

# ============================================================
# GRAFIK 3: HEATMAP MATRIKS
# ============================================================
st.subheader("🔥 Peta Panas (Heatmap) Matriks Kecamatan")

heatmap_raw = {
    "Kecamatan": ["Jaringan", "Darmaraja", "Pamulihan", "Ganeas", "Cimalaka",
                  "Situraja", "Jatinunggal", "Buahdua", "Jatinangor", "Rancakalong",
                  "Paseh", "Cimanggung", "Cibugel", "Conggeang", "Cisitu", "Cisarua"],
    "6":  [127203500, 590500, 6573000, 8466500, 5776000, 6859000, 6062000, 8231000,
           8911000, 3853000, 5837500, 4431000, 5877000, 5646000, 3876000, 0],
    "7":  [0, 116925000, 101665000, 101680000, 9131000, 80995000, 78020000, 83710000,
           90155000, 88705000, 83985000, 79655000, 96465000, 98640000, 12224000, 0],
    "8":  [0, 0, 10105000, 10168000, 9820500, 128545000, 115190500, 108410000, 114315000,
           123200000, 105953000, 118445000, 117860000, 122415000, 7475000, 0],
    "9":  [0, 0, 0, 0, 15044000, 9258000, 0, 124780000, 121605000, 141275000, 136700000,
           140925000, 100150000, 109680000, 116425000, 0],
    "10": [0, 0, 0, 0, 0, 122615000, 0, 119050000, 118455000, 126325000, 116725000,
           133470000, 122540000, 147435000, 143955000, 0],
    "11": [0, 0, 0, 0, 0, 0, 0, 0, 133229000, 119448365, 117769764, 144538766, 121411170,
           102641000, 150318901, 0],
    "12": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "13": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "14": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "15": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "16": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "17": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "18": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "19": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "20": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
df_heatmap = pd.DataFrame(heatmap_raw).set_index("Kecamatan")

fig_heatmap = px.imshow(
    df_heatmap,
    aspect="auto",
    color_continuous_scale="YlOrRd",
    labels=dict(x="Periode", y="Kecamatan", color="Penjualan (Rp)"),
    text_auto=".2s"
)
fig_heatmap.update_layout(
    height=600,
    template="plotly_white",
    xaxis_title="Periode",
    yaxis_title="Kecamatan"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.caption("💡 Heatmap matriks berwarna-warni menunjukkan distribusi penjualan per kecamatan di setiap periode.")

# ============================================================
# TABEL DATA DETAIL
# ============================================================
st.subheader("📋 Tabel Data Detail per Kecamatan")

df_display = df_kecamatan.sort_values("Total Penjualan", ascending=False).copy()
df_display["Total Penjualan"] = df_display["Total Penjualan"].apply(
    lambda x: f"Rp {x:,.0f}"
)
st.dataframe(df_display, use_container_width=True, hide_index=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class='footer'>
    <p>© 2025 Dashboard Koperasi</p>
</div>
""", unsafe_allow_html=True)