import '../domain/home_payload.dart';
import 'local_home_data_source.dart';

abstract class HomeRepository {
  Future<HomePayload> loadHome();
}

class MobileHomeRepository implements HomeRepository {
  const MobileHomeRepository({required this.dataSource});

  final LocalHomeDataSource dataSource;

  @override
  Future<HomePayload> loadHome() {
    return dataSource.load();
  }
}
