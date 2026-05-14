from dataclasses import dataclass, field
from typing import Dict, Any
from sqlalchemy.pool import NullPool
import urllib.parse
import os


@dataclass
class ConfigDB:
    yaml_config: Dict[str, Any] = field(default_factory=dict)

    db_name: str = field(default_factory=lambda: os.getenv('POSTGRES_DB', ''))
    host: str = field(default_factory=lambda: os.getenv('POSTGRES_HOST', 'postgres'))
    port: str = field(default_factory=lambda: os.getenv('POSTGRES_PORT', '5432'))
    username: str = field(default_factory=lambda: os.getenv('POSTGRES_USERNAME', ''))
    password: str = field(default_factory=lambda: os.getenv('POSTGRES_PASSWORD', ''))

    @property
    def protocol(self) -> str:
        proto = self.yaml_config.get('protocol', "postgresql+asyncpg")
        return proto.replace("://", "")

    @property
    def database_url(self) -> str:
        """Creating an activation URL"""
        if self.username and self.password:
            user = urllib.parse.quote_plus(self.username)
            pwd = urllib.parse.quote_plus(self.password)
            return f"{self.protocol}://{user}:{pwd}@{self.host}:{self.port}/{self.db_name}"
        elif self.username:
            user = urllib.parse.quote_plus(self.username)
            return f"{self.protocol}://{user}@{self.host}:{self.port}/{self.db_name}"
        else:
            return f"{self.protocol}://{self.host}:{self.port}/{self.db_name}"

    @property
    def engine_kwargs(self) -> Dict[str, Any]:
        """Parameters for creating engine SQLAlchemy"""
        # Basic settings for the engine
        engine_kwargs = {
            "echo": bool(self.yaml_config.get('echo', False)),
            "pool_pre_ping": bool(self.yaml_config.get('pre_ping', True)),
            "pool_recycle": int(self.yaml_config.get('pool_recycle', 3600)),
            "future": bool(self.yaml_config.get('future', True)),
        }

        # Pool settings
        pool_class = self.yaml_config.get('pool_class')
        if pool_class == "NullPool":
            engine_kwargs["poolclass"] = NullPool
        else:
            # Adding pool size settings only for QueuePool
            engine_kwargs.update({
                "pool_size": int(self.yaml_config.get('pool_size', 10)),
                "max_overflow": int(self.yaml_config.get('max_overflow', 30)),
            })

        return engine_kwargs

    @property
    def session_kwargs(self) -> Dict[str, Any]:
        """Parameters for creating an SQLAlchemy session"""
        db_config = self.yaml_config

        return {
            "expire_on_commit": bool(db_config.get('expire_on_commit', True)),
            "autocommit": bool(db_config.get('autocommit', False)),
            "autoflush": bool(db_config.get('autoflush', True)),
            "future": bool(db_config.get('future', True)),
        }
