import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:off_community_mobile/features/home/domain/home_payload.dart';

void main() {
  test('home payload includes all major sections', () async {
    final file = File('assets/data/home_payload.json');
    final decoded =
        jsonDecode(await file.readAsString()) as Map<String, dynamic>;
    final payload = HomePayload.fromJson(decoded);

    expect(payload.hero.title, isNotEmpty);
    expect(payload.worldcup.battleTracks, isNotEmpty);
    expect(payload.worldcup.leaderboard, isNotEmpty);
    expect(payload.culturePulse.stories, isNotEmpty);
    expect(payload.identity.topTags, isNotEmpty);
    expect(payload.monetization.offers, isNotEmpty);
    expect(payload.dataAssets.assets, isNotEmpty);
    expect(payload.dataAssets.manifest.targetTableHint, 'culture_items');
  });
}
