# Mercfinan Market Predictor

## Arquitetura
- `apps/api`: API FastAPI para inferência.
- `apps/data_worker`: worker que coleta dados em loop e gera janelas de entrada.
- `packages/model_core`: modelo, pré-processamento e contrato de input.
- `packages/database`: acesso a dados e modelos SQLAlchemy.

## Testes
- `pytest`

## Integração crítica
Quando o formato do input do modelo mudar em `packages/model_core`, rode o teste
`tests/test_integration_pipeline.py` para garantir que o payload gerado no
`data_worker` continua válido para a API.
