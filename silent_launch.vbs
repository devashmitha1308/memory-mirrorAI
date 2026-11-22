Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\devas\Dropbox\memory mirror AI"
WshShell.Run "cmd.exe /c service_runner.bat", 0, False
Set WshShell = Nothing
