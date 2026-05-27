$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$C  = "`e[36m"
$G  = "`e[32m"
$Y  = "`e[33m"
$R  = "`e[31m"
$B  = "`e[1m"
$D  = "`e[2m"
$W  = "`e[0m"
$LINE = "  " + ([string][char]0x2500 * 54)

function Section { param([string]$T)
    Write-Host ""
    Write-Host $LINE
    Write-Host ""
    Write-Host "  ${B}${C}▸  $T${W}"
    Write-Host "" }

function Info { param([string]$L, [string]$V)
    Write-Host ("  ${D}{0,-22}${W}  {1}" -f $L, $V) }

function Ok   { param([string]$T)
    Write-Host ("  ${G}✓${W}  ${G}{0,-26}${W}  ready"    -f $T) }

function Skip { param([string]$T)
    Write-Host ("  ${D}○  {0,-26}  optional${W}"          -f $T) }

function Fail { param([string]$T)
    Write-Host ("  ${R}✗${W}  ${R}{0,-26}${W}  missing"  -f $T) }

function Spinner {
    param([string]$Message, [System.Management.Automation.Job]$Job)
    $frames = [char[]]@(0x280B, 0x2819, 0x2839, 0x2838, 0x283C, 0x2834, 0x2826, 0x2827, 0x2807, 0x280F)
    $i = 0
    while ($Job.State -eq 'Running') {
        $f = $frames[$i % 10]
        Write-Host -NoNewline ("`r  ${Y}{0}${W}  ${C}{1,-26}${W}  ${D}fetching...${W}" -f $f, $Message)
        Start-Sleep -Milliseconds 80
        $i++
    }
    Write-Host ("`r  ${G}✓${W}  ${G}{0,-26}${W}  done                    " -f $Message)
}

function Run-Bg {
    param([string]$Message, [scriptblock]$Action)
    $job = Start-Job -ScriptBlock $Action
    Spinner -Message $Message -Job $job
    $null = Receive-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job
}

function Get-Zip {
    param([string]$Name, [string]$Url, [string]$Out)
    $job = Start-Job -ScriptBlock {
        param($u, $o)
        Invoke-WebRequest -Uri $u -OutFile $o -UseBasicParsing
    } -ArgumentList $Url, $Out
    Spinner -Message $Name -Job $job
    $null = Receive-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job
}

function Ask-Tool {
    param([string]$Name, [string]$Desc, [string]$Method)
    Write-Host ""
    Write-Host "  ${B}${Name}${W}  ${D}${Desc}${W}"
    Write-Host "  ${C}                ${D}${Method}${W}"
    $ans = Read-Host "  Install? ${B}[y/n]${W}  ->"
    return ($ans -eq 'y' -or $ans -eq 'Y')
}

Clear-Host
Write-Host "${C}"
Write-Host "  ██████   █████   ██▓       ▓█████ ▄▄▄        ██████▓██   ██▓"
Write-Host "▒██    ▒ ▒██▓  ██▒▓██▒       ▓█   ▀▒████▄    ▒██    ▒ ▒██  ██▒"
Write-Host "░ ▓██▄   ▒██▒  ██░▒██░       ▒███  ▒██  ▀█▄  ░ ▓██▄    ▒██ ██░"
Write-Host "  ▒   ██▒░██  █▀ ░▒██░       ▒▓█  ▄░██▄▄▄▄██   ▒   ██▒ ░ ▐██▓░"
Write-Host "▒██████▒▒░▒███▒█▄ ░██████▒   ░▒████▒▓█   ▓██▒▒██████▒▒ ░ ██▒▓░"
Write-Host "▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░   ░░ ▒░ ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ██▒▒▒"
Write-Host "░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░    ░ ░  ░ ▒   ▒▒ ░░ ░▒  ░ ░▓██ ░▒░"
Write-Host "░  ░  ░     ░   ░   ░ ░         ░    ░   ▒   ░  ░  ░  ▒ ▒ ░░"
Write-Host "      ░      ░        ░  ░      ░  ░     ░  ░      ░  ░ ░"
Write-Host "${W}"
Write-Host "  ${B}${Y}SQL Easy  ·  Installer  ·  v1.2.0${W}   ${D}sqleasy.orildo.sbs  [Windows]${W}"
Write-Host $LINE

