import 'package:web_socket_channel/web_socket_channel.dart';

import '../../config/env.dart';

class WebSocketService {
  WebSocketChannel? _channel;

  void connect(String path, {Map<String, String>? headers}) {
    final uri = Uri.parse('${Env.wsBaseUrl}$path');
    _channel = WebSocketChannel.connect(uri, headers: headers);
  }

  void send(Map<String, dynamic> data) {
    _channel?.sink.add(data);
  }

  Stream<dynamic> get stream => _channel!.stream;

  void disconnect() {
    _channel?.sink.close();
  }
}
