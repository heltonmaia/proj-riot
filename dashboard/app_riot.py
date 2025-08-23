import panel as pn
import folium
import param
import numpy as np
import pandas as pd
from folium import plugins

pn.extension('folium')

class RIoTMonitorApp(param.Parameterized):
    """R-IoT (Rural Internet of Things) - Sistema de monitoramento de gado com GPS"""
    
    # Coordenadas centrais ajustadas para mostrar ambas as localizações
    lat_centro = param.Number(default=-5.9520, bounds=(-7.0, -4.5))
    lon_centro = param.Number(default=-35.2060, bounds=(-38.0, -34.0))
    zoom_level = param.Integer(default=9, bounds=(5, 20))
    
    def __init__(self):
        super().__init__()
        self.vacas_data = self._generate_sample_data()
        
    def _generate_sample_data(self):
        """Gera dados de exemplo de vacas em duas localizações: Escola Agrícola de Jundiaí e UFRN Natal"""
        np.random.seed(42)
        
        # Coordenadas da Escola Agrícola de Jundiaí (UFRN)
        lat_jundiai = -6.0704
        lon_jundiai = -35.2085
        
        # Coordenadas da UFRN Campus Natal
        lat_natal = -5.8336
        lon_natal = -35.2034
        
        vacas = []
        
        # 10 vacas na Escola Agrícola de Jundiaí
        for i in range(10):
            lat_offset = np.random.uniform(-0.005, 0.005)  # ~500m de variação
            lon_offset = np.random.uniform(-0.005, 0.005)
            
            vacas.append({
                'id': f'Jundiaí_{i+1:02d}',
                'lat': lat_jundiai + lat_offset,
                'lon': lon_jundiai + lon_offset,
                'local': 'Escola Agrícola de Jundiaí',
                'status': np.random.choice(['Ativa', 'Pastando', 'Descansando']),
                'bateria': np.random.randint(20, 100)
            })
        
        # 7 vacas na UFRN Campus Natal
        for i in range(7):
            lat_offset = np.random.uniform(-0.003, 0.003)  # ~300m de variação
            lon_offset = np.random.uniform(-0.003, 0.003)
            
            vacas.append({
                'id': f'UFRN_{i+1:02d}',
                'lat': lat_natal + lat_offset,
                'lon': lon_natal + lon_offset,
                'local': 'UFRN Campus Natal',
                'status': np.random.choice(['Ativa', 'Pastando', 'Descansando']),
                'bateria': np.random.randint(20, 100)
            })
        
        return pd.DataFrame(vacas)
    
    def create_map(self):
        """Cria o mapa base mostrando ambas as localizações"""
        # Cria mapa centrado entre as duas localizações
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
        
        # Marcadores das instituições
        folium.Marker(
            location=[-6.0704, -35.2085],
            popup="🏫 Escola Agrícola de Jundiaí - UFRN<br>10 vacas monitoradas",
            icon=folium.Icon(color='blue', icon='university')
        ).add_to(m)
        
        folium.Marker(
            location=[-5.8336, -35.2034],
            popup="🏛️ UFRN Campus Natal<br>7 vacas monitoradas",
            icon=folium.Icon(color='purple', icon='university')
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
            Local: {vaca['local']}<br>
            Status: {vaca['status']}<br>
            Bateria GPS: {vaca['bateria']}%<br>
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
        
        # Adiciona círculos para mostrar áreas de pastagem
        folium.Circle(
            radius=300,
            location=[-6.0704, -35.2085],
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.1,
            popup="Área de Pastagem - Jundiaí"
        ).add_to(m)
        
        folium.Circle(
            radius=200,
            location=[-5.8336, -35.2034],
            color="purple",
            fill=True,
            fill_color="purple",
            fill_opacity=0.1,
            popup="Área de Pastagem - UFRN Natal"
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
        vacas_jundiai = len(self.vacas_data[self.vacas_data['local'] == 'Escola Agrícola de Jundiaí'])
        vacas_natal = len(self.vacas_data[self.vacas_data['local'] == 'UFRN Campus Natal'])
        vacas_ativas = len(self.vacas_data[self.vacas_data['status'] == 'Ativa'])
        bateria_media = self.vacas_data['bateria'].mean()
        
        stats_html = f"""
        <div style="padding: 15px; background-color: #f0f0f0; border-radius: 10px; margin: 10px;">
            <h3>📊 Estatísticas R-IoT</h3>
            <p><b>Total de Vacas:</b> {total_vacas}</p>
            <p><b>Escola Jundiaí:</b> {vacas_jundiai} vacas</p>
            <p><b>UFRN Natal:</b> {vacas_natal} vacas</p>
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
            "# 🐄 R-IoT Monitor",
            "*Rural Internet of Things*",
            self.get_stats_panel(),
            self.get_controls_panel(),
            pn.Spacer(height=20),
            "---",
            "**Localizações:**",
            "• Escola Agrícola de Jundiaí: 10 vacas",
            "• UFRN Campus Natal: 7 vacas",
            "",
            "**Instruções:**",
            "- Clique nos marcadores para detalhes",
            "- Use ferramentas para medir distâncias",
            "- Ajuste controles para navegar",
            width=350,
            margin=(10, 10)
        )
        
        # Layout principal
        dashboard = pn.template.MaterialTemplate(
            title="R-IoT - Rural Internet of Things - Monitor de Gado GPS",
            sidebar=sidebar,
            main=[map_pane],
            header_background='#2596be',
        )
        
        return dashboard

def create_app():
    """Função para criar a aplicação Panel"""
    app = RIoTMonitorApp()
    return app.create_dashboard()

# Para executar com: panel serve app_riot.py --show --autoreload
if __name__ == "__main__":
    app = create_app()
    app.servable()
else:
    # Quando importado pelo Panel server
    create_app().servable()