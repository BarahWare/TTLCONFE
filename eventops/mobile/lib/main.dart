import 'package:flutter/material.dart';

import 'app.dart';
import 'core/data/cache_helper.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await CacheHelper.init();
  runApp(const EventOpsApp());
}
