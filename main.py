import streamlit as st
import socket
import threading
from queue import Queue

# 1. Page Configuration (Stylish UI)
st.set_page_config(
    page_title="CyberToolkit Enterprise",
    page_icon="🛡️",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #00FFCC;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #888888;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ CyberToolkit Enterprise</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Next-Gen Port Scanner & Network Utility</div>', unsafe_allow_html=True)

# 2. Input Fields
target_ip = st.text_input("🎯 Target Host / IP Address", placeholder="e.g., 127.0.0.1 or scanme.nmap.org")

col1, col2 = st.columns(2)
with col1:
    start_port = st.number_input("⚡ Start Port", min_value=1, max_value=65535, value=1)
with col2:
    end_port = st.number_input("🛑 End Port", min_value=1, max_value=65535, value=100)

# 3. Port Scanning Logic (Fast Threaded Scanner)
def scan_port(ip, port, queue):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((ip, port))
        if result == 0:
            queue.put(port)
        sock.close()
    except Exception:
        pass

def start_scan(ip, s_port, e_port):
    queue = Queue()
    threads = []
    
    for port in range(s_port, e_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, queue))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
        
    open_ports = []
    while not queue.empty():
        open_ports.append(queue.get())
    return sorted(open_ports)

# 4. Trigger Scan
if st.button("🚀 Start Scanning Target", use_container_width=True):
    if not target_ip:
        st.error("Bhai, pehle Target IP ya Hostname toh enter karo! 😅")
    else:
        with st.spinner(f"Scanning {target_ip} from port {start_port} to {end_port}..."):
            try:
                # Resolve domain to IP if needed
                resolved_ip = socket.gethostbyname(target_ip)
                st.info(f"Scanning IP: {resolved_ip}")
                
                results = start_scan(resolved_ip, start_port, end_port)
                
                st.success("Scan Completed!")
                if results:
                    st.write("### 🟢 Open Ports Found:")
                    for p in results:
                        st.markdown(f"- **Port {p}**: OPEN")
                else:
                    st.warning("Koi open port nahi mila is range mein.")
            except socket.gaierror:
                st.error("Invalid Hostname/IP! Connection fail ho gayi.")
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
