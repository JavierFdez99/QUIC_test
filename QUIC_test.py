import asyncio
from aioquic.asyncio import QuicConnectionProtocol, connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, ProtocolNegotiated

class QUICClient(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            print(f"{self._quic._host}: Handshake completed, protocol {event.session_resumed}")
        if isinstance(event, ProtocolNegotiated):
            print(f"{self._quic._host}: Protocol negotiated, ALPN {event.alpn_protocol}")

async def check_quic_support(domain):
    config = QuicConfiguration(
        is_client=True,
        alpn_protocols=["h3-29", "h3-28", "h3-27", "h3"],  # Ajusta según necesidad
        verify_mode=False  # En un entorno de prueba
    )

    try:
        # Establece la conexión QUIC
        async with connect(domain, 443, configuration=config, create_protocol=QUICClient) as client:
            await asyncio.sleep(1)  # Espera a que los eventos se procesen
            return domain, True
    except Exception as e:
        print(f"Error connecting to {domain}: {str(e)}")
        return domain, False

async def main():
    domains = []
    # Asegúrate de que la ruta al archivo sites.txt sea la correcta
    with open('sites.txt', 'r') as file:
        domains = [line.strip() for line in file.readlines() if line.strip()]

    results = await asyncio.gather(*(check_quic_support(domain) for domain in domains))

    for domain, is_supported in results:
        print(f"{domain}: {'Soporta QUIC' if is_supported else 'No soporta QUIC'}")

if __name__ == '__main__':
    asyncio.run(main())
