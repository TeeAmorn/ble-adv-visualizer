using MySql.Data.MySqlClient;

string cs = @"server=localhost;userid=root;password=password;database=demo";

using var con = new MySqlConnection(cs);
con.Open();

Console.WriteLine($"MySQL version : {con.ServerVersion}");