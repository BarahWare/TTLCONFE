import 'dart:convert';
import 'package:hive_flutter/hive_flutter.dart';

class CacheHelper {
  static const _defaultTtl = Duration(minutes: 15);

  static Future<void> init() async {
    await Hive.initFlutter();
    await Hive.openBox('api_cache');
    await Hive.openBox('eventops');
  }

  static Box get _cache => Hive.box('api_cache');

  static Future<void> put(String key, dynamic data, {Duration? ttl}) async {
    final entry = {
      'data': jsonEncode(data),
      'expires_at': DateTime.now().add(ttl ?? _defaultTtl).toIso8601String(),
    };
    await _cache.put(key, entry);
  }

  static dynamic get(String key) {
    final entry = _cache.get(key) as Map?;
    if (entry == null) return null;
    final expires = DateTime.parse(entry['expires_at'] as String);
    if (DateTime.now().isAfter(expires)) {
      _cache.delete(key);
      return null;
    }
    return jsonDecode(entry['data'] as String);
  }

  static Future<void> remove(String key) => _cache.delete(key);
  static Future<void> clear() => _cache.clear();
}
