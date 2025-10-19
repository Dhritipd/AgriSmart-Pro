"""
Visualization utilities for creating charts with dark theme
COMPLETE UPDATED VERSION WITH FONT SIZE CUSTOMIZATION
"""
import plotly.graph_objects as go
import plotly.express as px
from config.settings import QUALITY_COLORS

# Dark theme configuration with font size customization
CHART_THEME = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(30, 41, 59, 0.3)',
    'font': dict(color='white', size=12, family='Arial, sans-serif'),
    'gridcolor': 'rgba(148, 163, 184, 0.2)',
    'linecolor': 'rgba(148, 163, 184, 0.3)',
}

def create_radar_chart(factors, font_size=12):
    """Create radar chart for factor analysis with dark theme"""
    categories = [f['name'] for f in factors]
    values = [f['score'] for f in factors]
    
    # Create updated theme with custom font size
    custom_theme = CHART_THEME.copy()
    custom_theme['font']['size'] = font_size
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Factor Scores',
        fillcolor='rgba(16, 185, 129, 0.3)',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8, color='#10b981')
    ))
    
    fig.update_layout(
        paper_bgcolor=custom_theme['paper_bgcolor'],
        plot_bgcolor='rgba(0,0,0,0)',
        font=custom_theme['font'],
        polar=dict(
            bgcolor='rgba(30, 41, 59, 0.5)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showline=True,
                linewidth=2,
                gridcolor=custom_theme['gridcolor'],
                color='white',
                tickfont=dict(size=font_size-2)
            ),
            angularaxis=dict(
                showline=True,
                linewidth=2,
                gridcolor=custom_theme['gridcolor'],
                color='white',
                tickfont=dict(size=font_size-2)
            )
        ),
        showlegend=False,
        title=dict(
            text="Factor Analysis Radar Chart",
            font=dict(color='#10b981', size=font_size+4, family='Arial, sans-serif')
        ),
        height=400
    )
    
    return fig


