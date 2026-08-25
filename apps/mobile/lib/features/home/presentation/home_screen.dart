import 'dart:math';

import 'package:flutter/material.dart';

import '../../../../core/utils/date_label.dart';
import '../data/mobile_home_repository.dart';
import '../domain/home_payload.dart';
import 'widgets/section_shell.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key, required this.repository});

  final HomeRepository repository;

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late final Future<HomePayload> _future;

  @override
  void initState() {
    super.initState();
    _future = widget.repository.loadHome();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureBuilder<HomePayload>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError || !snapshot.hasData) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Text(
                  'Unable to load the mobile world cup payload.',
                  style: Theme.of(context).textTheme.bodyLarge,
                ),
              ),
            );
          }

          return _HomeView(payload: snapshot.data!);
        },
      ),
    );
  }
}

class _HomeView extends StatefulWidget {
  const _HomeView({required this.payload});

  final HomePayload payload;

  @override
  State<_HomeView> createState() => _HomeViewState();
}

class _HomeViewState extends State<_HomeView> {
  late List<WorldcupTrackModel> _rotationPool;
  late List<WorldcupTrackModel> _leaderboard;
  late List<WorldcupTrackModel> _currentPair;
  int _streak = 0;
  int _totalVotes = 0;
  int _roundsPlayed = 0;

