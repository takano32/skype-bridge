var wShell = new ActiveXObject("WScript.Shell");

var args = WScript.Arguments
var arg = '';
for (i = 0; i < args.length; i++) {
    arg += args(i);
}

WScript.Echo(arg);

do {
    var oExec = wShell.Exec("ruby tsbot.rb " + arg);
    var pid = oExec.ProcessID;
    WScript.Echo(pid);
    WScript.Sleep(1000 * 180); // 180 secs
    var oExecKill = wShell.Exec("TASKKILL /F /PID " + pid);
    WScript.Sleep(1000);      //  1 sec
} while(true);

// WScript.Echo(oExecKill.Status);

