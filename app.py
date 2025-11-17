import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Simulación PID CI/CD", layout="wide")

# --- UI Sidebar ---
st.sidebar.title("Controlador PID y escenario")
Kp = st.sidebar.slider("Kp (Proporcional)", 0.0, 5.0, 1.0, 0.05)
Ki = st.sidebar.slider("Ki (Integral)", 0.0, 2.0, 0.2, 0.01)
Kd = st.sidebar.slider("Kd (Derivativo)", 0.0, 2.0, 0.1, 0.01)

st.sidebar.markdown("---")
setpoint = st.sidebar.slider("Referencia (setpoint)", 0.0, 2.0, 1.0, 0.05)
duration = st.sidebar.slider("Duración (pasos)", 100, 1000, 300, 50)
dt = st.sidebar.slider("Δt (s por paso)", 0.01, 0.2, 0.05, 0.01)

st.sidebar.markdown("---")
st.sidebar.subheader("Planta CI/CD")
tau = st.sidebar.slider("Constante de tiempo τ", 0.2, 3.0, 1.0, 0.05)   # rapidez de pipeline
gain = st.sidebar.slider("Ganancia de planta", 0.2, 2.0, 1.0, 0.05)        # sensibilidad del pipeline
delay_steps = st.sidebar.slider("Retardo (pasos)", 0, 20, 5, 1)             # latencia feedback/entrega
sat_u = st.sidebar.slider("Saturación de control |u|≤", 0.2, 5.0, 2.0, 0.1) # límites de actuación

st.sidebar.markdown("---")
st.sidebar.subheader("Perturbaciones")
noise_std = st.sidebar.slider("Ruido de medición σ", 0.0, 0.5, 0.05, 0.01)
pulse_amp = st.sidebar.slider("Pulso de perturbación (amplitud)", 0.0, 1.0, 0.5, 0.05)
pulse_start = st.sidebar.slider("Inicio del pulso", 10, 200, 50, 5)
pulse_len = st.sidebar.slider("Duración del pulso", 0, 200, 40, 5)

# --- Control Buttons ---
col_btn1, col_btn2, col_btn3 = st.columns(3)
start = col_btn1.button("▶ Iniciar / Continuar", use_container_width=True)
pause = col_btn2.button("⏸ Pausar", use_container_width=True)
reset = col_btn3.button("⟲ Reiniciar", use_container_width=True)

# --- Session state ---
if "running" not in st.session_state: st.session_state.running = False
if "k" not in st.session_state: st.session_state.k = 0
if "y" not in st.session_state: st.session_state.y = []
if "u" not in st.session_state: st.session_state.u = []
if "e" not in st.session_state: st.session_state.e = []
if "sp_hist" not in st.session_state: st.session_state.sp_hist = []
if "u_hist" not in st.session_state: st.session_state.u_hist = []
if "delay_buffer" not in st.session_state: st.session_state.delay_buffer = [0.0] * (delay_steps + 1)
if "int_acc" not in st.session_state: st.session_state.int_acc = 0.0
if "prev_e" not in st.session_state: st.session_state.prev_e = 0.0

# Handle buttons
if start:
    st.session_state.running = True
if pause:
    st.session_state.running = False
if reset:
    st.session_state.running = False
    st.session_state.k = 0
    st.session_state.y = []
    st.session_state.u = []
    st.session_state.e = []
    st.session_state.sp_hist = []
    st.session_state.u_hist = []
    st.session_state.delay_buffer = [0.0] * (delay_steps + 1)
    st.session_state.int_acc = 0.0
    st.session_state.prev_e = 0.0

# --- Helpers ---
def saturate(val, limit):
    if val > limit: return limit
    if val < -limit: return -limit
    return val

def plant_next(y, u_eff, disturbance, dt, tau, gain):
    # Planta de primer orden discreta: y[k+1] = y[k] + dt/tau * ( -y[k] + gain*u_eff ) + disturb
    return y + (dt / tau) * (-y + gain * u_eff) + disturbance

