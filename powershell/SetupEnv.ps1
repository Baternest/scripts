$OA_IP = "10.70.41.53"
$TestIP = "10.10.70.133"
$TPMBSW01_IP = "172.21.129.176"
$TPMBSWVU02_IP = "192.168.89.206"

$ROOT_CERT_PATH = "\\mbsw\tools\ca\root.crt"
$ROOT_CERT_PATH2 = "\\tp-mbsw-01\tools\ca\root.crt"

$file = "$env:windir\System32\drivers\etc\hosts"
$hosts = Get-Content $file
$reache_mbsw = $true

function ping([string]$ip) {
    if (Test-Connection $ip -Count 2 -Quiet) { return $true } else { return $false }
}

function compare-hostname([string]$name) {
    foreach ($line in $hosts) {
        if ($line -match "\b$name\b" -and ($line -notmatch "-$name-")) {
            return $true
        }
    }

    return $false
}

function add-host([string]$ip, [string]$name) {
    if (compare-hostname($name)) {
        Write-Output "hosts recored $name already exist!"
    }
    else {
        [string]::Join("`t", ("", $ip, $name)) | Add-Content -PassThru $file
    }
}

function import-cert([string]$path) {
    # Get-ChildItem -Path $path | Import-Certificate -CertStoreLocation Cert:\LocalMachine\Root
    CERTUTIL -addstore -enterprise -f root $path
}


# mbsw
if (ping($OA_IP)) {
    Write-Output "mbsw ip = $OA_IP`n"
    add-host $OA_IP mbsw
}
elseif (ping($TestIP)) {
    Write-Output "mbsw ip = $TestIP`n"
    add-host $TestIP mbsw

    # BSP Gerrit
    add-host $TestIP mbsw2
}
else {
    Write-Output "mbsw unreachable"
    $reache_mbsw = $false
}


# tp-mbsw-01
if (ping($TPMBSW01_IP)) {
    add-host $TPMBSW01_IP tp-mbsw-01
}
else {
    Write-Output "tp-mbsw-01 unreachable"
}


# tpmbswvu02
if (ping($TPMBSWVU02_IP)) {
    add-host $TPMBSWVU02_IP tpmbswvu02
}
else {
    Write-Output "tpmbswvu02 unreachable"
}

if ($reache_mbsw) {
    import-cert $ROOT_CERT_PATH
}
else {
    import-cert $ROOT_CERT_PATH2
}
