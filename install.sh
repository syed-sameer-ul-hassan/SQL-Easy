#!/bin/bash
set -e

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

spinner() {
    local pid=$1 msg="$2" i=0
    local f='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while kill -0 "$pid" 2>/dev/null; do
        printf "\r  ${Y}${f:$((i % 10)):1}${W}  ${C}%-26s${W}  ${D}fetching...${W}" "$msg"
        sleep 0.08
        i=$(( i + 1 ))
    done
    printf "\r  ${G}✓${W}  ${G}%-26s${W}  done                    \n" "$msg"
}

run_bg() {
    local msg="$1"; shift
    ("$@" &>/dev/null) &
    spinner $! "$msg"
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
printf "%s\n" "$LINE"

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
        printf "  ${R}✗  Unsupported OS: %s  →  use install.ps1 on Windows${W}\n" "$OS"
        exit 1 ;;
esac

case "$MACH" in
    x86_64)  ARCH="amd64" ;;
    aarch64) ARCH="arm64" ;;
    arm64)   ARCH="arm64" ;;
    armv7l)  ARCH="arm"  ;;
    *)       ARCH="amd64" ;;
esac

info "Platform"  "$PLATFORM  ($MACH)"

if ! command -v python3 &>/dev/null; then
    fail "Python3"
    if [ "$PLATFORM" = "macOS" ]; then
        printf "  ${Y}    →  brew install python3${W}\n"
    elif [ "$PLATFORM" = "Termux" ]; then
        printf "  ${Y}    →  pkg install python${W}\n"
    else
        printf "  ${Y}    →  sudo apt install python3${W}\n"
    fi
    exit 1
fi
info "Python3"  "$(python3 --version 2>&1 | cut -d' ' -f2)"

section "INSTALL PATH"

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"

if [ ! -f "$INSTALL_DIR/sqleasy" ]; then
    printf "  ${Y}[*] One-line install detected — cloning repository...${W}\n"
    if ! command -v git &>/dev/null; then
        fail "git"
        if   [ "$PLATFORM" = "Termux" ]; then printf "  ${Y}    →  pkg install git${W}\n"
        elif [ "$PLATFORM" = "macOS"  ]; then printf "  ${Y}    →  brew install git${W}\n"
        else                                  printf "  ${Y}    →  sudo apt install git${W}\n"
        fi
        exit 1
    fi
    if [ "$PLATFORM" = "Termux" ]; then
        CLONE_DIR="${PREFIX}/share/sqleasy"
    else
        CLONE_DIR="${HOME}/.local/share/sqleasy"
    fi
    rm -rf "$CLONE_DIR"
    git clone --depth=1 https://github.com/syed-sameer-ul-hassan/SQL-Easy.git "$CLONE_DIR" \
        || { printf "  ${R}✗  git clone failed. Check internet connection.${W}\n"; exit 1; }
    INSTALL_DIR="$CLONE_DIR"
    printf "  ${G}✓  Cloned to %s${W}\n" "$INSTALL_DIR"
fi

mkdir -p "$HOME/.config/sqleasy"
echo "$INSTALL_DIR" > "$HOME/.config/sqleasy/path"
info "Install path"  "$INSTALL_DIR"
info "Config"        "~/.config/sqleasy/path"

section "BACKEND TOOLS"

ask() {
    printf "  ${B}%-14s${W}  ${D}%s${W}\n" "$1" "$2"
    printf "  ${C}%-14s${W}  ${D}%s${W}\n" "" "$3"
    printf "  Install? ${B}[y/n]${W}  →  "; read -r ans
    [[ "$ans" =~ ^[Yy]$ ]]
}

printf "  ${Y}${B}Required Tools${W}  —  must have for the pipeline to work\n\n"

if ask "sqlmap" "SQL injection testing engine (detects and exploits vulns)" "uses apt"; then
    run_bg "sqlmap" ${USE_SUDO} apt install -y sqlmap unzip wget
