import os
from statistics import mean

import plotly.graph_objects as go
from api.models import Peak
from django.shortcuts import render
from plotly.offline import plot

print(os.path.dirname(__file__))


def generate_peak_point(peak_list):
    l_peak_name = []
    l_peak_lat = []
    l_peak_lon = []
    for peak in peak_list:
        l_peak_name.append(f"{peak.name} ({peak.altitude} m)")
        l_peak_lat.append(peak.lat)
        l_peak_lon.append(peak.long)

    return l_peak_name, l_peak_lat, l_peak_lon


def show_peaks(request):
    path_token_file = os.path.join(os.path.dirname(__file__), ".mapbox_token")
    with open(path_token_file, "r") as token:
        mapbox_access_token = token.read()
    peak_list = Peak.objects.all()
    l_names, l_lats, l_lons = generate_peak_point(peak_list)

    scatter_mapbox = go.Scattermapbox(
        lat=l_lats,
        lon=l_lons,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=l_names
    )
    fig = go.Figure(scatter_mapbox)
    fig.update_layout(
        autosize=True,
        width=1500,
        height=1000,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=mean([min(l_lats), max(l_lats)]),
                lon=mean([min(l_lons), max(l_lons)])
            ),
            pitch=0,
            zoom=8
        ),
    )

    plot_div = plot(fig, output_type='div')

    return render(request, "map.html", context={'plot_div': plot_div})
