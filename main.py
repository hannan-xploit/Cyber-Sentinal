import streamlit as st
import requests

# 1. Page Configuration (Stylish Dark Cyber Theme)
st.set_page_config(
    page_title="CyberToolkit - Breach Checker",
    page_icon="🔓",
    layout="centered"
)

# Custom Styling (Cyber Look)
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #FF3366;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #888888;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔓 CyberToolkit Enterprise</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Have I Been Pwned? — Email Leak Checker</div>', unsafe_allow_html=True)

# 2. Input Field for Email
email = st.text_input("📧 Enter Email Address to Check", placeholder="example@gmail.com")

# 3. Check Logic using Hibp Api (Using HaveIBeenPwned API or free open-source alternative like HaveIBeenPwned proxy)
def check_email_leak(email_to_check):
    # Free alternative / public API for breach check (HIBP officially requires an API key, so we use a public API lookup)
    url = f"https://api.breachdirectory.org/v1/secure?email={email_to_check}" # Or any other public API you were using
    # Note: If you have your own HIBP API Key, you can add headers:
    # headers = {"hibp-api-key": "YOUR_KEY_HERE"}
    
    # For a stable and free alternative, we can also check HIBP's public ranges if you used that,
    # but here is a simple public lookup simulation/fetch:
    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/abcde") # Example connection test
        # Let's perform the real API call that you configured in your original code:
        # (Using a standard public endpoint or mock check if key is not there)
        
        # HIBP Direct Lookup (Requires API Key in reality, otherwise returns 401/403)
        headers = {
            "User-Agent": "CyberToolkit-App",
        }
        api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email_to_check}"
        res = requests.get(api_url, headers=headers)
        
        if res.status_code == 200:
            return True, res.json() # Found breaches
        elif res.status_code == 404:
            return False, [] # Safe!
        elif res.status_code == 401 or res.status_code == 403:
            return None, "API_KEY_REQUIRED"
        else:
            return None, "ERROR"
    except Exception as e:
        return None, str(e)

# 4. Trigger Check
if st.button("🔍 Scan for Breaches", use_container_width=True):
    if not email:
        st.warning("Bhai, pehle email toh likho! 🤨")
    elif "@" not in email or "." not in email:
        st.error("Email address sahi format mein nahi hai.")
    else:
        with st.spinner(f"Checking data breaches for {email}..."):
            is_pwned, data = check_email_leak(email)
            
            if is_pwned is True:
                st.error(f"🚨 Oh No! This email has been PWNED/LEAKED!")
                st.write("### 📂 Found in the following breaches:")
                for breach in data:
                    st.markdown(f"- **{breach.get('Name', 'Unknown')}**: {breach.get('Domain', 'N/A')} (Date: {breach.get('BreachDate', 'N/A')})")
            elif is_pwned is False:
                st.success("🎉 Good news! No breaches found. Your email is SAFE!")
            elif data == "API_KEY_REQUIRED":
                # If HIBP key is missing, we can show a demo response or ask for key
                st.warning("⚠️ HIBP API requires an authorized API Key to run directly on the cloud.")
                st.info("Demo Mode: Your email format looks clean. Make sure to bind your `hibp-api-key` in the code headers!")
            else:
                st.error(f"Server connectivity issue: {data}")
