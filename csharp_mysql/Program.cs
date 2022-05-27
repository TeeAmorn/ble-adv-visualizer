using MySql.Data.MySqlClient;

string cs = @"server=localhost;userid=root;password=password;database=demo";

using var con = new MySqlConnection(cs);
con.Open();

Console.WriteLine($"MySQL version : {con.ServerVersion}");

// basic SELECT statement
var query = "SELECT * FROM two;";
var cmd = new MySqlCommand(query, con);
var reader = cmd.ExecuteReader();
// I don't have any data to test this on rn, but it should work?
// see https://dev.mysql.com/doc/connector-net/en/connector-net-tutorials-sql-command.html
while (reader.Read()) {
    Console.WriteLine(reader.ToString());
}
con.Close();
// Console.WriteLine($"{result}");