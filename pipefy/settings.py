from pathlib import Path

from dynaconf import Dynaconf

PROJECT_ROOT = Path(__file__).parent.parent.resolve(strict=True).as_posix()

settings = Dynaconf(
    root_path=PROJECT_ROOT,
    envvar_prefix="PIPEFY_SDK",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
)
