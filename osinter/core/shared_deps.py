DEP_FFUF = [
    {
        "name": "Download ffuf",
        "unarchive": {
            "src": "https://github.com/ffuf/ffuf/releases/download/v#{OSINTER_DEPS_FFUF_VERSION}/ffuf_#{OSINTER_DEPS_FFUF_VERSION}_#{OSINTER_OS}_#{OSINTER_CPU_ARCH}.tar.gz",
            "include": "ffuf",
            "dest": "#{OSINTER_TOOLS}",
            "remote_src": True,
        },
    }
]

DEP_DOCKER = [
    {
        "name": "Check if Docker is already installed",
        "command": "docker --version",
        "register": "docker_installed",
        "ignore_errors": True,
    },
    {
        "name": "Install Docker (Non-Debian)",
        "package": {"name": "docker", "state": "present"},
        "become": True,
        "when": "ansible_facts['os_family'] != 'Debian' and docker_installed.rc != 0",
    },
    {
        "name": "Install Docker (Debian)",
        "package": {
            "name": "docker.io",
            "state": "present",
        },
        "become": True,
        "when": "ansible_facts['os_family'] == 'Debian' and docker_installed.rc != 0",
    },
]

DEP_MASSDNS = [
    {
        "name": "install dev tools",
        "package": {"name": ["gcc", "git", "make"], "state": "present"},
        "become": True,
        "ignore_errors": True,
    },
    {
        "name": "Download massdns source code",
        "git": {
            "repo": "https://github.com/blechschmidt/massdns.git",
            "dest": "#{OSINTER_TEMP}/massdns",
            "single_branch": True,
            "version": "master",
        },
    },
    {
        "name": "Build massdns (Linux)",
        "command": {"chdir": "#{OSINTER_TEMP}/massdns", "cmd": "make", "creates": "#{OSINTER_TEMP}/massdns/bin/massdns"},
        "when": "ansible_facts['system'] == 'Linux'",
    },
    {
        "name": "Build massdns (non-Linux)",
        "command": {
            "chdir": "#{OSINTER_TEMP}/massdns",
            "cmd": "make nolinux",
            "creates": "#{OSINTER_TEMP}/massdns/bin/massdns",
        },
        "when": "ansible_facts['system'] != 'Linux'",
    },
    {
        "name": "Install massdns",
        "copy": {"src": "#{OSINTER_TEMP}/massdns/bin/massdns", "dest": "#{OSINTER_TOOLS}/", "mode": "u+x,g+x,o+x"},
    },
]

DEP_CHROMIUM = [
    {
        "name": "Install Chromium (Non-Debian)",
        "package": {"name": "chromium", "state": "present"},
        "become": True,
        "when": "ansible_facts['os_family'] != 'Debian'",
        "ignore_errors": True,
    },
    {
        "name": "Install Chromium dependencies (Ubuntu 24.04)",
        "package": {
            "name": "libasound2t64,libatk-bridge2.0-0,libatk1.0-0,libcairo2,libcups2,libdrm2,libgbm1,libnss3,libpango-1.0-0,libglib2.0-0,libxcomposite1,libxdamage1,libxfixes3,libxkbcommon0,libxrandr2",
            "state": "present",
        },
        "become": True,
        "when": "ansible_facts['distribution'] == 'Ubuntu' and ansible_facts['distribution_version'] == '24.04'",
        "ignore_errors": True,
    },
    {
        "name": "Install Chromium dependencies (Other Debian-based)",
        "package": {
            "name": "libasound2,libatk-bridge2.0-0,libatk1.0-0,libcairo2,libcups2,libdrm2,libgbm1,libnss3,libpango-1.0-0,libglib2.0-0,libxcomposite1,libxdamage1,libxfixes3,libxkbcommon0,libxrandr2",
            "state": "present",
        },
        "become": True,
        "when": "ansible_facts['os_family'] == 'Debian' and not (ansible_facts['distribution'] == 'Ubuntu' and ansible_facts['distribution_version'] == '24.04')",
        "ignore_errors": True,
    },
    {
        "name": "Get latest Chromium version (Debian)",
        "uri": {
            "url": "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2FLAST_CHANGE?alt=media",
            "return_content": True,
        },
        "register": "chromium_version",
        "when": "ansible_facts['os_family'] == 'Debian'",
        "ignore_errors": True,
    },
    {
        "name": "Download Chromium (Debian)",
        "unarchive": {
            "src": "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F{{ chromium_version.content }}%2Fchrome-linux.zip?alt=media",
            "remote_src": True,
            "dest": "#{OSINTER_TOOLS}",
            "creates": "#{OSINTER_TOOLS}/chrome-linux",
        },
        "when": "ansible_facts['os_family'] == 'Debian'",
        "ignore_errors": True,
    },
    # Because Ubuntu is a special snowflake, we have to bend over backwards to fix the chrome sandbox
    # see https://chromium.googlesource.com/chromium/src/+/main/docs/security/apparmor-userns-restrictions.md
    {
        "name": "Chown chrome_sandbox to root:root",
        "command": {"cmd": "chown -R root:root #{OSINTER_TOOLS}/chrome-linux/chrome_sandbox"},
        "when": "ansible_facts['os_family'] == 'Debian'",
        "become": True,
    },
    {
        "name": "Chmod chrome_sandbox to 4755",
        "command": {"cmd": "chmod -R 4755 #{OSINTER_TOOLS}/chrome-linux/chrome_sandbox"},
        "when": "ansible_facts['os_family'] == 'Debian'",
        "become": True,
    },
]

