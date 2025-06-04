// bin/server.dart
import 'dart:io';

Future<void> main() async {
  final server = await HttpServer.bind(InternetAddress.anyIPv4, 8080);
  print('Listening on localhost:${server.port}');

  await for (HttpRequest request in server) {
    request.response
      ..write('Hello from Dart AOT server!')
      ..close();
  }
}
