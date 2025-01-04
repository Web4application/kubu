// Example: utils/DataLoader.cs
using System;
using System.Collections.Generic;
using System.IO;

public class DataLoader
{
    public static List<Dictionary<string, string>> LoadData(string filePath)
    {
        var data = new List<Dictionary<string, string>>();
        var lines = File.ReadAllLines(filePath);

        if (lines.Length > 0)
        {
            var headers = lines[0].Split(',');

            for (int i = 1; i < lines.Length; i++)
            {
                var values = lines[i].Split(',');
                var row = new Dictionary<string, string>();

                for (int j = 0; j < headers.Length; j++)
                {
                    row[headers[j]] = values[j];
                }

                data.Add(row);
            }
        }

        return data;
    }

    public static List<Dictionary<string, string>> PreprocessData(List<Dictionary<string, string>> data)
    {
        // Example preprocessing steps
        data.RemoveAll(row => row.Values.Contains(null));
        return data;
    }

    public static void Main(string[] args)
    {
        string filePath = "path/to/data.csv";
        var data = LoadData(filePath);
        var preprocessedData = PreprocessData(data);

        foreach (var row in preprocessedData)
        {
            foreach (var kvp in row)
            {
                Console.Write($"{kvp.Key}: {kvp.Value} ");
            }
            Console.WriteLine();
        }
    }
}
