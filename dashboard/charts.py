"""
Charts Module
Tạo các charts và visualizations cho dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import List, Dict
import pandas as pd


def create_temperature_chart(data: List[Dict], city: str) -> go.Figure:
    """
    Tạo line chart cho nhiệt độ theo thời gian
    
    Args:
        data: List weather data dictionaries
        city: Tên thành phố
    
    Returns:
        Plotly Figure
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    # Temperature line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['temperature'],
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{y:.1f}°C</b><br>%{x}<extra></extra>'
    ))
    
    # Feels like line
    if 'feels_like' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['feels_like'],
            mode='lines',
            name='Feels Like',
            line=dict(color='#FFB347', width=2, dash='dash'),
            hovertemplate='<b>%{y:.1f}°C</b><br>%{x}<extra></extra>'
        ))
    
    fig.update_layout(
        title=f'Temperature Trend - {city}',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        font=dict(family='Arial', size=12)
    )
    
    return fig


def create_humidity_chart(data: List[Dict], city: str) -> go.Figure:
    """
    Tạo chart cho độ ẩm
    
    Args:
        data: List weather data dictionaries
        city: Tên thành phố
    
    Returns:
        Plotly Figure
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['humidity'],
        mode='lines+markers',
        name='Humidity',
        fill='tozeroy',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{y}%</b><br>%{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'Humidity Trend - {city}',
        xaxis_title='Time',
        yaxis_title='Humidity (%)',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        yaxis=dict(range=[0, 100])
    )
    
    return fig


def create_wind_speed_chart(data: List[Dict], city: str) -> go.Figure:
    """
    Tạo chart cho tốc độ gió
    
    Args:
        data: List weather data dictionaries
        city: Tên thành phố
    
    Returns:
        Plotly Figure
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['timestamp'],
        y=df['wind_speed'],
        name='Wind Speed',
        marker_color='#95E1D3',
        hovertemplate='<b>%{y:.1f} m/s</b><br>%{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'Wind Speed - {city}',
        xaxis_title='Time',
        yaxis_title='Wind Speed (m/s)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_multi_metric_chart(data: List[Dict], city: str) -> go.Figure:
    """
    Tạo chart kết hợp nhiều metrics
    
    Args:
        data: List weather data dictionaries
        city: Tên thành phố
    
    Returns:
        Plotly Figure với subplots
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Temperature', 'Humidity', 'Wind Speed', 'Pressure'),
        specs=[[{'secondary_y': False}, {'secondary_y': False}],
               [{'secondary_y': False}, {'secondary_y': False}]]
    )
    
    # Temperature
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['temperature'],
                   mode='lines', name='Temp', line=dict(color='#FF6B6B')),
        row=1, col=1
    )
    
    # Humidity
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['humidity'],
                   mode='lines', name='Humidity', line=dict(color='#4ECDC4')),
        row=1, col=2
    )
    
    # Wind Speed
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['wind_speed'],
                   mode='lines', name='Wind', line=dict(color='#95E1D3')),
        row=2, col=1
    )
    
    # Pressure
    if 'pressure' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['pressure'],
                       mode='lines', name='Pressure', line=dict(color='#FFB347')),
            row=2, col=2
        )
    
    fig.update_layout(
        title_text=f'Weather Metrics - {city}',
        showlegend=False,
        height=600,
        template='plotly_white'
    )
    
    return fig


def create_comparison_chart(data: List[Dict]) -> go.Figure:
    """
    Tạo chart so sánh giữa các cities
    
    Args:
        data: List comparison data dictionaries
    
    Returns:
        Plotly Figure
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['city'],
        y=df['avg_temp'],
        name='Avg Temperature',
        marker_color='#FF6B6B',
        text=df['avg_temp'].round(1),
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Temperature Comparison Across Cities',
        xaxis_title='City',
        yaxis_title='Average Temperature (°C)',
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig


def create_gauge_chart(value: float, title: str, range_max: float = 50) -> go.Figure:
    """
    Tạo gauge chart cho single metric
    
    Args:
        value: Giá trị hiện tại
        title: Tiêu đề
        range_max: Giá trị max của gauge
    
    Returns:
        Plotly Figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        delta={'reference': value * 0.9},
        gauge={
            'axis': {'range': [None, range_max], 'tickwidth': 1},
            'bar': {'color': "#FF6B6B"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, range_max * 0.5], 'color': '#E8F8F5'},
                {'range': [range_max * 0.5, range_max * 0.75], 'color': '#D5F4E6'},
                {'range': [range_max * 0.75, range_max], 'color': '#FADBD8'}
            ],
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


def create_weather_heatmap(data: pd.DataFrame) -> go.Figure:
    """
    Tạo heatmap cho weather data
    
    Args:
        data: DataFrame với weather data
    
    Returns:
        Plotly Figure
    """
    if data.empty:
        return go.Figure()
    
    # Pivot data for heatmap
    pivot_data = data.pivot_table(
        index='city',
        values='temperature',
        aggfunc='mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=[pivot_data.values],
        x=pivot_data.index,
        y=['Temperature'],
        colorscale='RdYlBu_r',
        text=[pivot_data.values],
        texttemplate='%{text:.1f}°C',
        textfont={"size": 12}
    ))
    
    fig.update_layout(
        title='Temperature Heatmap by City',
        height=200,
        template='plotly_white'
    )
    
    return fig
