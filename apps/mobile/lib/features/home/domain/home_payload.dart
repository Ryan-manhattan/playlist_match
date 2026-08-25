class HomePayload {
  const HomePayload({
    required this.generatedAt,
    required this.sourceFiles,
    required this.hero,
    required this.worldcup,
    required this.culturePulse,
    required this.identity,
    required this.monetization,
    required this.dataAssets,
  });

  final String generatedAt;
  final Map<String, String> sourceFiles;
  final HomeHero hero;
  final WorldcupSection worldcup;
  final CulturePulseSection culturePulse;
  final IdentitySection identity;
  final MonetizationSection monetization;
  final DataAssetsSection dataAssets;

  factory HomePayload.fromJson(Map<String, dynamic> json) {
    return HomePayload(
      generatedAt: json['generated_at'] as String? ?? '',
      sourceFiles: Map<String, String>.from(json['source_files'] as Map? ?? {}),
      hero: HomeHero.fromJson(
        json['hero'] as Map<String, dynamic>? ?? const {},
      ),
      worldcup: WorldcupSection.fromJson(
        json['worldcup'] as Map<String, dynamic>? ?? const {},
      ),
      culturePulse: CulturePulseSection.fromJson(
        json['culture_pulse'] as Map<String, dynamic>? ?? const {},
      ),
      identity: IdentitySection.fromJson(
        json['identity'] as Map<String, dynamic>? ?? const {},
      ),
      monetization: MonetizationSection.fromJson(
        json['monetization'] as Map<String, dynamic>? ?? const {},
      ),
      dataAssets: DataAssetsSection.fromJson(
        json['data_assets'] as Map<String, dynamic>? ?? const {},
      ),
    );
  }
}

class WorldcupSection {
  const WorldcupSection({
    required this.eyebrow,
    required this.title,
    required this.summary,
    required this.metrics,
    required this.battleTracks,
    required this.leaderboard,
    required this.primaryCta,
    required this.secondaryCta,
  });

  final String eyebrow;
  final String title;
  final String summary;
  final List<MetricChipModel> metrics;
  final List<WorldcupTrackModel> battleTracks;
  final List<WorldcupTrackModel> leaderboard;
  final CtaLink primaryCta;
  final CtaLink secondaryCta;

  factory WorldcupSection.fromJson(Map<String, dynamic> json) {
    return WorldcupSection(
      eyebrow: json['eyebrow'] as String? ?? '',
      title: json['title'] as String? ?? '',
      summary: json['summary'] as String? ?? '',
      metrics: (json['metrics'] as List? ?? const [])
          .map((item) => MetricChipModel.fromJson(item as Map<String, dynamic>))
          .toList(),
      battleTracks: (json['battle_tracks'] as List? ?? const [])
          .map(
            (item) => WorldcupTrackModel.fromJson(item as Map<String, dynamic>),
          )
          .toList(),
      leaderboard: (json['leaderboard'] as List? ?? const [])
          .map(
            (item) => WorldcupTrackModel.fromJson(item as Map<String, dynamic>),
          )
          .toList(),
      primaryCta: CtaLink.fromJson(
        json['primary_cta'] as Map<String, dynamic>? ?? const {},
      ),
      secondaryCta: CtaLink.fromJson(
        json['secondary_cta'] as Map<String, dynamic>? ?? const {},
      ),
    );
  }
}

class HomeHero {
  const HomeHero({
    required this.eyebrow,
    required this.title,
    required this.summary,
    required this.updatedAt,
    required this.metrics,
    required this.primaryCta,
    required this.secondaryCta,
  });

  final String eyebrow;
  final String title;
  final String summary;
  final String updatedAt;
  final List<MetricChipModel> metrics;
  final CtaLink primaryCta;
  final CtaLink secondaryCta;

