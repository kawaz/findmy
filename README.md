# Install

```sh
direnv allow
brew install poetry
poetry install
echo 'exports FINDMY_ACCOUNT_ID=your-apple-id' > .envrc-local
direnv allow
```

# リポジトリ作成時の備忘録

- .envrc を作成して `layout python python3` と書いて保存
- `direnv allow` で .envrc を承認
- `poetry init -n` でプロジェクトファイル作成(`brew install poetry` で入れておく)

