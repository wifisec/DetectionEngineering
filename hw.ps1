Write-Output "Hello, world!"

# Get the directory the script is running from
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Output the path to flag.txt in the same directory
"$scriptDir" | Out-File -FilePath (Join-Path $scriptDir "flag.txt") -Encoding UTF8
