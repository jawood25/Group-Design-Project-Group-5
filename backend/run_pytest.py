import pytest

if __name__ == '__main__':
    pytest.main([
        "-v",
        "--html=./backend_test/report.html",
        "--cov=backend",
        '--cov-report=term',
        "--cov-report=html:backend_test/coverage",
        '--cov-config=.coveragerc',
        "-W",
        "ignore"
    ])
