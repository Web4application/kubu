import UIKit
import Intents
import IntentsUI

class ViewController: UIViewController {
override func viewDidLoad() {
super.viewDidLoad()
let shortcut = INShortcut(intent: YourIntent())
let shortcutViewController = INUIAddVoiceShortcutViewController(shortcut: shortcut)
shortcutViewController.delegate = self
present(shortcutViewController, animated: true, completion: nil)
}
}

extension ViewController: INUIAddVoiceShortcutViewControllerDelegate {
func addVoiceShortcutViewController(_ controller: INUIAddVoiceShortcutViewController, didFinishWith voiceShortcut: INVoiceShortcut?, error: Error?) {
controller.dismiss(animated: true, completion: nil)
}

func addVoiceShortcutViewControllerDidCancel(_ controller: INUIAddVoiceShortcutViewController) {
controller.dismiss(animated: true, completion: nil)
}
}
