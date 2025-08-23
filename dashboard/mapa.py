import folium

# Localização central: Escola Agrícola de Jundiaí (UFRN)
lat_centro, lon_centro = -6.0704, -35.2085

# Simulação de vacas em volta da escola
coordenadas_vacas = [
    {"id": "Vaca 1", "lat": -6.0704, "lon": -35.2085},  # dentro da escola
    {"id": "Vaca 2", "lat": -6.0720, "lon": -35.2100},  # próxima ao pasto
    {"id": "Vaca 3", "lat": -6.0685, "lon": -35.2070},  # perto da entrada
    {"id": "Vaca 4", "lat": -6.0715, "lon": -35.2050},  # lado leste
]

# Cria o mapa centralizado na Escola Agrícola
m = folium.Map(location=[lat_centro, lon_centro], zoom_start=16, tiles="OpenStreetMap")

# Marcador da escola
folium.Marker(
    location=[lat_centro, lon_centro],
    popup="🏫 Escola Agrícola de Jundiaí - UFRN",
    icon=folium.Icon(color="blue", icon="university"),
).add_to(m)

# Adiciona marcadores das vacas
for vaca in coordenadas_vacas:
    folium.Marker(
        location=[vaca["lat"], vaca["lon"]],
        popup=f"🐄 {vaca['id']}",
        icon=folium.Icon(color="green", icon="info-sign"),
    ).add_to(m)

# Exemplo de cerca (geofence) em torno da escola
folium.Circle(
    radius=200,  # metros
    location=[lat_centro, lon_centro],
    color="red",
    fill=True,
    fill_color="red",
    fill_opacity=0.2,
    popup="Área de pastagem",
).add_to(m)

# Salva o mapa
m.save("vacas_jundai.html")

print("Mapa gerado! Abra o arquivo vacas_jundai.html no navegador.")
