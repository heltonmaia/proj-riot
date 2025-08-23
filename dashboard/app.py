import panel as pn
import folium
import param
import numpy as np
import pandas as pd
from folium import plugins

pn.extension('folium')

class RIoTMonitorApp(param.Parameterized):
    """R-IoT (Rural Internet of Things) - Sistema de monitoramento de gado com GPS"""
    
    def __init__(self):
        super().__init__()
        self.gado_data = self._generate_sample_data()
        
    def _generate_sample_data(self):
        """Gera dados de exemplo de gado em duas localizações: EAJ e UFRN Natal"""
        np.random.seed(42)
        
        # Coordenadas da Escola Agrícola de Jundiaí (EAJ)
        lat_jundiai = -6.0704
        lon_jundiai = -35.2085
        
        # Coordenadas da UFRN Campus Natal
        lat_natal = -5.8336
        lon_natal = -35.2034
        
        gado = []
        
        # 10 animais na EAJ - mix de vacas e bezerros
        tipos_eaj = ['Vaca'] * 6 + ['Bezerro'] * 4
        for i, tipo in enumerate(tipos_eaj):
            # Maior variação para garantir que apareçam no mapa
            lat_offset = np.random.uniform(-0.01, 0.01)  # ~1km de variação
            lon_offset = np.random.uniform(-0.01, 0.01)
            
            gado.append({
                'id': f'EAJ_{i+1:02d}',
                'tipo': tipo,
                'lat': lat_jundiai + lat_offset,
                'lon': lon_jundiai + lon_offset,
                'local': 'Escola Agrícola de Jundiaí (EAJ)',
                'status': np.random.choice(['Ativa', 'Pastando', 'Descansando', 'Ruminando']),
                'bateria': np.random.randint(15, 100),
                'idade_meses': np.random.randint(6, 60) if tipo == 'Vaca' else np.random.randint(2, 12),
                'peso_kg': np.random.randint(400, 650) if tipo == 'Vaca' else np.random.randint(80, 200),
                'temperatura': np.random.uniform(37.5, 39.5),
                'cortisol': np.random.uniform(10, 80),  # ng/ml
                'passos_24h': np.random.randint(2000, 8000),
                'freq_cardiaca': np.random.randint(60, 90)
            })
        
        # 7 animais na UFRN Campus Natal
        tipos_ufrn = ['Vaca'] * 4 + ['Bezerro'] * 3
        for i, tipo in enumerate(tipos_ufrn):
            lat_offset = np.random.uniform(-0.008, 0.008)  # ~800m de variação
            lon_offset = np.random.uniform(-0.008, 0.008)
            
            gado.append({
                'id': f'UFRN_{i+1:02d}',
                'tipo': tipo,
                'lat': lat_natal + lat_offset,
                'lon': lon_natal + lon_offset,
                'local': 'UFRN Campus Natal',
                'status': np.random.choice(['Ativa', 'Pastando', 'Descansando', 'Ruminando']),
                'bateria': np.random.randint(15, 100),
                'idade_meses': np.random.randint(6, 60) if tipo == 'Vaca' else np.random.randint(2, 12),
                'peso_kg': np.random.randint(400, 650) if tipo == 'Vaca' else np.random.randint(80, 200),
                'temperatura': np.random.uniform(37.5, 39.5),
                'cortisol': np.random.uniform(10, 80),  # ng/ml
                'passos_24h': np.random.randint(2000, 8000),
                'freq_cardiaca': np.random.randint(60, 90)
            })
        
        return pd.DataFrame(gado)
    
    def create_map(self):
        """Cria o mapa base mostrando ambas as localizações"""
        # Coordenadas centrais entre EAJ e UFRN
        lat_centro = -5.9520
        lon_centro = -35.2060
        
        # Cria mapa centrado entre as duas localizações
        m = folium.Map(
            location=[lat_centro, lon_centro],
            zoom_start=9,
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
            popup="""<b>🏫 Escola Agrícola de Jundiaí (EAJ)</b><br>
                    📍 UFRN Campus Macaíba<br>
                    🐄 6 vacas + 4 bezerros monitorados<br>
                    📡 Sistema R-IoT ativo""",
            icon=folium.Icon(color='blue', icon='university', prefix='fa')
        ).add_to(m)
        
        folium.Marker(
            location=[-5.8336, -35.2034],
            popup="""<b>🏛️ UFRN Campus Natal</b><br>
                    📍 Campus Central<br>
                    🐄 4 vacas + 3 bezerros monitorados<br>
                    📡 Sistema R-IoT ativo""",
            icon=folium.Icon(color='purple', icon='university', prefix='fa')
        ).add_to(m)
        
        # Adiciona o gado no mapa com ícones intuitivos
        for _, animal in self.gado_data.iterrows():
            # Ícones mais intuitivos baseados no tipo e status
            if animal['tipo'] == 'Vaca':
                base_color = 'darkred'  # Vacas adultas em cor mais escura
                if animal['status'] == 'Ativa':
                    color, icon = 'green', 'play'
                elif animal['status'] == 'Pastando':
                    color, icon = 'orange', 'leaf'
                elif animal['status'] == 'Ruminando':
                    color, icon = 'blue', 'circle'
                else:  # Descansando
                    color, icon = 'red', 'pause'
            else:  # Bezerro
                base_color = 'lightred'  # Bezerros em cor mais clara
                if animal['status'] == 'Ativa':
                    color, icon = 'lightgreen', 'play'
                elif animal['status'] == 'Pastando':
                    color, icon = 'beige', 'leaf'
                elif animal['status'] == 'Ruminando':
                    color, icon = 'lightblue', 'circle'
                else:  # Descansando
                    color, icon = 'pink', 'pause'
            
            # Define emoji e tamanho baseado no tipo
            emoji = '🐄' if animal['tipo'] == 'Vaca' else '🐮'
            
            # Avaliação de saúde baseada nos parâmetros
            cortisol_status = "Normal" if animal['cortisol'] < 40 else "Elevado" if animal['cortisol'] < 60 else "Alto"
            temp_status = "Normal" if animal['temperatura'] < 38.5 else "Elevada" if animal['temperatura'] < 39.0 else "Febre"
            atividade_status = "Baixa" if animal['passos_24h'] < 3000 else "Normal" if animal['passos_24h'] < 6000 else "Alta"
            
            # Cor do status de saúde
            if cortisol_status == "Alto" or temp_status == "Febre":
                saude_cor = "🔴"
            elif cortisol_status == "Elevado" or temp_status == "Elevada":
                saude_cor = "🟡"
            else:
                saude_cor = "🟢"
            
            popup_text = f"""
            <div style="width: 320px; font-family: Arial, sans-serif;">
                <div style="text-align: center; background: linear-gradient(90deg, #4CAF50, #2196F3); 
                           color: white; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                    <h3 style="margin: 0;">{emoji} {animal['id']}</h3>
                    <p style="margin: 5px 0; font-size: 14px;">{animal['tipo']} - {animal['local']}</p>
                </div>
                
                <div style="background: #f5f5f5; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    <h4 style="margin-top: 0; color: #333;">📊 Status Atual</h4>
                    <p><b>Status:</b> {animal['status']}</p>
                    <p><b>Saúde Geral:</b> {saude_cor}</p>
                    <p><b>Bateria GPS:</b> {animal['bateria']}%</p>
                </div>
                
                <div style="background: #f0f8ff; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    <h4 style="margin-top: 0; color: #333;">🩺 Parâmetros Vitais</h4>
                    <p><b>Temperatura:</b> {animal['temperatura']:.1f}°C <span style="color: {'red' if temp_status=='Febre' else 'orange' if temp_status=='Elevada' else 'green'};">({temp_status})</span></p>
                    <p><b>Freq. Cardíaca:</b> {animal['freq_cardiaca']} bpm</p>
                    <p><b>Cortisol:</b> {animal['cortisol']:.1f} ng/ml <span style="color: {'red' if cortisol_status=='Alto' else 'orange' if cortisol_status=='Elevado' else 'green'};">({cortisol_status})</span></p>
                </div>
                
                <div style="background: #fff8e1; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    <h4 style="margin-top: 0; color: #333;">🚶 Atividade (24h)</h4>
                    <p><b>Passos:</b> {animal['passos_24h']:,} <span style="color: {'green' if atividade_status=='Alta' else 'orange' if atividade_status=='Normal' else 'red'};">({atividade_status})</span></p>
                    <p><b>Idade:</b> {animal['idade_meses']} meses</p>
                    <p><b>Peso:</b> {animal['peso_kg']} kg</p>
                </div>
                
                <div style="background: #e8f5e8; padding: 8px; border-radius: 5px; margin: 5px 0; font-size: 12px;">
                    <b>📍 Coordenadas:</b> {animal['lat']:.6f}, {animal['lon']:.6f}
                </div>
            </div>
            """
            
            # Cria ícone customizado baseado no tipo
            if animal['tipo'] == 'Vaca':
                custom_icon = folium.DivIcon(
                    html=f"""
                    <div style="font-size: 28px; text-align: center; color: {color};">
                        🐄
                    </div>
                    """,
                    icon_size=(30, 30),
                    icon_anchor=(15, 15)
                )
            else:  # Bezerro
                custom_icon = folium.DivIcon(
                    html=f"""
                    <div style="font-size: 24px; text-align: center; color: {color};">
                        🐮
                    </div>
                    """,
                    icon_size=(25, 25),
                    icon_anchor=(12, 12)
                )
            
            folium.Marker(
                location=[animal['lat'], animal['lon']],
                popup=folium.Popup(popup_text, max_width=350),
                icon=custom_icon
            ).add_to(m)
        
        # Adiciona círculos para mostrar áreas de pastagem
        folium.Circle(
            radius=800,
            location=[-6.0704, -35.2085],
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.1,
            popup="Área de Pastagem - EAJ<br>Raio: 800m"
        ).add_to(m)
        
        folium.Circle(
            radius=600,
            location=[-5.8336, -35.2034],
            color="purple",
            fill=True,
            fill_color="purple",
            fill_opacity=0.1,
            popup="Área de Pastagem - UFRN Natal<br>Raio: 600m"
        ).add_to(m)
        
        # Adiciona controle de layers
        folium.LayerControl().add_to(m)
        
        # Plugin para medir distâncias
        plugins.MeasureControl().add_to(m)
        
        # Plugin para localização
        plugins.LocateControl().add_to(m)
        
        # Plugin de minimap
        plugins.MiniMap().add_to(m)
        
        return m
    
    def get_stats_panel(self):
        """Painel com estatísticas detalhadas do gado"""
        total_animais = len(self.gado_data)
        
        # Estatísticas por local
        eaj_data = self.gado_data[self.gado_data['local'].str.contains('EAJ')]
        ufrn_data = self.gado_data[self.gado_data['local'].str.contains('UFRN')]
        
        # Estatísticas por tipo
        vacas = self.gado_data[self.gado_data['tipo'] == 'Vaca']
        bezerros = self.gado_data[self.gado_data['tipo'] == 'Bezerro']
        
        # Status
        ativas = len(self.gado_data[self.gado_data['status'] == 'Ativa'])
        pastando = len(self.gado_data[self.gado_data['status'] == 'Pastando'])
        descansando = len(self.gado_data[self.gado_data['status'] == 'Descansando'])
        ruminando = len(self.gado_data[self.gado_data['status'] == 'Ruminando'])
        
        # Médias
        bateria_media = self.gado_data['bateria'].mean()
        temperatura_media = self.gado_data['temperatura'].mean()
        peso_medio_vacas = vacas['peso_kg'].mean() if len(vacas) > 0 else 0
        peso_medio_bezerros = bezerros['peso_kg'].mean() if len(bezerros) > 0 else 0
        
        # Alertas
        bateria_baixa = len(self.gado_data[self.gado_data['bateria'] < 20])
        temperatura_alta = len(self.gado_data[self.gado_data['temperatura'] > 39.0])
        
        # Cálculos adicionais para as novas métricas
        cortisol_medio = self.gado_data['cortisol'].mean()
        passos_medio = self.gado_data['passos_24h'].mean()
        freq_cardiaca_media = self.gado_data['freq_cardiaca'].mean()
        
        # Alertas avançados
        cortisol_alto = len(self.gado_data[self.gado_data['cortisol'] > 60])
        atividade_baixa = len(self.gado_data[self.gado_data['passos_24h'] < 3000])
        
        stats_html = f"""
        <div style="padding: 15px; background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
                    color: #ecf0f1; border-radius: 15px; margin: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <h3 style="margin-top: 0; text-align: center; color: #ecf0f1; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">📊 Estatísticas R-IoT</h3>
            
            <div style="background: linear-gradient(135deg, #3498db, #2980b9); padding: 12px; border-radius: 8px; margin: 10px 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                <h4 style="margin-top: 0; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">🏢 Por Localização</h4>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>EAJ:</b> {len(eaj_data)} animais ({len(eaj_data[eaj_data['tipo']=='Vaca'])} vacas, {len(eaj_data[eaj_data['tipo']=='Bezerro'])} bezerros)</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>UFRN Natal:</b> {len(ufrn_data)} animais ({len(ufrn_data[ufrn_data['tipo']=='Vaca'])} vacas, {len(ufrn_data[ufrn_data['tipo']=='Bezerro'])} bezerros)</p>
            </div>
            
            <div style="background: linear-gradient(135deg, #27ae60, #229954); padding: 12px; border-radius: 8px; margin: 10px 0;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                <h4 style="margin-top: 0; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">🐄 Status dos Animais</h4>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Ativas:</b> {ativas} | <b>Pastando:</b> {pastando}</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Descansando:</b> {descansando} | <b>Ruminando:</b> {ruminando}</p>
            </div>
            
            <div style="background: linear-gradient(135deg, #f39c12, #e67e22); padding: 12px; border-radius: 8px; margin: 10px 0;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                <h4 style="margin-top: 0; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">📈 Parâmetros Médios</h4>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Temperatura:</b> {temperatura_media:.1f}°C</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Cortisol:</b> {cortisol_medio:.1f} ng/ml</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Freq. Cardíaca:</b> {freq_cardiaca_media:.0f} bpm</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Atividade:</b> {passos_medio:.0f} passos/dia</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Bateria GPS:</b> {bateria_media:.1f}%</p>
            </div>
            
            <div style="background: linear-gradient(135deg, #9b59b6, #8e44ad); padding: 12px; border-radius: 8px; margin: 10px 0;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                <h4 style="margin-top: 0; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">⚖️ Peso Médio</h4>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Vacas:</b> {peso_medio_vacas:.0f} kg</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Bezerros:</b> {peso_medio_bezerros:.0f} kg</p>
            </div>
            
            <div style="background: linear-gradient(135deg, #e74c3c, #c0392b); padding: 12px; border-radius: 8px; margin: 10px 0;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                <h4 style="margin-top: 0; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">⚠️ Alertas de Saúde</h4>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Bateria Baixa (&lt;20%):</b> {bateria_baixa} animais</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Temperatura Alta (&gt;39°C):</b> {temperatura_alta} animais</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Cortisol Elevado (&gt;60):</b> {cortisol_alto} animais</p>
                <p style="color: #ecf0f1; margin: 5px 0;"><b>Atividade Baixa (&lt;3k passos):</b> {atividade_baixa} animais</p>
            </div>
        </div>
        """
        return pn.pane.HTML(stats_html)
    
    def create_dashboard(self):
        """Cria o dashboard completo"""
        # Cria o mapa
        map_obj = self.create_map()
        map_pane = pn.pane.plot.Folium(map_obj, sizing_mode='stretch_width', height=650)
        
        # Painel lateral
        sidebar = pn.Column(
            """# 🐄 R-IoT Monitor
            ### *Rural Internet of Things*
            
            Sistema de monitoramento de gado com GPS em tempo real para pesquisa e gestão pecuária.
            """,
            self.get_stats_panel(),
            pn.Spacer(height=20),
            """
            ---
            **🎯 Funcionalidades:**
            • Rastreamento GPS em tempo real
            • Monitoramento de saúde animal
            • Alertas automáticos
            • Geofencing inteligente
            • Analytics de comportamento
            
            **📍 Localizações Ativas:**
            • EAJ Macaíba: 10 animais
            • UFRN Natal: 7 animais
            
            **💡 Navegação:**
            Use o mouse para navegar pelo mapa.
            Clique nos marcadores para detalhes.
            """,
            width=380,
            margin=(10, 10),
            scroll=True
        )
        
        # Layout principal
        dashboard = pn.template.MaterialTemplate(
            title="R-IoT - Rural Internet of Things | Monitor de Gado GPS",
            sidebar=sidebar,
            main=[map_pane],
            header_background='#667eea',
            sidebar_width=400
        )
        
        return dashboard

def create_app():
    """Função para criar a aplicação Panel"""
    app = RIoTMonitorApp()
    return app.create_dashboard()

# Para executar com: panel serve app_riot_fixed.py --show --autoreload
if __name__ == "__main__":
    app = create_app()
    app.servable()
else:
    # Quando importado pelo Panel server
    create_app().servable()