// Inicializa o mapa
var map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Variável para armazenar o perímetro (caso precise remover do mapa antes de adicionar outro)
var cityPerimeter;

// Evento de clique no mapa
map.on('click', function(e) {
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;

    // Enviar dados de coordenadas ao servidor para coletar perímetro
    fetch('/coletar_dados', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ latitude: lat, longitude: lng })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Dados recebidos do servidor:", data);

        // Verificar se o dado de perímetro foi recebido
        if (data && data.perimetro && data.perimetro.length > 0) {
            // Remover o perímetro anterior, se existir
            if (cityPerimeter) {
                map.removeLayer(cityPerimeter);
            }

            // Desenhar o perímetro da cidade no mapa usando os dados recebidos
            cityPerimeter = L.polygon(data.perimetro, { color: 'blue' }).addTo(map);

            // Criar conteúdo para o popup com os dados recebidos
            var popupContent = `
                <div style="font-size:14px;">
                    <strong>Dados da Cidade:</strong><br>
                    Cidade: ${data.cidade}<br>
                    Perímetro: ${data.perimetro.length} pontos<br>
                    Área: ${data.area} km²<br>
                </div>
            `;

            // Exibir o popup no local do clique
            L.popup()
                .setLatLng(e.latlng)
                .setContent(popupContent)
                .openOn(map);
        } else {
            console.error("Dados de perímetro não recebidos ou inválidos:", data);
            alert("Não foi possível obter o perímetro da cidade clicada.");
        }
    })
    .catch(error => {
        console.error("Erro ao coletar dados:", error);
        alert("Erro ao coletar dados do servidor.");
    });
});
