var wShell = new ActiveXObject("WScript.Shell");

var args = WScript.Arguments
var arg = '';
for (i = 0; i < args.length; i++) {
    arg += args(i);
}

WScript.Echo(arg);

do {
    var oExec = wShell.Exec("ruby sig.rb " + arg);
    var pid = oExec.ProcessID;
    WScript.Echo(pid);
    // WScript.Sleep(1000 * 10); // 10 secs
    WScript.Sleep(1000 * 60 * 60 * 4); // 4 hours
    var oExecKill = wShell.Exec("TASKKILL /F /PID " + pid);
    WScript.Sleep(1000);
} while(true);

// WScript.Echo(oExecKill.Status);