Section "SYSTEM CHECK"
Info "Platform" "Windows  ($([System.Environment]::OSVersion.Version))"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Fail "Python"
    Write-Host "  ${Y}    →  python.org${W}"
    exit 1
}
Info "Python" ((python --version 2>&1) -replace "Python ", "")

Section "INSTALL PATH"
$INSTALL_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not $INSTALL_DIR -or -not (Test-Path "$INSTALL_DIR\sqleasy")) {
    Write-Host "  ${Y}[*] One-line install detected — cloning repository...${W}"
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "  ${R}✗  git not found. Install from: https://git-scm.com/download/win${W}"
        exit 1
    }
    $CLONE_DIR = "$env:LOCALAPPDATA\sqleasy"
    if (Test-Path $CLONE_DIR) { Remove-Item $CLONE_DIR -Recurse -Force }
    git clone --depth=1 https://github.com/syed-sameer-ul-hassan/SQL-Easy.git $CLONE_DIR
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ${R}✗  git clone failed. Check internet connection.${W}"
        exit 1
    }
    $INSTALL_DIR = $CLONE_DIR
    Write-Host "  ${G}✓  Cloned to $INSTALL_DIR${W}"
}

$CONFIG_DIR = "$env:USERPROFILE\.config\sqleasy"
New-Item -ItemType Directory -Force -Path $CONFIG_DIR | Out-Null
Set-Content -Path "$CONFIG_DIR\path" -Value $INSTALL_DIR
Info "Install path"  $INSTALL_DIR
Info "Config"        "~\.config\sqleasy\path"

Section "BACKEND TOOLS"

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\tools" | Out-Null
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\sqlmap" | Out-Null

Write-Host "  ${Y}${B}Required Tools${W}  —  must have for the pipeline to work"

if (Ask-Tool "sqlmap" "SQL injection testing engine (detects and exploits vulns)" "zip extract to ~\sqlmap") {
    Get-Zip -Name "sqlmap" `
        -Url "https://github.com/sqlmapproject/sqlmap/archive/refs/tags/1.7.8.zip" `
        -Out "$env:TEMP\sqlmap.zip"
    Expand-Archive -Path "$env:TEMP\sqlmap.zip" -DestinationPath "$env:USERPROFILE\sqlmap" -Force
    Move-Item "$env:USERPROFILE\sqlmap\sqlmap-1.7.8\*" "$env:USERPROFILE\sqlmap" -Force -EA SilentlyContinue
    Remove-Item "$env:USERPROFILE\sqlmap\sqlmap-1.7.8" -Force -EA SilentlyContinue
} else {
    Fail "sqlmap"
}

if (Ask-Tool "subfinder" "Discovers all subdomains of the target domain" "binary download") {
    Get-Zip -Name "subfinder" `
        -Url "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_windows_amd64.zip" `
        -Out "$env:TEMP\subfinder.zip"
    Expand-Archive -Path "$env:TEMP\subfinder.zip" -DestinationPath "$env:USERPROFILE\tools" -Force
} else {
    Fail "subfinder"
}

if (Ask-Tool "httpx" "Probes which subdomains are actually alive" "binary download") {
    Get-Zip -Name "httpx" `
        -Url "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_windows_amd64.zip" `
        -Out "$env:TEMP\httpx.zip"
    Expand-Archive -Path "$env:TEMP\httpx.zip" -DestinationPath "$env:USERPROFILE\tools" -Force
} else {
    Fail "httpx"
}

