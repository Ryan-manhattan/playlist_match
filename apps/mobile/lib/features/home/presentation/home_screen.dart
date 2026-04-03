import 'package:flutter/material.dart';

import '../../../../core/utils/date_label.dart';
import '../data/mobile_home_repository.dart';
import '../domain/home_payload.dart';
import 'widgets/section_shell.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.repository});

  final HomeRepository repository;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureBuilder<HomePayload>(
        future: repository.loadHome(),
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError || !snapshot.hasData) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Text(
                  'Unable to load the mobile foundation payload.',
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

class _HomeView extends StatelessWidget {
  const _HomeView({required this.payload});

  final HomePayload payload;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return DecoratedBox(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFF181311), Color(0xFF12100F), Color(0xFF0F0D0D)],
        ),
      ),
      child: SafeArea(
        child: CustomScrollView(
          slivers: [
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(18, 16, 18, 36),
              sliver: SliverList(
                delegate: SliverChildListDelegate.fixed([
                  _HeroCard(
                    hero: payload.hero,
                    generatedAt: payload.generatedAt,
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: 'Culture Pulse',
                    title: payload.culturePulse.headline,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          payload.culturePulse.summary,
                          style: theme.textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 18),
                        for (final story in payload.culturePulse.stories)
                          _StoryTile(story: story),
                        const SizedBox(height: 12),
                        Wrap(
                          spacing: 10,
                          runSpacing: 10,
                          children: payload.culturePulse.chartHighlights
                              .map((item) => _ChartChip(item: item))
                              .toList(),
                        ),
                        const SizedBox(height: 18),
                        Text(
                          'Normalized inputs for future community generation',
                          style: theme.textTheme.titleMedium,
                        ),
                        const SizedBox(height: 10),
                        for (final item in payload.culturePulse.normalizedItems)
                          _NormalizedItemTile(item: item),
                      ],
                    ),
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: 'Identity',
                    title: payload.identity.headline,
                    trailing: _RouteBadge(
                      text: payload.identity.signalCta.label,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          payload.identity.summary,
                          style: theme.textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 16),
                        Wrap(
                          spacing: 10,
                          runSpacing: 10,
                          children: payload.identity.topTags
                              .map(
                                (tag) => Chip(
                                  label: Text('${tag.tag} · ${tag.count}'),
                                ),
                              )
                              .toList(),
                        ),
                        const SizedBox(height: 18),
                        for (final contextEntry in payload.identity.contexts)
                          _ContextTile(entry: contextEntry),
                      ],
                    ),
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: 'Monetization',
                    title:
                        'Offers and CTA momentum built from live local signals',
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          payload.monetization.contextLine,
                          style: theme.textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            Expanded(
                              child: _StatPanel(
                                label: 'Total leads',
                                value:
                                    '${payload.monetization.leadSummary.totalLeads}',
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: _StatPanel(
                                label: '7-day leads',
                                value:
                                    '${payload.monetization.leadSummary.recentSevenDays}',
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 18),
                        for (final offer in payload.monetization.offers)
                          _OfferTile(offer: offer),
                        const SizedBox(height: 18),
                        Text(
                          'CTA Momentum',
                          style: theme.textTheme.titleMedium,
                        ),
                        const SizedBox(height: 10),
                        for (final momentum
                            in payload.monetization.momentumEntries)
                          _MomentumTile(entry: momentum),
                      ],
                    ),
                  ),
                  const SizedBox(height: 18),
                  SectionShell(
                    eyebrow: 'Data Assets',
                    title: 'Local-first data layer ready for Supabase return',
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: _StatPanel(
                                label: 'Fresh ratio',
                                value:
                                    '${payload.dataAssets.pipeline.freshRatio.toStringAsFixed(1)}%',
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: _StatPanel(
                                label: 'Normalized items',
                                value: '${payload.dataAssets.manifest.count}',
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 18),
                        Text(
                          'Target table: ${payload.dataAssets.manifest.targetTableHint}',
                          style: theme.textTheme.titleMedium,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Schema ${payload.dataAssets.manifest.schemaVersion} · ${payload.dataAssets.manifest.normalizedPath}',
                          style: theme.textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 16),
                        for (final asset in payload.dataAssets.assets)
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
}

class _HeroCard extends StatelessWidget {
  const _HeroCard({required this.hero, required this.generatedAt});

  final HomeHero hero;
  final String generatedAt;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(32),
        border: Border.all(color: theme.colorScheme.outline),
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF2E201A), Color(0xFF181311), Color(0xFF10201A)],
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            hero.eyebrow.toUpperCase(),
            style: theme.textTheme.labelLarge?.copyWith(
              color: theme.colorScheme.secondary,
              letterSpacing: 1.4,
            ),
          ),
          const SizedBox(height: 12),
          Text(hero.title, style: theme.textTheme.displayLarge),
          const SizedBox(height: 16),
          Text(hero.summary, style: theme.textTheme.bodyLarge),
          const SizedBox(height: 18),
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: hero.metrics
                .map(
                  (metric) =>
                      Chip(label: Text('${metric.label}: ${metric.value}')),
                )
                .toList(),
          ),
          const SizedBox(height: 22),
          Row(
            children: [
              Expanded(
                child: FilledButton(
                  onPressed: () {},
                  child: Text(hero.primaryCta.label),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: OutlinedButton(
                  onPressed: () {},
                  child: Text(hero.secondaryCta.label),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            'Payload ${shortDateLabel(generatedAt)} · hero ${shortDateLabel(hero.updatedAt)}',
            style: theme.textTheme.bodyMedium,
          ),
        ],
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
      padding: const EdgeInsets.only(bottom: 14),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '${story.source} · ${shortDateLabel(story.publishedAt)}',
            style: theme.textTheme.bodyMedium,
          ),
          const SizedBox(height: 4),
          Text(story.title, style: theme.textTheme.titleMedium),
          const SizedBox(height: 4),
          Text(story.summary, style: theme.textTheme.bodyMedium),
        ],
      ),
    );
  }
}

