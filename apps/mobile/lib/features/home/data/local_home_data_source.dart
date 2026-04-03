import 'dart:convert';

import 'package:flutter/services.dart';

import '../domain/home_payload.dart';

class LocalHomeDataSource {
  const LocalHomeDataSource({required this.assetPath});

  final String assetPath;

  Future<HomePayload> load() async {
    final raw = await rootBundle.loadString(assetPath);
    final decoded = jsonDecode(raw) as Map<String, dynamic>;
    return HomePayload.fromJson(decoded);
  }
}