def create_comparison_chart(comparison_results, font_size=12):
    """Create bar chart for multi-crop comparison with dark theme"""
    crops = [r['crop'].title() for r in comparison_results]
    scores = [r['score'] for r in comparison_results]
    colors = [QUALITY_COLORS.get(r['quality'], '#888888') for r in comparison_results]
    
    # Create updated theme with custom font size
    custom_theme = CHART_THEME.copy()
    custom_theme['font']['size'] = font_size
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=crops,
        y=scores,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255, 255, 255, 0.2)', width=2)
        ),
        text=[f"{s:.1f}%" for s in scores],
        textposition='outside',
        textfont=dict(color='white', size=font_size),
        hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor=custom_theme['paper_bgcolor'],
        plot_bgcolor=custom_theme['plot_bgcolor'],
        font=custom_theme['font'],
        title=dict(
            text="Crop Quality Comparison",
            font=dict(color='#10b981', size=font_size+4)
        ),
        xaxis=dict(
            title="Crop Type",
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        yaxis=dict(
            title="Quality Score (%)",
            range=[0, 110],
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        height=400,
        showlegend=False
    )
    
    return fig


def create_yield_comparison_chart(comparison_results, font_size=12):
    """Create grouped bar chart for yield comparison with dark theme"""
    crops = [r['crop'].title() for r in comparison_results]
    scores = [r['score'] for r in comparison_results]
    yields = [float(r['yield']) for r in comparison_results]
    
    # Create updated theme with custom font size
    custom_theme = CHART_THEME.copy()
    custom_theme['font']['size'] = font_size
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Quality Score',
        x=crops,
        y=scores,
        marker=dict(
            color='#10b981',
            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
        ),
        yaxis='y'
    ))
    
    fig.add_trace(go.Bar(
        name='Yield (t/ha)',
        x=crops,
        y=yields,
        marker=dict(
            color='#3b82f6',
            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
        ),
        yaxis='y2'
    ))
    
    fig.update_layout(
        paper_bgcolor=custom_theme['paper_bgcolor'],
        plot_bgcolor=custom_theme['plot_bgcolor'],
        font=custom_theme['font'],
        title=dict(
            text="Quality Score vs Yield Comparison",
            font=dict(color='#10b981', size=font_size+4)
        ),
        xaxis=dict(
            title="Crop Type",
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        yaxis=dict(
            title="Quality Score (%)",
            side='left',
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        yaxis2=dict(
            title="Yield (tonnes/ha)",
            side='right',
            overlaying='y',
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        barmode='group',
        height=400,
        legend=dict(
            font=dict(color='white', size=font_size-1),
            bgcolor='rgba(30, 41, 59, 0.5)',
            bordercolor='rgba(148, 163, 184, 0.3)',
            borderwidth=1
        )
    )
    
    return fig


def create_history_trend_chart(history_data, font_size=12):
    """Create line chart for historical trends with dark theme"""
    if not history_data:
        return None
    
    history_data = list(reversed(history_data))[-20:]
    timestamps = [record['timestamp'] for record in history_data]
    scores = [record['score'] for record in history_data]
    
    # Create updated theme with custom font size
    custom_theme = CHART_THEME.copy()
    custom_theme['font']['size'] = font_size
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(timestamps))),
        y=scores,
        mode='lines+markers',
        name='Quality Score',
        line=dict(color='#10b981', width=3),
        marker=dict(size=10, color='#10b981', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.2)',
        hovertemplate='<b>Record %{x}</b><br>Score: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor=custom_theme['paper_bgcolor'],
        plot_bgcolor=custom_theme['plot_bgcolor'],
        font=custom_theme['font'],
        title=dict(
            text="Quality Score Trend Over Time",
            font=dict(color='#10b981', size=font_size+4)
        ),
        xaxis=dict(
            title="Prediction Number",
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        yaxis=dict(
            title="Quality Score (%)",
            range=[0, 110],
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        height=300,
        showlegend=False
    )
    
    return fig


def create_cost_breakdown_pie(cost_data, font_size=12):
    """Create pie chart for cost breakdown with dark theme"""
    labels = ['Seeds', 'Fertilizer', 'Labor', 'Irrigation']
    values = [
        cost_data['seed'],
        cost_data['fertilizer'],
        cost_data['labor'],
        cost_data['irrigation']
    ]
    
    colors = ['#10b981', '#3b82f6', '#f59e0b', '#06b6d4']
    
    # Create updated theme with custom font size
    custom_theme = CHART_THEME.copy()
    custom_theme['font']['size'] = font_size
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(
            colors=colors,
            line=dict(color='rgba(30, 41, 59, 1)', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(color='white', size=font_size),
        hovertemplate='<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        paper_bgcolor=custom_theme['paper_bgcolor'],
        plot_bgcolor='rgba(0,0,0,0)',
        font=custom_theme['font'],
        title=dict(
            text="Cost Breakdown",
            font=dict(color='#10b981', size=font_size+4)
        ),
        height=400,
        showlegend=True,
        legend=dict(
            font=dict(color='white', size=font_size-1),
            bgcolor='rgba(30, 41, 59, 0.5)',
            bordercolor='rgba(148, 163, 184, 0.3)',
            borderwidth=1
        )
    )
    
    return fig


def create_npk_comparison_chart(fertilizer_data, font_size=12):
    """Create grouped bar chart for NPK comparison with dark theme"""
    nutrients = ['Nitrogen', 'Phosphorus', 'Potassium']
    
    current = [
        fertilizer_data['current']['N'],
        fertilizer_data['current']['P'],
        fertilizer_data['current']['K']
    ]
    
    required = [
        fertilizer_data['required']['N'],
        fertilizer_data['required']['P'],
        fertilizer_data['required']['K']
    ]
    
    deficit = [
        fertilizer_data['deficit']['N'],
        fertilizer_data['deficit']['P'],
        fertilizer_data['deficit']['K']
    ]
    
    # Create updated theme with custom font size
    custom_theme = CHART_THEME.copy()
    custom_theme['font']['size'] = font_size
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current',
        x=nutrients,
        y=current,
        marker=dict(
            color='#3b82f6',
            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
        ),
        hovertemplate='<b>Current</b><br>%{x}: %{y} kg/ha<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Required',
        x=nutrients,
        y=required,
        marker=dict(
            color='#10b981',
            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
        ),
        hovertemplate='<b>Required</b><br>%{x}: %{y} kg/ha<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Deficit',
        x=nutrients,
        y=deficit,
        marker=dict(
            color='#ef4444',
            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
        ),
        hovertemplate='<b>Deficit</b><br>%{x}: %{y} kg/ha<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor=custom_theme['paper_bgcolor'],
        plot_bgcolor=custom_theme['plot_bgcolor'],
        font=custom_theme['font'],
        title=dict(
            text="NPK Status - Current vs Required",
            font=dict(color='#10b981', size=font_size+4)
        ),
        xaxis=dict(
            title="Nutrient",
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        yaxis=dict(
            title="Amount (kg/ha)",
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        barmode='group',
        height=400,
        legend=dict(
            font=dict(color='white', size=font_size-1),
            bgcolor='rgba(30, 41, 59, 0.5)',
            bordercolor='rgba(148, 163, 184, 0.3)',
            borderwidth=1
        )
    )
    
    return fig


def create_weather_forecast_chart(forecast_data, font_size=12):
    """Create area chart for weather forecast with dark theme"""
    if not forecast_data:
        return None
    
    days = [f['day'] for f in forecast_data]
    temps = [f['temp'] for f in forecast_data]
    rain = [f['rain'] for f in forecast_data]
    
    # Create updated theme with custom font size
    custom_theme = CHART_THEME.copy()
    custom_theme['font']['size'] = font_size
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=temps,
        mode='lines+markers',
        name='Temperature (°C)',
        line=dict(color='#f59e0b', width=3),
        marker=dict(size=10, color='#f59e0b', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(245, 158, 11, 0.2)',
        hovertemplate='<b>%{x}</b><br>Temperature: %{y}°C<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=days,
        y=rain,
        name='Rainfall (mm)',
        marker=dict(
            color='#3b82f6',
            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
        ),
        yaxis='y2',
        opacity=0.7,
        hovertemplate='<b>%{x}</b><br>Rainfall: %{y} mm<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor=custom_theme['paper_bgcolor'],
        plot_bgcolor=custom_theme['plot_bgcolor'],
        font=custom_theme['font'],
        title=dict(
            text="5-Day Weather Forecast",
            font=dict(color='#10b981', size=font_size+4)
        ),
        xaxis=dict(
            title="Day",
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        yaxis=dict(
            title="Temperature (°C)",
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        yaxis2=dict(
            title="Rainfall (mm)",
            overlaying='y',
            side='right',
            gridcolor=custom_theme['gridcolor'],
            color='white',
            tickfont=dict(size=font_size-1)
        ),
        height=300,
        hovermode='x unified',
        legend=dict(
            font=dict(color='white', size=font_size-1),
            bgcolor='rgba(30, 41, 59, 0.5)',
            bordercolor='rgba(148, 163, 184, 0.3)',
            borderwidth=1
        )
    )
    
    return fig


def create_recommendation_chart(recommendation_data, font_size=14):
    """Create a styled chart for displaying recommendations with adjustable font size"""
    
    # Create updated theme with custom font size
    custom_theme = CHART_THEME.copy()
    custom_theme['font']['size'] = font_size
    
    fig = go.Figure()
    
    # Add invisible trace to create the layout
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='text',
        text=[''],
        showlegend=False,
        hoverinfo='none'
    ))
    
    # Create the recommendation text with HTML formatting
    recommendation_text = f"""
    <div style='text-align: center; font-family: Arial, sans-serif;'>
        <span style='font-size: {font_size + 6}px; font-weight: bold; color: #10b981;'>RECOMMENDATION</span><br>
        <span style='font-size: {font_size + 4}px; font-weight: bold;'>Nitrogen: Adjust from 50 to ~100 kg/ha</span><br><br>
        <span style='font-size: {font_size + 2}px; color: #ef4444; font-weight: bold;'>ACTION REQUIRED</span>
    </div>
    """
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30, 41, 59, 0.3)',
        font=custom_theme['font'],
        title=dict(
            text="Fertilization Recommendation",
            font=dict(color='#10b981', size=font_size+6)
        ),
        xaxis=dict(
            visible=False,
            range=[0, 1]
        ),
        yaxis=dict(
            visible=False,
            range=[0, 1]
        ),
        height=200,
        margin=dict(t=60, b=40, l=40, r=40),
        annotations=[
            dict(
                x=0.5,
                y=0.5,
                xref='paper',
                yref='paper',
                text=recommendation_text,
                showarrow=False,
                font=dict(size=font_size),
                align='center',
                bordercolor='#10b981',
                borderwidth=2,
                borderpad=10,
                bgcolor='rgba(30, 41, 59, 0.7)'
            )
        ]
    )
    
    return fig