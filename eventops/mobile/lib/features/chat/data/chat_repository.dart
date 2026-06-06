import '../../../core/data/base_repository.dart';

class ChatMessage {
  final int id;
  final String content;
  final String senderName;
  final DateTime createdAt;

  ChatMessage({
    required this.id,
    required this.content,
    required this.senderName,
    required this.createdAt,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) => ChatMessage(
        id: json['id'] as int,
        content: json['content'] as String,
        senderName: json['sender_name'] as String? ?? '',
        createdAt: DateTime.parse(json['created_at'] as String),
      );
}

class ChatChannel {
  final int id;
  final String name;
  final String? lastMessage;

  ChatChannel({required this.id, required this.name, this.lastMessage});

  factory ChatChannel.fromJson(Map<String, dynamic> json) => ChatChannel(
        id: json['id'] as int,
        name: json['name'] as String,
        lastMessage: json['last_message'] as String?,
      );
}

class ChatRepository extends BaseRepository {
  ChatRepository(super.api);

  @override
  String get cachePrefix => 'chat';

  Future<List<ChatChannel>> getChannels(int eventId) => fetchList(
        path: '/api/v1/events/$eventId/chat/channels',
        fromJson: (j) => ChatChannel.fromJson(j as Map<String, dynamic>),
      );

  Future<List<ChatMessage>> getMessages(int channelId) => fetchList(
        path: '/api/v1/chat/channels/$channelId/messages',
        fromJson: (j) => ChatMessage.fromJson(j as Map<String, dynamic>),
      );
}
