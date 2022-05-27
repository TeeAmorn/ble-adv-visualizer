using System.IO;
// path to the csv file
string path = "one.csv";

string[] lines = System.IO.File.ReadAllLines(path);
foreach(string line in lines)
{
    string[] columns = line.Split(',');
    for (int i = 0 ; i < columns.Length; i++) {
        // write blank entries as null for rn
        if (columns[i] == "") {
            columns[i] = "null";
        }
        Console.Write(columns[i] + " ");
    }
    Console.Write("\n");
}