# --- Live charts placeholders ---
st.title("Simulación interactiva: CI/CD como lazo cerrado con PID")
left, middle, right = st.columns([1.2, 1.2, 1.2])
plot_error = left.empty()
plot_control = middle.empty()
plot_output = right.empty()

# --- Main simulation loop step-by-step ---
if st.session_state.k == 0 and len(st.session_state.y) == 0:
    # Initialize with zero output
    st.session_state.y.append(0.0)
    st.session_state.u.append(0.0)
    st.session_state.e.append(setpoint - st.session_state.y[-1])
    st.session_state.sp_hist.append(setpoint)

# Run step when playing
if st.session_state.running:
    # Measurement noise
    meas_noise = np.random.normal(0.0, noise_std)
    y_meas = st.session_state.y[-1] + meas_noise

    # Error
    e = setpoint - y_meas

    # Disturbance pulse
    in_pulse = (pulse_start <= st.session_state.k < pulse_start + pulse_len)
    disturbance = pulse_amp if in_pulse else 0.0

    # PID terms
    P = Kp * e
    st.session_state.int_acc += e * dt  # integral accum
    # Anti-windup: clamp integral
    st.session_state.int_acc = np.clip(st.session_state.int_acc, -10.0, 10.0)
    I = Ki * st.session_state.int_acc
    D = Kd * (e - st.session_state.prev_e) / dt

    u = P + I + D
    u = saturate(u, sat_u)

    # Delay line for actuation
    st.session_state.delay_buffer.append(u)
    u_eff = st.session_state.delay_buffer.pop(0)  # delayed control applied
    st.session_state.u_hist.append(u)

    # Plant update
    y_next = plant_next(st.session_state.y[-1], u_eff, disturbance, dt, tau, gain)
    st.session_state.y.append(float(y_next))
    st.session_state.u.append(float(u))
    st.session_state.e.append(float(e))
    st.session_state.sp_hist.append(setpoint)

    st.session_state.prev_e = e
    st.session_state.k += 1

    # Pace the loop
    time.sleep(dt)

# --- Build DataFrame for charts ---
k_axis = np.arange(len(st.session_state.y))
df = pd.DataFrame({
    "k": k_axis,
    "error": st.session_state.e,
    "control_u": st.session_state.u,
    "output_y": st.session_state.y,
    "setpoint": st.session_state.sp_hist,
})

# --- Plot: Error ---
fig_e = go.Figure()
fig_e.add_trace(go.Scatter(x=df["k"], y=df["error"], name="Error e[k]", mode="lines"))
fig_e.update_layout(title="Señal de error", xaxis_title="Paso k", yaxis_title="e[k]", height=300)
plot_error.plotly_chart(fig_e, use_container_width=True)

# --- Plot: Control ---
fig_u = go.Figure()
fig_u.add_trace(go.Scatter(x=df["k"], y=df["control_u"], name="Control u[k]", mode="lines"))
fig_u.update_layout(title="Señal de control", xaxis_title="Paso k", yaxis_title="u[k]", height=300)
plot_control.plotly_chart(fig_u, use_container_width=True)

# --- Plot: Output ---
fig_y = go.Figure()
fig_y.add_trace(go.Scatter(x=df["k"], y=df["output_y"], name="Salida y[k]", mode="lines"))
fig_y.add_trace(go.Scatter(x=df["k"], y=df["setpoint"], name="Referencia", mode="lines", line=dict(dash="dash")))
fig_y.update_layout(title="Salida del sistema vs referencia", xaxis_title="Paso k", yaxis_title="y[k]", height=300)
plot_output.plotly_chart(fig_y, use_container_width=True)

# --- Status ---
st.markdown("---")
st.markdown("Estado de simulación")
col_s1, col_s2, col_s3 = st.columns(3)
col_s1.metric("Paso k", st.session_state.k)
col_s2.metric("Último error e[k]", f"{st.session_state.e[-1]:.3f}")
col_s3.metric("Última salida y[k]", f"{st.session_state.y[-1]:.3f}")

st.caption("Ajustá Kp, Ki, Kd y los parámetros de planta/perturbación para explorar estabilidad, sobreimpulso y régimen permanente. Usá los botones para iniciar, pausar o reiniciar.")