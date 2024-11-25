import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)

# Load CSV data
df = pd.read_csv("assets/LBG Step Up Data Set.csv")

df['income_group'] = pd.cut(
    df['annual_inc'],
    bins=[0, 50000, 100000, 150000, float('inf')],
    labels=['<50k', '50k-100k', '100k-150k', '>150k']
)

high_risk_df = df[df['loan_status'].isin(['Default', 'Charged Off'])]

# App Layout
app.layout = html.Div([
    # Header Section
    html.Div([
        html.Img(src='assets/logo_lloyds.png', className='logo'),
        html.H1("Loan Repayment Tool", className='header-title'),
    ], className='header'),

    # Main Content Section
    html.Div([
        # Side Panel
        html.Div([
            html.Button([
                html.Img(src='/assets/check-shield.svg', style={'height': '20px', 'margin-right': '10px'}),
                "Risk Mitigation"
            ], id="open-risk-mitigation", className='side-button'),

            html.Button([
                html.Img(src='/assets/key.svg', style={'height': '20px', 'margin-right': '10px'}),
                "Classification Keys"
            ], id="open-risk-classification", className='side-button'),

            html.Button([
                html.Img(src='/assets/vertical-line-chart.svg', style={'height': '20px', 'margin-right': '10px'}),
                "Confidence Score"
            ], id="open-confidence-score", className='side-button'),

            html.Button([
                html.Img(src='/assets/info-circle.svg', style={'height': '20px', 'margin-right': '10px'}),
                "How To Use"
            ], id="open-dashboard-tips", className='side-button'),
        ], className='side-column'),

        # Data Visualizations (Left Column)
        html.Div([
            # Bar Chart
            html.Div([
                html.H3("Income vs Loan Status"),
                dcc.Graph(
                    id='bar-chart',
                    figure=px.bar(
                        df,
                        x='annual_inc',
                        y='loan_status',
                        barmode='group',
                        labels={"annual_inc": "Income (£)", "loan_status": "Loan Status"}
                    ).update_layout(
                        margin=dict(l=20, r=20, t=10, b=5),
                        width=300,
                        height=140
                    ),
                ),
                html.P("This bar chart shows income vs. loan status, highlighting trends."),
            ], className='data-card'),

            html.Div([
                html.H3("Income Distribution (High-Risk Customers)"),
                dcc.Graph(
                    id='income-pie-chart',
                    figure=px.pie(
                        high_risk_df,
                        names='income_group',
                        color_discrete_sequence=['#007B5F', '#99c49d', '#A9D5C6', '#a8d2f0']  # Lloyds colors
                    ).update_layout(
                        margin=dict(l=20, r=20, t=10, b=10),
                        width=300,
                        height=140
                    ),
                ),
                html.P("Insights: High income alone does not full determine high risk status. Other factors likely contribute to risk."),
            ], className='data-card'),

            # Placeholder for Demographics Chart
            html.Div([
                html.H3("Customer Demographics"),
                dcc.Graph(
                    id='demographics-chart',

                ),
                html.P("This chart shows demographic trends of loan applicants."),
            ], className='data-card'),


            # Placeholder for Repayment Trends
            html.Div([
                html.H3("Repayment Trends"),
                dcc.Graph(
                    id='repayment-trends-chart',

                ),
                html.P("This chart shows repayment patterns over time."),
            ], className='data-card'),
        ], className='left-column'),




        # Prediction Model (Right Column)
        html.Div([
            html.H3("Predict New Customer", className='prediction-title'),

            # Input fields container
            html.Div([
                html.Div([
                    html.Label("Annual Income"),
                    dcc.Input(id='annual-income', type='number', placeholder="Enter annual income")
                ], className='input-container'),

                html.Div([
                    html.Label("Loan Amount"),
                    dcc.Input(id='loan-amount', type='number', placeholder="Enter loan amount")
                ], className='input-container'),

                html.Div([
                    html.Label("Employment Length"),
                    dcc.Input(id='employment-length', type='number', placeholder="Enter employment length")
                ], className='input-container'),

                html.Div([
                    html.Label("Interest Rate (%)"),
                    dcc.Input(id='interest-rate', type='number', placeholder="Enter interest rate")
                ], className='input-container'),

                # Dropdown example
                html.Div([
                    html.Label("Loan Purpose"),
                    dcc.Dropdown(
                        id='loan-purpose',
                        options=[
                            {'label': 'Home', 'value': 'Home'},
                            {'label': 'Car', 'value': 'Car'},
                            {'label': 'Education', 'value': 'Education'}
                        ],
                        placeholder="Select loan purpose"
                    )
                ], className='input-container'),
            ], className='input-group'),

            # Predict button
            html.Button("Predict", id='predict-button', n_clicks=0),

            # Prediction result area
            html.Div(id='prediction-result')
        ], className='prediction-card')
    ], className='content-layout'),
])

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
