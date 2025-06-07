// Import necessary package descriptions
import PackageDescription

// Define the package
let package = Package(
  name: "kubu-hai",
  platforms: [
    .macOS(.v13)
  ],
  dependencies: [
    .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.2.0"),
    .package(name: "kubu-haiGenerativeAI", path: "../../"),
    .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0"),
    .package(url: "https://github.com/vapor/queues.git", from: "1.0.0")
  ],
  targets: [
    .executableTarget(
      name: "generate-content",
      dependencies: [
        .product(name: "ArgumentParser", package: "swift-argument-parser"),
        .product(name: "GoogleGenerativeAI", package: "kubu-haiGenerativeAI")
      ],
      path: "Sources"
    ),
    .target(
      name: "kubu-hai",
      dependencies: [
        .product(name: "Vapor", package: "vapor"),
        .product(name: "Queues", package: "queues")
      ]
    ),
    .target(
      name: "Run",
      dependencies: ["App"]
    )
  ]
)
