import SwiftUI

@MainActor
class FunctionCallingViewModel: ObservableObject {
    @Published var messages = [ChatMessage]()
    @Published var busy = false
    @Published var error: Error?
    @Published var recognizedText = ""

    private var functionCalls = [FunctionCall]()
    private var model: GenerativeModel
    private var chat: Chat
    private var chatTask: Task<Void, Never>?
    private let speechRecognitionManager = SpeechRecognitionManager()
    private let textToSpeechManager = TextToSpeechManager()

    init() {
        model = GenerativeModel(
            name: "gemini-1.5-flash-latest",
            apiKey: APIKey.default,
            tools: [Tool(functionDeclarations: [
                FunctionDeclaration(
                    name: "get_exchange_rate",
                    description: "Get the exchange rate for currencies between countries",
                    parameters: [
                        "currency_from": Schema(
                            type: .string,
                            format: "enum",
                            description: "The currency to convert from in ISO 4217 format",
                            enumValues: ["USD", "EUR", "JPY", "GBP", "AUD", "CAD"]
                        ),
                        "currency_to": Schema(
                            type: .string,
                            format: "enum",
                            description: "The currency to convert to in ISO 4217 format",
                            enumValues: ["USD", "EUR", "JPY", "GBP", "AUD", "CAD"]
                        ),
                    ],
                    requiredParameters: ["currency_from", "currency_to"]
                ),
            ])]
        )
        chat = model.startChat()

        speechRecognitionManager.$recognizedText
            .receive(on: DispatchQueue.main)
            .assign(to: &$recognizedText)
    }

    func startRecognition() {
        speechRecognitionManager.startRecognition()
    }

    func sendMessage(_ text: String, streaming: Bool = true) async {
        error = nil
        chatTask?.cancel()

        chatTask = Task {
            busy = true
            defer {
                busy = false
            }

            let userMessage = ChatMessage(message: text, participant: .user)
            messages.append(userMessage)

            let systemMessage = ChatMessage.pending(participant: .system)
            messages.append(systemMessage)

            do {
                repeat {
                    if streaming {
                        try await internalSendMessageStreaming(text)
                    } else {
                        try await internalSendMessage(text)
                    }
                } while !functionCalls.isEmpty
            } catch {
                self.error = error
                messages.removeLast()
            }

            textToSpeechManager.speak(text: messages.last?.message ?? "")
        }
    }

    func startNewChat() {
        stop()
        error = nil
        chat = model.startChat()
        messages.removeAll()
    }

    func stop() {
        chatTask?.cancel()
        error = nil
    }

    private func internalSendMessageStreaming(_ text: String) async throws {
        let functionResponses = try await processFunctionCalls()
        let responseStream: AsyncThrowingStream<GenerateContentResponse, Error>
        if functionResponses.isEmpty {
            responseStream = chat.sendMessageStream(text)
        } else {
            for functionResponse in functionResponses {
                messages.insert(functionResponse.chatMessage(), at: messages.count - 1)
            }
            responseStream = chat.sendMessageStream(functionResponses.modelContent())
        }
        for try await chunk in responseStream {
            processResponseContent(content: chunk)
        }
    }

    private func internalSendMessage(_ text: String) async throws {
        let functionResponses = try await processFunctionCalls()
        let response: GenerateContentResponse
        if functionResponses.isEmpty {
            response = try await chat.sendMessage(text)
        } else {
            for functionResponse in functionResponses {