else
    fail "sqlmap"
fi

if ask "subfinder" "Discovers all subdomains of the target domain" "binary download"; then
    run_bg "subfinder" bash -c "wget -q 'https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_${ARCH}.zip' -O /tmp/s.zip && unzip -q -o /tmp/s.zip subfinder -d /tmp/ && ${USE_SUDO} mv /tmp/subfinder ${BIN_DIR}/ && ${USE_SUDO} chmod +x ${BIN_DIR}/subfinder"
else
    fail "subfinder"
fi

if ask "httpx" "Probes which subdomains are actually alive" "binary download"; then
    run_bg "httpx" bash -c "wget -q 'https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_${ARCH}.zip' -O /tmp/h.zip && unzip -q -o /tmp/h.zip httpx -d /tmp/ && ${USE_SUDO} mv /tmp/httpx ${BIN_DIR}/ && ${USE_SUDO} chmod +x ${BIN_DIR}/httpx"
else
    fail "httpx"
fi

if ask "katana" "Crawls live hosts to find injectable URLs with parameters" "binary download"; then
    run_bg "katana" bash -c "wget -q 'https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_${ARCH}.zip' -O /tmp/k.zip && unzip -q -o /tmp/k.zip katana -d /tmp/ && ${USE_SUDO} mv /tmp/katana ${BIN_DIR}/ && ${USE_SUDO} chmod +x ${BIN_DIR}/katana"
else
    fail "katana"
fi

printf "\n  ${Y}${B}Optional Tools${W}  —  enhance results but the pipeline works without them\n\n"

if ask "nuclei" "Broad vulnerability scanner (runs after SQLMap for extra coverage)" "binary download"; then
    run_bg "nuclei" bash -c "wget -q 'https://github.com/projectdiscovery/nuclei/releases/download/v3.3.9/nuclei_3.3.9_linux_${ARCH}.zip' -O /tmp/n.zip && unzip -q -o /tmp/n.zip nuclei -d /tmp/ && ${USE_SUDO} mv /tmp/nuclei ${BIN_DIR}/ && ${USE_SUDO} chmod +x ${BIN_DIR}/nuclei"
else
    skip "nuclei"
fi

if ask "gau" "Historical URL harvester (gets old URLs from internet archives)" "binary download"; then
    run_bg "gau" bash -c "wget -q 'https://github.com/lc/gau/releases/download/v2.2.4/gau_2.2.4_linux_${ARCH}.tar.gz' -O /tmp/gau.tar.gz && tar -xzf /tmp/gau.tar.gz -C /tmp/ gau && ${USE_SUDO} mv /tmp/gau ${BIN_DIR}/ && ${USE_SUDO} chmod +x ${BIN_DIR}/gau"
else
    skip "gau"
fi

if command -v pip3 &>/dev/null; then
    if ask "arjun" "Hidden parameter bruteforcer (finds params not visible in page source)" "pip3 install"; then
        run_bg "arjun" pip3 install arjun -q
    else
        skip "arjun"
    fi
else
    skip "arjun"
fi

section "GLOBAL COMMAND"
run_bg "sqleasy  →  ${BIN_DIR}" bash -c "${USE_SUDO} cp '$INSTALL_DIR/sqleasy' '${BIN_DIR}/sqleasy' && ${USE_SUDO} chmod +x '${BIN_DIR}/sqleasy'"

section "VERIFICATION"
MISSING=0
for tool in subfinder httpx katana sqlmap sqleasy; do
    if command -v "$tool" &>/dev/null; then ok   "$tool"
    else                                    fail "$tool"; MISSING=$(( MISSING + 1 ))
    fi
done
echo ""
for tool in nuclei arjun gau; do
    if command -v "$tool" &>/dev/null; then ok   "$tool  (optional)"
    else                                    skip "$tool"
    fi
done

printf "\n%s\n" "$LINE"
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
