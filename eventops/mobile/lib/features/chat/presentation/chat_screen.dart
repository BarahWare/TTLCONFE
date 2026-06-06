import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:lucide_icons/lucide_icons.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../shared/widgets/app_card.dart';
import '../data/chat_repository.dart';
import '../presentation/chat_cubit.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    context.read<ChatCubit>().loadChannels(1);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<ChatCubit, ChatState>(
      builder: (context, state) {
        return Padding(
          padding: const EdgeInsets.all(AppSpacing.md),
          child: Column(
            children: [
              Expanded(
                child: state.loading
                    ? const Center(child: CircularProgressIndicator())
                    : ListView.builder(
                        itemCount: state.channels.length,
                        itemBuilder: (_, i) {
                          final ch = state.channels[i];
                          return Padding(
                            padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                            child: AppCard(
                              child: ListTile(
                                leading: const CircleAvatar(
                                  backgroundColor: AppColors.primary,
                                  child: Icon(Icons.person,
                                      color: Colors.white, size: 16),
                                ),
                                title: Text(ch.name,
                                    style: const TextStyle(
                                        color: AppColors.textPrimary)),
                                subtitle: ch.lastMessage != null
                                    ? Text(ch.lastMessage!,
                                        style: const TextStyle(
                                            color: AppColors.textSecondary,
                                            fontSize: 12))
                                    : null,
                              ),
                            ),
                          );
                        },
                      ),
                ),
              ),
              const Divider(color: AppColors.outline),
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      style: const TextStyle(color: AppColors.textPrimary),
                      decoration: const InputDecoration(
                        hintText: 'Type a message...',
                        hintStyle: TextStyle(color: AppColors.textTertiary),
                        border: InputBorder.none,
                      ),
                    ),
                  ),
                  const Icon(LucideIcons.send,
                      color: AppColors.primary, size: 20),
                  const SizedBox(width: AppSpacing.sm),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}
