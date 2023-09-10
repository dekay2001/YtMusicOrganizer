import os
import sys

import bolt
import behave_restful.bolt_behave_restful as bbr

bolt.register_module_tasks(bbr)

bolt.register_task('clear-pyc', [
    'delete-pyc',
    'delete-pyc.from-tests',
])

bolt.register_task('ut', ['clear-pyc', 'set-vars.test', 'shell.pytest'])
bolt.register_task('ct', ['clear-pyc', 'set-vars.test', 'conttest'])
bolt.register_task('cov', ['clear-pyc', 'set-vars.test', 'shell.pytest.cov'])



# Directories
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, 'SVC')
TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')
OUTPUT_UNIT_COVERAGE_DIR = os.path.join(PROJECT_ROOT, 'output', 'unit-coverage')



config = { 
    'set-vars': {
        'test': {
            'vars': {
                'ENVIRONMENT': 'lcl',
            }
        },
    },
    'delete-pyc': {
        'sourcedir': SRC_DIR,
        'recursive': True,
        'from-tests': {
            'sourcedir': TESTS_DIR,
        },
    },
    "shell": {
        
        "pytest": {
            "command": sys.executable,
            "arguments": ["-m", "pytest", TESTS_DIR],
            "cov": {
                "arguments": [
                    "-m",
                    "pytest",
                    # "--cov=ytm",
                    "--cov-report",
                    f"html:{OUTPUT_UNIT_COVERAGE_DIR}",
                    TESTS_DIR,
                ]
            },
        },
    },
    'conttest': {
        'task': 'ut',
        'directory': PROJECT_ROOT,
    },
}