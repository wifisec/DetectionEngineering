# Define the message and target path
$message = "Hello World"
$tempFolder = $env:WINDIR + "\Temp"
$fileName = "flag.txt"
$filePath = Join-Path -Path $tempFolder -ChildPath $fileName

# Output the message to the console and the file
$message | Tee-Object -FilePath $filePath
