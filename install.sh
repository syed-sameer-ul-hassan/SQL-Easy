#!/bin/bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
cat << 'EOF'
  ██████   █████   ██▓       ▓█████ ▄▄▄        ██████▓██   ██▓
▒██    ▒ ▒██▓  ██▒▓██▒       ▓█   ▀▒████▄    ▒██    ▒ ▒██  ██▒
░ ▓██▄   ▒██▒  ██░▒██░       ▒███  ▒██  ▀█▄  ░ ▓██▄    ▒██ ██░
  ▒   ██▒░██  █▀ ░▒██░       ▒▓█  ▄░██▄▄▄▄██   ▒   ██▒ ░ ▐██▓░
▒██████▒▒░▒███▒█▄ ░██████▒   ░▒████▒▓█   ▓██▒▒██████▒▒ ░ ██▒▓░
▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░   ░░ ▒░ ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ██▒▒▒ 
░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░    ░ ░  ░ ▒   ▒▒ ░░ ░▒  ░ ░▓██ ░▒░ 
░  ░  ░     ░   ░   ░ ░         ░    ░   ▒   ░  ░  ░  ▒ ▒ ░░  
      ░      ░        ░  ░      ░  ░     ░  ░      ░  ░ ░     
                                                      ░ ░     
EOF
echo -e "${YELLOW}                  [ SQL Easy Installer ]${NC}"
echo ""

OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="linux" ;;
    Darwin*) PLATFORM="mac" ;;
    *)       echo -e "${RED}[-] Unsupported OS: $OS. Use install.ps1 for Windows.${NC}"; exit 1 ;;
esac
echo -e "${CYAN}[>] Detected platform: ${PLATFORM}${NC}"

if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[-] Python3 is required but not found.${NC}"
    if [ "$PLATFORM" = "mac" ]; then
        echo -e "${YELLOW}[*] Install it with: brew install python3${NC}"
    else
        echo -e "${YELLOW}[*] Install it with: sudo apt install python3${NC}"
    fi
    exit 1
fi
echo -e "${GREEN}[+] Python3 found.${NC}"

if ! command -v git &>/dev/null; then
    echo -e "${YELLOW}[*] Git not found. Installing...${NC}"
    if [ "$PLATFORM" = "mac" ]; then
        brew install git
    else
        sudo apt install -y git
    fi
fi
echo -e "${GREEN}[+] Git found.${NC}"

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
if [ ! -f "$INSTALL_DIR/main.py" ]; then
    INSTALL_DIR="$HOME/sql-easy"
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo -e "${YELLOW}[*] Existing clone found. Pulling latest...${NC}"
        git -C "$INSTALL_DIR" pull
    else
        echo -e "${CYAN}[>] Cloning SQL Easy repository...${NC}"
        git clone https://github.com/syed-sameer-ul-hassan/SQL-Easy.git "$INSTALL_DIR"
    fi
fi

echo -e "${CYAN}[>] Using installation directory: ${INSTALL_DIR}${NC}"

mkdir -p "$HOME/.config/sqleasy"
echo "$INSTALL_DIR" > "$HOME/.config/sqleasy/path"
echo -e "${GREEN}[+] Saved install path to ~/.config/sqleasy/path${NC}"

echo -e "${CYAN}[>] Installing global 'sqleasy' command to /usr/local/bin/...${NC}"
sudo cp "$INSTALL_DIR/sqleasy" /usr/local/bin/sqleasy
sudo chmod +x /usr/local/bin/sqleasy

echo ""
echo -e "${GREEN}[+] SQL Easy installed successfully!${NC}"
echo ""
echo -e "${YELLOW}Available commands (from anywhere in terminal):${NC}"
echo -e "${CYAN}  sqleasy start${NC}                       Launch the tool"
echo -e "${CYAN}  sqleasy start -d example.com${NC}        Scan a specific domain"
echo -e "${CYAN}  sqleasy start -d example.com -t 20${NC}  Fast multi-threaded scan"
echo -e "${CYAN}  sqleasy install${NC}                     Install backend tools"
echo -e "${CYAN}  sqleasy update${NC}                      Update to latest version"
echo -e "${CYAN}  sqleasy uninstall${NC}                   Remove installed tools"
echo -e "${CYAN}  sqleasy help${NC}                        Show full help menu"
echo ""
