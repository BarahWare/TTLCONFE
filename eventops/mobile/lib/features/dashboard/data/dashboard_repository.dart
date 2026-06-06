import '../../../core/data/base_repository.dart';

class DashboardMetrics {
  final String event;
  final String eventStatus;
  final int totalSchedules;
  final int totalTasks;
  final int tasksCompleted;
  final int tasksPending;
  final int scheduleConflicts;
  final double compliancePct;
  final Map<String, dynamic>? children;
  final Map<String, dynamic>? kitchen;
  final Map<String, dynamic>? sales;
  final Map<String, dynamic>? guests;

  DashboardMetrics({
    required this.event,
    required this.eventStatus,
    required this.totalSchedules,
    required this.totalTasks,
    required this.tasksCompleted,
    required this.tasksPending,
    required this.scheduleConflicts,
    required this.compliancePct,
    this.children,
    this.kitchen,
    this.sales,
    this.guests,
  });

  factory DashboardMetrics.fromJson(Map<String, dynamic> json) =>
      DashboardMetrics(
        event: json['event'] as String,
        eventStatus: json['event_status'] as String,
        totalSchedules: json['total_schedules'] as int? ?? 0,
        totalTasks: json['total_tasks'] as int? ?? 0,
        tasksCompleted: json['tasks_completed'] as int? ?? 0,
        tasksPending: json['tasks_pending'] as int? ?? 0,
        scheduleConflicts: json['schedule_conflicts'] as int? ?? 0,
        compliancePct: (json['compliance_pct'] as num?)?.toDouble() ?? 0,
        children: json['children'] as Map<String, dynamic>?,
        kitchen: json['kitchen'] as Map<String, dynamic>?,
        sales: json['sales'] as Map<String, dynamic>?,
        guests: json['guests'] as Map<String, dynamic>?,
      );
}

class DashboardRepository extends BaseRepository {
  DashboardRepository(super.api);

  @override
  String get cachePrefix => 'dashboard';

  Future<DashboardMetrics> getMetrics(int eventId) => fetch(
        path: '/api/v1/events/$eventId/dashboard',
        fromJson: (j) => DashboardMetrics.fromJson(j as Map<String, dynamic>),
      );
}
