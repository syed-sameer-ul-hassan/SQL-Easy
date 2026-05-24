$ErrorActionPreference = "Stop"

$CYAN   = "`e[36m"
$GREEN  = "`e[32m"
$YELLOW = "`e[33m"
$RED    = "`e[31m"
$NC     = "`e[0m"

Write-Host "${CYAN}"
Write-Host " 
  ██████   █████   ██▓       ▓█████ ▄▄▄        ██████ ▓██   ██▓
▒██    ▒ ▒██▓  ██▒▓██▒       ▓█   ▀▒████▄    ▒██    ▒  ▒██  ██▒
░ ▓██▄   ▒██▒  ██░▒██░       ▒███  ▒██  ▀█▄  ░ ▓██▄     ▒██ ██░
  ▒   ██▒░██  █▀ ░▒██░       ▒▓█  ▄░██▄▄▄▄██   ▒   ██▒  ░▐██▓░
▒██████▒▒░▒███▒█▄ ░██████▒   ░▒████▒▓█   ▓██▒▒██████▒▒  ░██▒▓░
▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░   ░░ ▒░ ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░   ██▒▒▒ 
░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░    ░ ░  ░ ▒   ▒▒ ░░ ░▒  ░ ░ ▓██░▒░ 
░  ░  ░     ░   ░   ░ ░         ░    ░   ▒   ░  ░  ░  ▒  ▒ ░░  
      ░      ░        ░  ░      ░  ░     ░  ░      ░  ░  ░     
                                                      ░  ░      "
Write-Host "${YELLOW}                  [ SQL Easy Installer ]${NC}"
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

$choice = Read-Host "${CYAN}[?] Do you want to download and install all required backend tools (SQLMap, Subfinder, Httpx, Katana)? [y/n]${NC}"
if ($choice -eq 'y' -or $choice -eq 'Y') {
    Write-Host "${YELLOW}[*] Downloading SQLMap...${NC}"
    Invoke-WebRequest -Uri "https://github.com/sqlmapproject/sqlmap/archive/refs/tags/1.7.8.zip" -OutFile "$env:TEMP\sqlmap.zip"
    Expand-Archive -Path "$env:TEMP\sqlmap.zip" -DestinationPath "$env:USERPROFILE\sqlmap" -Force
    Move-Item -Path "$env:USERPROFILE\sqlmap\sqlmap-1.7.8\*" -Destination "$env:USERPROFILE\sqlmap" -Force
    Remove-Item -Path "$env:USERPROFILE\sqlmap\sqlmap-1.7.8" -Force
    $env:PATH += ";$env:USERPROFILE\sqlmap"
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")
    
    Write-Host "${YELLOW}[*] Downloading Subfinder...${NC}"
    Invoke-WebRequest -Uri "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_windows_amd64.zip" -OutFile "$env:TEMP\subfinder.zip"
    Expand-Archive -Path "$env:TEMP\subfinder.zip" -DestinationPath "$env:USERPROFILE\tools" -Force
    $env:PATH += ";$env:USERPROFILE\tools"
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")
    
    Write-Host "${YELLOW}[*] Downloading Httpx...${NC}"
    Invoke-WebRequest -Uri "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_windows_amd64.zip" -OutFile "$env:TEMP\httpx.zip"
    Expand-Archive -Path "$env:TEMP\httpx.zip" -DestinationPath "$env:USERPROFILE\tools" -Force
    $env:PATH += ";$env:USERPROFILE\tools"
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")
    
    Write-Host "${YELLOW}[*] Downloading Katana...${NC}"
    Invoke-WebRequest -Uri "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_windows_amd64.zip" -OutFile "$env:TEMP\katana.zip"
    Expand-Archive -Path "$env:TEMP\katana.zip" -DestinationPath "$env:USERPROFILE\tools" -Force
    $env:PATH += ";$env:USERPROFILE\tools"
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")
    
    Write-Host "${GREEN}[+] All tools installed successfully!${NC}"
} else {
    Write-Host "${YELLOW}[*] Skipping tool installation.${NC}"
}

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
