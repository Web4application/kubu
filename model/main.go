package main

import (
"context"
"fmt"
"log"
"net/http"
"encoding/json"

openai "github.com/openai/openai-go"
"github.com/Web4application/kubu-hai/somepackage" // Importing a package from kubu-hai
)

func main() {
http.HandleFunc("/generate", generateHandler)
http.HandleFunc("/kubu", kubuHandler) // Adding a new handler for kubu-hai functionality
log.Fatal(http.ListenAndServe(":8080", nil))
}

func generateHandler(w http.ResponseWriter, r *http.Request) {
client := openai.NewClient("AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10")

req := openai.CompletionRequest{
Model:  "text-davinci-003",
Prompt: "Once upon a time",
MaxTokens: 50,
}

resp, err := client.CreateCompletion(context.Background(), req)
if err != nil {
http.Error(w, err.Error(), http.StatusInternalServerError)
return
}

json.NewEncoder(w).Encode(resp.Choices[0].Text)
}

func kubuHandler(w http.ResponseWriter, r *http.Request) {
result := somepackage.SomeFunction() // Calling a function from kubu-hai
fmt.Fprintln(w, result)
}
