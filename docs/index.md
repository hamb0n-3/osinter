# Getting Started

<video controls="" autoplay="" name="media"><source src="https://github.com/blacklanternsecurity/osinter/assets/20261699/e539e89b-92ea-46fa-b893-9cde94eebf81" type="video/mp4"></video>

_A OSINTER scan in real-time - visualization with [VivaGraphJS](https://github.com/blacklanternsecurity/osinter-vivagraphjs)_

## Installation

!!! info "Supported Platforms"

    Only **Linux** is supported at this time. **Windows** and **macOS** are *not* supported. If you use one of these platforms, consider using [Docker](#Docker).

OSINTER offers multiple methods of installation, including **pipx** and **Docker**. If you're looking to tinker or write your own module, see [Setting up a Dev Environment](./dev/dev_environment.md).

### [Python (pip / pipx)](https://pypi.org/project/osinter/)


???+ note inline end

    `pipx` installs OSINTER inside its own virtual environment.

```bash
# stable version
pipx install osinter

# bleeding edge (dev branch)
pipx install --pip-args '\--pre' osinter

# execute osinter command
osinter --help
```

### [Docker](https://hub.docker.com/r/blacklanternsecurity/osinter)

Docker images are provided, along with helper script `osinter-docker.sh` to persist your scan data.

Scans are output to `~/.osinter/scans` (the usual place for OSINTER scan data).

```bash
# bleeding edge (dev)
docker run -it blacklanternsecurity/osinter --help

# stable
docker run -it blacklanternsecurity/osinter:stable --help

# helper script
git clone https://github.com/blacklanternsecurity/osinter && cd osinter
./osinter-docker.sh --help
```

Note: If you need to pass in a custom preset, you can do so by mapping the preset into the container:

```bash
# use the preset `my_preset.yml` from the current directory
docker run --rm -it \
  -v "$HOME/.osinter/scans:/root/.osinter/scans" \
  -v "$PWD/my_preset.yml:/my_preset.yml" \
  blacklanternsecurity/osinter -p /my_preset.yml
```

## Example Commands

Below are some examples of common scans.

<!-- OSINTER EXAMPLE COMMANDS -->
**Subdomains:**

```bash
# Perform a full subdomain enumeration on evilcorp.com
osinter -t evilcorp.com -p subdomain-enum
```

**Subdomains (passive only):**

```bash
# Perform a passive-only subdomain enumeration on evilcorp.com
osinter -t evilcorp.com -p subdomain-enum -rf passive
```

**Subdomains + port scan + web screenshots:**

```bash
# Port-scan every subdomain, screenshot every webpage, output to current directory
osinter -t evilcorp.com -p subdomain-enum -m portscan gowitness -n my_scan -o .
```

**Subdomains + basic web scan:**

```bash
# A basic web scan includes wappalyzer, robots.txt, and other non-intrusive web modules
osinter -t evilcorp.com -p subdomain-enum web-basic
```

**Web spider:**

```bash
# Crawl www.evilcorp.com up to a max depth of 2, automatically extracting emails, secrets, etc.
osinter -t www.evilcorp.com -p spider -c web.spider_distance=2 web.spider_depth=2
```

**Everything everywhere all at once:**

```bash
# Subdomains, emails, cloud buckets, port scan, basic web, web screenshots, nuclei
osinter -t evilcorp.com -p kitchen-sink
```
<!-- END OSINTER EXAMPLE COMMANDS -->

## API Keys

OSINTER works just fine without API keys. However, there are certain modules that need them to function. If you have API keys and want to make use of these modules, you can place them either in your preset:

```yaml title="my_preset.yml"
description: My custom subdomain enum preset

include:
  - subdomain-enum
  - cloud-enum

config:
  modules:
    shodan_dns:
      api_key: deadbeef
    virustotal:
      api_key: cafebabe
```

...in OSINTER's global YAML config (`~/.config/osinter/osinter.yml`):

Note: this will ensure the API keys are used in all scans, regardless of preset.

```yaml title="~/.config/osinter/osinter.yml"
modules:
  shodan_dns:
    api_key: deadbeef
  virustotal:
    api_key: cafebabe
```

...or directly on the command-line:

```bash
# specify API key with -c
osinter -t evilcorp.com -f subdomain-enum -c modules.shodan_dns.api_key=deadbeef modules.virustotal.api_key=cafebabe
```

For more information, see [Configuration](./scanning/configuration.md). For a full list of modules, including which ones require API keys, see [List of Modules](./modules/list_of_modules.md).

[Next Up: Scanning -->](./scanning/index.md){ .md-button .md-button--primary }
