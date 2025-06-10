let model = GenerativeModel(name: "gemini-1.5-flash-latest", apiKey: ""AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10)
let cookieImage = UIImage(...)
let prompt = "Do these look store-bought or homemade?"

let response = try await model.generateContent(prompt, cookieImage)
