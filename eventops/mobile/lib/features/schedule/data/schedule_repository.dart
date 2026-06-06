import '../../../core/data/base_repository.dart';

class ScheduleItem {
  final int id;
  final String title;
  final String? location;
  final DateTime startTime;
  final DateTime endTime;
  final List<String> assignedUsers;

  ScheduleItem({
    required this.id,
    required this.title,
    this.location,
    required this.startTime,
    required this.endTime,
    this.assignedUsers = const [],
  });

  factory ScheduleItem.fromJson(Map<String, dynamic> json) => ScheduleItem(
        id: json['id'] as int,
        title: json['title'] as String,
        location: json['location'] as String?,
        startTime: DateTime.parse(json['start_time'] as String),
        endTime: DateTime.parse(json['end_time'] as String),
        assignedUsers: (json['assigned_users'] as List?)?.cast<String>() ?? [],
      );
}

class ScheduleRepository extends BaseRepository {
  ScheduleRepository(super.api);

  @override
  String get cachePrefix => 'schedule';

  Future<List<ScheduleItem>> getByEvent(int eventId) => fetchList(
        path: '/api/v1/events/$eventId/schedules',
        fromJson: (j) => ScheduleItem.fromJson(j as Map<String, dynamic>),
      );
}
