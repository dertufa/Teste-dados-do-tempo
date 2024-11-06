// Inicializa o mapa
var map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Evento de clique no mapa
map.on('click', function(e) {
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;

    // Enviar dados de coordenadas ao servidor
    fetch('/coletar_dados', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ latitude: lat, longitude: lng })
    })
    .then(response => response.json())
    .then(data => {
        // Criar um conteúdo HTML para o popup com os dados recebidos
        var popupContent = `
            <div style="font-size:14px;">
                <strong>Dados Climáticos:</strong><br>
                Latitude: ${data.latitude}<br>
                Longitude: ${data.longitude}<br>
                Temperatura: ${data.temperatura} °C<br>
                Precipitação: ${data.precipitacao} mm<br>
                Umidade: ${data.umidade} %<br>
                Velocidade do Vento: ${data.velocidade_vento} m/s<br>
                Radiação UV: ${data.radiacao_uv}<br>
                CO₂: ${data.concentracao_co2}<br>
                Data e Hora: ${data.data_hora}
            </div>
        `;

        // Exibir os dados em um popup no local do clique
        L.popup()
            .setLatLng(e.latlng)
            .setContent(popupContent)
            .openOn(map);
    })
    .catch(error => {
        console.error("Erro ao coletar dados:", error);
    });
});
