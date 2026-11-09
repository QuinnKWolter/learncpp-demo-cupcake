"""Regression checks for bounded stdin/output and Linux descendant cleanup."""
import sys
import time
from execution import compilation_directory, invoke, MAX_OUTPUT


def main():
    with compilation_directory() as cwd:
        result = invoke([sys.executable, '-c', 'import time; time.sleep(10)'], cwd,
                        stdin='x' * (2 * 1024**2), timeout=0.2)
        assert result['timedOut'], result
        result = invoke([sys.executable, '-c', f'import os; os.write(1, b"x" * {MAX_OUTPUT + 10000})'], cwd)
        assert result['outputLimited'] and len(result['stdout']) <= MAX_OUTPUT, result
        result = invoke([sys.executable, '-c', 'print("ok")'], cwd)
        assert result['exitCode'] == 0 and result['stdout'] == 'ok\n', result
        if sys.platform == 'linux':
            # A parent that exits must not leave a descendant executing after grading.
            code = ('import os,time,pathlib; child=os.fork(); '
                    'time.sleep(0.3) if child==0 else None; '
                    'pathlib.Path("orphan-survived").write_text("bad") if child==0 else None')
            result = invoke([sys.executable, '-c', code], cwd)
            assert result['exitCode'] == 0, result
            time.sleep(0.5)
            assert not (cwd / 'orphan-survived').exists(), 'Descendant survived its parent'
    print('Execution regression checks passed (stdin, fast output, normal exit'
          + (', Linux descendants' if sys.platform == 'linux' else '') + ').')


if __name__ == '__main__':
    main()
