#!/bin/bash
set -e

R='\033[0;31m'
G='\033[0;32m'
Y='\033[0;33m'
C='\033[0;36m'
M='\033[0;35m'
B='\033[1m'
D='\033[2m'
W='\033[0m'

HR='  ------------------------------------------------------'

section() {
    echo ""
    echo -e "${B}${C}  --[ ${1} ]${W}${D}${C}$(printf '%*s' $((40 - ${#1})) '' | tr ' ' '-')${W}"
    echo ""
}

dot_line() {
    local label="$1"
    local value="$2"
    local color="${3:-$W}"
    local pad=$(( 32 - ${#label} ))
    local dots
    dots=$(printf '%*s' "$pad" '' | tr ' ' '.')
    printf "  ${C}%s${W}${D}%s${W}  ${color}%s${W}\n" "$label" "$dots" "$value"
}

ok_line() {
    printf "  ${G}%-28s${W}${D}..........${W}  ${G}READY${W}\n" "$1"
}

skip_line() {
    printf "  ${D}%-28s..........  optional${W}\n" "$1"
}

fail_line() {
    printf "  ${R}%-28s${W}${D}..........${W}  ${R}MISSING${W}\n" "$1"
}

progress_bar() {
    local pid=$1
    local msg=$2
    local width=24
    local i=0
    while kill -0 "$pid" 2>/dev/null; do
        local pos=$(( i % (width * 2) ))
        local fill=$(( pos < width ? pos : width * 2 - pos ))
        local bar
        bar=$(printf '%*s' "$fill" '' | tr ' ' '#')$(printf '%*s' "$((width - fill))" '' | tr ' ' '.')
        printf "\r  ${C}%-30s${W}  [${G}%s${W}]" "$msg" "$bar"
        sleep 0.06
        i=$(( i + 1 ))
    done
    local full
    full=$(printf '%*s' "$width" '' | tr ' ' '#')
    printf "\r  ${G}%-30s${W}  [${G}%s${W}]  ${G}done${W}\n" "$msg" "$full"
}

run_bg() {
    local msg="$1"; shift
    ("$@" &>/dev/null) &
    progress_bar $! "$msg"
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
printf "${W}"
echo ""
printf "  ${B}${Y}SQL Easy  Installer${W}   ${D}v1.1.0  |  sqleasy.orildo.sbs${W}\n"
echo -e "$HR"
echo ""

# ----------------------------------------------------------------
#  Environment check
# ----------------------------------------------------------------
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="linux" ;;
    Darwin*) PLATFORM="mac" ;;
    *)
        printf "\n  ${R}Unsupported OS: %s  ->  use install.ps1 on Windows${W}\n" "$OS"
        exit 1 ;;
esac
dot_line "Platform"  "$PLATFORM"         "$G"
dot_line "OS kernel" "$(uname -r | cut -d- -f1)"

if ! command -v python3 &>/dev/null; then
    dot_line "Python3" "NOT FOUND" "$R"
    if [ "$PLATFORM" = "mac" ]; then
        printf "  ${Y}  -> brew install python3${W}\n"
    else
        printf "  ${Y}  -> sudo apt install python3${W}\n"
    fi
    exit 1
fi
dot_line "Python3"  "$(python3 --version 2>&1 | cut -d' ' -f2)"  "$G"

if ! command -v git &>/dev/null; then
    printf "  ${Y}Git not found - installing...${W}\n"
    if [ "$PLATFORM" = "mac" ]; then
        run_bg "Installing git" brew install git
    else
        run_bg "Installing git" sudo apt install -y git
    fi
fi
dot_line "Git"  "$(git --version | cut -d' ' -f3)"  "$G"
echo ""
echo -e "$HR"

# ----------------------------------------------------------------
#  Repository
# ----------------------------------------------------------------
section "Repository"
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
if [ ! -f "$INSTALL_DIR/main.py" ]; then
    INSTALL_DIR="$HOME/sql-easy"
    if [ -d "$INSTALL_DIR/.git" ]; then
        run_bg "Updating from GitHub" git -C "$INSTALL_DIR" pull
    else
        printf "  ${C}Cloning from GitHub...${W}\n"
        git clone https://github.com/syed-sameer-ul-hassan/SQL-Easy.git "$INSTALL_DIR"
        dot_line "Clone" "complete" "$G"
    fi
fi
mkdir -p "$HOME/.config/sqleasy"
echo "$INSTALL_DIR" > "$HOME/.config/sqleasy/path"
dot_line "Install path"   "$INSTALL_DIR"               "$G"
dot_line "Config saved"   "~/.config/sqleasy/path"     "$G"
echo ""
echo -e "$HR"

# ----------------------------------------------------------------
#  Tool installation
# ----------------------------------------------------------------
section "Backend Tools"
printf "  ${C}Install SQLMap / Subfinder / Httpx / Katana + optional tools?${W}\n"
printf "  ${D}(Nuclei and Arjun require Go / pip3)${W}\n\n"
printf "  ${B}[y/n]${W}  -> "; read -r choice

if [[ "$choice" =~ ^[Yy]$ ]]; then
    echo ""
    run_bg "sqlmap  (via apt)"     sudo apt install -y sqlmap unzip wget

    run_bg "subfinder" bash -c "wget -q 'https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip' -O /tmp/s.zip && unzip -q -o /tmp/s.zip subfinder -d /tmp/ && sudo mv /tmp/subfinder /usr/local/bin/ && sudo chmod +x /usr/local/bin/subfinder"

    run_bg "httpx" bash -c "wget -q 'https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip' -O /tmp/h.zip && unzip -q -o /tmp/h.zip httpx -d /tmp/ && sudo mv /tmp/httpx /usr/local/bin/ && sudo chmod +x /usr/local/bin/httpx"

    run_bg "katana" bash -c "wget -q 'https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip' -O /tmp/k.zip && unzip -q -o /tmp/k.zip katana -d /tmp/ && sudo mv /tmp/katana /usr/local/bin/ && sudo chmod +x /usr/local/bin/katana"

    if command -v go &>/dev/null; then
        run_bg "nuclei  (via go)"  go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
        run_bg "gau     (via go)"  go install github.com/lc/gau/v2/cmd/gau@latest
    else
        skip_line "nuclei  (go not found)"
        skip_line "gau     (go not found)"
    fi

    if command -v pip3 &>/dev/null; then
        run_bg "arjun   (via pip3)" pip3 install arjun -q
    else
        skip_line "arjun   (pip3 not found)"
    fi
else
    printf "\n  ${D}Skipping tool installation.${W}\n"
fi
echo ""
echo -e "$HR"

# ----------------------------------------------------------------
#  Register command
# ----------------------------------------------------------------
section "Global Command"
run_bg "sqleasy -> /usr/local/bin" bash -c "sudo cp '$INSTALL_DIR/sqleasy' /usr/local/bin/sqleasy && sudo chmod +x /usr/local/bin/sqleasy"
echo ""
echo -e "$HR"

# ----------------------------------------------------------------
#  Verification
# ----------------------------------------------------------------
section "Verification"
MISSING=0
for tool in subfinder httpx katana sqlmap sqleasy; do
    if command -v "$tool" &>/dev/null; then
        ok_line "$tool"
    else
        fail_line "$tool"
        MISSING=$((MISSING + 1))
    fi
done
echo ""
for tool in nuclei arjun gau; do
    if command -v "$tool" &>/dev/null; then
        ok_line "$tool  (optional)"
    else
        skip_line "$tool"
    fi
done

echo ""
echo -e "$HR"

if [ "$MISSING" -eq 0 ]; then
    printf "\n  ${B}${G}All tools ready.  SQL Easy v1.1.0 is installed.${W}\n\n"
else
    printf "\n  ${Y}%d required tool(s) missing.  Run: sqleasy install${W}\n\n" "$MISSING"
fi

echo -e "$HR"
echo ""
printf "  ${B}${C}Quick Start${W}\n\n"
printf "  ${C}sqleasy start${W}                    launch interactive scan\n"
printf "  ${C}sqleasy start -d example.com${W}     scan a domain directly\n"
printf "  ${C}sqleasy start -d t.com --dump${W}    full database extraction\n"
printf "  ${C}sqleasy logs${W}                     view previous results\n"
printf "  ${C}sqleasy report${W}                   full report summary\n"
printf "  ${C}sqleasy update${W}                   update to latest version\n"
printf "  ${C}sqleasy help${W}                     all commands and flags\n"
echo ""
echo -e "$HR"
printf "\n  ${D}sqleasy.orildo.sbs   |   bugs: bug.orildo.sbs${W}\n\n"