  factory HomeHero.fromJson(Map<String, dynamic> json) {
    return HomeHero(
      eyebrow: json['eyebrow'] as String? ?? '',
      title: json['title'] as String? ?? '',
      summary: json['summary'] as String? ?? '',
      updatedAt: json['updated_at'] as String? ?? '',
      metrics: (json['metrics'] as List? ?? const [])
          .map((item) => MetricChipModel.fromJson(item as Map<String, dynamic>))
          .toList(),
      primaryCta: CtaLink.fromJson(
        json['primary_cta'] as Map<String, dynamic>? ?? const {},
      ),
      secondaryCta: CtaLink.fromJson(
        json['secondary_cta'] as Map<String, dynamic>? ?? const {},
      ),
    );
  }
}

class CulturePulseSection {
  const CulturePulseSection({
    required this.headline,
    required this.summary,
    required this.stories,
    required this.chartHighlights,
    required this.normalizedItems,
  });

  final String headline;
  final String summary;
  final List<StoryCardModel> stories;
  final List<ChartHighlightModel> chartHighlights;
  final List<NormalizedItemModel> normalizedItems;

  factory CulturePulseSection.fromJson(Map<String, dynamic> json) {
    return CulturePulseSection(
      headline: json['headline'] as String? ?? '',
      summary: json['summary'] as String? ?? '',
      stories: (json['stories'] as List? ?? const [])
          .map((item) => StoryCardModel.fromJson(item as Map<String, dynamic>))
          .toList(),
      chartHighlights: (json['chart_highlights'] as List? ?? const [])
          .map(
            (item) =>
                ChartHighlightModel.fromJson(item as Map<String, dynamic>),
          )
          .toList(),
      normalizedItems: (json['normalized_items'] as List? ?? const [])
          .map(
            (item) =>
                NormalizedItemModel.fromJson(item as Map<String, dynamic>),
          )
          .toList(),
    );
  }
}

class IdentitySection {
  const IdentitySection({
    required this.headline,
    required this.summary,
    required this.topTags,
    required this.contexts,
    required this.signalCta,
  });

  final String headline;
  final String summary;
  final List<TagSignalModel> topTags;
  final List<IdentityContextModel> contexts;
  final CtaLink signalCta;

  factory IdentitySection.fromJson(Map<String, dynamic> json) {
    return IdentitySection(
      headline: json['headline'] as String? ?? '',
      summary: json['summary'] as String? ?? '',
      topTags: (json['top_tags'] as List? ?? const [])
          .map((item) => TagSignalModel.fromJson(item as Map<String, dynamic>))
          .toList(),
      contexts: (json['contexts'] as List? ?? const [])
          .map(
            (item) =>
                IdentityContextModel.fromJson(item as Map<String, dynamic>),
          )
          .toList(),
      signalCta: CtaLink.fromJson(
        json['signal_cta'] as Map<String, dynamic>? ?? const {},
      ),
    );
  }
}

class MonetizationSection {
  const MonetizationSection({
    required this.contextLine,
    required this.leadSummary,
    required this.offers,
    required this.momentumEntries,
  });

  final String contextLine;
  final LeadSummaryModel leadSummary;
  final List<OfferModel> offers;
  final List<MomentumEntryModel> momentumEntries;

  factory MonetizationSection.fromJson(Map<String, dynamic> json) {
    return MonetizationSection(
      contextLine: json['context_line'] as String? ?? '',
      leadSummary: LeadSummaryModel.fromJson(
        json['lead_summary'] as Map<String, dynamic>? ?? const {},
      ),
      offers: (json['offers'] as List? ?? const [])
          .map((item) => OfferModel.fromJson(item as Map<String, dynamic>))
          .toList(),
      momentumEntries: (json['momentum_entries'] as List? ?? const [])
          .map(
            (item) => MomentumEntryModel.fromJson(item as Map<String, dynamic>),
          )
          .toList(),
    );
  }
}

class DataAssetsSection {
  const DataAssetsSection({
    required this.pipeline,
    required this.manifest,
    required this.assets,
  });

  final PipelineHealthModel pipeline;
  final ManifestModel manifest;
  final List<DataAssetModel> assets;

