# Mercfinan

## Projeto: Market Predictor Alpha

Stack implementada neste repositório:
- Python 3.11 + FastAPI para API de inferência
- PyTorch para modelagem
- PostgreSQL/TimescaleDB via Docker Compose
- Monorepo gerenciado por Poetry

### Estrutura
- `apps/api`: API (somente inferência)
- `apps/data_worker`: worker que baixa dados em loop
- `packages/model_core`: modelo e pré-processamento modularizado
- `packages/database`: acesso a dados/TimescaleDB

### Regras de arquitetura aplicadas
1. Não há notebooks em produção; código de ML está em módulos Python.
2. A API não treina modelo; ingestão e coleta ficam no worker.
3. Transformações ocorrem em memória (`normalize_window`) sem mutar dados brutos.
