#include <stdio.h>
#include <string.h>
#include <sys/param.h>


#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/timers.h"
#include "freertos/event_groups.h"

#include "esp_wifi.h"
#include "esp_log.h"
#include "esp_netif.h"
#include "esp_camera.h"
#include "esp_crt_bundle.h"
#include "esp_http_client.h"
#include "esp_http_server.h"
#include "nvs_flash.h"
#include "env_config.h"
#include "esp_sntp.h"

#include "driver/temperature_sensor.h"

static const char *TAG = "sending_data";

extern const uint8_t supabase_root_ca_pem_start[] asm("_binary_supabase_root_ca_pem_start");
extern const uint8_t supabase_root_ca_pem_end[]   asm("_binary_supabase_root_ca_pem_end");

// temperatura =======================================================================
temperature_sensor_handle_t temp_sensor = NULL;
temperature_sensor_config_t temp_sensor_config = TEMPERATURE_SENSOR_CONFIG_DEFAULT(10, 50);

// camera - pinagem =================================================================
#define CAM_PIN_PWDN    -1   
#define CAM_PIN_RESET   -1   
#define CAM_PIN_XCLK    15   
#define CAM_PIN_SIOD    4    
#define CAM_PIN_SIOC    5    
#define CAM_PIN_D7      16
#define CAM_PIN_D6      17
#define CAM_PIN_D5      18
#define CAM_PIN_D4      12
#define CAM_PIN_D3      10
#define CAM_PIN_D2      8
#define CAM_PIN_D1      9
#define CAM_PIN_D0      11
#define CAM_PIN_VSYNC   6    
#define CAM_PIN_HREF    7    
#define CAM_PIN_PCLK    13   

// html ============================================================================
static const char* html_page = "<html><body style><h1>ESP32-S3 CAM</h1><img src=\"/stream\"></body></html>";

// camera ==========================================================================
void init_camera(){
    camera_config_t config = {
        // Pinos de controle
        .pin_pwdn       = CAM_PIN_PWDN,     // Power down (-1 = ignorado)
        .pin_reset      = CAM_PIN_RESET,    // Reset (-1 = ignorado)
        .pin_xclk       = CAM_PIN_XCLK,    // Clock externo saindo do ESP (GPIO 15)

        // Pinos I2C (SCCB) para configurar registradores internos da câmera
        .pin_sccb_sda   = CAM_PIN_SIOD,
        .pin_sccb_scl   = CAM_PIN_SIOC,

        // Barramento de dados paralelo de 8 bits
        .pin_d7         = CAM_PIN_D7,
        .pin_d6         = CAM_PIN_D6,
        .pin_d5         = CAM_PIN_D5,
        .pin_d4         = CAM_PIN_D4,
        .pin_d3         = CAM_PIN_D3,
        .pin_d2         = CAM_PIN_D2,
        .pin_d1         = CAM_PIN_D1,
        .pin_d0         = CAM_PIN_D0,

        // Sinais de sincronização
        .pin_vsync      = CAM_PIN_VSYNC,
        .pin_href       = CAM_PIN_HREF,
        .pin_pclk       = CAM_PIN_PCLK,

        .xclk_freq_hz   = 8000000,          // Frequência do clock externo: 8 MHz
        .ledc_timer     = LEDC_TIMER_0,     // Timer LEDC usado para gerar o XCLK via PWM
        .ledc_channel   = LEDC_CHANNEL_0,   // Canal LEDC correspondente

        .pixel_format   = PIXFORMAT_JPEG,   // Câmera já entrega os dados comprimidos em JPEG
        .frame_size     = FRAMESIZE_QVGA,   // Resolução: 320×240 pixels

        .jpeg_quality   = 20,               // Qualidade JPEG: 0 (melhor) a 63 (pior)
        .fb_count       = 1,                // Número de framebuffers (1 = sem double buffering)
        .fb_location    = CAMERA_FB_IN_PSRAM, // Armazena o frame na PSRAM (não na RAM interna
    };

    ESP_ERROR_CHECK(esp_camera_init(&config));  

    ESP_LOGI(TAG, "Camera OK");  // confirmando inicialização
}
// =================================================================================

// wi-fi ===========================================================================
void wifi_init()
{
    nvs_flash_init();                        // Inicializa o NVS — obrigatório antes do WiFi (guarda calibrações)
    esp_netif_init();                        // Inicializa a stack TCP/IP (lwIP)
    esp_event_loop_create_default();         // Cria o loop de eventos padrão do sistema
    esp_netif_create_default_wifi_sta();     // Cria a interface de rede no modo Station (STA)

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();  // Preenche config WiFi com valores padrão
    esp_wifi_init(&cfg);                     // Inicializa o driver WiFi com essa config

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
        },
    };

    esp_wifi_set_mode(WIFI_MODE_STA);                  // Define modo Station (cliente, não AP)
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);    // Aplica as credenciais na interface STA
    esp_wifi_start();                                   // Liga o rádio WiFi
    esp_wifi_connect();                                 // Inicia a tentativa de associação

    ESP_LOGI(TAG, "Conectando ao WiFi...");  
}
// =================================================================================


// temperatura ======================================================================
void init_temp(){
    
    ESP_ERROR_CHECK(temperature_sensor_install(&temp_sensor_config, &temp_sensor));
    ESP_LOGI(TAG, "Sensor de temperatura configurado ");
    
    ESP_ERROR_CHECK(temperature_sensor_enable(temp_sensor));
    ESP_LOGI(TAG, "Sensor de temperatura ativado com sucesso!");
}

