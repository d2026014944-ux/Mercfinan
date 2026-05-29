# Mercfinan

## Projeto: Market Predictor Alpha

Stack implementada neste repositório:
- Python 3.11 + FastAPI para API de inferência
- PyTorch para modelagem
- PostgreSQL/TimescaleDB via Docker Compose
- Monorepo gerenciado por Poetry

### Estrutura
- `src/market_predictor/api`: API (somente inferência)
- `src/market_predictor/worker`: pipeline de treinamento separado
- `src/market_predictor/ml`: modelo e pré-processamento modularizado
- `src/market_predictor/db`: acesso de leitura para séries temporais

### Regras de arquitetura aplicadas
1. Não há notebooks em produção; código de ML está em módulos Python.
2. A API não treina modelo; treinamento fica no worker.
3. Transformações ocorrem em memória (`normalize_window`) sem mutar dados brutos.
