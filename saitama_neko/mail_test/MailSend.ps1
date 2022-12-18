function SendMail($subject, $body) {
    $EmailFrom = "zopopop0140@gmail.com"
    $EmailTo = @("zopopop0140@gmail.com")
    $Subject = $subject
    $Body = $body
    $SMTPServer = "smtp.gmail.com" 
    $SMTPPort = 587
    $password = ConvertTo-SecureString "odfivqnnquytcxlr" -AsPlainText -Force
    $username = "zopopop0140"
    $credential = New-Object System.Management.Automation.PSCredential($username, $password)

    Send-MailMessage `
        -From $EmailFrom `
        -to $EmailTo `
        -Subject $Subject `
        -Body $Body `
        -SmtpServer $SMTPServer `
        -port $SMTPPort `
        -UseSsl -Credential $credential `
        -DeliveryNotificationOption None `
        -Encoding UTF8 `
        -ErrorAction Stop
}

$subject = "hoge"
$body = "aaaa"
# SendMail関数の実衁E
SendMail $subject $body