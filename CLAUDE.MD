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

## Arquitetura de Deploy (AWS / Cloud)
- **Infraestrutura como Código (IaC):** Terraform. Nenhuma infraestrutura será criada clicando no painel da nuvem.
- **CI/CD:** GitHub Actions para rodar testes, buildar imagens Docker e aprovar o deploy.
- **Model Registry:** Os pesos do modelo (.pt / .h5) NÃO sobem no Git. Eles serão armazenados em um Bucket S3 ou MLflow e baixados no momento do build/deploy.
- **Ambiente de Execução:** AWS ECS (Elastic Container Service) com Fargate (Serverless Containers) para a API e o Worker.
- **Banco de Dados:** Amazon RDS (PostgreSQL) com TimescaleDB.