float get_temperature(){
    float tsens;
    ESP_ERROR_CHECK(temperature_sensor_get_celsius(temp_sensor, &tsens));
    ESP_LOGI(TAG, "Temperatura %.2f", tsens);
    return tsens;
}
// =================================================================================

// https ===========================================================================
esp_err_t handler_http(esp_http_client_event_t *evt){
    if (evt->event_id == HTTP_EVENT_ON_DATA)
        ESP_LOGI(TAG, "Resposta: %.*s", evt->data_len, (char*)evt->data);

    return ESP_OK;
}

void http_post_request(){
    float tsens;
    char url[200];
    snprintf(url, sizeof(url), "%s/rest/v1/%s",  SUPABASE_URL, SUPABASE_TABLE);

    tsens = get_temperature();

    char post_data[150];
    snprintf(post_data, sizeof(post_data), "{\"temperature\": %.2f}", tsens);

    esp_http_client_config_t config = {
        .url            = url,
        .method         = HTTP_METHOD_POST,
        .event_handler  = handler_http,
        .cert_pem       = (const char *)supabase_root_ca_pem_start,
        .timeout_ms     = 10000,
    };


    esp_http_client_handle_t client = esp_http_client_init(&config);

    esp_http_client_set_method(client, HTTP_METHOD_POST);
    esp_http_client_set_header(client, "Content-Type", "application/json");
    esp_http_client_set_header(client, "apikey", SUPABASE_KEY);
    esp_http_client_set_header(client, "Authorization", "Bearer " SUPABASE_KEY);
    esp_http_client_set_header(client, "Prefer", "return=representation");
    esp_http_client_set_post_field(client, post_data, strlen(post_data));

    esp_err_t err = esp_http_client_perform(client);

    if (err==ESP_OK) ESP_LOGI(TAG, "Sucesso ao enviar!");
    else ESP_LOGE(TAG, "Erro ao enviar :%s", esp_err_to_name(err));

    esp_http_client_cleanup(client);

}

void http_post_image(){
    char url[1000];
    time_t now = time(NULL);
    snprintf(url, sizeof(url), "%s/storage/v1/object/images/imagem_%ld",
             SUPABASE_URL, (long)now);

    camera_fb_t *fb = esp_camera_fb_get();
    if(!fb){
        ESP_LOGE(TAG, "Erro em captar frame");
        return;
    }

    esp_http_client_config_t config = {
        .url            = url,
        .method         = HTTP_METHOD_POST,
        .event_handler  = handler_http,
        .cert_pem       = (const char *)supabase_root_ca_pem_start,
        .timeout_ms     = 10000,
        .buffer_size_tx = 4096,
        .buffer_size    = 4096,
    };

    esp_http_client_handle_t client = esp_http_client_init(&config);

    esp_http_client_set_header(client, "Content-Type", "image/jpeg");
    esp_http_client_set_header(client, "apikey", SUPABASE_KEY);
    esp_http_client_set_header(client, "Authorization", "Bearer " SUPABASE_KEY);
    esp_http_client_set_header(client, "Prefer", "return=representation");

    // open informa o Content-Length e envia os headers — sem passar pelo buffer problemático
    esp_err_t err = esp_http_client_open(client, fb->len);
    if(err != ESP_OK){
        ESP_LOGE(TAG, "Open falhou: %s", esp_err_to_name(err));
        esp_camera_fb_return(fb);
        esp_http_client_cleanup(client);
        return;
    }

    // envia o body (bytes JPEG) direto no socket
    int written = esp_http_client_write(client, (const char*)fb->buf, fb->len);
    if(written < 0){
        ESP_LOGE(TAG, "Write falhou");
    } else {
        ESP_LOGI(TAG, "Bytes enviados: %d / %d", written, fb->len);
    }

    // lê os headers da resposta
    esp_http_client_fetch_headers(client);
    ESP_LOGI(TAG, "HTTP Status: %d", esp_http_client_get_status_code(client));

    esp_camera_fb_return(fb);   // libera o framebuffer
    esp_http_client_cleanup(client);
}

// =================================================================================

void http_task(void *pV){

    ESP_LOGI(TAG, "Cert size: %d bytes", 
             (int)(supabase_root_ca_pem_end - supabase_root_ca_pem_start));
    ESP_LOGI(TAG, "Cert inicio: %.27s", (char*)supabase_root_ca_pem_start);
    ESP_LOGI(TAG, "Cert fim: %.26s", (char*)(supabase_root_ca_pem_end - 26));
    
    time_t now;
    struct tm timeinfo;
    time(&now);
    localtime_r(&now, &timeinfo);
    ESP_LOGI(TAG, "Hora de inicio: %d-%02d-%02d",
        timeinfo.tm_year + 1900,
        timeinfo.tm_mon + 1,
        timeinfo.tm_mday);

    while(1){
        http_post_request();
        http_post_image();
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
    
    vTaskDelete(NULL);
}

void app_main(void)
{
    wifi_init();
    vTaskDelay(pdMS_TO_TICKS(5000));

    // sincronizando o horario
    esp_sntp_setoperatingmode(SNTP_OPMODE_POLL);
    esp_sntp_setservername(0, "pool.ntp.org");
    esp_sntp_init();

    int retry = 0;
    
    while (sntp_get_sync_status() != SNTP_SYNC_STATUS_COMPLETED && retry++ < 20) {
        ESP_LOGI(TAG, "Aguardando SNTP... (%d)", retry);
        vTaskDelay(pdMS_TO_TICKS(500));
    }

    ESP_LOGI(TAG, "Horário sincronizado!");
    init_camera();
    init_temp();

    
    xTaskCreate(http_task, "http_task", 16384, NULL, 5, NULL);
    


}