if (Ask-Tool "katana" "Crawls live hosts to find injectable URLs with parameters" "binary download") {
    Get-Zip -Name "katana" `
        -Url "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_windows_amd64.zip" `
        -Out "$env:TEMP\katana.zip"
    Expand-Archive -Path "$env:TEMP\katana.zip" -DestinationPath "$env:USERPROFILE\tools" -Force
} else {
    Fail "katana"
}

Write-Host ""
Write-Host "  ${Y}${B}Optional Tools${W}  —  enhance results but the pipeline works without them"

if (Ask-Tool "nuclei" "Broad vulnerability scanner (runs after SQLMap for extra coverage)" "binary download") {
    Get-Zip -Name "nuclei" `
        -Url "https://github.com/projectdiscovery/nuclei/releases/download/v3.3.9/nuclei_3.3.9_windows_amd64.zip" `
        -Out "$env:TEMP\nuclei.zip"
    Expand-Archive -Path "$env:TEMP\nuclei.zip" -DestinationPath "$env:USERPROFILE\tools" -Force
} else {
    Skip "nuclei"
}

if (Ask-Tool "gau" "Historical URL harvester (gets old URLs from internet archives)" "binary download") {
    Get-Zip -Name "gau" `
        -Url "https://github.com/lc/gau/releases/download/v2.2.4/gau_2.2.4_windows_amd64.zip" `
        -Out "$env:TEMP\gau.zip"
    Expand-Archive -Path "$env:TEMP\gau.zip" -DestinationPath "$env:USERPROFILE\tools" -Force
} else {
    Skip "gau"
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    if (Ask-Tool "arjun" "Hidden parameter bruteforcer (finds params not visible in page source)" "pip install") {
        python -m pip install arjun -q
    } else {
        Skip "arjun"
    }
} else {
    Skip "arjun"
}

$env:PATH += ";$env:USERPROFILE\sqlmap;$env:USERPROFILE\tools"
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")
Info "PATH" "updated"

Section "GLOBAL COMMAND"
$WRAPPER = "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\sqleasy.cmd"
Set-Content -Path $WRAPPER -Value "@python `"$INSTALL_DIR\sqleasy`" %*"
Info "sqleasy.cmd" $WRAPPER

Section "VERIFICATION"
$missing = 0
foreach ($tool in @("python", "sqlmap", "subfinder", "httpx", "katana")) {
    if (Get-Command $tool -ErrorAction SilentlyContinue) { Ok   $tool }
    else                                                  { Fail $tool; $missing++ }
}
Write-Host ""
foreach ($tool in @("nuclei", "arjun", "gau")) {
    if (Get-Command $tool -ErrorAction SilentlyContinue) { Ok   "$tool  (optional)" }
    else                                                  { Skip $tool }
}

Write-Host ""
Write-Host $LINE
if ($missing -eq 0) {
    Write-Host ""
    Write-Host "  ${G}${B}✓  All tools ready.  SQL Easy v1.2.0 is installed.${W}"
} else {
    Write-Host ""
    Write-Host "  ${Y}✗  $missing required tool(s) missing.  Re-run with [y] to install.${W}"
}

Section "QUICK START"
Write-Host "  ${C}sqleasy start${W}                    launch interactive scan"
Write-Host "  ${C}sqleasy start -d example.com${W}     scan a domain directly"
Write-Host "  ${C}sqleasy start -d t.com --dump${W}    full database extraction"
Write-Host "  ${C}sqleasy logs${W}                     view previous results"
Write-Host "  ${C}sqleasy report${W}                   full report summary"
Write-Host "  ${C}sqleasy update${W}                   update to latest version"
Write-Host "  ${C}sqleasy help${W}                     all commands and flags"
Write-Host ""
Write-Host $LINE
Write-Host ""
Write-Host "  ${D}sqleasy.orildo.sbs   ·   bugs: bug.orildo.sbs${W}"
Write-Host ""
