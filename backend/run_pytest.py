import pytest

if __name__ == '__main__':
    pytest.main([
        "-v",
        "--html=report.html",
        "--cov=backend",
        '--cov-report=term',
        "--cov-report=html",
        '--cov-config=.coveragerc',
        "-W",
        "ignore"
    ])
