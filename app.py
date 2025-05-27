import streamlit as st
import base64
import time
from crypto import generate_key, encrypt_text, decrypt_text
from cryptography.fernet import InvalidToken

st.set_page_config(
    page_title="🔐 Text Crypto App",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a more attractive UI with animations and enhanced styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp { 
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%); 
        color: #FAFAFA; 
    }
    
    .stButton>button { 
        background: linear-gradient(90deg, #FF4E50 0%, #F9D423 100%); 
        color: #FFFFFF; 
        font-weight: 600; 
        border: none; 
        border-radius: 8px; 
        padding: 0.6rem 1.2rem; 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover { 
        transform: translateY(-3px) scale(1.02); 
        box-shadow: 0 7px 14px rgba(255, 78, 80, 0.3); 
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }
    
    .card { 
        background: rgba(32, 33, 36, 0.8); 
        padding: 2rem; 
        border-radius: 16px; 
        margin-bottom: 2rem; 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        backdrop-filter: blur(10px);
        animation: fadeIn 0.6s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(249, 212, 35, 0.5); }
        50% { box-shadow: 0 0 20px rgba(249, 212, 35, 0.8); }
        100% { box-shadow: 0 0 5px rgba(249, 212, 35, 0.5); }
    }
    
    .keybox { 
        background: rgba(22, 23, 26, 0.9); 
        padding: 1.5rem; 
        border-radius: 12px; 
        font-family: 'Courier New', monospace; 
        border: 1px solid rgba(255, 78, 80, 0.3); 
        animation: glow 2s infinite;
    }
    
    textarea { 
        background: rgba(22, 23, 26, 0.9); 
        color: #FAFAFA; 
        border: 1px solid rgba(255, 255, 255, 0.2); 
        border-radius: 8px; 
        padding: 1rem; 
        width: 100%; 
        font-family: 'Courier New', monospace;
        transition: border 0.3s ease;
    }
    
    textarea:focus {
        border: 1px solid rgba(255, 78, 80, 0.5);
        box-shadow: 0 0 10px rgba(255, 78, 80, 0.3);
    }
    
    .stTextInput>div>div>input {
        background: rgba(22, 23, 26, 0.9);
        color: #FAFAFA;
        border: 1px solid rgba(255, 78, 80, 0.3);
        border-radius: 8px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border: 1px solid rgba(255, 78, 80, 0.7);
        box-shadow: 0 0 10px rgba(255, 78, 80, 0.3);
    }
    
    .stRadio>div {
        background: rgba(32, 33, 36, 0.7);
        padding: 0.8rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stRadio>div:hover {
        border: 1px solid rgba(255, 78, 80, 0.3);
    }
    
    .stFileUploader>div>button {
        background: linear-gradient(90deg, #3A7BD5 0%, #00D2FF 100%);
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stFileUploader>div>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 210, 255, 0.3);
    }
    
    .main-title {
        text-align: center;
        font-size: 3.2rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, #FF4E50 0%, #F9D423 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.5px;
        animation: fadeIn 1s ease-out;
    }
    
    .subtitle {
        text-align: center;
        margin-bottom: 2.5rem;
        opacity: 0.9;
        font-size: 1.2rem;
        font-weight: 300;
        animation: fadeIn 1.2s ease-out;
    }
    
    .mode-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2.5rem;
        animation: fadeIn 1.4s ease-out;
    }
    
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px;
        padding: 1rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    .stSuccess {
        background: rgba(25, 135, 84, 0.2);
        border: 1px solid rgba(25, 135, 84, 0.5);
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.2);
        border: 1px solid rgba(255, 193, 7, 0.5);
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.2);
        border: 1px solid rgba(220, 53, 69, 0.5);
    }
    
    .stInfo {
        background: rgba(13, 202, 240, 0.2);
        border: 1px solid rgba(13, 202, 240, 0.5);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #F9D423;
        display: flex;
        align-items: center;
    }
    
    .section-title svg {
        margin-right: 0.5rem;
    }
    
    code {
        border-radius: 8px;
        padding: 1rem !important;
        background-color: rgba(22, 23, 26, 0.9) !important;
        color: #F9D423 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.9rem !important;
        border: 1px solid rgba(249, 212, 35, 0.3) !important;
        transition: all 0.3s ease;
    }
    
    code:hover {
        border-color: rgba(249, 212, 35, 0.7) !important;
        box-shadow: 0 0 15px rgba(249, 212, 35, 0.3);
    }
    
    /* Animated background */
    .bg-animation {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.15;
        background: linear-gradient(125deg, #FF4E50, #F9D423, #3A7BD5, #00D2FF);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    
    <!-- Animated background div -->
    <div class="bg-animation"></div>
""", unsafe_allow_html=True)

# Use HTML for better styling of the title
st.markdown('<h1 class="main-title">🔐 Secure Text Encryption & Decryption</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Protect your sensitive text files with military-grade encryption</p>', unsafe_allow_html=True)

# Add animated icons
icon_html = """
<div style="text-align: center; margin-bottom: 2rem; animation: fadeIn 1.5s ease-out;">
    <span style="font-size: 3rem; margin: 0 1rem; display: inline-block; animation: pulse 2s infinite;">🔒</span>
    <span style="font-size: 3rem; margin: 0 1rem; display: inline-block; animation: pulse 2s infinite 0.5s;">🔑</span>
    <span style="font-size: 3rem; margin: 0 1rem; display: inline-block; animation: pulse 2s infinite 1s;">📄</span>
</div>
<style>
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}
</style>
"""
st.markdown(icon_html, unsafe_allow_html=True)

# Store the current mode in session state to detect changes
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "encrypt"

# Create a more visually appealing mode selector
st.markdown('<div class="mode-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    mode = st.radio("Select Operation Mode", ["🗝️ Encrypt", "🔑 Decrypt"], horizontal=True, key="mode_selector")
    
    # Check if mode has changed and clear uploaded file if it has
    current_mode = "encrypt" if mode.startswith("🗝️") else "decrypt"
    if current_mode != st.session_state.current_mode:
        # Reset the file uploader by using a unique key based on time
        st.session_state.uploader_key = f"file_uploader_{time.time()}"
        st.session_state.current_mode = current_mode
        # Ensure the uploaded file is cleared from session state
        if 'uploaded' in st.session_state:
            del st.session_state.uploaded
st.markdown('</div>', unsafe_allow_html=True)

# Create a unique key for the file uploader to force refresh when mode changes
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = "file_uploader_initial"

# Use columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded = st.file_uploader("Upload .txt or .enc file", type=None, key=st.session_state.uploader_key)
    
    # Store the uploaded file in session state
    if uploaded is not None:
        st.session_state.uploaded = uploaded

# Check if we have an uploaded file either from this session or from session state
if uploaded is None and 'uploaded' not in st.session_state:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.info("📤 Please upload a file to proceed.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
elif uploaded is None and 'uploaded' in st.session_state:
    uploaded = st.session_state.uploaded

# Read raw bytes once
raw_bytes = uploaded.getvalue()

if mode.startswith("🗝️"):
    # Encrypt mode: show plain text preview in a card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    try:
        plain_text = raw_bytes.decode('utf-8')
        st.markdown('<div class="section-title"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2V8H20" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M16 13H8" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M16 17H8" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 9H9H8" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Original Text (preview)</div>', unsafe_allow_html=True)
        st.text_area("", plain_text, height=200)
    except UnicodeDecodeError:
        st.error("❌ Uploaded file isn't valid UTF-8 text.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create columns for the encrypt button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        encrypt_button = st.button("🔒 Encrypt File", use_container_width=True)
    
    if encrypt_button:
        # Generate key & encrypt
        key = generate_key()
        cipher_bytes = encrypt_text(raw_bytes, key)
        
        # Success message with animation
        st.balloons()
        st.success("✅ Encryption successful!")
        
        # Display the key in a visually appealing card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15 7C16.1046 7 17 6.10457 17 5C17 3.89543 16.1046 3 15 3C13.8954 3 13 3.89543 13 5C13 6.10457 13.8954 7 15 7Z" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 17L17 21" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 21L17 17" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12.5 7.5L3.5 16.5" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 11L9.5 13.5" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Your Encryption Key</div>', unsafe_allow_html=True)
        st.warning("⚠️ **IMPORTANT:** Copy and save this key securely. Without it, you cannot decrypt your file!")
        st.code(key.decode(), language=None)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display the encrypted text in another card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 16V12" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 8H12.01" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Encrypted Text (Base64)</div>', unsafe_allow_html=True)
        st.text_area("", cipher_bytes.decode(), height=200)
        
        # Simple direct download button
        st.download_button(
            label="⬇️ Download Encrypted File",
            data=cipher_bytes,
            file_name=uploaded.name + ".enc",
            mime="application/octet-stream"
        )
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Decrypt mode: show cipher text preview in a card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    try:
        cipher_preview = raw_bytes.decode()
        st.markdown('<div class="section-title"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19 11H5C3.89543 11 3 11.8954 3 13V20C3 21.1046 3.89543 22 5 22H19C20.1046 22 21 21.1046 21 20V13C21 11.8954 20.1046 11 19 11Z" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Encrypted Text (preview)</div>', unsafe_allow_html=True)
        st.text_area("", cipher_preview, height=200)
    except UnicodeDecodeError:
        # If raw_bytes are not base64-text, show a message
        st.info("📁 Binary encrypted file detected - no preview available")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create a card for key input
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 2L19 4M11.3891 11.6109C12.3844 12.6062 12.3844 14.1938 11.3891 15.1891C10.3938 16.1844 8.80619 16.1844 7.81091 15.1891C6.81563 14.1938 6.81563 12.6062 7.81091 11.6109C8.80619 10.6156 10.3938 10.6156 11.3891 11.6109ZM15.05 6.5L17.5 9M17.5 9L20.5 12L19 13.5L17 11.5L14 8.5L11 5.5L7.5 2L6 3.5L9 6.5L11.5 9L14 11.5L15.5 13L17 11.5L17.5 9Z" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Enter Decryption Key</div>', unsafe_allow_html=True)
    
    # Simple key input field
    key_input = st.text_input("Paste your Fernet key", type="password", help="Enter the encryption key you received when encrypting the file")
    key_bytes = key_input.encode() if key_input else None
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create columns for the decrypt button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        decrypt_button = st.button("🔓 Decrypt File", use_container_width=True)
    
    if decrypt_button:
        if not key_bytes:
            st.warning("⚠️ Please provide a decryption key to continue.")
        else:
            try:
                plain_bytes = decrypt_text(raw_bytes, key_bytes)
                plain_text = plain_bytes.decode('utf-8')

                # Success message with animation
                st.balloons()
                st.success("✅ Decryption successful!")
                
                # Display decrypted text in a card
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 4V2" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 22V20" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4.92993 4.93005L6.33993 6.34005" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M17.6599 17.66L19.0699 19.07" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 12H4" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M20 12H22" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.33993 17.66L4.92993 19.07" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M19.0699 4.93005L17.6599 6.34005" stroke="#F9D423" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Decrypted Text</div>', unsafe_allow_html=True)
                st.text_area("", plain_text, height=200)
                
                # Create a download button for the decrypted file
                output_filename = uploaded.name.replace(".enc", ".txt")
                if output_filename == uploaded.name:  # If no .enc extension was found
                    output_filename = "decrypted_" + uploaded.name
                    
                st.download_button(
                    label="⬇️ Download Decrypted File",
                    data=plain_bytes,
                    file_name=output_filename,
                    mime="text/plain"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            except InvalidToken:
                st.error("❌ Invalid key or corrupted file. Please check your key and try again.")
            except Exception as e:
                st.error(f"❌ Decryption failed: {e}")
