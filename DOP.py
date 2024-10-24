import pandas as pd
import numpy as np
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from flask import Flask

# Define Flask server
server = Flask(__name__)

# Define the Dash app and bind it to the Flask server
app = Dash(__name__, server=server)

# Path to the CSV file (Update this with the correct path on PythonAnywhere)
file_path = r'/Users/srikrishna/Desktop/DoP1/data21.csv'    # Use the actual path to your CSV file on PythonAnywhere

# Define initial values for A and w (these can be changed in the code or via the web interface)
A = 2  # Amplitude
w = 2 * np.pi  # Angular frequency (example: 2*pi for 1 Hz)

# Function to read the CSV and return the time values
def get_time_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df['time']

# Read initial time data from the CSV file
time_values = get_time_from_csv(file_path)

# App layout for the Dash web application
app.layout = html.Div([
    html.Div([
        html.Label('Amplitude (A):'),
        dcc.Input(id='amplitude-input', type='number', value=A, step=0.1),

        html.Label('Angular Frequency (w):'),
        dcc.Input(id='frequency-input', type='number', value=w, step=0.1)
    ]),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(id='interval-component', interval=1 * 1000, n_intervals=0),  # Update every second
])

# Update graph dynamically
@app.callback(
    Output('live-graph', 'figure'),
    [Input('amplitude-input', 'value'), Input('frequency-input', 'value'), Input('interval-component', 'n_intervals')]
)
def update_graph(amplitude, frequency, n):
    # Update A and w with input values
    A = amplitude
    w = frequency

    # Calculate the new sine wave with updated A and w
    sine_wave = A * np.sin(w * time_values)

    # Create the updated graph
    fig = go.Figure(data=[go.Scatter(x=time_values, y=sine_wave, mode='lines', name='Sine Wave')])
    fig.update_layout(title='Live Sine Wave Graph', xaxis_title='Time', yaxis_title='Asin(wt)')
    return fig

# Run the app in debug mode
if __name__ == '__main__':
    app.run_server(debug=True,port=5000)