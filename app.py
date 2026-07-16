import streamlit as st
import time
from modules.breach_check import BreachChecker
from modules.ip_reputation import IPReputation
from modules.url_safety import URLSafetyScanner

# 1. Page Config - Dark Cyber Theme Default
st.set_page_config(
    page_title="CyberIntel Sentinel Dashboard",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Extreme CSS Injection (Pure Neon Style, High-Performance Layouts)
st.markdown("""
    <style>
        /* Base Styling */
        .stApp {
            background-color: #030712;
            color: #e5e7eb;
            font-family: 'Courier New', Courier, monospace;
        }

        /* Continuous High-Performance Animations */
        @keyframes scan-glow {
            0% { box-shadow: 0 0 10px rgba(57, 255, 20, 0.2); border-color: #1f2937; }
            50% { box-shadow: 0 0 25px rgba(57, 255, 20, 0.6); border-color: #39ff14; }
            100% { box-shadow: 0 0 10px rgba(57, 255, 20, 0.2); border-color: #1f2937; }
        }

        @keyframes cyber-shimmer {
            0% { text-shadow: 0 0 5px rgba(56, 189, 248, 0.5); }
            50% { text-shadow: 0 0 20px rgba(56, 189, 248, 0.9); }
            100% { text-shadow: 0 0 5px rgba(56, 189, 248, 0.5); }
        }

        @keyframes text-blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* Banner Container Custom Neon Theme */
        .neon-banner {
            background: radial-gradient(circle, #090d1a 0%, #030712 100%);
            border: 2px solid #1f6feb;
            border-radius: 12px;
            padding: 35px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 0 20px rgba(31, 111, 235, 0.3);
            position: relative;
            overflow: hidden;
        }

        .neon-title {
            color: #38bdf8;
            font-size: 3.2rem;
            font-weight: 900;
            letter-spacing: 5px;
            margin: 0;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.8);
            animation: cyber-shimmer 3s infinite ease-in-out;
        }

        .neon-subtitle {
            color: #8b949e;
            font-size: 1.15rem;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        /* Responsive Dashboard Cards */
        .cyber-card {
            background-color: #0b0f19;
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 24px;
            margin-top: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .cyber-card:hover {
            border-color: #38bdf8;
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(56, 189, 248, 0.2);
        }

        /* Custom Status and Interactive Dots */
        .sys-online {
            color: #39ff14;
            font-weight: bold;
            animation: text-blink 1.5s infinite;
        }

        /* Custom Styling for Tabs */
        div[data-testid="stTabBar"] {
            background-color: #0b0f19;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #1f2937;
        }

        div[data-testid="stTabBar"] button {
            color: #8b949e !important;
            font-weight: bold !important;
            font-size: 1.1rem !important;
            border-radius: 6px !important;
            border: 1px solid transparent !important;
            transition: all 0.2s ease;
        }

        div[data-testid="stTabBar"] button[aria-selected="true"] {
            color: #38bdf8 !important;
            background-color: #111827 !important;
            border: 1px solid #38bdf8 !important;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        }

        /* Custom Big Action Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #1f6feb 0%, #38bdf8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            padding: 15px 35px !important;
            font-size: 1.2rem !important;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4) !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }

        div.stButton > button:first-child:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 30px rgba(56, 189, 248, 0.7) !important;
        }

        /* Global Footer design */
        .neon-footer {
            text-align: center;
            padding: 25px;
            margin-top: 50px;
            border-top: 1px solid #1f2937;
            color: #6e7681;
            font-size: 0.95rem;
        }
        .neon-footer strong {
            color: #39ff14;
            text-shadow: 0 0 8px rgba(57, 255, 20, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

# 3. Main Header Banner
st.markdown("""
    <div class="neon-banner">
        <div class="neon-title">👁️ CYBERINTEL SENTINEL</div>
        <div class="neon-subtitle">Autonomous Threat Reconnaissance & Dark Web Intelligence Hub</div>
    </div>
""", unsafe_allow_html=True)

# 4. Sidebar: Telemetry & Status
st.sidebar.markdown("### 🖥️ SENTINEL STATUS")
st.sidebar.markdown("""
    <div style='background-color: #0b0f19; padding: 20px; border-radius: 12px; border: 1px solid #1f6feb; box-shadow: 0 0 15px rgba(31, 111, 235, 0.2);'>
        <strong style='color: #8b949e;'>Engine Core:</strong> <span class="sys-online">ACTIVE [●]</span><br>
        <strong style='color: #8b949e;'>Response Latency:</strong> 4ms (Fast Cache)<br>
        <strong style='color: #8b949e;'>Data Stream:</strong> TLS 1.3 Decrypted<br>
        <strong style='color: #8b949e;'>Global Node State:</strong> <span style='color: #38bdf8; font-weight:bold;'>Optimal</span>
    </div>
""", unsafe_allow_html=True)

# Developer Profile Sidebar Widget
st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #111827 0%, #030712 100%); padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-top: 30px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);'>
        <span style='color: #8b949e; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px;'>SYSTEM ARCHITECT</span><br>
        <strong style='color: #39ff14; font-size: 1.15rem; text-shadow: 0 0 8px rgba(57,255,20,0.5);'>Hannan Ashraf</strong><br>
        <span style='color: #38bdf8; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;'>Junior Cyber Security Specialist</span>
    </div>
""", unsafe_allow_html=True)

# 5. Core Application Tabs
tab1, tab2, tab3 = st.tabs([
    "🕵️‍♂️ Breach Radar",
    "🌐 IP Reputation Hub",
    "🛡️ Domain Integrity Analyzer"
])

# ----------------- TAB 1: BREACH RADAR -----------------
with tab1:
    st.markdown("### 🔍 Live Identity Leak Verification")
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        email_input = st.text_input("Enter Identity Vector (Email)", placeholder="target@domain.com", key="radar_email")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_r:
        st.image("https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcR07fJ6S7y38eW66T8u-V3T3zLqg8l1Y6r7wXp7bS89G2L7v9y-X6v1D2g-S8v7", caption="Global Cyber Recon Network", use_container_width=True)

    if st.button("RUN DEEP IDENTITY SEARCH", key="btn_breach"):
        if email_input:
            with st.spinner("Decryption sequences processing in CPU cache..."):
                time.sleep(0.3)  # Fast execution feel
                res = BreachChecker.check_email(email_input)
                
                if res["status"] == "success":
                    if res["compromised"]:
                        st.error(f"🚨 TARGET IDENTITY COMPROMISED - Status: {res['severity']}")
                        st.markdown(f"**Identified Leaks ({res['leaks_found']}):**")
                        for leak in res["breaches"]:
                            st.markdown(f"- ⚠️ *{leak}*")
                        st.warning(f"💡 **Mitigation Recommendation:** {res['suggestion']}")
                    else:
                        st.balloons()
                        st.success("🎉 IDENTITY INTEGRITY SHIELDED!")
                        st.info(f"💡 **Sentinel Tip:** {res['suggestion']}")
                else:
                    st.error(res["message"])
        else:
            st.warning("⚠️ Put an email first to begin trace.")

# ----------------- TAB 2: IP REPUTATION HUB -----------------
with tab2:
    st.markdown("### 📡 Host IP Reputation Scan")
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        ip_input = st.text_input("Enter Suspicious Target IPv4 Address", placeholder="e.g., 185.220.101.5", key="reputation_ip")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_r:
        st.image("https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcR7fS9s2Yt8vP7mK-V4zT3l7g7fXp6l6v7w8Qp9bS77L1v2y-X5v0D1g-S7v8", caption="Telemetry Host Diagnostics Map", use_container_width=True)

    if st.button("DECODE IP THREAT PROFILE", key="btn_reputation"):
        if ip_input:
            with st.spinner("Resolving IP trace matrices..."):
                time.sleep(0.3)
                res = IPReputation.query_ip(ip_input)
                
                if res["status"] == "success":
                    risk_lvl = res["risk"]
                    if "HIGH" in risk_lvl:
                        st.error(f"🚨 Threat Alert: {risk_lvl}")
                    elif "MEDIUM" in risk_lvl:
                        st.warning(f"⚠️ Warning Status: {risk_lvl}")
                    else:
                        st.success(f"🛡️ Safe Node Protocol: {risk_lvl}")
                        
                    st.markdown(f"""
                        <div style='background: #090d1a; padding: 20px; border-radius: 10px; border: 1px solid #1f2937;'>
                            <strong>🔥 Telemetry Abuse Score:</strong> {res['score']}% <br>
                            <strong>💡 Mapped Category:</strong> {res['category']} <br>
                            <strong>🏢 Network Provider (ISP):</strong> {res['isp']} <br>
                            <strong>🌍 Geo Registry:</strong> {res['country']}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(res["message"])
        else:
            st.warning("⚠️ Target IP input stream is unassigned.")

# ----------------- TAB 3: DOMAIN INTEGRITY ANALYZER -----------------
with tab3:
    st.markdown("### 🔗 Domain Fraud & Phishing Vector Isolation")
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        url_input = st.text_input("Enter Target Domain / URL", placeholder="e.g., login-security-paypal.update-info.com", key="safety_url")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_r:
        st.image("https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcT7fS9v3Yt8vP6mK-V4zT3l7g7fXp6l6v7w8Qp9bS77L1v2y-X5v0D1g-S7v9", caption="Target URL Deconstruction Network", use_container_width=True)

    if st.button("EXECUTE ENVELOPE DECONSTRUCTION", key="btn_url"):
        if url_input:
            with st.spinner("Analyzing hostname structures and domain anomalies..."):
                time.sleep(0.3)
                res = URLSafetyScanner.analyze_url(url_input)
                
                if res["status"] == "success":
                    if not res["safe"]:
                        st.error(f"🚨 DECEPTIVE VECTOR ENCOUNTERED: {res['verdict']}")
                    else:
                        st.success(f"🛡️ Security Clear: {res['verdict']}")
                        
                    st.markdown(f"**Host Analyzed:** `{res['domain']}`")
                    st.markdown(f"**Anomaly Threat Meter:** `{res['risk_score']}/100`")
                    
                    st.markdown("**Structural Analysis Metrics:**")
                    for reason in res["reasons"]:
                        st.markdown(f"- 🔬 *{reason}*")
                    st.info(f"🚨 **Urgent Action Plan:** {res['action_required']}")
                else:
                    st.error(res["message"])
        else:
            st.warning("⚠️ URL source stream is empty.")

# 6. Global Fixed Footer (Clean & Professional Branding)
st.markdown("""
    <div class="neon-footer">
        ⚡ CyberIntel Sentinel Hub | Made  by <strong>Hannan Ashraf</strong> (Junior Cyber Security Student)
    </div>
""", unsafe_allow_html=True)