  factory DataAssetsSection.fromJson(Map<String, dynamic> json) {
    return DataAssetsSection(
      pipeline: PipelineHealthModel.fromJson(
        json['pipeline'] as Map<String, dynamic>? ?? const {},
      ),
      manifest: ManifestModel.fromJson(
        json['manifest'] as Map<String, dynamic>? ?? const {},
      ),
      assets: (json['assets'] as List? ?? const [])
          .map((item) => DataAssetModel.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }
}

class MetricChipModel {
  const MetricChipModel({required this.label, required this.value});

  final String label;
  final String value;

  factory MetricChipModel.fromJson(Map<String, dynamic> json) {
    return MetricChipModel(
      label: json['label'] as String? ?? '',
      value: json['value']?.toString() ?? '',
    );
  }
}

class StoryCardModel {
  const StoryCardModel({
    required this.source,
    required this.title,
    required this.summary,
    required this.publishedAt,
  });

  final String source;
  final String title;
  final String summary;
  final String publishedAt;

  factory StoryCardModel.fromJson(Map<String, dynamic> json) {
    return StoryCardModel(
      source: json['source'] as String? ?? '',
      title: json['title'] as String? ?? '',
      summary: json['summary'] as String? ?? '',
      publishedAt: json['published_at'] as String? ?? '',
    );
  }
}

class ChartHighlightModel {
  const ChartHighlightModel({
    required this.source,
    required this.title,
    required this.artist,
  });

  final String source;
  final String title;
  final String artist;

  factory ChartHighlightModel.fromJson(Map<String, dynamic> json) {
    return ChartHighlightModel(
      source: json['source'] as String? ?? '',
      title: json['title'] as String? ?? '',
      artist: json['artist'] as String? ?? '',
    );
  }
}

class NormalizedItemModel {
  const NormalizedItemModel({
    required this.title,
    required this.creator,
    required this.sourceType,
    required this.publishedAt,
  });

  final String title;
  final String creator;
  final String sourceType;
  final String publishedAt;

  factory NormalizedItemModel.fromJson(Map<String, dynamic> json) {
    return NormalizedItemModel(
      title: json['title'] as String? ?? '',
      creator: json['creator'] as String? ?? '',
      sourceType: json['source_type'] as String? ?? '',
      publishedAt: json['published_at'] as String? ?? '',
    );
  }
}

class TagSignalModel {
  const TagSignalModel({
    required this.tag,
    required this.count,
    required this.source,
  });

  final String tag;
  final int count;
  final String source;

  factory TagSignalModel.fromJson(Map<String, dynamic> json) {
    return TagSignalModel(
      tag: json['tag'] as String? ?? '',
      count: json['count'] as int? ?? 0,
      source: json['source'] as String? ?? '',
    );
  }
}

class IdentityContextModel {
  const IdentityContextModel({
    required this.tag,
    required this.context,
    required this.source,
  });

  final String tag;
  final String context;
  final String source;

  factory IdentityContextModel.fromJson(Map<String, dynamic> json) {
    return IdentityContextModel(
      tag: json['tag'] as String? ?? '',
      context: json['context'] as String? ?? '',
      source: json['source'] as String? ?? '',
    );
  }
}

class LeadSummaryModel {
  const LeadSummaryModel({
    required this.totalLeads,
    required this.recentSevenDays,
    required this.goalKeywords,
  });

  final int totalLeads;
  final int recentSevenDays;
  final List<String> goalKeywords;

  factory LeadSummaryModel.fromJson(Map<String, dynamic> json) {
    return LeadSummaryModel(
      totalLeads: json['total_leads'] as int? ?? 0,
      recentSevenDays: json['recent_seven_days'] as int? ?? 0,
      goalKeywords: (json['goal_keywords'] as List? ?? const [])
          .map((item) => item.toString())
          .toList(),
    );
  }
}

class OfferModel {
  const OfferModel({
    required this.tagline,
    required this.title,
    required this.description,
    required this.price,
    required this.bullets,
    required this.ctaLabel,
  });

  final String tagline;
  final String title;
  final String description;
  final String price;
  final List<String> bullets;
  final String ctaLabel;

  factory OfferModel.fromJson(Map<String, dynamic> json) {
    return OfferModel(
      tagline: json['tagline'] as String? ?? '',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      price: json['price'] as String? ?? '',
      bullets: (json['bullets'] as List? ?? const [])
          .map((item) => item.toString())
          .toList(),
      ctaLabel: json['cta_label'] as String? ?? '',
    );
  }
}

class MomentumEntryModel {
  const MomentumEntryModel({
    required this.tag,
    required this.intentLabel,
    required this.message,
    required this.ctaLabel,
  });

  final String tag;
  final String intentLabel;
  final String message;
  final String ctaLabel;

  factory MomentumEntryModel.fromJson(Map<String, dynamic> json) {
    return MomentumEntryModel(
      tag: json['tag'] as String? ?? '',
      intentLabel: json['intent_label'] as String? ?? '',
      message: json['message'] as String? ?? '',
      ctaLabel: json['cta_label'] as String? ?? '',
    );
  }
}

class PipelineHealthModel {
  const PipelineHealthModel({
    required this.freshRatio,
    required this.freshAssets,
    required this.staleAssets,
    required this.oldestAssetName,
  });

  final double freshRatio;
  final int freshAssets;
  final int staleAssets;
  final String oldestAssetName;

  factory PipelineHealthModel.fromJson(Map<String, dynamic> json) {
    return PipelineHealthModel(
      freshRatio: (json['fresh_ratio'] as num? ?? 0).toDouble(),
      freshAssets: json['fresh_assets'] as int? ?? 0,
      staleAssets: json['stale_assets'] as int? ?? 0,
      oldestAssetName: json['oldest_asset_name'] as String? ?? '',
    );
  }
}

class ManifestModel {
  const ManifestModel({
    required this.count,
    required this.schemaVersion,
    required this.targetTableHint,
    required this.normalizedPath,
  });

  final int count;
  final String schemaVersion;
  final String targetTableHint;
  final String normalizedPath;

  factory ManifestModel.fromJson(Map<String, dynamic> json) {
    return ManifestModel(
      count: json['count'] as int? ?? 0,
      schemaVersion: json['schema_version'] as String? ?? '',
      targetTableHint: json['target_table_hint'] as String? ?? '',
      normalizedPath: json['normalized_path'] as String? ?? '',
    );
  }
}

class DataAssetModel {
  const DataAssetModel({
    required this.name,
    required this.metricLabel,
    required this.metricValue,
    required this.updatedAt,
  });

  final String name;
  final String metricLabel;
  final String metricValue;
  final String updatedAt;

  factory DataAssetModel.fromJson(Map<String, dynamic> json) {
    return DataAssetModel(
      name: json['name'] as String? ?? '',
      metricLabel: json['metric_label'] as String? ?? '',
      metricValue: json['metric_value']?.toString() ?? '',
      updatedAt: json['updated_at'] as String? ?? '',
    );
  }
}

class WorldcupTrackModel {
  const WorldcupTrackModel({
    required this.id,
    required this.title,
    required this.artist,
    required this.source,
    required this.statLabel,
    required this.statValue,
  });

  final String id;
  final String title;
  final String artist;
  final String source;
  final String statLabel;
  final String statValue;

  factory WorldcupTrackModel.fromJson(Map<String, dynamic> json) {
    return WorldcupTrackModel(
      id: json['id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      artist: json['artist'] as String? ?? '',
      source: json['source'] as String? ?? '',
      statLabel: json['stat_label'] as String? ?? '',
      statValue: json['stat_value']?.toString() ?? '',
    );
  }
}

class CtaLink {
  const CtaLink({required this.label, required this.link});

  final String label;
  final String link;

  factory CtaLink.fromJson(Map<String, dynamic> json) {
    return CtaLink(
      label: json['label'] as String? ?? '',
      link: json['link'] as String? ?? '',
    );
  }
}
