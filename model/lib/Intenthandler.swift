import Intents

class IntentHandler: INExtension, YourIntentHandling {
func handle(intent: YourIntent, completion: @escaping (YourIntentResponse) -> Void) {
// Handle the intent and provide a response
let response = YourIntentResponse(code: .success, userActivity: nil)
completion(response)
}
}
