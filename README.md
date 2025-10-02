# Karrio Community Plugins
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkarrioapi%2Fcommunity.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkarrioapi%2Fcommunity?ref=badge_shield)


Welcome to the Karrio Community Plugins repository! This is a public collection of community-contributed plugins that extend Karrio's functionality. Think of it as a "poor-man's plugin marketplace" where developers can share and discover useful shipping integrations and tools.

## Table of Contents

### Carrier Connectors

- [DHL Express](#dhl-express)
- [FedEx](#fedex)
- [UPS](#ups)
- [USPS](#usps)
- [Canada Post](#canada-post)
- [Australia Post](#australia-post)
- [La Poste](#la-poste)
- [Purolator](#purolator)
- [SEKO](#seko)
- [Sendle](#sendle)
- [DHL Parcel DE](#dhl-parcel-de)
- [DHL Universal](#dhl-universal)
- [DHL Poland](#dhl-poland)
- [USPS International](#usps-international)

### Community Carrier Plugins

- [Karrio Community Plugins](#karrio-community-plugins)
  - [Table of Contents](#table-of-contents)
    - [Carrier Connectors](#carrier-connectors)
    - [Community Carrier Plugins](#community-carrier-plugins)
    - [Utility Plugins](#utility-plugins)
  - [About This Repository](#about-this-repository)
  - [How to Use](#how-to-use)
  - [Contributing](#contributing)
    - [Plugin Development Resources](#plugin-development-resources)
  - [Available Plugins](#available-plugins)
    - [Carrier Connectors](#carrier-connectors-1)
      - [DHL Express](#dhl-express)
      - [FedEx](#fedex)
      - [UPS](#ups)
      - [USPS](#usps)
      - [Canada Post](#canada-post)
      - [Australia Post](#australia-post)
      - [La Poste](#la-poste)
      - [Purolator](#purolator)
      - [SEKO](#seko)
      - [Sendle](#sendle)
      - [DHL Parcel DE](#dhl-parcel-de)
      - [DHL Universal](#dhl-universal)
      - [DHL Poland](#dhl-poland)
      - [USPS International](#usps-international)
    - [Community Carrier Plugins](#community-carrier-plugins-1)
      - [Aramex](#aramex)
      - [Allied Express](#allied-express)
      - [Allied Express Local](#allied-express-local)
      - [Amazon Shipping](#amazon-shipping)
      - [Asendia US](#asendia-us)
      - [BoxKnight](#boxknight)
      - [Canpar](#canpar)
      - [BPost](#bpost)
      - [Colissimo](#colissimo)
      - [Dicom](#dicom)
      - [EasyPost](#easypost)
      - [EasyShip](#easyship)
      - [Hay Post](#hay-post)
      - [Geodis](#geodis)
      - [Locate2U](#locate2u)
      - [NationEx](#nationex)
      - [Roadie](#roadie)
      - [TGE](#tge)
      - [Royal Mail](#royal-mail)
      - [Zoom2U](#zoom2u)
      - [TNT](#tnt)
      - [Chronopost](#chronopost)
      - [DPD](#dpd)
      - [Eshipper](#eshipper)
      - [Freightcom](#freightcom)
      - [Sapient](#sapient)
    - [Utility Plugins](#utility-plugins-1)
      - [Address Complete](#address-complete)
      - [Google Geocoding](#google-geocoding)
  - [License](#license)
  - [Support](#support)


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkarrioapi%2Fcommunity.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkarrioapi%2Fcommunity?ref=badge_large)

### Utility Plugins

- [Address Complete](#address-complete)
- [Google Geocoding](#google-geocoding)

## About This Repository

This repository serves as a public collection of community-contributed plugins for [Karrio](https://github.com/karrioapi/karrio), the open-source shipping integration platform. Unlike the enterprise-focused [Karrio Insiders](https://github.com/karrioapi/karrio-insiders), this repository is completely open-source and community-driven.

## How to Use

Each plugin in this repository can be installed independently. The installation method varies depending on the plugin type:

- Python packages can be installed via pip
- Non-Python packages (like Address Complete) can be downloaded directly
- Some plugins may require additional setup steps

## Contributing

We welcome contributions! To add your plugin to this repository:

1. Fork this repository
2. Create a new directory for your plugin under the appropriate category
3. Include a README.md with:
   - Plugin description
   - Installation instructions
   - Usage examples
   - Dependencies
   - License information
4. Submit a pull request

### Plugin Development Resources

- [Karrio Plugin Development Guide](https://docs.karrio.io/plugins/development)
- [Karrio SDK Documentation](https://docs.karrio.io/sdk)
- [Example Plugins](https://github.com/karrioapi/karrio/tree/main/plugins)

## Available Plugins

### Carrier Connectors

#### DHL Express

```bash
pip install karrio.dhl_express
```

#### FedEx

```bash
pip install karrio.fedex
```

#### UPS

```bash
pip install karrio.ups
```

#### USPS

```bash
pip install karrio.usps
```

#### Canada Post

```bash
pip install karrio.canadapost
```

#### Australia Post

```bash
pip install karrio.australiapost
```

#### La Poste

```bash
pip install karrio.laposte
```

#### Purolator

```bash
pip install karrio.purolator
```

#### SEKO

```bash
pip install karrio.seko
```

#### Sendle

```bash
pip install karrio.sendle
```

#### DHL Parcel DE

```bash
pip install karrio.dhl_parcel_de
```

#### DHL Universal

```bash
pip install karrio.dhl_universal
```

#### DHL Poland

```bash
pip install karrio.dhl_poland
```

#### USPS International

```bash
pip install karrio.usps_international
```

### Community Carrier Plugins

#### Aramex

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/aramex
```

#### Allied Express

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/allied_express
```

#### Allied Express Local

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/allied_express_local
```

#### Amazon Shipping

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/amazon_shipping
```

#### Asendia US

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/asendia_us
```

#### BoxKnight

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/boxknight
```

#### Canpar

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/canpar
```

#### BPost

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/bpost
```

#### Colissimo

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/colissimo
```

#### Dicom

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/dicom
```

#### EasyPost

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/easypost
```

#### EasyShip

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/easyship
```

#### Hay Post

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/hay_post
```

#### Geodis

```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/geodis
```

#### Locate2U
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/locate2u
```

#### NationEx
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/nationex
```

#### Roadie
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/roadie
```

#### TGE
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/tge
```

#### Royal Mail
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/royalmail
```

#### Zoom2U
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/zoom2u
```

#### TNT
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/tnt
```

#### Chronopost
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/chronopost
```

#### DPD
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/dpd
```

#### Eshipper
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/eshipper
```

#### Freightcom
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/freightcom
```

#### Sapient
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/sapient
```

### Utility Plugins

#### Address Complete
Download the latest release from the [Address Complete releases page](https://github.com/karrioapi/karrio-community/releases) and follow the installation instructions in the plugin's README.

#### Google Geocoding
```bash
pip install git+https://github.com/karrioapi/karrio-community.git#subdirectory=community/plugins/googlegeocoding
```

## License

This repository is licensed under the [Apache License 2.0](LICENSE). Each plugin may have its own license - please check the individual plugin directories for specific license information.

## Support

For support with community plugins:
- Open an issue in this repository
- Join our [Discord community](https://discord.gg/gS88uE7sEx)
- Check the [Karrio documentation](https://docs.karrio.io)