DEP_MASSCAN = [
    {
        "name": "install os deps (Debian)",
        "package": {"name": ["gcc", "git", "make", "libpcap0.8-dev"], "state": "present"},
        "become": True,
        "when": "ansible_facts['os_family'] == 'Debian'",
        "ignore_errors": True,
    },
    {
        "name": "install dev tools (Non-Debian)",
        "package": {"name": ["gcc", "git", "make", "libpcap"], "state": "present"},
        "become": True,
        "when": "ansible_facts['os_family'] != 'Debian'",
        "ignore_errors": True,
    },
    {
        "name": "Download masscan source code",
        "git": {
            "repo": "https://github.com/robertdavidgraham/masscan.git",
            "dest": "#{OSINTER_TEMP}/masscan",
            "single_branch": True,
            "version": "master",
        },
    },
    {
        "name": "Build masscan",
        "command": {
            "chdir": "#{OSINTER_TEMP}/masscan",
            "cmd": "make -j",
            "creates": "#{OSINTER_TEMP}/masscan/bin/masscan",
        },
    },
    {
        "name": "Install masscan",
        "copy": {"src": "#{OSINTER_TEMP}/masscan/bin/masscan", "dest": "#{OSINTER_TOOLS}/", "mode": "u+x,g+x,o+x"},
    },
]

DEP_JAVA = [
    {
        "name": "Check if Java is installed",
        "command": "which java",
        "register": "java_installed",
        "ignore_errors": True,
    },
    {
        "name": "Install latest JRE (Debian)",
        "package": {"name": ["default-jre"], "state": "present"},
        "become": True,
        "when": "ansible_facts['os_family'] == 'Debian' and java_installed.rc != 0",
    },
    {
        "name": "Install latest JRE (Arch)",
        "package": {"name": ["jre-openjdk"], "state": "present"},
        "become": True,
        "when": "ansible_facts['os_family'] == 'Archlinux' and java_installed.rc != 0",
    },
    {
        "name": "Install latest JRE (Fedora)",
        "package": {"name": ["which", "java-latest-openjdk-headless"], "state": "present"},
        "become": True,
        "when": "ansible_facts['os_family'] == 'RedHat' and java_installed.rc != 0",
    },
    {
        "name": "Install latest JRE (Alpine)",
        "package": {"name": ["openjdk11"], "state": "present"},
        "become": True,
        "when": "ansible_facts['os_family'] == 'Alpine' and java_installed.rc != 0",
    },
]

# shared module dependencies -- ffuf, massdns, chromium, etc.
SHARED_DEPS = {}
for var, val in list(locals().items()):
    if var.startswith("DEP_") and isinstance(val, list):
        var = var.split("_", 1)[-1].lower()
        SHARED_DEPS[var] = val
