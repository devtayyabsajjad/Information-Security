<div align="center">

# 🔐 Secure Text Encryption & Decryption

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Cryptography](https://img.shields.io/badge/Cryptography-40.0.1-green?style=for-the-badge&logo=lockup)](https://cryptography.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212748842-9fcbad5b-6173-4175-8a61-521f19bf3b0c.gif" width="500">
</p>

**A modern, secure application for encrypting and decrypting text files using military-grade encryption**

</div>

## ✨ Features

- 🔒 **Secure Encryption**: Encrypt any text file with Fernet symmetric encryption (AES-128 in CBC mode)
- 🔑 **Easy Decryption**: Decrypt files using the same key with a user-friendly interface
- 📊 **Live Preview**: See your original and processed text in real-time
- 💾 **One-Click Downloads**: Download encrypted/decrypted files directly from the browser
- 🌙 **Beautiful UI**: Modern, responsive design with animations and intuitive controls
- 🔄 **Seamless Mode Switching**: Switch between encryption and decryption modes with automatic file refresh

## 🖼️ Screenshots

<div align="center"> 
<table>
  <tr>
    <td><img src="https://github.com/streamlit/streamlit/raw/develop/examples/data/screenshot.png" alt="Encryption Mode" width="400"/></td>
    <td><img src="https://github.com/streamlit/streamlit/raw/develop/examples/data/screenshot.png" alt="Decryption Mode" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>Encryption Mode</b></td>
    <td align="center"><b>Decryption Mode</b></td>
  </tr>
</table>
</div>

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone <repo_url>
cd text_crypto_app

# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 🔍 How It Works

1. **Encryption**:
   - Upload any text file
   - Click the "Encrypt" button
   - Copy and securely save the generated key
   - Download the encrypted file

2. **Decryption**:
   - Upload an encrypted file (`.enc`)
   - Paste the encryption key
   - Click the "Decrypt" button
   - Download the decrypted file

## 🔒 Security

This application uses the [Fernet](https://cryptography.io/en/latest/fernet/) implementation from the Python cryptography package, which provides:

- AES-128 encryption in CBC mode
- PKCS7 padding
- HMAC using SHA256 for authentication
- Secure random IV generation

⚠️ **Important**: Always keep your encryption keys secure. Without the correct key, encrypted data cannot be recovered.

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)**: For the web interface
- **[Cryptography](https://cryptography.io/)**: For encryption/decryption operations
- **[Python](https://www.python.org/)**: Core programming language

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### Made with ❤️ for secure communications

</div>