  @override
  void initState() {
    super.initState();
    _rotationPool = List<WorldcupTrackModel>.from(widget.payload.worldcup.battleTracks);
    _leaderboard = List<WorldcupTrackModel>.from(widget.payload.worldcup.leaderboard);
    _totalVotes = _parseMetricValue(
      widget.payload.worldcup.metrics.isNotEmpty
          ? widget.payload.worldcup.metrics.last.value
          : 0,
    );
    _currentPair = _buildInitialPair();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return DecoratedBox(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFF160F11), Color(0xFF100E12), Color(0xFF0B0A0C)],
        ),
      ),
      child: SafeArea(
        child: CustomScrollView(
          slivers: [
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(18, 16, 18, 40),
              sliver: SliverList(
                delegate: SliverChildListDelegate.fixed([
                  _HeroCard(
                    hero: widget.payload.hero,
                    generatedAt: widget.payload.generatedAt,
                    streak: _streak,
                    totalVotes: _totalVotes,
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: widget.payload.worldcup.eyebrow,
                    title: widget.payload.worldcup.title,
                    trailing: _RouteBadge(
                      text: widget.payload.worldcup.primaryCta.label,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          widget.payload.worldcup.summary,
                          style: theme.textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 18),
                        Wrap(
                          spacing: 10,
                          runSpacing: 10,
                          children: widget.payload.worldcup.metrics
                              .map((metric) => _MetricPill(metric: metric))
                              .toList(),
                        ),
                        const SizedBox(height: 22),
                        _BattleStage(
                          tracks: _currentPair,
                          streak: _streak,
                          roundsPlayed: _roundsPlayed,
                          onPick: _handlePick,
                          onRefresh: _refreshPair,
                        ),
                        const SizedBox(height: 18),
                        _LeaderboardPanel(tracks: _leaderboard),
                      ],
                    ),
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: 'Culture Radar',
                    title: widget.payload.culturePulse.headline,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          widget.payload.culturePulse.summary,
                          style: theme.textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 16),
                        for (final story in widget.payload.culturePulse.stories)
                          _StoryTile(story: story),
                        const SizedBox(height: 16),
                        Text(
                          'Hot chart references',
                          style: theme.textTheme.titleMedium,
                        ),
                        const SizedBox(height: 10),
                        Wrap(
                          spacing: 10,
                          runSpacing: 10,
                          children: widget.payload.culturePulse.chartHighlights
                              .map((item) => _ChartChip(item: item))
                              .toList(),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: 'Signal Stack',
                    title: widget.payload.identity.headline,
                    trailing: _RouteBadge(
                      text: widget.payload.identity.signalCta.label,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          widget.payload.identity.summary,
                          style: theme.textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 16),
                        Wrap(
                          spacing: 10,
                          runSpacing: 10,
                          children: widget.payload.identity.topTags
                              .map((tag) => Chip(label: Text('${tag.tag} · ${tag.count}')))
                              .toList(),
                        ),
                        const SizedBox(height: 16),
                        for (final contextEntry in widget.payload.identity.contexts.take(4))
                          _ContextTile(entry: contextEntry),
                      ],
                    ),
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: 'Conversion Engine',
                    title: 'Offers built to turn battle energy into next steps',
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          widget.payload.monetization.contextLine,
                          style: theme.textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            Expanded(
                              child: _StatPanel(
                                label: 'Total leads',
                                value: '${widget.payload.monetization.leadSummary.totalLeads}',
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: _StatPanel(
                                label: '7-day leads',
                                value: '${widget.payload.monetization.leadSummary.recentSevenDays}',
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        for (final offer in widget.payload.monetization.offers)
                          _OfferTile(offer: offer),
                        const SizedBox(height: 16),
                        for (final momentum in widget.payload.monetization.momentumEntries)
                          _MomentumTile(entry: momentum),
                      ],
                    ),
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: 'Ops Room',
                    title: 'Local payload health for the Flutter layer',
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: _StatPanel(
                                label: 'Fresh ratio',
                                value:
                                    '${widget.payload.dataAssets.pipeline.freshRatio.toStringAsFixed(1)}%',
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: _StatPanel(
                                label: 'Normalized items',
                                value: '${widget.payload.dataAssets.manifest.count}',
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Target table: ${widget.payload.dataAssets.manifest.targetTableHint}',
                          style: theme.textTheme.titleMedium,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Schema ${widget.payload.dataAssets.manifest.schemaVersion} · ${widget.payload.dataAssets.manifest.normalizedPath}',
                          style: theme.textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 16),
                        for (final asset in widget.payload.dataAssets.assets)
                          _AssetTile(asset: asset),
                      ],
                    ),
                  ),
                ]),
              ),
            ),
          ],
        ),
      ),
    );
  }

  List<WorldcupTrackModel> _buildInitialPair() {
    if (_rotationPool.length >= 2) {
      return _rotationPool.take(2).toList();
    }
    if (_leaderboard.length >= 2) {
      return _leaderboard.take(2).toList();
    }
    return _rotationPool.isEmpty
        ? const []
        : [for (final track in _rotationPool.take(2)) track];
  }

  void _handlePick(WorldcupTrackModel picked) {
    if (_currentPair.length < 2) return;

    setState(() {
      _streak += 1;
      _roundsPlayed += 1;
      _totalVotes += 1;
      _bumpTrack(picked);
      _refreshPair();
    });
  }

  void _refreshPair() {
    if (_rotationPool.length < 2) {
      _rotationPool = List<WorldcupTrackModel>.from(_leaderboard);
    }

    if (_rotationPool.length < 2) {
      _currentPair = _rotationPool;
      return;
    }

    final random = Random(_streak + _roundsPlayed + 1);
    _rotationPool.shuffle(random);
    _currentPair = _rotationPool.take(2).toList();
  }

  void _bumpTrack(WorldcupTrackModel picked) {
    final currentIndex = _leaderboard.indexWhere((item) => item.id == picked.id);
    final track = WorldcupTrackModel(
      id: picked.id,
      title: picked.title,
      artist: picked.artist,
      source: picked.source,
      statLabel: 'Wins',
      statValue: '${_streak + 1}',
    );

    if (currentIndex >= 0) {
      _leaderboard.removeAt(currentIndex);
    }
    _leaderboard.insert(0, track);
    if (_leaderboard.length > 5) {
      _leaderboard = _leaderboard.take(5).toList();
    }
  }

  int _parseMetricValue(Object value) {
    return int.tryParse(value.toString().replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
  }
}

class _HeroCard extends StatelessWidget {
  const _HeroCard({
    required this.hero,
    required this.generatedAt,
    required this.streak,
    required this.totalVotes,
  });

  final HomeHero hero;
  final String generatedAt;
  final int streak;
  final int totalVotes;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(34),
        border: Border.all(color: theme.colorScheme.outline),
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF3D1C20), Color(0xFF1B1114), Color(0xFF11161D)],
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            hero.eyebrow.toUpperCase(),
            style: theme.textTheme.labelLarge?.copyWith(
              color: const Color(0xFFF3A8A0),
              letterSpacing: 1.8,
            ),
          ),
          const SizedBox(height: 10),
          Text(hero.title, style: theme.textTheme.displayLarge),
          const SizedBox(height: 14),
          Text(hero.summary, style: theme.textTheme.bodyLarge),
          const SizedBox(height: 18),
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: [
              for (final metric in hero.metrics) _MetricPill(metric: metric),
              _MetricPill(
                metric: MetricChipModel(label: 'streak', value: '$streak'),
              ),
              _MetricPill(
                metric: MetricChipModel(label: 'votes', value: '$totalVotes'),
              ),
            ],
          ),
          const SizedBox(height: 18),
          Row(
            children: [
              Expanded(
                child: _HeroActionButton(
                  label: hero.primaryCta.label,
                  filled: true,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _HeroActionButton(
                  label: hero.secondaryCta.label,
                  filled: false,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            'Payload updated ${shortDateLabel(generatedAt)}',
            style: theme.textTheme.bodyMedium,
          ),
        ],
      ),
    );
  }
}

