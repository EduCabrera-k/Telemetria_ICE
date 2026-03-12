module AppTelemetria {
    struct DatosSistema {
        string nombreUsuario;
        double cpuUso;
        double ramUsadaGB;
        double ramTotalGB;
        string tiempoActivo;
    };

    interface MonitorCentral {
        // Los agentes de Python usan esto para "empujar" sus datos
        void reportarMetricas(DatosSistema datos);
    };
};