import '../../../core/data/base_repository.dart';

class TaskItem {
  final int id;
  final String title;
  final String? description;
  final String status;
  final String? priority;
  final DateTime? dueDatetime;

  TaskItem({
    required this.id,
    required this.title,
    this.description,
    required this.status,
    this.priority,
    this.dueDatetime,
  });

  factory TaskItem.fromJson(Map<String, dynamic> json) => TaskItem(
        id: json['id'] as int,
        title: json['title'] as String,
        description: json['description'] as String?,
        status: json['status'] as String? ?? 'pending',
        priority: json['priority'] as String?,
        dueDatetime: json['due_datetime'] != null
            ? DateTime.parse(json['due_datetime'] as String)
            : null,
      );
}

class TaskRepository extends BaseRepository {
  TaskRepository(super.api);

  @override
  String get cachePrefix => 'task';

  Future<List<TaskItem>> getByEvent(int eventId) => fetchList(
        path: '/api/v1/events/$eventId/tasks',
        fromJson: (j) => TaskItem.fromJson(j as Map<String, dynamic>),
      );

  Future<void> updateStatus(int taskId, String status) async {
    await api.patch('/api/v1/tasks/$taskId', data: {'status': status});
  }
}
