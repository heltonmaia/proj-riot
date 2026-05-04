idf_component_register(SRCS "sending_data_main.c" # "sending_data_main_working.c"
                       PRIV_REQUIRES spi_flash esp_driver_tsens
                       INCLUDE_DIRS ""
                       REQUIRES esp_wifi esp_event esp_netif nvs_flash esp_http_server esp_http_client esp-tls
)

target_add_binary_data(${COMPONENT_TARGET} "supabase_root_ca.pem" TEXT)