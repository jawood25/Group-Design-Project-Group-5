import pytest

if __name__ == '__main__':
    pytest.main([
        "-v",
        "--html=./backend/report.html",
        "--cov=backend",
        '--cov-report=term',
        "--cov-report=html:backend/coverage",
        '--cov-config=.coveragerc',
        "-W",
        "ignore"
    ])
