# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="포트폴리오 최적화 시뮬레이터", layout="wide")

st.title("📊 투자 자산 포트폴리오 최적화 시뮬레이터")
st.markdown("현대 포트폴리오 이론(MPT) 기반의 자산 배분 시뮬레이터입니다.")

st.sidebar.header("⚙️ 자산별 매개변수 설정")

st.sidebar.subheader("Asset A (주식)")
ret_a = st.sidebar.slider("Asset A 기대수익률 (%)", 0.0, 30.0, 12.0, 0.5) / 100
vol_a = st.sidebar.slider("Asset A 위험 (%)", 0.0, 50.0, 20.0, 0.5) / 100

st.sidebar.subheader("Asset B (채권)")
ret_b = st.sidebar.slider("Asset B 기대수익률 (%)", 0.0, 30.0, 6.0, 0.5) / 100
vol_b = st.sidebar.slider("Asset B 위험 (%)", 0.0, 50.0, 8.0, 0.5) / 100

st.sidebar.subheader("Asset C (현금)")
ret_c = st.sidebar.slider("Asset C 기대수익률 (%)", 0.0, 30.0, 4.0, 0.5) / 100
vol_c = st.sidebar.slider("Asset C 위험 (%)", 0.0, 50.0, 3.0, 0.5) / 100

np.random.seed(42)
num_portfolios = 500
results = np.zeros((3, num_portfolios))
weights_record = []

for i in range(num_portfolios):
    weights = np.random.random(3)
    weights /= np.sum(weights)
    weights_record.append(weights)
    
    p_ret = weights[0]*ret_a + weights[1]*ret_b + weights[2]*ret_c
    p_vol = np.sqrt((weights[0]*vol_a)**2 + (weights[1]*vol_b)**2 + (weights[2]*vol_c)**2)
    
    results[0,i] = p_ret
    results[1,i] = p_vol
    results[2,i] = (p_ret - 0.02) / p_vol if p_vol > 0 else 0

df_portfolios = pd.DataFrame({
    'Return': results[0] * 100,
    'Risk': results[1] * 100,
    'Sharpe': results[2],
    'Weights': weights_record
})

max_sharpe_idx = df_portfolios['Sharpe'].idxmax()
min_vol_idx = df_portfolios['Risk'].idxmin()
max_sharpe = df_portfolios.iloc[max_sharpe_idx]
min_vol = df_portfolios.iloc[min_vol_idx]

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 효율적 투자선 시각화")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_portfolios['Risk'], y=df_portfolios['Return'],
        mode='markers',
        marker=dict(size=5, color=df_portfolios['Sharpe'], colorscale='Viridis', showscale=True),
        text=[f"A:{w[0]:.1%}, B:{w[1]:.1%}, C:{w[2]:.1%}" for w in df_portfolios['Weights']],
        name='포트폴리오 조합'
    ))
    fig.add_trace(go.Scatter(
        x=[max_sharpe['Risk']], y=[max_sharpe['Return']],
        mode='markers', marker=dict(color='red', size=12, symbol='star'),
        name='최대 샤프지수'
    ))
    fig.add_trace(go.Scatter(
        x=[min_vol['Risk']], y=[min_vol['Return']],
        mode='markers', marker=dict(color='orange', size=12, symbol='diamond'),
        name='최소 분산'
    ))
    fig.update_layout(xaxis_title="위험 (%)", yaxis_title="기대수익률 (%)", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 최적 결과")
    st.markdown("### 🔥 최대 샤프지수")
    st.metric("수익률", f"{max_sharpe['Return']:.2f}%")
    st.metric("위험도", f"{max_sharpe['Risk']:.2f}%")
    
    st.markdown("---")
    st.markdown("### 🛡️ 최소 분산")
    st.metric("수익률", f"{min_vol['Return']:.2f}%")
    st.metric("위험도", f"{min_vol['Risk']:.2f}%")
