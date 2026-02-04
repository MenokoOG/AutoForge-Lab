import nox


@nox.session
def backend_tests(session: nox.Session) -> None:
    session.install("-e", "./backend[dev]")
    session.run("pytest", "-q", "--cov=app", "--cov-report=term-missing", "backend/tests")


@nox.session
def backend_lint(session: nox.Session) -> None:
    session.install("-e", "./backend[dev]")
    session.run("ruff", "check", "backend/app", "backend/tests")


@nox.session
def backend_format(session: nox.Session) -> None:
    session.install("-e", "./backend[dev]")
    session.run("ruff", "format", "backend/app", "backend/tests")


@nox.session
def backend_types(session: nox.Session) -> None:
    session.install("-e", "./backend[dev]")
    session.run("pyright", "backend/app")