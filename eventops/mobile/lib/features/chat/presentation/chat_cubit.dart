import 'package:flutter_bloc/flutter_bloc.dart';

import '../data/chat_repository.dart';

class ChatState {
  final List<ChatChannel> channels;
  final List<ChatMessage> messages;
  final bool loading;
  final String? error;

  const ChatState({
    this.channels = const [],
    this.messages = const [],
    this.loading = false,
    this.error,
  });
}

class ChatCubit extends Cubit<ChatState> {
  final ChatRepository repository;

  ChatCubit(this.repository) : super(const ChatState());

  Future<void> loadChannels(int eventId) async {
    emit(const ChatState(loading: true));
    try {
      final channels = await repository.getChannels(eventId);
      emit(ChatState(channels: channels));
    } catch (e) {
      emit(ChatState(error: e.toString()));
    }
  }

  Future<void> loadMessages(int channelId) async {
    try {
      final messages = await repository.getMessages(channelId);
      emit(ChatState(messages: messages, channels: state.channels));
    } catch (e) {
      emit(ChatState(error: e.toString(), channels: state.channels));
    }
  }
}
