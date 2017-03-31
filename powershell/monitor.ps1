
$PortScriptBlock = {
	$HostIP = "172.21.129.176"
	$GuestIP = "192.168.173.128"
	
    $LogFile = "E:\Gerrit\port.log"

    function ConnectPort 
    {
        param ( [int]$Port )
 
        # Initialize object
        $Test = new-object Net.Sockets.TcpClient
 
        # Attempt connection, 300 millisecond timeout, returns boolean
        ( $Test.BeginConnect( $HostIP, $Port, $Null, $Null ) ).AsyncWaitHandle.WaitOne( 300 )

        $Result = $Test.Connected;
 
        # Cleanup
        $Test.Close()

        return $Result 
    }

    function ResetPortProxy
    {
        param ( [int]$Port )

        netsh interface portproxy delete v4tov4 listenport=$Port listenaddress=$HostIP
        netsh interface portproxy add v4tov4 listenport=$Port listenaddress=$HostIP connectport=$Port connectaddress=$GuestIP
    }

    $Ports = @("22","443","29418")
    while ($True)
    {
        foreach ($Port in $Ports)
        {
            $Result = ConnectPort $Port
            if ($Result -ne "True")
            {
                $DateTime = Get-Date
                "$DateTime ConnectPort $Port failed." | Add-Content -PassThru $LogFile
                ResetPortProxy $Port    
            }
            Start-Sleep -Seconds 10
        }
    }
}

$MonitorScriptBlock =
{
	$File = "E:\Gerrit\RestartNat.log"
	$Action = 'Restart-Service "VMware NAT Service"'
    $Global:FileChanged = $false

    function Wait-FileChange {
        param(
            [string]$File,
            [string]$Action
        )

        $FilePath = Split-Path $File -Parent
        $FileName = Split-Path $File -Leaf
        $ScriptBlock = [scriptblock]::Create($Action)

        $Watcher = New-Object IO.FileSystemWatcher $FilePath, $FileName -Property @{ 
            IncludeSubdirectories = $false
            EnableRaisingEvents = $true
        }
        $onChange = Register-ObjectEvent $Watcher Changed -Action {$global:FileChanged = $true}

        while ($global:FileChanged -eq $false){
            Start-Sleep -Seconds 1
        }

        & $ScriptBlock 
        Unregister-Event -SubscriptionId $onChange.Id
    }

    while ($True)
    {
        $Global:FileChanged = $false
        Wait-FileChange -File $File -Action $Action
        Start-Sleep -Seconds 5
        $DateTime = Get-Date
        "$DateTime Restart VMware NAT Service" | Add-Content -PassThru $File
        Start-Sleep -Seconds 5
    }
}

$PortJob=[powershell]::create()
$PortJob.addscript($PortScriptBlock)
$PortJob.begininvoke()

$MonitorJob=[powershell]::create()
$MonitorJob.addscript($MonitorScriptBlock)
$MonitorJob.begininvoke()