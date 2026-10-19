using System;
using System.Diagnostics;
using System.IO;

class Program {
    static int Main(string[] args) {
        string baseDir = AppDomain.CurrentDomain.BaseDirectory;
        string tscJs = Path.Combine(baseDir, "tsc.js");
        string nodeExe = Path.GetFullPath(Path.Combine(baseDir, @"..\..\..\..\node\win\node.exe"));
        if (!File.Exists(nodeExe)) {
            nodeExe = "node.exe";
        }
        ProcessStartInfo psi = new ProcessStartInfo();
        psi.FileName = nodeExe;
        psi.UseShellExecute = false;
        psi.Arguments = "\"" + tscJs + "\"";
        foreach (string arg in args) {
            psi.Arguments += " \"" + arg.Replace("\"", "\\\"") + "\"";
        }
        using (Process p = Process.Start(psi)) {
            p.WaitForExit();
            return p.ExitCode;
        }
    }
}
