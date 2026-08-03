"""Resolução da raiz do repositório para carregadores."""

from pathlib import Path

def _caminho_padrao_base():
    """Diretorio raiz do repositorio do Orquestrador (pai de tela/)."""
    return Path(__file__).resolve().parent.parent.parent
def _para_base(caminho_base):
    if caminho_base is None:
        return _caminho_padrao_base()
    if isinstance(caminho_base, Path):
        return caminho_base
    return Path(caminho_base)
