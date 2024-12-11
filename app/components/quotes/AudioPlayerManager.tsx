import AVFoundation

class AudioPlayerManager: ObservableObject {
    private var audioPlayer: AVAudioPlayer?

    func playAudio(from url: URL) {
        do {
            audioPlayer = try AVAudioPlayer(contentsOf: url)
            audioPlayer?.prepareToPlay()
            audioPlayer?.play()
        } catch {
            print("Error playing audio: \(error.localizedDescription)")
        }
    }

    func pauseAudio() {
        audioPlayer?.pause()
    }

    func stopAudio() {
        audioPlayer?.stop()
        audioPlayer = nil
    }
}
