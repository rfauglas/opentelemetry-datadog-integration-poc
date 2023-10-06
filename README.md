Recommended IDE is vscode (offers debug/completion ) with devcontainer extension.
To use Ide you have to select interpreter (Linux: Ctrl + shift +p: "Python: select interpreter", then "3.9.17")

Create .env file in root folder: 
```
DD_API_KEY=...
DD_HOSTNAME=...
```

To run tests.
* Docker compose: docker compose exec poc pytest
* In dev container: either using vs code Launch config or "Testing" vscode extension.