#!/bin/bash

R='\033[0;31m'
G='\033[0;32m'
Y='\033[0;33m'
C='\033[0;36m'
B='\033[1m'
D='\033[2m'
W='\033[0m'

LINE='  ──────────────────────────────────────────────────────'

section() { printf "\n%s\n\n  ${B}${C}▸  %s${W}\n\n" "$LINE" "$1"; }
info()    { printf "  ${D}%-22s${W}  %s\n" "$1" "$2"; }
ok()      { printf "  ${G}✓${W}  ${G}%-26s${W}  ready\n"    "$1"; }
skip()    { printf "  ${D}○  %-26s  optional${W}\n"          "$1"; }
fail()    { printf "  ${R}✗${W}  ${R}%-26s${W}  missing\n"  "$1"; }
ask() {
    printf "  ${B}%-14s${W}  ${D}%s${W}\n" "$1" "$2"
    printf "  Install? ${B}[y/n]${W}  →  "; read -r ans
    [[ "$ans" =~ ^[Yy]$ ]]
}

printf "${C}"
cat << 'BANNER'
  ██████   █████   ██▓       ▓█████ ▄▄▄        ██████▓██   ██▓
▒██    ▒ ▒██▓  ██▒▓██▒       ▓█   ▀▒████▄    ▒██    ▒ ▒██  ██▒
░ ▓██▄   ▒██▒  ██░▒██░       ▒███  ▒██  ▀█▄  ░ ▓██▄    ▒██ ██░
  ▒   ██▒░██  █▀ ░▒██░       ▒▓█  ▄░██▄▄▄▄██   ▒   ██▒ ░ ▐██▓░
▒██████▒▒░▒███▒█▄ ░██████▒   ░▒████▒▓█   ▓██▒▒██████▒▒ ░ ██▒▓░
▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░   ░░ ▒░ ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ██▒▒▒
░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░    ░ ░  ░ ▒   ▒▒ ░░ ░▒  ░ ░▓██ ░▒░
░  ░  ░     ░   ░   ░ ░         ░    ░   ▒   ░  ░  ░  ▒ ▒ ░░
      ░      ░        ░  ░      ░  ░     ░  ░      ░  ░ ░
BANNER
printf "${W}\n"
printf "  ${B}${Y}SQL Easy  ·  Installer  ·  v1.2.0${W}   ${D}sqleasy.orildo.sbs${W}\n"
printf "%s\n\n" "$LINE"

section "SYSTEM CHECK"

OS="$(uname -s)"
MACH="$(uname -m)"
case "$OS" in
    Linux*)
        if [ -n "$TERMUX_VERSION" ]; then
            PLATFORM="Termux"
            BIN_DIR="$PREFIX/bin"
            USE_SUDO=""
        else
            PLATFORM="Linux"
            BIN_DIR="/usr/local/bin"
            USE_SUDO="sudo"
        fi
        ;;
    Darwin*)
        PLATFORM="macOS"
        BIN_DIR="/usr/local/bin"
        USE_SUDO="sudo"
        ;;
    *)
        printf "  ${R}Unsupported OS: %s${W}\n" "$OS"
        exit 1
        ;;
esac

case "$MACH" in
    x86_64)  ARCH="amd64" ;;
    aarch64) ARCH="arm64" ;;
    arm64)   ARCH="arm64" ;;
    armv7l)  ARCH="arm"  ;;
    *)       ARCH="amd64" ;;
esac

info "Platform" "$PLATFORM ($MACH)"

if ! command -v python3 &>/dev/null; then
    fail "python3"
    printf "  ${Y}Install python3 first, then re-run this script.${W}\n"
    exit 1
fi
ok "python3"

section "INSTALL PATH"

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"

if [ ! -f "$INSTALL_DIR/sqleasy" ]; then
    printf "\n  One-line install detected — cloning repository...\n"
    if ! command -v git &>/dev/null; then
        fail "git"
        printf "  ${Y}Install git first.${W}\n"
        exit 1
    fi
    if [ "$PLATFORM" = "Termux" ]; then
        CLONE_DIR="${PREFIX}/share/sqleasy"
    else
        CLONE_DIR="${HOME}/.local/share/sqleasy"
    fi
    rm -rf "$CLONE_DIR"
    if ! git clone --depth=1 https://github.com/syed-sameer-ul-hassan/SQL-Easy.git "$CLONE_DIR"; then
        printf "  ${R}git clone failed.${W}\n"
        exit 1
    fi
    INSTALL_DIR="$CLONE_DIR"
    ok "cloned to $INSTALL_DIR"
