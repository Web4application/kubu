 // Use App Hosting's automatic initialization feature
const firebaseApp = initializeApp();

// Automatically connects to emulator locally, 
// or to your production db when deployed to App Hosting.
const db = getFirestore(); 