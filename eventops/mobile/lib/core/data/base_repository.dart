import 'package:dio/dio.dart';

import 'cache_helper.dart';
import '../network/api_client.dart';

abstract class BaseRepository {
  final ApiClient api;

  BaseRepository(this.api);

  String get cachePrefix;

  Future<T> fetch<T>({
    required String path,
    required T Function(dynamic json) fromJson,
    Map<String, dynamic>? params,
    bool forceRefresh = false,
  }) async {
    final cacheKey = '$cachePrefix:$path';
    if (!forceRefresh) {
      final cached = CacheHelper.get(cacheKey);
      if (cached != null) return fromJson(cached);
    }
    final response = await api.get(path, params: params);
    final data = response.data;
    if (response.statusCode == 200) {
      await CacheHelper.put(cacheKey, data);
    }
    return fromJson(data);
  }

  Future<List<T>> fetchList<T>({
    required String path,
    required T Function(dynamic json) fromJson,
    Map<String, dynamic>? params,
    bool forceRefresh = false,
  }) async {
    final cacheKey = '$cachePrefix:list:$path';
    if (!forceRefresh) {
      final cached = CacheHelper.get(cacheKey);
      if (cached is List) return cached.map((e) => fromJson(e)).toList();
    }
    final response = await api.get(path, params: params);
    final data = response.data as List;
    if (response.statusCode == 200) {
      await CacheHelper.put(cacheKey, data);
    }
    return data.map((e) => fromJson(e)).toList();
  }
}
