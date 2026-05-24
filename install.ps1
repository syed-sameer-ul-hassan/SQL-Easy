$ErrorActionPreference = "Stop"

$CYAN   = "`e[36m"
$GREEN  = "`e[32m"
$YELLOW = "`e[33m"
$RED    = "`e[31m"
$NC     = "`e[0m"

Write-Host "${CYAN}"
Write-Host "███████  ██████  ██          ███████  █████  ███████ ██    ██ "
Write-Host "██      ██    ██ ██          ██      ██   ██ ██       ██  ██  "
Write-Host "███████ ██    ██ ██          █████   ███████ ███████   ████   "
Write-Host "     ██ ██ ▄▄ ██ ██          ██      ██   ██      ██    ██    "
Write-Host "███████  ██████  ███████     ███████ ██   ██ ███████    ██    "
Write-Host "            ▀▀                                                "
Write-Host "${YELLOW}              [ SQL Easy Installer — Windows ]${NC}"
Write-Host ""

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "${RED}[-] Python3 not found. Install from https://python.org and re-run.${NC}"
    exit 1
}
Write-Host "${GREEN}[+] Python found.${NC}"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "${RED}[-] Git not found. Install from https://git-scm.com and re-run.${NC}"
    exit 1
}
Write-Host "${GREEN}[+] Git found.${NC}"

$INSTALL_DIR = "$env:USERPROFILE\sql-easy"
if (Test-Path "$INSTALL_DIR\.git") {
    Write-Host "${YELLOW}[*] Existing installation found. Pulling latest changes...${NC}"
    git -C $INSTALL_DIR pull
} else {
    Write-Host "${CYAN}[>] Cloning SQL Easy repository...${NC}"
    git clone https://github.com/syed-sameer-ul-hassan/SQL-Easy.git $INSTALL_DIR
}

$CONFIG_DIR = "$env:USERPROFILE\.config\sqleasy"
New-Item -ItemType Directory -Force -Path $CONFIG_DIR | Out-Null
Set-Content -Path "$CONFIG_DIR\path" -Value $INSTALL_DIR
Write-Host "${GREEN}[+] Saved install path to ~/.config/sqleasy/path${NC}"

$SCRIPTS_DIR = "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps"
$WRAPPER = "$SCRIPTS_DIR\sqleasy.cmd"
Set-Content -Path $WRAPPER -Value "@python `"$INSTALL_DIR\sqleasy`" %*"
Write-Host "${GREEN}[+] Registered global 'sqleasy' command.${NC}"

Write-Host ""
Write-Host "${GREEN}[+] SQL Easy installed successfully!${NC}"
Write-Host ""
Write-Host "${YELLOW}Available commands (open a new terminal):${NC}"
Write-Host "${CYAN}  sqleasy start${NC}                       Launch the tool"
Write-Host "${CYAN}  sqleasy start -d example.com${NC}        Scan a specific domain"
Write-Host "${CYAN}  sqleasy install${NC}                     Install backend tools"
Write-Host "${CYAN}  sqleasy update${NC}                      Update to latest version"
Write-Host "${CYAN}  sqleasy uninstall${NC}                   Remove installed tools"
Write-Host "${CYAN}  sqleasy help${NC}                        Show full help menu"
Write-Host ""
