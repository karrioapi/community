import karrio.core.metadata as metadata
import karrio.mappers.colissimo as mappers
import karrio.providers.colissimo.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="colissimo",
    label="Colissimo",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    service_levels=units.DEFAULT_SERVICES,
    # New fields
    website="https://www.colissimo.entreprise.laposte.fr/en",
    documentation="https://www.colissimo.entreprise.laposte.fr/en/tools-and-services",
    description="Envoi de colis en France et dans le monde entier, livraison à domicile ou en point de retrait, Colissimo vous offre un choix de services qui facilitent votre quotidien.",
)
