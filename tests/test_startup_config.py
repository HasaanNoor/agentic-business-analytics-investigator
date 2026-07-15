import pytest

from src.api.startup_config import StartupConfigError, validate_startup_config


def test_valid_development_startup_configuration():
    config = validate_startup_config(
        {
            "APP_ENV": "development",
            "RUN_MIGRATIONS_ON_STARTUP": "true",
            "SYNC_OUTPUTS_ON_STARTUP": "true",
            "DATABASE_URL": "postgresql+psycopg2://analytics_user:analytics_password@db:5432/analytics_local",
        }
    )

    assert config.production is False
    assert config.run_migrations_on_startup is True
    assert config.sync_outputs_on_startup is True


def test_valid_production_api_configuration():
    config = validate_startup_config(
        {
            "APP_ENV": "production",
            "RUN_MIGRATIONS_ON_STARTUP": "false",
            "SYNC_OUTPUTS_ON_STARTUP": "false",
            "DATABASE_URL": "postgresql+psycopg2://app_user:strong_password@db.example.com:5432/analytics_prod",
        }
    )

    assert config.production is True
    assert config.run_migrations_on_startup is False
    assert config.sync_outputs_on_startup is False


def test_invalid_production_configuration_with_migrations_enabled():
    with pytest.raises(StartupConfigError, match="RUN_MIGRATIONS_ON_STARTUP must be false"):
        validate_startup_config(
            {
                "APP_ENV": "production",
                "RUN_MIGRATIONS_ON_STARTUP": "true",
                "SYNC_OUTPUTS_ON_STARTUP": "false",
                "DATABASE_URL": "postgresql+psycopg2://app_user:strong_password@db.example.com:5432/analytics_prod",
            }
        )


def test_invalid_production_configuration_with_sync_enabled():
    with pytest.raises(StartupConfigError, match="SYNC_OUTPUTS_ON_STARTUP must be false"):
        validate_startup_config(
            {
                "APP_ENV": "production",
                "RUN_MIGRATIONS_ON_STARTUP": "false",
                "SYNC_OUTPUTS_ON_STARTUP": "true",
                "DATABASE_URL": "postgresql+psycopg2://app_user:strong_password@db.example.com:5432/analytics_prod",
            }
        )


def test_rejects_default_development_database_credentials_in_production():
    with pytest.raises(StartupConfigError) as exc_info:
        validate_startup_config(
            {
                "APP_ENV": "production",
                "RUN_MIGRATIONS_ON_STARTUP": "false",
                "SYNC_OUTPUTS_ON_STARTUP": "false",
                "DATABASE_URL": "postgresql+psycopg2://analytics_user:analytics_password@db:5432/analytics_local",
            }
        )

    message = str(exc_info.value)
    assert "default development database username" in message
    assert "default development database password" in message
    assert "default development database name" in message


def test_production_validation_message_does_not_expose_secret_values():
    secret_password = "super-secret-password"

    with pytest.raises(StartupConfigError) as exc_info:
        validate_startup_config(
            {
                "APP_ENV": "production",
                "RUN_MIGRATIONS_ON_STARTUP": "true",
                "SYNC_OUTPUTS_ON_STARTUP": "true",
                "DATABASE_URL": f"postgresql+psycopg2://analytics_user:{secret_password}@db:5432/analytics_prod",
            }
        )

    message = str(exc_info.value)
    assert secret_password not in message
    assert "analytics_user" not in message
