import streamlit as st
import datetime
import os
import io
from PIL import Image

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

# --- Page Settings & Responsive Design ---
st.set_page_config(page_title="Smart CAM Inspection System", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F4F6F9; }
    h1 { color: #2C3E50; font-family: 'sans-serif'; font-size: 24px; }
    .stButton>button { width: 100%; font-weight: bold; height: 45px; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📹 Smart CAM Inspection System")
st.write("Fill in the fields, capture product & label photos sequentially, and download the PDF report.")

# --- Using Standard Global Font ---
final_font = "Helvetica"
final_font_bold = "Helvetica-Bold"

# Initialize Session State
if "prod_img_data" not in st.session_state: st.session_state.prod_img_data = None
if "label_img_data" not in st.session_state: st.session_state.label_img_data = None

# --- Layout Division ---
col1, col2 = st.columns(2)

# --- LEFT COLUMN: Inspection Form & PDF Generation ---
with col1:
    st.subheader("📝 Inspection Information")
    
    date_val = st.date_input("Inspection Date", datetime.date.today())
    
    inspectors = ["Lee Wan-hee", "Cho Kyung-seok", "Kim Min-woo", "Lee Hong-gyu"]
    inspector_val = st.selectbox("Inspector", inspectors, index=1)
    
    pn_val = st.text_input("P/N (Product Name)", placeholder="Enter product name")
    lot_val = st.text_input("LOT No.", placeholder="Enter LOT number")
    manufacturer_val = st.text_input("Manufacturer", value="ABSFIL")
    client_val = st.text_input("Client", placeholder="Enter client name")
    
    st.markdown("---")
    st.subheader("💾 Export Report")
    
    # 파일명 정의
    formatted_date = date_val.strftime("%Y%m%d") if hasattr(date_val, 'strftime') else str(date_val).replace("-", "")
    clean_pn = pn_val if pn_val else "Unknown_PN"
    pdf_filename = f"{formatted_date}_{clean_pn}_Inspection.pdf"

    # PDF 바이트 생성 함수 (다운로드 시 실시간 빌드)
    def generate_pdf_bytes():
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Header Box
        c.setFillColor(colors.HexColor("#1A252F"))
        c.rect(40, 720, 530, 45, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(final_font_bold, 18)
        c.drawString(55, 733, "SMART CAM INSPECTION REPORT")
        
        # Summary Table
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.setFont(final_font_bold, 12)
        c.drawString(45, 690, "1. Inspection Summary")
        
        c.setLineWidth(0.8)
        c.setStrokeColor(colors.HexColor("#BDC3C7"))
        c.rect(40, 550, 530, 125, fill=0, stroke=1)
        c.line(40, 633, 570, 633)
        c.line(40, 591, 570, 591)
        c.line(305, 550, 305, 675)
        
        c.setFont(final_font_bold, 10)
        c.setFillColor(colors.HexColor("#7F8C8D"))
        c.drawString(50, 658, "Date:")
        c.drawString(315, 658, "Inspector:")
        c.drawString(50, 616, "Product Name (P/N):")
        c.drawString(315, 616, "LOT Number:")
        c.drawString(50, 574, "Manufacturer:")
        c.drawString(315, 574, "Client Name:")
        
        c.setFont(final_font, 10.5)
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.drawString(130, 658, str(date_val))
        c.drawString(405, 658, inspector_val)
        c.drawString(160, 616, clean_pn)
        c.drawString(405, 616, lot_val if lot_val else "-")
        c.drawString(130, 574, manufacturer_val)
        c.drawString(405, 574, client_val if client_val else "-")
            
        # Photos Layout
        y_photo_title = 515
        y_photo_box = 325
        c.setFont(final_font_bold, 12)
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.drawString(45, y_photo_title, "2. Captured Evidence")
        
        frame_w = 250
        frame_h = 175
        
        if st.session_state.prod_img_data:
            st.session_state.prod_img_data.save("temp_p.jpg")
            c.setFont(final_font_bold, 10)
            c.setFillColor(colors.HexColor("#2C3E50"))
            c.drawString(45, y_photo_box + frame_h + 5, "[ Image 01: Product Frame ]")
            c.drawImage("temp_p.jpg", 40, y_photo_box, width=frame_w, height=frame_h)
            c.rect(40, y_photo_box, frame_w, frame_h, fill=0, stroke=1)
        else:
            c.setStrokeColor(colors.HexColor("#E74C3C"))
            c.rect(40, y_photo_box, frame_w, frame_h, fill=0, stroke=1)
            c.setFont(final_font, 10)
            c.setFillColor(colors.HexColor("#E74C3C"))
            c.drawString(110, y_photo_box + (frame_h/2), "Missing Product Image")
            
        if st.session_state.label_img_data:
            st.session_state.label_img_data.save("temp_l.jpg")
            c.setFont(final_font_bold, 10)
            c.setFillColor(colors.HexColor("#2C3E50"))
            c.drawString(325, y_photo_box + frame_h + 5, "[ Image 02: Label Frame ]")
            c.drawImage("temp_l.jpg", 320, y_photo_box, width=frame_w, height=frame_h)
            c.setStrokeColor(colors.HexColor("#BDC3C7"))
            c.rect(320, y_photo_box, frame_w, frame_h, fill=0, stroke=1)
        else:
            c.setStrokeColor(colors.HexColor("#E74C3C"))
            c.rect(320, y_photo_box, frame_w, frame_h, fill=0, stroke=1)
            c.setFont(final_font, 10)
            c.setFillColor(colors.HexColor("#E74C3C"))
            c.drawString(390, y_photo_box + (frame_h/2), "Missing Label Image")
            
        # Footer
        c.setStrokeColor(colors.HexColor("#1A252F"))
        c.setLineWidth(1)
        c.line(40, 80, 570, 80)
        c.setFont(final_font, 8)
        c.setFillColor(colors.HexColor("#95A5A6"))
        c.drawString(45, 65, "This report is systematically generated via Smart CAM Inspection Module.")
        c.save()
        
        # 임시 생성 이미지 즉시 삭제 (지정 폴더 청결 유지)
        if os.path.exists("temp_p.jpg"): os.remove("temp_p.jpg")
        if os.path.exists("temp_l.jpg"): os.remove("temp_l.jpg")
        
        buffer.seek(0)
        return buffer.getvalue()

    # 다운로드 버튼 (누르면 생성과 동시에 다운로드 진행)
    st.download_button(
        label="📥 Generate & Download PDF Report",
        data=generate_pdf_bytes(),
        file_name=pdf_filename,
        mime="application/pdf",
        type="primary"
    )

# --- RIGHT COLUMN: Sequenced Camera & Preview Check Board ---
with col2:
    st.subheader("📸 Step 1: Capture Product")
    cam_prod = st.camera_input("Product Camera Screen", key="cam_1")
    if cam_prod:
        st.session_state.prod_img_data = Image.open(cam_prod)
        st.success("Product Photo Saved!")

    st.markdown("---")
    st.subheader("📸 Step 2: Capture Label")
    cam_label = st.camera_input("Label Camera Screen", key="cam_2")
    if cam_label:
        st.session_state.label_img_data = Image.open(cam_label)
        st.success("Label Photo Saved!")

    st.markdown("---")
    st.subheader("🖼️ Preview Captured Images")
    
    view_col1, view_col2 = st.columns(2)
    with view_col1:
        st.write("**[ Product Preview ]**")
        if st.session_state.prod_img_data:
            st.image(st.session_state.prod_img_data, use_container_width=True)
        else: st.info("No Product Image")
            
    with view_col2:
        st.write("**[ Label Preview ]**")
        if st.session_state.label_img_data:
            st.image(st.session_state.label_img_data, use_container_width=True)
        else: st.info("No Label Image")
