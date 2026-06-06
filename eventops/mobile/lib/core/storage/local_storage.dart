import 'package:hive_flutter/hive_flutter.dart';

class LocalStorage {
  static Future<void> init() async {
    await Hive.initFlutter();
  }

  static Box get _box => Hive.box('eventops');

  static String? get token => _box.get('token') as String?;

  static set token(String? value) {
    if (value == null) {
      _box.delete('token');
    } else {
      _box.put('token', value);
    }
  }
}
