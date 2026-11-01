// Lanzador: sincroniza texturas y modelos 3D de PZ B42 a Roblox Studio y abre el mapa.
using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows.Forms;

class PZLauncher
{
    static string FindStudio()
    {
        string[] roots = {
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Roblox", "Versions"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Roblox", "Versions"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Roblox", "Versions")
        };
        var found = roots.Where(Directory.Exists)
            .SelectMany(r => Directory.GetDirectories(r))
            .Select(d => Path.Combine(d, "RobloxStudioBeta.exe"))
            .Where(File.Exists)
            .OrderByDescending(f => File.GetLastWriteTimeUtc(f))
            .FirstOrDefault();
        return found;
    }

    static int CopyFolder(string src, string dst)
    {
        if (!Directory.Exists(src)) return 0;
        Directory.CreateDirectory(dst);
        int copied = 0;
        foreach (string f in Directory.GetFiles(src))
        {
            string target = Path.Combine(dst, Path.GetFileName(f));
            if (!File.Exists(target) || new FileInfo(target).Length != new FileInfo(f).Length || File.GetLastWriteTimeUtc(target) < File.GetLastWriteTimeUtc(f))
            {
                File.Copy(f, target, true);
                copied++;
            }
        }
        return copied;
    }

    [STAThread]
    static int Main(string[] args)
    {
        string baseDir = AppDomain.CurrentDomain.BaseDirectory;
        string place = Path.Combine(baseDir, "PZ_Rosewood.rbxlx");
        string texDir = Path.Combine(baseDir, "textures");
        string meshDir = Path.Combine(baseDir, "meshes");
        
        try
        {
            if (!File.Exists(place)) throw new Exception("No se encontro el archivo del mapa: " + place);
            string studio = FindStudio();
            if (studio == null) throw new Exception("No se encontro Roblox Studio instalado en el equipo.");
            
            string contentRoot = Path.Combine(Path.GetDirectoryName(studio), "content", "pz42");
            Directory.CreateDirectory(contentRoot);
            
            // Copiar texturas al raiz de pz42 y a pz42/textures
            int t1 = CopyFolder(texDir, contentRoot);
            int t2 = CopyFolder(texDir, Path.Combine(contentRoot, "textures"));
            // Copiar mallas a pz42/meshes
            int m1 = CopyFolder(meshDir, Path.Combine(contentRoot, "meshes"));
            
            Console.WriteLine("==========================================================");
            Console.WriteLine("PROJECT ZOMBOID (BUILD 42) -> ROBLOX STUDIO RECREATION 1:1");
            Console.WriteLine("==========================================================");
            Console.WriteLine("Assets sincronizados en Roblox: " + contentRoot);
            Console.WriteLine("Texturas actualizadas: " + t1);
            Console.WriteLine("Mallas 3D actualizadas: " + m1);
            Console.WriteLine("Abriendo mapa en Roblox Studio...");
            
            var psi = new ProcessStartInfo(studio, "-task EditFile -localPlaceFile \"" + place + "\"");
            psi.UseShellExecute = false;
            psi.WorkingDirectory = Path.GetDirectoryName(studio);
            Process.Start(psi);
            
            Console.WriteLine("Listo! Roblox Studio se ha iniciado.");
            return 0;
        }
        catch (Exception e)
        {
            MessageBox.Show(e.Message, "Project Zomboid B42 -> Roblox Studio", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 1;
        }
    }
}