fi

mkdir -p "$HOME/.config/sqleasy"
echo "$INSTALL_DIR" > "$HOME/.config/sqleasy/path"
info "Install path" "$INSTALL_DIR"
info "Config"        "~/.config/sqleasy/path"

section "BACKEND TOOLS"

_TMPDIR="${TMPDIR:-/tmp}"
if [ "$PLATFORM" = "Termux" ]; then
    _TMPDIR="${PREFIX}/tmp"
    mkdir -p "$_TMPDIR"
fi

if ! command -v wget &>/dev/null || ! command -v unzip &>/dev/null; then
    if [ "$PLATFORM" = "Termux" ]; then
        printf "  Installing wget & unzip via pkg...\n"
        pkg install -y wget unzip &>/dev/null || apt install -y wget unzip &>/dev/null
    else
        printf "  Installing wget & unzip...\n"
        ${USE_SUDO} apt install -y wget unzip &>/dev/null
    fi
fi

install_binary() {
    local name="$1" url="$2" dest="$3"
    local tmpfile="${_TMPDIR}/sqleasy_${name}_$$"

    printf "\n  Installing %s...\n" "$name"
    if ! wget -q "$url" -O "$tmpfile"; then
        printf "  ${R}✗  %s download failed${W}\n" "$name"
        return 1
    fi

    if [ "$dest" = "zip" ]; then
        if ! unzip -q -o "$tmpfile" "$name" -d "${_TMPDIR}/"; then
            printf "  ${R}✗  %s unzip failed${W}\n" "$name"
            rm -f "$tmpfile"
            return 1
        fi
        tmpfile="${_TMPDIR}/$name"
    elif [ "$dest" = "tar" ]; then
        if ! tar -xzf "$tmpfile" -C "${_TMPDIR}/" "$name"; then
            printf "  ${R}✗  %s tar extract failed${W}\n" "$name"
            rm -f "$tmpfile"
            return 1
        fi
        tmpfile="${_TMPDIR}/$name"
    fi

    if [ ! -f "$tmpfile" ]; then
        printf "  ${R}✗  %s binary not found after extract${W}\n" "$name"
        return 1
    fi

    if ! ${USE_SUDO} mv "$tmpfile" "${BIN_DIR}/${name}"; then
        printf "  ${R}✗  %s move to %s failed${W}\n" "$name" "$BIN_DIR"
        return 1
    fi
    ${USE_SUDO} chmod +x "${BIN_DIR}/${name}"
    ok "$name"
}

printf "\n  ${Y}Required Tools${W}\n"

_pkg_cmd() {
    if [ "$PLATFORM" = "Termux" ]; then
        echo "pkg install -y"
    else
        echo "${USE_SUDO} apt install -y"
    fi
}

install_sqlmap() {
    if [ "$PLATFORM" = "Termux" ]; then
        SQLMAP_DIR="${PREFIX}/share/sqlmap"
    else
        SQLMAP_DIR="${HOME}/.local/share/sqlmap"
    fi

    printf "  Trying: clone sqlmap repo...\n"
    rm -rf "$SQLMAP_DIR"
    if command -v git &>/dev/null && \
       git clone --depth=1 https://github.com/sqlmapproject/sqlmap.git "$SQLMAP_DIR" &>/dev/null; then
        ${USE_SUDO} tee "${BIN_DIR}/sqlmap" >/dev/null <<EOF
#!/bin/bash
exec python3 "$SQLMAP_DIR/sqlmap.py" "\$@"
EOF
        ${USE_SUDO} chmod +x "${BIN_DIR}/sqlmap"
        ok "sqlmap (cloned)"
        return 0
    fi

    _pip="pip3"
    if [ "$PLATFORM" = "Termux" ] && ! command -v pip3 &>/dev/null && command -v pip &>/dev/null; then
        _pip="pip"
    fi
    printf "  Trying: pip install sqlmap...\n"
    if command -v $_pip &>/dev/null && $_pip install sqlmap -q &>/dev/null; then
        ok "sqlmap (pip)"
        return 0
    fi

    printf "  Trying: package manager...\n"
    if $(_pkg_cmd) sqlmap &>/dev/null; then
        ok "sqlmap (package)"
        return 0
    fi

    fail "sqlmap"
    printf "  ${Y}  All methods failed. Manually install sqlmap then re-run.${W}\n"
    return 1
}

