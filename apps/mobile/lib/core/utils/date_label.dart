String shortDateLabel(String raw) {
  if (raw.isEmpty) {
    return '';
  }

  final normalized = raw.length >= 10 ? raw.substring(0, 10) : raw;
  return normalized.replaceAll('-', '.');
}
