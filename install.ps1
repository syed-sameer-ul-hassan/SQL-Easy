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
$HR = "  ------------------------------------------------------"

function Section {
    param([string]$Title)
    $pad = "-" * [Math]::Max(0, 40 - $Title.Length)
    Write-Host ""
    Write-Host "${B}${C}  --[ $Title ]${W}${D}${C}$pad${W}"
    Write-Host ""
}

function Dot-Line {
    param([string]$Label, [string]$Value, [string]$Color = $W)
    $dots = "." * [Math]::Max(2, 34 - $Label.Length)
    Write-Host "  ${C}$Label${W}${D}$dots${W}  ${Color}$Value${W}"
}

function Ok-Line   { param([string]$T); Write-Host ("  ${G}{0,-28}${W}${D}..........${W}  ${G}READY${W}" -f $T) }
function Skip-Line { param([string]$T); Write-Host ("  ${D}{0,-28}..........  optional${W}" -f $T) }
function Fail-Line { param([string]$T); Write-Host ("  ${R}{0,-28}${W}${D}..........${W}  ${R}MISSING${W}" -f $T) }

function Progress-Bar {
    param([string]$Message, [System.Management.Automation.Job]$Job)
    $width = 24
    $i = 0
    while ($Job.State -eq 'Running') {
        $pos   = $i % ($width * 2)
        $fill  = if ($pos -lt $width) { $pos } else { $width * 2 - $pos }
        $bar   = ("#" * $fill) + ("." * ($width - $fill))
        Write-Host -NoNewline "`r  ${C}$($Message.PadRight(30))${W}  [${G}$bar${W}]"
        Start-Sleep -Milliseconds 60
        $i++
    }
    $full = "#" * $width
    Write-Host "`r  ${G}$($Message.PadRight(30))${W}  [${G}$full${W}]  ${G}done${W}"
}

function Run-Bg {
    param([string]$Message, [scriptblock]$Action)
    $job = Start-Job -ScriptBlock $Action
    Progress-Bar -Message $Message -Job $job
    $null = Receive-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job
}

function Get-Zip {
    param([string]$Name, [string]$Url, [string]$Out)
    $job = Start-Job -ScriptBlock {
        param($u,$o)
        Invoke-WebRequest -Uri $u -OutFile $o -UseBasicParsing
    } -ArgumentList $Url, $Out
    Progress-Bar -Message $Name -Job $job
    $null = Receive-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job
}

# ----------------------------------------------------------------
#  Banner
# ----------------------------------------------------------------
Write-Host "${C}"
Write-Host "  ██████   █████   ██▓       ▓█████ ▄▄▄        ██████ ▓██   ██▓"
Write-Host "▒██    ▒ ▒██▓  ██▒▓██▒       ▓█   ▀▒████▄    ▒██    ▒  ▒██  ██▒"
Write-Host "░ ▓██▄   ▒██▒  ██░▒██░       ▒███  ▒██  ▀█▄  ░ ▓██▄     ▒██ ██░"
Write-Host "  ▒   ██▒░██  █▀ ░▒██░       ▒▓█  ▄░██▄▄▄▄██   ▒   ██▒  ░▐██▓░"
Write-Host "▒██████▒▒░▒███▒█▄ ░██████▒   ░▒████▒▓█   ▓██▒▒██████▒▒  ░██▒▓░"
Write-Host "▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░   ░░ ▒░ ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░   ██▒▒▒"
Write-Host "░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░    ░ ░  ░ ▒   ▒▒ ░░ ░▒  ░ ░ ▓██░▒░"
Write-Host "░  ░  ░     ░   ░   ░ ░         ░    ░   ▒   ░  ░  ░  ▒  ▒ ░░"
Write-Host "      ░      ░        ░  ░      ░  ░     ░  ░      ░  ░  ░"
Write-Host "${W}"
Write-Host "  ${B}${Y}SQL Easy  Installer${W}   ${D}v1.1.0  |  sqleasy.orildo.sbs  [Windows]${W}"
Write-Host $HR
Write-Host ""

# ----------------------------------------------------------------
#  Environment
# ----------------------------------------------------------------
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Dot-Line "Python" "NOT FOUND  ->  python.org" $R
    exit 1
}
Dot-Line "Python"   ((python --version 2>&1) -replace "Python ","")  $G
Dot-Line "Platform" "Windows  ($([System.Environment]::OSVersion.Version))"  $G

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Dot-Line "Git" "NOT FOUND  ->  git-scm.com" $R
    exit 1
}
Dot-Line "Git" ((git --version) -replace "git version ","")  $G
Write-Host ""
Write-Host $HR