if command -v sqlmap &>/dev/null; then
    ok "sqlmap (already exists)"
elif ask "sqlmap" "SQL injection engine (install)"; then
    install_sqlmap
else
    fail "sqlmap"
fi

if command -v subfinder &>/dev/null; then
    ok "subfinder (already exists)"
elif ask "subfinder" "subdomain discovery (binary download)"; then
    install_binary "subfinder" \
        "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_${ARCH}.zip" \
        "zip"
else
    fail "subfinder"
fi

if command -v httpx &>/dev/null; then
    ok "httpx (already exists)"
elif ask "httpx" "live host prober (binary download)"; then
    install_binary "httpx" \
        "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_${ARCH}.zip" \
        "zip"
else
    fail "httpx"
fi

if command -v katana &>/dev/null; then
    ok "katana (already exists)"
elif ask "katana" "URL crawler (binary download)"; then
    install_binary "katana" \
        "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_${ARCH}.zip" \
        "zip"
else
    fail "katana"
fi

printf "\n  ${Y}Optional Tools${W}\n"

if command -v nuclei &>/dev/null; then
    ok "nuclei (already exists)"
elif ask "nuclei" "vulnerability scanner (binary download)"; then
    install_binary "nuclei" \
        "https://github.com/projectdiscovery/nuclei/releases/download/v3.3.9/nuclei_3.3.9_linux_${ARCH}.zip" \
        "zip"
else
    skip "nuclei"
fi

if command -v gau &>/dev/null; then
    ok "gau (already exists)"
elif ask "gau" "historical URL harvester (binary download)"; then
    install_binary "gau" \
        "https://github.com/lc/gau/releases/download/v2.2.4/gau_2.2.4_linux_${ARCH}.tar.gz" \
        "tar"
else
    skip "gau"
fi

_pip_cmd="pip3"
if [ "$PLATFORM" = "Termux" ] && ! command -v pip3 &>/dev/null && command -v pip &>/dev/null; then
    _pip_cmd="pip"
fi

if command -v arjun &>/dev/null; then
    ok "arjun (already exists)"
elif command -v "$_pip_cmd" &>/dev/null && ask "arjun" "hidden parameter finder (pip install)"; then
    printf "  Installing arjun via %s...\n" "$_pip_cmd"
    if "$_pip_cmd" install arjun -q &>/dev/null; then
        ok "arjun"
    else
        skip "arjun (install failed)"
    fi
else
    skip "arjun"
fi

section "GLOBAL COMMAND"
printf "\n  Setting up sqleasy command...\n"
if command -v sqleasy &>/dev/null; then
    ok "sqleasy (already exists)"
elif ${USE_SUDO} cp "$INSTALL_DIR/sqleasy" "${BIN_DIR}/sqleasy" && ${USE_SUDO} chmod +x "${BIN_DIR}/sqleasy"; then
    ok "sqleasy"
else
    fail "sqleasy"
fi

section "VERIFICATION"

MISSING=0
for tool in subfinder httpx katana sqlmap sqleasy; do
    if command -v "$tool" &>/dev/null; then
        ok "$tool"
    else
        fail "$tool"
        MISSING=$(( MISSING + 1 ))
    fi
done

for tool in nuclei arjun gau; do
    if command -v "$tool" &>/dev/null; then
        ok "$tool (optional)"
    else
        skip "$tool"
    fi
done

printf "\n"
if [ "$MISSING" -eq 0 ]; then
    printf "\n  ${G}${B}✓  All tools ready.  SQL Easy v1.2.0 is installed.${W}\n"
else
    printf "\n  ${Y}✗  %d required tool(s) missing.  Run: sqleasy install${W}\n" "$MISSING"
fi

section "QUICK START"
printf "  ${C}sqleasy start${W}                    launch interactive scan\n"
printf "  ${C}sqleasy start -d example.com${W}     scan a domain directly\n"
printf "  ${C}sqleasy start -d t.com --dump${W}    full database extraction\n"
printf "  ${C}sqleasy logs${W}                     view previous results\n"
printf "  ${C}sqleasy report${W}                   full report summary\n"
printf "  ${C}sqleasy update${W}                   update to latest version\n"
printf "  ${C}sqleasy help${W}                     all commands and flags\n"
printf "\n%s\n" "$LINE"
printf "\n  ${D}sqleasy.orildo.sbs   ·   bugs: bug.orildo.sbs${W}\n\n"
