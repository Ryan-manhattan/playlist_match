import 'package:flutter_test/flutter_test.dart';

import 'package:off_community_mobile/app.dart';

void main() {
  testWidgets('worldcup-first home renders', (WidgetTester tester) async {
    await tester.pumpWidget(const OffCommunityApp());
    await tester.pumpAndSettle();

    expect(find.text('Pick fast,\nkeep the streak alive.'), findsOneWidget);
    expect(find.text('One-tap battles built like a mini game.'), findsOneWidget);
  });
}