# ----------------------------------------------------------------
#  Repository
# ----------------------------------------------------------------
Section "Repository"
$INSTALL_DIR = "$env:USERPROFILE\sql-easy"
if (Test-Path "$INSTALL_DIR\.git") {
    Run-Bg -Message "Updating from GitHub" -Action {
        param($d) git -C $d pull
    }
} else {
    Write-Host "  ${C}Cloning from GitHub...${W}"
    git clone https://github.com/syed-sameer-ul-hassan/SQL-Easy.git $INSTALL_DIR
    Dot-Line "Clone" "complete" $G
}
$CONFIG_DIR = "$env:USERPROFILE\.config\sqleasy"
New-Item -ItemType Directory -Force -Path $CONFIG_DIR | Out-Null
Set-Content -Path "$CONFIG_DIR\path" -Value $INSTALL_DIR
Dot-Line "Install path"  $INSTALL_DIR           $G
Dot-Line "Config saved"  "~\.config\sqleasy\path"  $G
Write-Host ""
Write-Host $HR

# ----------------------------------------------------------------
#  Tools
# ----------------------------------------------------------------
Section "Backend Tools"
Write-Host "  ${C}Install SQLMap / Subfinder / Httpx / Katana?${W}"
Write-Host "  ${D}(Nuclei and Arjun require Go / pip)${W}"
Write-Host ""
$choice = Read-Host "  ${B}[y/n]${W}  ->"

if ($choice -eq 'y' -or $choice -eq 'Y') {
    Write-Host ""
    New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\tools" | Out-Null

    Get-Zip -Name "sqlmap" `
        -Url "https://github.com/sqlmapproject/sqlmap/archive/refs/tags/1.7.8.zip" `
        -Out "$env:TEMP\sqlmap.zip"
    Expand-Archive -Path "$env:TEMP\sqlmap.zip" -DestinationPath "$env:USERPROFILE\sqlmap" -Force
    Move-Item "$env:USERPROFILE\sqlmap\sqlmap-1.7.8\*" "$env:USERPROFILE\sqlmap" -Force -EA SilentlyContinue
    Remove-Item "$env:USERPROFILE\sqlmap\sqlmap-1.7.8" -Force -EA SilentlyContinue

    Get-Zip -Name "subfinder" `
        -Url "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_windows_amd64.zip" `
        -Out "$env:TEMP\subfinder.zip"
    Expand-Archive -Path "$env:TEMP\subfinder.zip" -DestinationPath "$env:USERPROFILE\tools" -Force

    Get-Zip -Name "httpx" `
        -Url "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_windows_amd64.zip" `
        -Out "$env:TEMP\httpx.zip"
    Expand-Archive -Path "$env:TEMP\httpx.zip" -DestinationPath "$env:USERPROFILE\tools" -Force

    Get-Zip -Name "katana" `
        -Url "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_windows_amd64.zip" `
        -Out "$env:TEMP\katana.zip"
    Expand-Archive -Path "$env:TEMP\katana.zip" -DestinationPath "$env:USERPROFILE\tools" -Force

    $env:PATH += ";$env:USERPROFILE\sqlmap;$env:USERPROFILE\tools"
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")
    Dot-Line "PATH" "updated" $G
} else {
    Write-Host "  ${D}Skipping tool installation.${W}"
}
Write-Host ""
Write-Host $HR

# ----------------------------------------------------------------
#  Register command
# ----------------------------------------------------------------
Section "Global Command"
$WRAPPER = "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\sqleasy.cmd"
Set-Content -Path $WRAPPER -Value "@python `"$INSTALL_DIR\sqleasy`" %*"
Dot-Line "sqleasy.cmd" $WRAPPER $G
Write-Host ""
Write-Host $HR

# ----------------------------------------------------------------
#  Verification
# ----------------------------------------------------------------
Section "Verification"
$missing = 0
foreach ($tool in @("python", "git", "sqlmap")) {
    if (Get-Command $tool -ErrorAction SilentlyContinue) { Ok-Line $tool }
    else { Fail-Line $tool; $missing++ }
}
Write-Host ""
foreach ($tool in @("nuclei", "arjun", "gau")) {
    if (Get-Command $tool -ErrorAction SilentlyContinue) { Ok-Line "$tool  (optional)" }
    else { Skip-Line $tool }
}

Write-Host ""
Write-Host $HR

if ($missing -eq 0) {
    Write-Host ""
    Write-Host "  ${B}${G}All tools ready.  SQL Easy v1.1.0 is installed.${W}"
    Write-Host ""
} else {
    Write-Host "  ${Y}$missing required tool(s) missing.  Re-run with [y] to install.${W}"
}

Write-Host $HR
Write-Host ""
Write-Host "  ${B}${C}Quick Start${W}"
Write-Host ""
Write-Host "  ${C}sqleasy start${W}                    launch interactive scan"
Write-Host "  ${C}sqleasy start -d example.com${W}     scan a domain directly"
Write-Host "  ${C}sqleasy start -d t.com --dump${W}    full database extraction"
Write-Host "  ${C}sqleasy logs${W}                     view previous results"
Write-Host "  ${C}sqleasy report${W}                   full report summary"
Write-Host "  ${C}sqleasy update${W}                   update to latest version"
Write-Host "  ${C}sqleasy help${W}                     all commands and flags"
Write-Host ""
Write-Host $HR
Write-Host ""
Write-Host "  ${D}sqleasy.orildo.sbs   |   bugs: bug.orildo.sbs${W}"
Write-Host ""