class _BattleStage extends StatelessWidget {
  const _BattleStage({
    required this.tracks,
    required this.streak,
    required this.roundsPlayed,
    required this.onPick,
    required this.onRefresh,
  });

  final List<WorldcupTrackModel> tracks;
  final int streak;
  final int roundsPlayed;
  final ValueChanged<WorldcupTrackModel> onPick;
  final VoidCallback onRefresh;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(24),
        color: const Color(0xFF120F12),
        border: Border.all(color: theme.colorScheme.outline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  'Quick battle',
                  style: theme.textTheme.headlineMedium?.copyWith(fontSize: 22),
                ),
              ),
              TextButton(
                onPressed: onRefresh,
                child: const Text('Next'),
              ),
            ],
          ),
          const SizedBox(height: 6),
          Text(
            'Round ${roundsPlayed + 1} · streak $streak',
            style: theme.textTheme.bodyMedium,
          ),
          const SizedBox(height: 16),
          if (tracks.length < 2)
            Text(
              'Not enough tracks to start a battle yet.',
              style: theme.textTheme.bodyLarge,
            )
          else
            Column(
              children: [
                _BattleCard(
                  track: tracks[0],
                  accent: const Color(0xFFF3A8A0),
                  onTap: () => onPick(tracks[0]),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  child: Text(
                    'VS',
                    style: theme.textTheme.headlineMedium?.copyWith(
                      color: const Color(0xFFF3A8A0),
                    ),
                  ),
                ),
                _BattleCard(
                  track: tracks[1],
                  accent: const Color(0xFF93D7C4),
                  onTap: () => onPick(tracks[1]),
                ),
              ],
            ),
        ],
      ),
    );
  }
}

class _BattleCard extends StatelessWidget {
  const _BattleCard({
    required this.track,
    required this.accent,
    required this.onTap,
  });

  final WorldcupTrackModel track;
  final Color accent;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(20),
      child: Ink(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: const Color(0xFF171317),
          border: Border.all(color: accent.withValues(alpha: 0.55)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              track.source.toUpperCase(),
              style: theme.textTheme.labelLarge?.copyWith(
                color: accent,
                fontSize: 11,
                letterSpacing: 1.2,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              track.title,
              style: theme.textTheme.headlineMedium?.copyWith(
                fontSize: 28,
                height: 0.98,
              ),
            ),
            const SizedBox(height: 6),
            Text(track.artist, style: theme.textTheme.bodyLarge),
            const SizedBox(height: 20),
            Text(
              '${track.statLabel}: ${track.statValue}',
              style: theme.textTheme.bodyMedium,
            ),
            const SizedBox(height: 12),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: accent.withValues(alpha: 0.55)),
              ),
              alignment: Alignment.center,
              child: Text(
                'Choose',
                style: theme.textTheme.labelLarge?.copyWith(color: accent),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _LeaderboardPanel extends StatelessWidget {
  const _LeaderboardPanel({required this.tracks});

  final List<WorldcupTrackModel> tracks;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(24),
        color: const Color(0xFF151116),
        border: Border.all(color: theme.colorScheme.outline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Live ladder', style: theme.textTheme.titleMedium),
          const SizedBox(height: 12),
          for (var index = 0; index < tracks.length; index++)
            Padding(
              padding: EdgeInsets.only(bottom: index == tracks.length - 1 ? 0 : 10),
              child: Row(
                children: [
                  SizedBox(
                    width: 26,
                    child: Text(
                      '${index + 1}',
                      style: theme.textTheme.headlineMedium?.copyWith(fontSize: 20),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(tracks[index].title, style: theme.textTheme.titleMedium),
                        Text(tracks[index].artist, style: theme.textTheme.bodyMedium),
                      ],
                    ),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    '${tracks[index].statValue} ${tracks[index].statLabel}',
                    style: theme.textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}

class _MetricPill extends StatelessWidget {
  const _MetricPill({required this.metric});

  final MetricChipModel metric;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: theme.colorScheme.outline),
        color: const Color(0xFF171316),
      ),
      child: RichText(
        text: TextSpan(
          style: theme.textTheme.bodyMedium,
          children: [
            TextSpan(text: '${metric.label.toUpperCase()} '),
            TextSpan(
              text: metric.value,
              style: theme.textTheme.labelLarge?.copyWith(color: theme.colorScheme.primary),
            ),
          ],
        ),
      ),
    );
  }
}

class _HeroActionButton extends StatelessWidget {
  const _HeroActionButton({required this.label, required this.filled});

  final String label;
  final bool filled;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      height: 52,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(18),
        color: filled ? theme.colorScheme.primary : Colors.transparent,
        border: Border.all(color: theme.colorScheme.outline),
      ),
      alignment: Alignment.center,
      child: Text(
        label,
        style: theme.textTheme.labelLarge?.copyWith(
          color: filled ? const Color(0xFF160F11) : theme.colorScheme.onSurface,
        ),
      ),
    );
  }
}

