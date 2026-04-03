import 'package:flutter/material.dart';

import 'core/theme/app_theme.dart';
import 'features/home/data/local_home_data_source.dart';
import 'features/home/data/mobile_home_repository.dart';
import 'features/home/presentation/home_screen.dart';

class OffCommunityApp extends StatelessWidget {
  const OffCommunityApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'off_community',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: HomeScreen(
        repository: MobileHomeRepository(
          dataSource: const LocalHomeDataSource(
            assetPath: 'assets/data/home_payload.json',
          ),
        ),
      ),
    );
  }
}
