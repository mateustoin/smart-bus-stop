/* Parser: smart bus stop */
const ignore_vars = [];

/**
* This is the main function to parse the payload. Everything else doesn't require your attention.
* @param {String} payload_raw
* @returns {Object} containing key and value to TagoIO
*/
function parsePayload(payload_raw) {
    try {
        // COnverte payload recebido para formato hexadecimal
        const buffer = Buffer.from(payload_raw, 'hex');

        // O payload é composto por:
        // Byte 0 - identificador de evento (0x00: mensagem comum; 0x01: emergência)
        // Byte 1 - contador de pessoas
        var id_evento = buffer.readInt8(0);
        var contador_pessoas = buffer.readInt8(1);
        
        // Informa status do ponto de ônibus com base na mensagem recebida
        var status_ponto_onibus;
        switch(id_evento)
        {
          case 0:
              status_ponto_onibus = "Ponto de ônibus sem emergência";
              break;

          case 1:
              status_ponto_onibus = "EMERGÊNCIA!";
              break;   

          default:
              status_ponto_onibus = "Desconhecido";     
              break;
        }
        
        // Fixa a latitude e longitude no IC3 (para testes)
        var latitude = -22.813407;
        var longitude = -47.0643614;

        // More information about buffers can be found here: https://nodejs.org/api/buffer.html
        const data = [
            { variable: 'id_evento', value: id_evento, unit: ' ' },
            { variable: 'contador_pessoas', value: contador_pessoas, unit: ' ' },
            { variable: 'status_ponto_onibus', value: status_ponto_onibus, unit: ' ' },
            { variable: "localizacao", value: "localizacao", "location": { "lat": latitude, "lng": longitude } },
        ];
        return data;
    }
    catch (e) {
        console.log(e);
        return [{ variable: 'parse_error', value: e.message }];
    }
}

// Remove/filtra variaveis indesejadas e faz parse to payload para JSON
payload = payload.filter(x => !ignore_vars.includes(x.variable));

const payload_raw = payload.find(x => x.variable === 'payload_raw' || x.variable === 'payload' || x.variable === 'data');
if (payload_raw) {
    const { value, serie, time } = payload_raw;

    if (value) {
        payload = payload.concat(parsePayload(value).map(x => ({ ...x, serie, time: x.time || time })));
    }
}