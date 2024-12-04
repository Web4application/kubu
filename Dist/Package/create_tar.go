package main

import (
"archive/tar"
"os"
"log"
"io"
)

func main() {
file, err := os.Open("example.tar")
if err != nil {
log.Fatal(err)
}
defer file.Close()

tr := tar.NewReader(file)

for {
header, err := tr.Next()
if err == io.EOF {
break
}
if err != nil {
log.Fatal(err)
}

log.Printf("Contents of %s:", header.Name)
if _, err := io.Copy(os.Stdout, tr); err != nil {
log.Fatal(err)
}
}
}