class _StoryTile extends StatelessWidget {
  const _StoryTile({required this.story});

  final StoryCardModel story;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(22),
          border: Border.all(color: theme.colorScheme.outline),
          color: const Color(0xFF151216),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(story.source.toUpperCase(), style: theme.textTheme.labelLarge),
            const SizedBox(height: 8),
            Text(story.title, style: theme.textTheme.titleMedium),
            const SizedBox(height: 6),
            Text(story.summary, style: theme.textTheme.bodyMedium),
          ],
        ),
      ),
    );
  }
}

class _ChartChip extends StatelessWidget {
  const _ChartChip({required this.item});

  final ChartHighlightModel item;

  @override
  Widget build(BuildContext context) {
    return Chip(label: Text('${item.source}: ${item.title}'));
  }
}

class _ContextTile extends StatelessWidget {
  const _ContextTile({required this.entry});

  final IdentityContextModel entry;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: const Color(0xFF151216),
          border: Border.all(color: theme.colorScheme.outline),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(entry.tag, style: theme.textTheme.titleMedium),
            const SizedBox(height: 4),
            Text(entry.context, style: theme.textTheme.bodyMedium),
          ],
        ),
      ),
    );
  }
}

class _OfferTile extends StatelessWidget {
  const _OfferTile({required this.offer});

  final OfferModel offer;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(22),
          color: const Color(0xFF151216),
          border: Border.all(color: theme.colorScheme.outline),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(offer.tagline.toUpperCase(), style: theme.textTheme.labelLarge),
            const SizedBox(height: 8),
            Text(offer.title, style: theme.textTheme.headlineMedium),
            const SizedBox(height: 6),
            Text(offer.description, style: theme.textTheme.bodyMedium),
            const SizedBox(height: 10),
            Text(offer.price, style: theme.textTheme.titleMedium),
          ],
        ),
      ),
    );
  }
}

class _MomentumTile extends StatelessWidget {
  const _MomentumTile({required this.entry});

  final MomentumEntryModel entry;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: const Color(0xFF151216),
          border: Border.all(color: theme.colorScheme.outline),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('${entry.tag} · ${entry.intentLabel}', style: theme.textTheme.titleMedium),
            const SizedBox(height: 6),
            Text(entry.message, style: theme.textTheme.bodyMedium),
          ],
        ),
      ),
    );
  }
}

class _AssetTile extends StatelessWidget {
  const _AssetTile({required this.asset});

  final DataAssetModel asset;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: const Color(0xFF151216),
          border: Border.all(color: theme.colorScheme.outline),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(asset.name, style: theme.textTheme.titleMedium),
                  const SizedBox(height: 4),
                  Text(asset.updatedAt, style: theme.textTheme.bodyMedium),
                ],
              ),
            ),
            const SizedBox(width: 12),
            Text(
              '${asset.metricValue} ${asset.metricLabel}',
              style: theme.textTheme.labelLarge,
            ),
          ],
        ),
      ),
    );
  }
}

class _StatPanel extends StatelessWidget {
  const _StatPanel({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: theme.colorScheme.outline),
        color: const Color(0xFF151216),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label.toUpperCase(), style: theme.textTheme.labelLarge),
          const SizedBox(height: 10),
          Text(value, style: theme.textTheme.headlineMedium),
        ],
      ),
    );
  }
}

class _RouteBadge extends StatelessWidget {
  const _RouteBadge({required this.text});

  final String text;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: theme.colorScheme.outline),
      ),
      child: Text(
        text.toUpperCase(),
        style: theme.textTheme.labelLarge?.copyWith(fontSize: 10),
      ),
    );
  }
}