class _ChartChip extends StatelessWidget {
  const _ChartChip({required this.item});

  final ChartHighlightModel item;

  @override
  Widget build(BuildContext context) {
    return Chip(label: Text('${item.source}: ${item.title} · ${item.artist}'));
  }
}

class _NormalizedItemTile extends StatelessWidget {
  const _NormalizedItemTile({required this.item});

  final NormalizedItemModel item;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return ListTile(
      contentPadding: EdgeInsets.zero,
      title: Text(item.title, style: theme.textTheme.titleMedium),
      subtitle: Text(
        '${item.creator} · ${item.sourceType} · ${shortDateLabel(item.publishedAt)}',
        style: theme.textTheme.bodyMedium,
      ),
    );
  }
}

class _ContextTile extends StatelessWidget {
  const _ContextTile({required this.entry});

  final IdentityContextModel entry;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            margin: const EdgeInsets.only(top: 4),
            width: 8,
            height: 8,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: theme.colorScheme.primary,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(entry.tag, style: theme.textTheme.titleMedium),
                const SizedBox(height: 2),
                Text(entry.context, style: theme.textTheme.bodyMedium),
              ],
            ),
          ),
        ],
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

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        color: theme.colorScheme.surfaceContainerHighest.withOpacity(0.22),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(offer.tagline.toUpperCase(), style: theme.textTheme.bodyMedium),
          const SizedBox(height: 6),
          Text(offer.title, style: theme.textTheme.titleMedium),
          const SizedBox(height: 4),
          Text(offer.description, style: theme.textTheme.bodyMedium),
          const SizedBox(height: 10),
          Text(offer.price, style: theme.textTheme.labelLarge),
          const SizedBox(height: 10),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: offer.bullets
                .map((bullet) => Chip(label: Text(bullet)))
                .toList(),
          ),
          const SizedBox(height: 12),
          Align(
            alignment: Alignment.centerLeft,
            child: FilledButton.tonal(
              onPressed: () {},
              child: Text(offer.ctaLabel),
            ),
          ),
        ],
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

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: theme.colorScheme.outline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '${entry.tag} · ${entry.intentLabel}',
            style: theme.textTheme.titleMedium,
          ),
          const SizedBox(height: 6),
          Text(entry.message, style: theme.textTheme.bodyMedium),
          const SizedBox(height: 10),
          Text(entry.ctaLabel, style: theme.textTheme.labelLarge),
        ],
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

    return ListTile(
      contentPadding: EdgeInsets.zero,
      title: Text(asset.name, style: theme.textTheme.titleMedium),
      subtitle: Text(
        '${asset.metricLabel}: ${asset.metricValue} · ${shortDateLabel(asset.updatedAt)}',
        style: theme.textTheme.bodyMedium,
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
      child: Text(text, style: theme.textTheme.bodyMedium),
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
        borderRadius: BorderRadius.circular(20),
        color: theme.colorScheme.surfaceContainerHighest.withOpacity(0.2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: theme.textTheme.bodyMedium),
          const SizedBox(height: 4),
          Text(value, style: theme.textTheme.headlineMedium),
        ],
      ),
    );
  }
}
