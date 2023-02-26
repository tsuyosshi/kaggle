# 実行方法 (WSL環境)
1. .kaggle.json を /kaggle/ にコピー

2. 
```
docker build .
```
3. 
```
docker-compose -f docker-compose.yml up -d
```
4. vscode で kaggle-container にアタッチ

5. コンテナ内で作業 (kaggle api 使用可)