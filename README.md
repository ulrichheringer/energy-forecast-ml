# energy-forecast-ml

Prevê consumo energético diário com SARIMA, separação temporal de avaliação e dados sintéticos sazonais.

## Dados

O pipeline gera dados sintéticos determinísticos localmente, identificados como sintéticos em `pipeline.py`. Nenhum dado privado ou download externo é necessário. A divisão e a semente de avaliação são descritas junto às métricas abaixo.

## Instalação e execução

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python cli.py evaluate
python cli.py train --model model.joblib
python cli.py predict --model model.joblib
```

## Métricas obtidas

Seed 42: SARIMA avaliado cronologicamente em 90 dias finais, após 1.005 dias de treino — MAE **2,9880 MWh**, RMSE **3,7568 MWh**. A série sintética tem padrão semanal, tendência pequena e ruído normal; os erros não estimam desempenho em medidores reais.

Limitação: dados e regras de geração simplificados; antes de uso real, substitua-os por dados com licença e proveniência adequadas e valide fora da amostra.
