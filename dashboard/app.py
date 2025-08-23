import panel as pn
import folium
import param
import numpy as np
import pandas as pd
from folium import plugins

pn.extension('folium')

class VacasMonitorApp(param.Parameterized):
    """R-IoT (Rural Internet of Things) - Sistema de monitoramento de gado com GPS"""
    
    # Coordenadas centrais do RN (região de Natal)
    lat_centro = param.Number(default=-5.7945, bounds=(-7.0, -4.5))
    lon_centro = param.Number(default=-35.2110, bounds=(-38.0, -34.0))
    zoom_level = param.Integer(default=10, bounds=(5, 20))
    
    def __init__(self):
        super().__init__()
        self.vacas_data = self._generate_sample_data()
        
    def _generate_sample_data(self):
        """Gera dados de exemplo de vacas no RN"""
        np.random.seed(42)
        n_vacas = 10
        
        # Coordenadas aproximadas do RN
        lat_base = -5.7945
        lon_base = -35.2110
        
        vacas = []
        for i in range(n_vacas):
            # Distribui as vacas em um raio de ~50km
            lat_offset = np.random.uniform(-0.5, 0.5)
            lon_offset = np.random.uniform(-0.5, 0.5)
            
            vacas.append({
                'id': f'Vaca_{i+1:02d}',
                'lat': lat_base + lat_offset,
                'lon': lon_base + lon_offset,
                'status': np.random.choice(['Ativa', 'Pastando', 'Descansando']),
                'bateria': np.random.randint(20, 100)
            })
        
        return pd.DataFrame(vacas)
    
    def create_map(self):
        """Cria o mapa base do Rio Grande do Norte"""
        # Cria mapa centrado no RN
        m = folium.Map(
            location=[self.lat_centro, self.lon_centro],
            zoom_start=self.zoom_level,
            tiles='OpenStreetMap'
        )
        
        # Adiciona diferentes layers de mapa
        folium.TileLayer(
            tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png',
            attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.',
            name='Stamen Terrain'
        ).add_to(m)
        
        folium.TileLayer(
            tiles='CartoDB positron',
            attr='© OpenStreetMap contributors © CARTO',
            name='CartoDB Positron'
        ).add_to(m)
        
        # Marcador para Natal (capital do RN)
        folium.Marker(
            location=[-5.7945, -35.2110],
            popup="🏛️ Natal - RN",
            icon=folium.Icon(color='blue', icon='star')
        ).add_to(m)
        
        # Adiciona as vacas no mapa
        for _, vaca in self.vacas_data.iterrows():
            # Cor do ícone baseada no status
            color_map = {
                'Ativa': 'green',
                'Pastando': 'orange', 
                'Descansando': 'red'
            }
            
            popup_text = f"""
            <b>🐄 {vaca['id']}</b><br>
            Status: {vaca['status']}<br>
            Bateria: {vaca['bateria']}%<br>
            Coordenadas: {vaca['lat']:.4f}, {vaca['lon']:.4f}
            """
            
            folium.Marker(
                location=[vaca['lat'], vaca['lon']],
                popup=popup_text,
                icon=folium.Icon(
                    color=color_map.get(vaca['status'], 'gray'),
                    icon='info-sign'
                )
            ).add_to(m)
        
        # Adiciona controle de layers
        folium.LayerControl().add_to(m)
        
        # Plugin para medir distâncias
        plugins.MeasureControl().add_to(m)
        
        # Plugin para localização
        plugins.LocateControl().add_to(m)
        
        return m
    
    def get_stats_panel(self):
        """Painel com estatísticas das vacas"""
        total_vacas = len(self.vacas_data)
        vacas_ativas = len(self.vacas_data[self.vacas_data['status'] == 'Ativa'])
        bateria_media = self.vacas_data['bateria'].mean()
        
        stats_html = f"""
        <div style="padding: 15px; background-color: #f0f0f0; border-radius: 10px; margin: 10px;">
            <h3>📊 Estatísticas do Rebanho</h3>
            <p><b>Total de Vacas:</b> {total_vacas}</p>
            <p><b>Vacas Ativas:</b> {vacas_ativas}</p>
            <p><b>Bateria Média GPS:</b> {bateria_media:.1f}%</p>
        </div>
        """
        return pn.pane.HTML(stats_html)
    
    def get_controls_panel(self):
        """Painel com controles da aplicação"""
        controls = pn.Column(
            "## 🎛️ Controles",
            pn.Param(self, parameters=['lat_centro', 'lon_centro', 'zoom_level'],
                    widgets={
                        'lat_centro': pn.widgets.NumberInput,
                        'lon_centro': pn.widgets.NumberInput,
                        'zoom_level': pn.widgets.IntSlider
                    }),
            width=300
        )
        return controls
    
    def create_dashboard(self):
        """Cria o dashboard completo"""
        # Cria o mapa
        map_obj = self.create_map()
        map_pane = pn.pane.plot.Folium(map_obj, sizing_mode='stretch_width', height=600)
        
        # Painel lateral
        sidebar = pn.Column(
            "# 🐄 Monitor de Vacas - RN",
            self.get_stats_panel(),
            self.get_controls_panel(),
            pn.Spacer(height=20),
            "---",
            "**Instruções:**",
            "- Use os controles para ajustar o centro do mapa",
            "- Clique nos marcadores para ver detalhes das vacas",
            "- Use as ferramentas do mapa para medir distâncias",
            width=350,
            margin=(10, 10)
        )
        
        # Layout principal
        dashboard = pn.template.MaterialTemplate(
            title="Monitor de Vacas GPS - Rio Grande do Norte",
            sidebar=sidebar,
            main=[map_pane],
            header_background='#2596be',
        )
        
        return dashboard

def create_app():
    """Função para criar a aplicação Panel"""
    app = VacasMonitorApp()
    return app.create_dashboard()

# Para executar com: panel serve app.py --show --autoreload
if __name__ == "__main__":
    app = create_app()
    app.servable()
else:
    # Quando importado pelo Panel server
    create_app().servable()