$servicesToMonitor = "jenkinsslave-D__Jenkins"
$subject = "Restarting $serviceToMonitor service" 
$message = "Service $serviceToMonitor not running. Restarting..."
$logFile = (Get-Item $PSCommandPath).BaseName + ".log"

function mailit($subj, $msg) {
  $EmailList = "my@mail.com"
  $MailMessage = @{
    To          = $EmailList
    From        = "DONOTREPLY@host"
    Subject     = $subject
    Body        = $message
    SmtpServer  = "relay.smtp.com"
    ErrorAction = "SilentlyContinue" 
  }

  Send-MailMessage @MailMessage 
} 

foreach ($serviceToMonitor in $servicesToMonitor) {
  $dateTime = Get-Date
  if ((Get-Service -Name $serviceToMonitor).Status -ne "Running") {
    Start-Service -Name $serviceToMonitor
    # Restart-Service -Name $ServiceName $serviceToMonitor    
    "[$dateTime] $serviceToMonitor not running! Restarting..." | Add-Content $logFile
    # mailit $subj $msg
    # Start-Sleep -Seconds 30
  }
  else {
    "[$dateTime] $serviceToMonitor is running." | Add-Content $logFile
  }
}
