"""
Dashboard Application
Real-time Weather Dashboard using Plotly Dash
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from db_connector import DatabaseConnector
from charts import (
    create_temperature_chart,
    create_humidity_chart,
    create_wind_speed_chart,
    create_comparison_chart,
    create_gauge_chart
)
from configs.settings import Settings

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.title = "Weather Real-time Dashboard"

# Initialize database connector
db = DatabaseConnector()

# Get available cities
try:
    CITIES = db.get_all_cities()
    if not CITIES:
        CITIES = Settings.get_cities()
except:
    CITIES = Settings.get_cities()


# Layout
def create_layout():
    """Create dashboard layout"""
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("🌤️ Weather Real-time Dashboard", 
                       className="text-center text-primary mb-4 mt-4"),
                html.P("Real-time weather monitoring across multiple cities",
                      className="text-center text-muted")
            ])
        ]),
        
        html.Hr(),
        
        # Controls
        dbc.Row([
            dbc.Col([
                html.Label("Select City:", className="fw-bold"),
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[{'label': city, 'value': city} for city in CITIES],
                    value=CITIES[0] if CITIES else None,
                    clearable=False,
                    className="mb-3"
                )
            ], md=4),
            
            dbc.Col([
                html.Label("Time Range (hours):", className="fw-bold"),
                dcc.Dropdown(
                    id='time-range',
                    options=[
                        {'label': 'Last 1 Hour', 'value': 1},
                        {'label': 'Last 3 Hours', 'value': 3},
                        {'label': 'Last 6 Hours', 'value': 6},
                        {'label': 'Last 12 Hours', 'value': 12},
                        {'label': 'Last 24 Hours', 'value': 24},
                    ],
                    value=6,
                    clearable=False,
                    className="mb-3"
                )
            ], md=4),
            
            dbc.Col([
                html.Label("Auto Refresh:", className="fw-bold"),
                dcc.Interval(
                    id='interval-component',
                    interval=30*1000,  # 30 seconds
                    n_intervals=0
                ),
                html.Div(id='last-update', className="text-muted")
            ], md=4)
        ]),
        
        html.Hr(),
        
        # Statistics Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Avg Temperature", className="card-title"),
                        html.H2(id='avg-temp', className="text-danger"),
                        html.P("°C", className="text-muted")
                    ])
                ], className="mb-3 shadow-sm")
            ], md=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Max Temperature", className="card-title"),
                        html.H2(id='max-temp', className="text-warning"),
                        html.P("°C", className="text-muted")
                    ])
                ], className="mb-3 shadow-sm")
            ], md=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Avg Humidity", className="card-title"),
                        html.H2(id='avg-humidity', className="text-info"),
                        html.P("%", className="text-muted")
                    ])
                ], className="mb-3 shadow-sm")
            ], md=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Avg Wind Speed", className="card-title"),
                        html.H2(id='avg-wind', className="text-success"),
                        html.P("m/s", className="text-muted")
                    ])
                ], className="mb-3 shadow-sm")
            ], md=3),
        ]),
        
        # Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='temperature-chart')
                    ])
                ], className="mb-3 shadow")
            ], md=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='humidity-chart')
                    ])
                ], className="mb-3 shadow")
            ], md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='wind-chart')
                    ])
                ], className="mb-3 shadow")
            ], md=6)
        ]),
        
        # City Comparison
        dbc.Row([
            dbc.Col([
                html.H3("City Comparison", className="mt-3 mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='comparison-chart')
                    ])
                ], className="shadow")
            ])
        ]),
        
        # Footer
        html.Hr(),
        html.Footer([
            html.P("Weather Real-time Data Engineering Pipeline | Powered by Kafka + Spark + MySQL",
                  className="text-center text-muted")
        ], className="mt-4 mb-4")
        
    ], fluid=True)


app.layout = create_layout()


# Callbacks
@app.callback(
    [
        Output('avg-temp', 'children'),
        Output('max-temp', 'children'),
        Output('avg-humidity', 'children'),
        Output('avg-wind', 'children'),
        Output('temperature-chart', 'figure'),
        Output('humidity-chart', 'figure'),
        Output('wind-chart', 'figure'),
        Output('comparison-chart', 'figure'),
        Output('last-update', 'children')
    ],
    [
        Input('interval-component', 'n_intervals'),
        Input('city-dropdown', 'value'),
        Input('time-range', 'value')
    ]
)
def update_dashboard(n_intervals, selected_city, time_range):
    """Update all dashboard components"""
    
    if not selected_city:
        return ["--"] * 4 + [{}] * 4 + ["No data"]
    
    try:
        # Get data
        weather_data = db.get_weather_by_city(selected_city, hours=time_range)
        stats = db.get_weather_statistics(selected_city, hours=time_range)
        comparison_data = db.get_comparison_data(CITIES)
        
        # Statistics
        avg_temp = f"{stats.get('avg_temp', 0):.1f}" if stats else "--"
        max_temp = f"{stats.get('max_temp', 0):.1f}" if stats else "--"
        avg_humidity = f"{stats.get('avg_humidity', 0):.0f}" if stats else "--"
        avg_wind = f"{stats.get('avg_wind_speed', 0):.1f}" if stats else "--"
        
        # Charts
        temp_chart = create_temperature_chart(weather_data, selected_city)
        humidity_chart = create_humidity_chart(weather_data, selected_city)
        wind_chart = create_wind_speed_chart(weather_data, selected_city)
        comparison_chart = create_comparison_chart(comparison_data)
        
        # Last update time
        last_update = f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return [
            avg_temp, max_temp, avg_humidity, avg_wind,
            temp_chart, humidity_chart, wind_chart, comparison_chart,
            last_update
        ]
        
    except Exception as e:
        print(f"Error updating dashboard: {str(e)}")
        return ["Error"] * 4 + [{}] * 4 + [f"Error: {str(e)}"]


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Weather Dashboard")
    print("=" * 70)
    print(f"Dashboard URL: http://{Settings.DASHBOARD_HOST}:{Settings.DASHBOARD_PORT}")
    print(f"Monitoring cities: {', '.join(CITIES)}")
    print("=" * 70)
    
    app.run_server(
        host=Settings.DASHBOARD_HOST,
        port=Settings.DASHBOARD_PORT,
        debug=Settings.DASHBOARD_DEBUG
    )
