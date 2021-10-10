import os
from statistics import mean

import plotly.graph_objects as go
from api.models import Peak
from django.shortcuts import render
from plotly.offline import plot


def generate_peak_point(peak_list):
    """
    Generate list of name, latitude and longitude
    :param peak_list: list of peak record
    :return: a tuple with the 3 list.
    """
    l_peak_name = []
    l_peak_lat = []
    l_peak_lon = []
    for peak in peak_list:
        l_peak_name.append(f"{peak.name} ({peak.altitude} m)")
        l_peak_lat.append(peak.lat)
        l_peak_lon.append(peak.long)

    return l_peak_name, l_peak_lat, l_peak_lon


def show_peaks(request):
    """
    Place peak points on the map and display its
    """
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
    # if l_lat and l_lon are empty center map on Toulouse
    center_lat = mean([min(l_lats), max(l_lats)]) if l_lats else 43.6044622
    center_lon = mean([min(l_lons), max(l_lons)]) if l_lats else 1.4442469
    fig.update_layout(
        autosize=True,
        width=1500,
        height=1000,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=center_lat,
                lon=center_lon
            ),
            pitch=0,
            zoom=8
        ),
    )

    plot_div = plot(fig, output_type='div')

    return render(request, "map/map.html", context={'plot_div': plot_div})
