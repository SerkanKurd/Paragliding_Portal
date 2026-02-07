import streamlit as st
import pandas as pd
import pydeck as pdk
import IGC_file_parse as igc
import os
import time


st.title("Mini Doarama - 3D Uçuş İzleyici")

uploaded_file = "250519112547.igc"

if uploaded_file is not None:
    # points = []
    # for track in gpx.tracks:
    #     for segment in track.segments:
    #         for p in segment.points:
    #             points.append({"lat": p.latitude, "lon": p.longitude, "alt": p.elevation})

    df = igc.getfile(uploaded_file)

    # Calculate relative time in seconds for animation
    df["timestamp"] = (df["datetime"] - df["datetime"].min()).dt.total_seconds()

    # Deck.gl TripsLayer expects coordinates and timestamps.
    layer = pdk.Layer(
        "TripsLayer",
        data=[{
            "path": df[["longitude", "latitude", "pressure_altitude_m"]].values.tolist(),
            "timestamps": df["timestamp"].values.tolist()
        }],
        get_path="path",
        get_timestamps="timestamps",
        get_color=[255, 0, 0],
        width_min_pixels=5,
        trail_length=600,
        current_time=0,
    )

    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom=12,
        pitch=45  # 3D görünüm açısı
    )

    # Use MAPBOX_API_KEY from environment to enable Mapbox satellite basemap.
    mapbox_token = os.getenv("MAPBOX_API_KEY") or "pk.eyJ1Ijoic2FoaXBzaXoiLCJhIjoiY21renR6aXNhMDV5YzNmcXp5cDBkYzcyYSJ9.LxbCxA5G5sD42jlQ0wAXAg"

    layers = [layer]

    if mapbox_token:
        map_style = "mapbox://styles/mapbox/satellite-v9"
        terrain_layer = pdk.Layer(
            "TerrainLayer",
            elevation_decoder={"rScaler": 6553.6, "gScaler": 25.6, "bScaler": 0.1, "offset": -10000},
            texture=f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{{z}}/{{x}}/{{y}}?access_token={mapbox_token}",
            elevation_data=f"https://api.mapbox.com/v4/mapbox.terrain-rgb/{{z}}/{{x}}/{{y}}.pngraw?access_token={mapbox_token}",
        )
        layers.insert(0, terrain_layer)
    else:
        map_style = "light"
        st.warning("Mapbox token not found. Satellite basemap requires a Mapbox API token in MAPBOX_API_KEY.")

    # Animation controls
    max_time = int(df["timestamp"].max())
    
    if st.button("Play Animation"):
        chart = st.empty()
        for t in range(0, max_time + 1, 5):
            layer.current_time = t
            deck = pdk.Deck(
                layers=layers,
                initial_view_state=view_state,
                map_style=map_style,
                api_keys={"mapbox": mapbox_token} if mapbox_token else None
            )
            chart.pydeck_chart(deck)
            time.sleep(0.05)
    else:
        slider_val = st.slider("Time", 0, max_time, max_time)
        layer.current_time = slider_val
        deck = pdk.Deck(
            layers=layers,
            initial_view_state=view_state,
            map_style=map_style,
            api_keys={"mapbox": mapbox_token} if mapbox_token else None
        )
        st.pydeck_chart(deck)

    st.write("Uçuş Verileri:", df)
