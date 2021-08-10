"""
A simple app demonstrating how to manually construct a navbar with a customised
layout using the Navbar component and the supporting Nav, NavItem, NavLink,
NavbarBrand, and NavbarToggler components.

Requires dash-bootstrap-components 0.3.0 or later
"""
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
# try running the app with one of the Bootswatch themes e.g.
# app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

nav = dbc.Nav(
    [
        dbc.NavbarBrand("Navbar", href="#", className="navbar-brand"),
        dbc.NavLink("Active", active=True, href="#", className="nav-link active"),
        dbc.NavLink("A link", href="#"),
        dbc.NavLink("Another link", href="#"),
        dbc.NavLink("Disabled", disabled=True, href="#"),
    ],
    className="navbar navbar-expand-lg navbar-dark bg-primary",
)


app.layout = html.Div([nav])


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
